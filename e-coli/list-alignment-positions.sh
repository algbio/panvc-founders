#!/bin/bash

set -e

ls -d call/*-msd5 | while read x
do
	acc="${x##*/}"
	echo "${x}"
	samtools view -F 1540 ${x}/baseline_vc/sortedfixed.gatk.bam			| awk '{ print $4 }' | gzip > "aligned-positions/${acc}.baseline.gatk.txt.gz"
	samtools view -F 1540 ${x}/ext_vc/sortedfixed.gatk.bam				| awk '{ print $4 }' | gzip > "aligned-positions/${acc}.panvc.gatk.txt.gz"
	samtools view -F 1540 ${x}/baseline_vc/sorted-alns2.samtools.bam	| awk '{ print $4 }' | gzip > "aligned-positions/${acc}.baseline.samtools.txt.gz"
	samtools view -F 1540 ${x}/ext_vc/sorted-alns2.samtools.bam			| awk '{ print $4 }' | gzip > "aligned-positions/${acc}.panvc.samtools.txt.gz"
done
