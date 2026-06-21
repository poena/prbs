# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PRBS (Pseudo-Random Binary Sequence) generator toolkit in Python. It supports standard PRBS orders (prbs7, prbs9, prbs15, prbs23, prbs31) and user-defined LFSR polynomials. Output is hex-encoded, MSB-first.

## Running the Scripts

Both scripts share the same CLI interface:

```bash
# Pre-defined PRBS mode
python3 python/prbs.py --mode='prbs_7' --length=80 --width=32

# User-defined polynomial
python3 python/prbs.py --mode='user_define' --expression='[23,21,16,8,5,2]' --length=80 --width=64 --seed=0x1dbfbc

# Matrix-based generator (same flags)
python3 python/prbs_matrix_gen.py --mode='prbs_31' --length=160 --width=32
```

CLI flags: `-m/--mode`, `-l/--length`, `-w/--width`, `-e/--expression`, `-s/--seed`.

`prbs_matrix_gen.py` requires `numpy` (`pip install numpy`); `prbs.py` has no external dependencies.

## Architecture

There are two independent implementations of PRBS generation:

### `python/prbs.py` — Bit-serial LFSR simulation
Simulates the LFSR one bit at a time. `real_calculate_prbs` advances the shift register by XOR-ing the tapped positions (given as the `expression` list of tap indices), appends each output bit, then groups the bit sequence into hex words via `bin2hex`. The `expression` format is `[degree, tap1, tap2, ...]` where the first element is the LFSR length.

### `python/prbs_matrix_gen.py` — Matrix (parallel) approach
Computes PRBS output `parallel_width` bits at a time using GF(2) linear algebra. `base_matrix_gen` builds the companion matrix `A` for the LFSR polynomial, then multiplies it by itself `parallel_width` times (with mod-2 reduction) to form a transformation matrix `M`. `prbs_next` applies `M` to the current state vector to produce the next `parallel_width` output bits in one step. This approach is suited for hardware verification where you need to advance the PRBS state by a fixed word width.

### Shared conventions
- PRBS polynomials are stored as `[init_seed, [degree, tap, ...]]` in the predefined dict.
- The `expression` list uses 1-based tap indices matching the standard polynomial notation (e.g., `[7, 6]` means x^7 + x^6 + 1).
- `bin2hex` pads the last group and formats each word as `0x`-prefixed hex with width `out_len//4` nibbles.
