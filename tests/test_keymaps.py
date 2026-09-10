"""Static consistency tests for the mauc-qmk keymaps.

These run without the QMK toolchain (no `qmk` CLI needed) and guard the
bug classes seen in the wild:
  - editing one board's copy when the layout is shared via symlink
  - VIA EEPROM shadowing firmware (recovery keys must exist)
  - layer_count / COMBO_COUNT drifting from the shared header
  - stale per-board metadata (readme, emacs compile-command)

Run:  pytest tests/   (from repo root)
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KEYBOARDS = REPO_ROOT / "keyboards"
CANON_HEADER = (
    KEYBOARDS / "absolem_mauc" / "keymaps" / "default" / "absolem_layouts.h"
)
# Boards sharing the absolem layout via symlink (yask_trackball excluded:
# separate layout).
SHARED_BOARDS = [
    "absolem_mauc",
    "yask_bois",
    "chonky_bois",
    "signum_absolem",
    "box_o_alps",
    "box_o_alps_stm32f4x1",
]


def header_text():
    return CANON_HEADER.read_text()


def strip_comments(text):
    """Remove //-line and /* */-block comments (enough for this file)."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return "\n".join(
        ln for ln in text.splitlines() if not ln.lstrip().startswith("//")
    )


def active_lines(text):
    """Lines with live code (all comments stripped)."""
    return strip_comments(text).splitlines()


def test_canonical_header_exists():
    assert CANON_HEADER.is_file()


def test_shared_header_symlinks_intact():
    """All absolem boards must resolve to the canonical header file."""
    for board in SHARED_BOARDS:
        if board == "absolem_mauc":
            continue
        link = KEYBOARDS / board / "keymaps" / "default" / "absolem_layouts.h"
        assert link.is_symlink(), f"{board} header is no longer a symlink"
        assert link.resolve() == CANON_HEADER.resolve(), (
            f"{board} header points at {link.resolve()}, "
            f"expected {CANON_HEADER.resolve()}"
        )


def test_layer_count_matches_header():
    """keyboard.json layer_count must equal layers defined in header."""
    text = header_text()
    enum_m = re.search(r"enum layer_names \{(.*?)\};", text, re.S)
    assert enum_m, "enum layer_names not found"
    enum_layers = [
        n.strip() for n in enum_m.group(1).split(",") if n.strip()
    ]
    defined = set(re.findall(r"\[(_\w+)\]\s*=\s*LAYOUT_absolem", text))
    assert set(enum_layers) == defined, (
        f"enum {enum_layers} != keymaps array {sorted(defined)}"
    )
    for board in SHARED_BOARDS:
        kb_json = KEYBOARDS / board / "keyboard.json"
        if not kb_json.is_file():  # e.g. info.json-era boards
            continue
        data = json.loads(kb_json.read_text())
        lc = data.get("dynamic_keymap", {}).get("layer_count")
        assert lc == len(enum_layers), (
            f"{board}: layer_count={lc} but header defines "
            f"{len(enum_layers)} layers {enum_layers}"
        )


def test_combo_count_matches_header():
    """COMBO_COUNT in each config.h must equal active COMBO() entries."""
    n_combos = len(
        re.findall(r"^\s*COMBO\(", "\n".join(active_lines(header_text())), re.M)
    )
    assert n_combos > 0
    for board in SHARED_BOARDS:
        cfg = KEYBOARDS / board / "keymaps" / "default" / "config.h"
        m = re.search(r"#define\s+COMBO_COUNT\s+(\d+)", cfg.read_text())
        assert m, f"{board}: COMBO_COUNT not found"
        assert int(m.group(1)) == n_combos, (
            f"{board}: COMBO_COUNT={m.group(1)} but header has "
            f"{n_combos} active COMBO() entries"
        )


def test_no_duplicate_defines():
    seen = {}
    dupes = set()
    for ln in active_lines(header_text()):
        m = re.match(r"\s*#define\s+(\w+)", ln)
        if m:
            seen.setdefault(m.group(1), 0)
            seen[m.group(1)] += 1
            if seen[m.group(1)] > 1:
                dupes.add(m.group(1))
    assert not dupes, f"duplicate #defines: {sorted(dupes)}"


def test_no_deprecated_bare_reset():
    """Bare RESET was removed from QMK; use QK_BOOT. Skip LAYOUT/comments."""
    bad = [
        ln.strip()
        for ln in active_lines(header_text())
        if re.search(r"(?<![A-Z_])RESET(?![A-Z_])", ln)
    ]
    assert not bad, f"deprecated bare RESET found: {bad}"


def test_no_commented_out_layout_blocks():
    """Dead commented LAYOUT / combo / drag_scroll blocks must stay deleted."""
    commented_layout = [
        ln for ln in header_text().splitlines()
        if ln.lstrip().startswith("//") and "LAYOUT_absolem(" in ln
    ]
    assert not commented_layout, (
        f"commented-out layout blocks: {commented_layout}"
    )
    raw_combos = len(re.findall(r"COMBO\(", header_text()))
    live_combos = len(re.findall(r"COMBO\(", strip_comments(header_text())) )
    assert raw_combos == live_combos, (
        f"{raw_combos - live_combos} COMBO() entries stuck in comments"
    )
    assert "drag_scroll" not in header_text(), "dead drag_scroll block present"


def test_scroll_lock_exposed_on_base():
    base = re.search(
        r"\[_COLEMAK\]\s*=\s*LAYOUT_absolem\((.*?)\),",
        header_text(),
        re.S,
    ).group(1)
    assert "KC_SCRL" in base, "KC_SCRL missing from _COLEMAK base layer"


def test_recovery_keys_present():
    """QK_BOOT + EEPROM clear must be reachable (VIA shadows firmware)."""
    array = re.search(
        r"keymaps\[\]\[MATRIX_ROWS\]\[MATRIX_COLS\]\s*=\s*\{(.*)\};",
        header_text(),
        re.S,
    ).group(1)
    assert "QK_BOOT" in array or "QK_BOOTLOADER" in array, (
        "no bootloader key in keymap"
    )
    assert "QK_CLEAR_EEPROM" in array or "EE_CLR" in array, (
        "no EEPROM-clear key in keymap"
    )


def layout_args(inner):
    """Split a LAYOUT_* inner block into top-level comma-separated args."""
    args, depth, cur = [], 0, ""
    for ch in inner:
        if ch == "(":
            depth += 1
            cur += ch
        elif ch == ")":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            args.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        args.append(cur.strip())
    return args


def misc_bottom_row():
    """Bottom-row (10 keys) of the _MISC layer in wired order.

    Order: lx0 lx1 L31 L30 lx2 | rx0 R31 R30 rx1 rx2.
    lx*/rx* are UNWIRED on 34-key splits; wired thumbs are idx 2,3,6,7.
    """
    text = strip_comments(header_text())
    m = re.search(r"\[_MISC\]\s*=\s*LAYOUT_absolem\(", text)
    assert m, "_MISC layer not found"
    depth, i = 1, m.end()
    while depth:
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
        i += 1
    args = layout_args(text[m.end() : i - 1])
    assert len(args) == 40, f"_MISC has {len(args)} keys, expected 40"
    return args[30:40]


def test_misc_recovery_keys_on_wired_thumbs():
    bottom = misc_bottom_row()
    assert bottom[6] in ("QK_BOOT", "QK_BOOTLOADER"), (
        f"R31 should be bootloader key: {bottom}"
    )
    assert bottom[7] in ("QK_CLEAR_EEPROM", "EE_CLR"), (
        f"R30 should be EEPROM-clear key: {bottom}"
    )
    for idx in (0, 1, 4, 5, 8, 9):
        assert bottom[idx] == "KC_NO", (
            f"unwired pos {idx} must stay KC_NO, got {bottom[idx]}"
        )


def test_readme_titles_match_board():
    for board in SHARED_BOARDS:
        readme = KEYBOARDS / board / "keymaps" / "default" / "readme.md"
        if not readme.is_file():
            continue
        content = readme.read_text()
        assert re.search(rf"\b{re.escape(board)}\b", content), (
            f"{board}/readme.md does not mention {board}: {content.strip()!r}"
        )
        others = [
            b
            for b in SHARED_BOARDS
            if b != board and re.search(rf"\b{re.escape(b)}\b", content)
        ]
        assert not others, f"{board}/readme.md mentions wrong board(s): {others}"


def test_compile_commands_match_board():
    for board in SHARED_BOARDS:
        kc = KEYBOARDS / board / "keymaps" / "default" / "keymap.c"
        first = kc.read_text().splitlines()[0]
        if "compile-command" not in first:
            continue
        assert board in first, (
            f"{board}/keymap.c compile-command references another "
            f"board: {first.strip()!r}"
        )


def test_usb_pids_unique():
    pids = {}
    for kb_json in sorted(KEYBOARDS.glob("*/keyboard.json")):
        data = json.loads(kb_json.read_text())
        pid = data.get("usb", {}).get("pid")
        if pid:
            assert pid not in pids, (
                f"duplicate PID {pid}: {kb_json.parent.name} and {pids[pid]}"
            )
            pids[pid] = kb_json.parent.name
    assert pids
