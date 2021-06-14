#!/bin/bash

set -e
set -x

ref=e.coli-k12-mg1655.no-linebreaks.fa

cat accession-list-de-novo.txt | grep -v -E "^[#]" | while read sample
do
	for msd in 5
	do
		for vc in gatk samtools
		do
			src_vcf_pg="call/${sample}-msd${msd}/ext_vc/pg_variants.${vc}.vcf"
			~/cs-home/vcf_to_unaligned --reference="${ref}" --variants="${src_vcf_pg}" --output="predicted/${sample}-msd${msd}.panvc.${vc}.fa" --log="predicted-log/${sample}-msd${msd}.panvc.${vc}.log" --fasta-header="${sample}" -s 0 -p 0 -c "e-coli-msd${msd}"
			src_vcf_baseline="call/${sample}-msd${msd}/baseline_vc/variants.${vc}.vcf"
			~/cs-home/vcf_to_unaligned --reference="${ref}" --variants="${src_vcf_baseline}" --output="predicted/${sample}-msd${msd}.baseline.${vc}.fa" --log="predicted-log/${sample}-msd${msd}.baseline.${vc}.log" --fasta-header="${sample}" -s 0 -p 0 -c "e-coli-msd${msd}"
		done
	done
done
