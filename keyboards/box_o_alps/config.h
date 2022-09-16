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
#define DEVICE_VER 0x0011
#define MANUFACTURER Sander Boer
#define PRODUCT Box_o_alps
#define DESCRIPTION A custom boxy keyboard

/* key matrix size */
//according to crkbd rows are doubled ?
#define MATRIX_ROWS 4
#define MATRIX_COLS 10

/* key matrix pins */

// #define MATRIX_ROW_PINS { B3, B4, B5, B6, C15, C14, C13 } // pins A0, 15, 14, 16
// #define MATRIX_COL_PINS { A8, A9, A10, A11, A12, A4, A5, A6, A7, B0 }
// A5 A6 A7 B6 A8 A9 A12
// B1 B4 B5 B6 B7 B8 B9 B12
#define MATRIX_ROW_PINS { D7, E6, B4, B5 }
#define MATRIX_COL_PINS { B3, B2, D1, D0, D4, B1, F7, F6, F5, F4 }


/* COL2ROW, ROW2COL*/
#define DIODE_DIRECTION COL2ROW

/* Set 0 if debouncing isn't needed */
// #define DEBOUNCE 5
#define DEBOUNCE 0

/* Mechanical locking support. Use KC_LCAP, KC_LNUM or KC_LSCR instead in keymap */
#define LOCKING_SUPPORT_ENABLE
