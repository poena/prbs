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

# Galois LFSR structure instead of the default Fibonacci
python3 python/prbs.py --mode='prbs_7' --length=80 --width=32 --type='galois'
```

CLI flags: `-m/--mode`, `-l/--length`, `-w/--width`, `-e/--expression`, `-s/--seed`, `-t/--type`.

`prbs_matrix_gen.py` requires `numpy` (`pip install numpy`); `prbs.py` has no external dependencies.

## Architecture

There are two independent implementations of PRBS generation:

### `python/prbs.py` — Bit-serial LFSR simulation
Simulates the LFSR one bit at a time. `real_calculate_prbs` advances the shift register by XOR-ing the tapped positions (given as the `expression` list of tap indices), appends each output bit, then groups the bit sequence into hex words via `bin2hex`. The `expression` format is `[degree, tap1, tap2, ...]` where the first element is the LFSR length.

### `python/prbs_matrix_gen.py` — Matrix (parallel) approach
Computes PRBS output `parallel_width` bits at a time using GF(2) linear algebra. `base_matrix_gen` builds the companion matrix `A` for the LFSR polynomial, then multiplies it by itself `parallel_width` times (with mod-2 reduction) to form a transformation matrix `M`. `prbs_next` applies `M` to the current state vector to produce the next `parallel_width` output bits in one step. This approach is suited for hardware verification where you need to advance the PRBS state by a fixed word width.

### LFSR structure: Fibonacci vs Galois
Both scripts accept `-t/--type` with `fibonacci` (default, the original behavior) or `galois`. The two forms are separate register topologies for the same polynomial, so they emit the *same* m-sequence but at a different phase — do not expect identical hex output between them. Verified equivalence: for prbs_15 the Galois stream is the Fibonacci stream rotated by 32753 of its 32767-bit period.

- **Fibonacci** — taps are XOR-ed together and fed back into one end; output is the bit shifted out. `prbs.py:real_calculate_prbs`.
- **Galois** — the bit shifted out toggles every tap position in parallel. `prbs.py:galois_calculate_prbs`, which builds an integer toggle mask with bit `t-1` set for each term of `expression`. The degree term is included and is the feedback into the top bit, so the mask comes from iterating the whole `expression` list, not `expression[1:]`.

In `prbs_matrix_gen.py` the choice only affects `companion_matrix`, which returns `eye(n, k=1)` with a tap-populated bottom row for Fibonacci, or `eye(n, k=-1)` with a tap-populated last column for Galois. Everything downstream is shared.

### Shared conventions
- PRBS polynomials are stored as `[init_seed, [degree, tap, ...]]` in the predefined dict.
- The `expression` list uses 1-based tap indices matching the standard polynomial notation (e.g., `[7, 6]` means x^7 + x^6 + 1).
- State vectors in `prbs_matrix_gen.py` are MSB-first (`v[i]` is bit `n-1-i`); `prbs.py:real_calculate_prbs` reverses to LSB-first internally. Watch this when comparing the two implementations.
- `bin2hex` pads the last group and formats each word as `0x`-prefixed hex with width `out_len//4` nibbles.

## Verifying changes

There is no test suite. To check a generator change, assert the properties an m-sequence must have — period `2^n - 1` and `2^(n-1)` ones per period:

```bash
cd python && python3 -c "
import prbs
n=9; L=(1<<n)-1
s=prbs.generate_prbs('prbs_9',length=2*L,lfsr_type='galois')
print(all(s[i]==s[i+L] for i in range(L)), sum(s[:L])==(L+1)//2)"
```

Changes to `prbs_matrix_gen.py` are best checked by stepping `companion_matrix` against the bit-serial implementation in `prbs.py` one state at a time, rather than by eyeballing hex.
