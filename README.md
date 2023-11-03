# PanVC with Founder Sequences

> **_NOTE:_** This repository contains the experiments described in our reviesed manuscript completed in the end of May 2021. In case there are any problems running the experiments, please contact us by e-mail.

PanVC is a set of tools to be used as part of a variant calling workflow that uses short reads as its input. The reads are aligned to an index generated from a multiple sequence alignment. A suitable index may be built from founder sequences.

Running a variant calling workflow that utilizes PanVC consists of the following phases:

 * Generating founder sequences from known variants
 * Indexing the founder sequences
 * Running the read alignment and variant calling workflow

Our software consists of the following components:

 * [vcf2multialign](https://github.com/tsnorri/vcf2multialign) for generating founder sequences and predicted sequences from known variants
 * [PanVC](https://gitlab.com/dvalenzu/PanVC/-/tree/PanVC-2.0-rc-tsnorri) includes tools for various phases of the variant calling workflow, including indexing the known sequences, aligning short reads to the index and generating an ad-hoc reference sequence for re-aligning the reads
 * [PanVC sample workflow](https://github.com/algbio/panvc-sample-workflow) for running a variant calling workflow that utilizes PanVC


## Requirements
 
 * [Snakemake](https://snakemake.readthedocs.io/) (tested with version 5.24.0)
 * [Conda](https://conda.io/) (tested with version 4.8.5)


## Installing

All necessary components for running the experiments from our provided inputs are installed by running Snakemake, which in turn invokes Conda. To install the components to a predefined location, e.g. in `conda-env` in the root of the cloned repository, please run the following commands. (By default, i.e. when `--conda-prefix` is not given, the Conda environment is placed in a hidden .snakemake directory in the working directory when Snakemake is run. This may be less convenient for running multiple experiments.)

Please note, however, that prebuilt binaries for some of the software are only available for Linux on x86-64.

 1. Clone the repository with `git clone --recursive https://github.com/algbio/panvc-founders.git`
 2. `cd panvc-founders`
 3. Prepare the Conda environments with the following command:
    * `snakemake --cores 1 --printshellcmds --use-conda --conda-prefix ./conda-env conda_environment conda_environment_gatk conda_environment_edlib conda_environment_happy conda_environment_vcfcat`


## Running the experiments

On a high level, the experiments are run as follows:

 1. Decide which experiments to run and possibly modify the configuration files in the subdirectory of the corresponding experiment.
 2. Download and unarchive the reads provided with the experiments
 3. Do one of the following:
    * Download and unarchive the pre-generated indices provided with the experiments in question and call variants by running Snakemake
    * Download and decompress the founder sequences provided with the experiments in question, generate the index and call variants by running Snakemake
 4. Process the variant calling results to e.g. calculate edit distances from a specific sequence or calculate statistics from the called variants.

We provide scripts to automatize these steps.

Each experiment involves aligning different sets of reads to different indices. Inputs for the [artificial mutation experiment](#experiments-with-artificial-mutations) are the smallest and therefore parts of the experiment should be the fastest to run.

---

## Experiment data

### Experiments with artificial mutations

Please see [README.md](experiments-with-artificial-mutations/README.md) under [experiments-with-artificial-mutations](experiments-with-artificial-mutations).

---

### Experiments with natural E.coli reads

Please see [README.md](e-coli/README.md) under [e-coli](e-coli).

---

### Take-one-out experiment with human chromosome 1

Please see [README.md](take-one-out-experiment-with-human-chr-1/README.md) under [take-one-out-experiment-with-human-chr-1](take-one-out-experiment-with-human-chr-1).

---

### Scalability experiment

#### Running the experiment

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
