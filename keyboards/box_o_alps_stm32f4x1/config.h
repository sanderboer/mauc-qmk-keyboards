// -*- compile-command: (concat "pushd " sndr-project-root " && lxqt-sudo make bo_o_alps:default:avrdude-split-right"); -*-
/*
Copyright 2022 Sander Boer

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

#include "config_common.h"

/* USB Device descriptor parameter */
#define VENDOR_ID 0xFEED
#define PRODUCT_ID 0x0000
#define DEVICE_VER 0x0001
#define MANUFACTURER Sander Boer
#define PRODUCT Box_o_alps
#define DESCRIPTION A custom boxy keyboard

/* key matrix size */
//according to crkbd rows are doubled ?
#define MATRIX_ROWS 7
#define MATRIX_COLS 10

/* key matrix pins */

/*
#define MATRIX_ROW_PINS { B3, B4, B5, B6, C15, C14, C13 } // pins A0, 15, 14, 16
#define MATRIX_COL_PINS { A8, A9, A10, A11, A12, A4, A5, A6, A7, B0 }

Another quirk of F401 and F411 (not really specific to WeAct boards) is that, in additions to USB pins (A11 and A12), pins A9 and B2 are also not usable for the matrix (A9 has an undocumented internal pulldown due to its intended usage for USB VBUS sensing, and B2 is used as the BOOT1 input during reset, so it needs an external pulldown to make it possible to enter DFU). It may be possible to use pins A9 and B2 for some other purposes that are compatible with having a pulldown on the pin.
*/
#define MATRIX_ROW_PINS { B3, B4, B5, B6, C15, C14, C13 } // pins A0, 15, 14, 16



// unusable: A9, A11, A12, B2, B0
// A8 => B13, A9 => B14, A10 => B15, A11 => B7, A12 => B8
//#define MATRIX_COL_PINS { B13, B14, B15, B7, B8, A0, A7, A6, A5, A4 }

// unusable: A9, A11, A12, B2
// A9 => B14,  A11 => B7, A12 => B8
#define MATRIX_COL_PINS { A8, B13, A10, B14, B15, B0, A7, A6, A5, A4 }


// #define MATRIX_ROW_PINS { C15, C14, C13 } // pins A0, 15, 14, 16
// #define MATRIX_COL_PINS { A8, A9,  B0 }



/* COL2ROW, ROW2COL*/
#define DIODE_DIRECTION COL2ROW

/* Set 0 if debouncing isn't needed */
// #define DEBOUNCE 5
#define DEBOUNCE 10

/* Mechanical locking support. Use KC_LCAP, KC_LNUM or KC_LSCR instead in keymap */
#define LOCKING_SUPPORT_ENABLE
