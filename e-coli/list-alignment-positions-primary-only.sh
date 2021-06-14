#!/bin/bash

set -e

ls -d call/*-msd5 | while read x
do
	acc="${x##*/}"
	samtools view -F 3844 ${x}/baseline_vc/sortedfixed.gatk.bam			| awk '{ print $4 }' | gzip > "aligned-positions-primary/${acc}.baseline.gatk.txt.gz"
	samtools view -F 3844 ${x}/ext_vc/sortedfixed.gatk.bam				| awk '{ print $4 }' | gzip > "aligned-positions-primary/${acc}.panvc.gatk.txt.gz"
	samtools view -F 3844 ${x}/baseline_vc/sorted-alns2.samtools.bam	| awk '{ print $4 }' | gzip > "aligned-positions-primary/${acc}.baseline.samtools.txt.gz"
	samtools view -F 3844 ${x}/ext_vc/sorted-alns2.samtools.bam			| awk '{ print $4 }' | gzip > "aligned-positions-primary/${acc}.panvc.samtools.txt.gz"
done
