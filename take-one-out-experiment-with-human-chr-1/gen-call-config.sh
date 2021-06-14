#!/bin/bash

set -e

python3 ../panvc-sample-workflow/generate_snakemake_config_for_call.py --pgindex-dir index --output-dir call --benchmark-dir benchmark-call -r1 sampled-reads/ERR194147_1.sample05.fastq.gz -r2 sampled-reads/ERR194147_2.sample05.fastq.gz --store-merged-reads-with-originals --vc-method GATK SAMTOOLS --ploidy 2 --ploidy-file GRCh37 --max-memory-MB 100000 --output-config config-call.yaml
