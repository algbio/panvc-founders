#!/bin/bash

set -e

python3 store_gap_positions.py --input indices/e-coli-msd5/e-coli-msd5/recombinant.n1.gapped --support-rank --output gap-positions/ref-positions.dat
