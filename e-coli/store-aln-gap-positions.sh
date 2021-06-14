#!/bin/bash

set -e

ls -d call/*-msd5 | while read x
do
	acc="${x##*/}"
	input="call/${acc}/adhoc_ref_files/e-coli-msd5/adhoc_reference.aligned_to_ref"
	echo "${acc}"
	python3 store_gap_positions.py --input "${input}" --support-select --output "gap-positions/${acc}-adhoc-ref-positions.dat"
done
