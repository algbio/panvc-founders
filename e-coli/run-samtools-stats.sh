#!/bin/bash

set -e
set -x

samtools=samtools

ls call | while read x
do
	"${samtools}" stats -@ 4 "call/${x}/ext_vc/sortedfixed.gatk.bam" > "samtools-stats/${x}.panvc.gatk.txt"

	baseline_bam="call/${x}/baseline_vc/sortedfixed.gatk.bam"
	if [ -f "${baseline_bam}" ]
	then
		"${samtools}" stats -@ 4 "${baseline_bam}" > "samtools-stats/${x}.baseline.gatk.txt"
	fi

	#"${samtools}" stats -@ 4 "call/${x}/ext_vc/sorted-alns2.samtools.bam" > "samtools-stats/${x}.panvc.samtools.txt"
	#"${samtools}" stats -@ 4 "call/${x}/baseline_vc/sorted-alns2.samtools.bam" > "samtools-stats/${x}.baseline.samtools.txt"
done
