#!/bin/bash

set -e
set -x


cat accession-list-de-novo.txt | grep -v -E "^[#]" | while read sample
do
	for msd in 5 #10 20 50 100
	do
		for vc in gatk samtools
		do
			for wf in baseline panvc
			do
				#contigs="../e-coli-de-novo/spades/${sample}/contigs.fasta"
				contigs="de-novo/${sample}/contigs.fa.gz"
				ref="predicted/${sample}-msd${msd}.${wf}.${vc}.fa"
				quast_dir="quast/${sample}-msd${msd}.${wf}.${vc}.d"
				quast.py "${contigs}" -r "${ref}" -t 70 -o "${quast_dir}"
			done
		done
	done
done
