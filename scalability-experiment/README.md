# Scalability Experiment

This directory contains the scripts needed to run the scalability experiment.

## Running the experiment

 1. `cd scalability-experiment`
 2. Download the index inputs and extract. Please see the commands below. The files should be automatically placed in a subdirectory called *a2m*.
     * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/a2m-msd30.tar.bz2`
     * `pbzip2 -dc a2m-msd30.tar.bz2 | tar x`
 3. Download the reads. Please see the commands below.
     * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/reads/ERR1025645_sample05_1.fq.gz`
     * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/reads/ERR1025645_sample05_2.fq.gz`
 4. Run Snakemake to generate the index for PanVC with e.g. `snakemake --configfile config-index.yaml --snakefile ../panvc-sample-workflow/Snakefile.index --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=500000`
 5. Run Snakemake to align the reads with PanVC with e.g. `snakemake --configfile config-ERR1025645-pg.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=500000 -- call-ERR1025645-pg/ext_vc/sorted-alns2.samtools.bam`
 6. Run Snakemake to generate an index and align the reads with baseline with e.g. `snakemake --configfile config-ERR1025645-baseline.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=500000 -- call-ERR1025645-baseline/baseline_vc/sorted-alns2.samtools.bam`

The alignments for PanVC and baseline will be placed in *call-ERR1025645-pg/ext_vc/sorted-alns2.samtools.bam* and *call-ERR1025645-baseline/baseline_vc/sorted-alns2.samtools.bam* respectively. The benchmarks will be located in the following directories:

| Path                           | Description                                |
| ------------------------------ | ------------------------------------------ |
| benchmark-index-combined-msd30 | PanVC’s indexing steps                     |
| benchmark-ERR1025645-pg        | PanVC’s read mapping steps                 |
| benchmark-ERR1025645-baseline  | Baseline’s indexing and read mapping steps |

To collect the benchmarks from one directory to a single file, *summarize-benchmark.sh* may be used, e.g. `summarize-benchmark.sh benchmark-index-combined-msd30`. The script will prepend two columns to Snakemake’s benchmarking output: The first will contain the name of the step in the workflow and the value of the second will be “panvc” in the case of PanVC-specific steps. When running the baseline workflow, a step called “bwa_index_ref” will generate the index. In the case of PanVC, the same step is part of the read alignment and variant calling workflow because the index for BWA is generated from the ad hoc reference.
