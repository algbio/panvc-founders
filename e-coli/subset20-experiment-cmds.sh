#!/bin/bash

set -e

cat accession-list.txt | sort -n | while read x
do
	echo "snakemake --configfile config-common-call-subset20.yaml config-call-subset20/${x}.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 5 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=16384"
done
