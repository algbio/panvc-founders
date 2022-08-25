# Take-one-out experiment with human chromosome 1

This directory contains the scripts needed to run the take-one-out experiment with human chromosome 1.

## Running the experiment

1. Download the [indexing input](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr1/human-chr1-a2m.tar.bz2) with e.g. `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr1/human-chr1-a2m.tar.bz2`. Extract the contents to the `take-one-out-experiment-with-human-chr-1` directory with e.g. `pbzip2 -dc human-chr1-a2m.tar.bz2 | tar x`.
2. Download the [sampled reads](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr1/human-chr1-sampled-reads.tar) with e.g. `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr1/human-chr1-sampled-reads.tar`. Extract the contents with `tar xf human-chr1-sampled-reads.tar`.
3. Download the [Genome in a Bottle truthset](http://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/NA12878_HG001/latest/GRCh37/HG001_GRCh37_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer.vcf.gz) and the associated [TBI index](http://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/NA12878_HG001/latest/GRCh37/HG001_GRCh37_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer.vcf.gz.tbi) with e.g. the following commands:
   * `wget ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/NA12878_HG001/latest/GRCh37/HG001_GRCh37_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer.vcf.gz`
   * `wget ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/NA12878_HG001/latest/GRCh37/HG001_GRCh37_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer.vcf.gz.tbi`
4. Download the [hs37d5 reference](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz) and extract with e.g. `wget http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz && gunzip hs37d5.fa.gz`. 
5. Generate the index for PanVC with e.g. the following command: `snakemake --configfile config-index.yaml --snakefile ../panvc-sample-workflow/Snakefile.index --cores 72 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
6. Run the workflow with e.g. the following command: `snakemake --configfile config-call.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 88 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
7. Run Hap.py with e.g. `snakemake --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env`. The results are placed in `hap.py`.
