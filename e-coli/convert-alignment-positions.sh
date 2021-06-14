#!/bin/bash

set -e

ls -d call/*-msd5 | while read x
do
	echo "${x}"
	acc="${x##*/}"
	for vc in gatk #samtools
	do
		python3 convert_alignment_positions.py --alignment-positions "aligned-positions/${acc}.panvc.${vc}.txt.gz" --reference-positions gap-positions/ref-positions.dat --ad-hoc-reference-positions "gap-positions/${acc}-adhoc-ref-positions.dat" | gzip > "converted-aligned-positions/${acc}.panvc.${vc}.txt.gz"
	done
done
