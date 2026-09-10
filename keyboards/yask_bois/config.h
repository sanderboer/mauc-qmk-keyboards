/*
Copyright 2020 Sander Boer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#pragma once

// Split handedness is stored in EEPROM (set by flashing
// uf2-split-left / uf2-split-right once per half).
#define EE_HANDS
// Right half is the USB master: plug USB into the right side and
// `qmk flash -kb yask_bois -km default -bl uf2-split-right` is enough
// for keymap-only changes. Flash both halves after an EEPROM clear
// to restore handedness.
#define MASTER_RIGHT

#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_TIMEOUT 200U
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_LED GP17
