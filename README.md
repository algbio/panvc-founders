# PanVC with Founder Sequences

> **_NOTE:_**  We are currently updating the experiment scripts in the repository. In case you would like to run the new experiments in our revised manuscript, please contact us by e-mail.

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

### Founder quality experiment

#### Running the experiment

 1. `cd founder-quality-experiment`
 2. Download (some of) the reads used in the experiment and extract. Please see the commands below. The reads should be automatically placed in a subdirectory called *reads*.
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov10.tar`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov20.tar`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov50.tar`
    * `tar xf cov10.tar`
    * `tar xf cov20.tar`
    * `tar xf cov50.tar`
 3. Download (some of) the indices used in the experiment and extract. Please see the commands below. Each index should be automatically placed in its own subdirectory, *index-founders* and *index-predicted*.
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/indices/index-founders.tar.bz2`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/indices/index-predicted.tar.bz2`
    * `tar xjf index-founders.tar.bz2`
    * `tar xjf index-predicted.tar.bz2`
 4. Download the [truthset variants](https://github.com/Illumina/PlatinumGenomes/) with e.g.`wget https://s3.eu-central-1.amazonaws.com/platinum-genomes/2017-1.0/hg38/small_variants/NA12877/NA12877.vcf.gz`
 5. Get the human chromosome 21 GRCh38 reference sequence. We used the following:
    * `wget http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa`
    The provided Snakefile will extract the chromosome in question to a file called *chr21.fa* with the identifier *chr21*.
 6. Run the variant calling workflow with the following commands.
    * `snakemake --configfile config-common-call.yaml config-call/founders-10.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/founders-20.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/founders-50.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/predicted-10.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/predicted-20.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/predicted-50.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
  7. Run Snakemake to compare the results to the truthset variants with e.g. `snakemake --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env`. The comparison results will be placed to a subdirectory called *hap.py*.
  8. Run `python3 summarize.py` to create a summary of hap.py’s results.

#### Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archives themselves have not been re-compressed.)

| File                                                                                                    | Coverage |
| ------------------------------------------------------------------------------------------------------- | -------- |
| [cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov10.tar) | 10x      |
| [cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov20.tar) | 20x      |
| [cov50.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov50.tar) | 50x      |

#### Indices for use with `Snakefile.call`

The following archives contain indices generated with `Snakefile.index`.

| Index | Index file |
| ----- | ---------- |
| Index generated with founder sequences | [index-founders.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/indices/index-founders.tar.bz2) |
| Index generated with all predicted sequences | [index-predicted.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/indices/index-predicted.tar.bz2) |

#### Sequences used as input when generating the indices

| Input | File |
| ----- | ---- |
| Founder sequences | [founder-sequences.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/index-input/founder-sequences.a2m.bz2) |
| Predicted sequences | [predicted-sequences.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/index-input/predicted-sequences.a2m.bz2) |

---

### Experiments with artificial mutations

#### Running the experiment

The experiment consists of running the workflow with 192 different inputs. For testing purposes, a subset of the inputs may be used. To run the experiment, please follow these steps.

To simplify running the experiment, the repository contains a helper script, [experiment\_helper.py](experiments-with-artificial-mutations/experiment_helper.py). All its available options may be listed with `python3 experiment_helper.py --help`.

 1. `cd experiments-with-artificial-mutations`
 2. The identifiers of the inputs are listed in [all-experiment-names.txt](experiments-with-artificial-mutations/all-experiment-names.txt). Decide with which inputs to run the experiment, copy the list with e.g. `cp -i all-experiment-names.txt experiment-names.txt` and possibly remove some of the lines in order to run the experiment with fewer inputs.
 3. Do one of the following:
    * Download prepared indices needed to run the experiment as follows:
        1. Create a list of the compressed index URLs with `python3 experiment_helper.py --print-index-urls --experiment-list experiment-names.txt > index-urls.txt`
        2. Download the files with e.g. `wget --content-disposition --trust-server-names -i index-urls.txt`
        3. Extract the contents of the archives with e.g. `ls *.tar.bz2 | while read x; do pbzip2 -d -c "$x" | tar x; done`. The indices should be automatically placed in a subdirectory called *indices*. The downloaded .tar.gz files are not needed after this step.
    * Download A2M inputs and generate the indices as follows:
        1. Create a list of the corresponding input files with `python3 experiment_helper.py --print-index-input-urls --experiment-list experiment-names.txt > index-input-urls.txt`
        2. Download the files with e.g. `wget --content-disposition --trust-server-names -i index-input-urls.txt`
        3. Extract the contents of the archives to a subdirectory called *a2m*.
        4. Get a list of commands to generate the indices from experiment\_helper.py. These may be piped directly to the shell with e.g. `python3 experiment_helper.py --print-indexing-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 32 --conda-prefix ../conda-env --resources mem_mb=16000' | bash -x -e`. Alternatively, since some of the steps of the workflow have not been parallelised, the commands may be written to a file and executed with e.g. [GNU Parallel](https://www.gnu.org/software/parallel/): `python3 experiment_helper.py ... > index-commands.txt; parallel -j16 < index-commands.txt`.
 4. Download [the reads used in the experiment](#reads-used-in-the-experiment-1) and extract. Please see the commands below. The compressed FASTQ files should be automatically placed in a subdirectory called *genreads*. (In addition to the separate read files, some parts of the workflow require all the reads in one file. The file is automatically generated as part of the workflow but we also provide the generated files.)
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov10.tar`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov20.tar`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov10-renamed.tar`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov20-renamed.tar`
    * `tar xf genreads-cov10.tar`
    * `tar xf genreads-cov20.tar`
    * `tar xf genreads-cov10-renamed.tar`
    * `tar xf genreads-cov20-renamed.tar`
 5. Download [sequences-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/sequences-truth.tar.gz) and extract. The plain text files should be automatically placed in a subdirectory called *sequences-truth*.
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/sequences-truth.tar.gz`
    * `tar xzf sequences-truth.tar.gz`
 6. Download [e.coli.fa.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/e.coli.fa.gz) and extract. Some of our tools require the sequence part of the FASTA to not contain any newlines; we have modified the file accordingly.
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/e.coli.fa.gz`
    * `gunzip e.coli.fa.gz`
 7. Run the variant calling workflow. To this end, get a list of commands from experiment\_helper.py. These may be piped directly to the shell with e.g. `python3 experiment_helper.py --print-variant-calling-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 32 --conda-prefix ../conda-env --resources mem_mb=16000' | bash -x -e`.
 8. Generate the predicted sequences from the variants. As the process is rather I/O intensive, we recommend using one core with Snakemake: `python3 experiment_helper.py --print-predicted-sequence-generation-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 1 --conda-prefix ../conda-env' | bash -x -e`
 9. Compare the predicted sequences to the truth with Edlib: `python3 experiment_helper.py --print-sequence-comparison-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 32 --conda-prefix ../conda-env --resources mem_mb=16000' | bash -x -e`
 10. Run `./summarize-edlib-scores.sh` to create a summary of the calculated scores in TSV format.

The generated files are placed in subdirectories as listed in the following table.

| Result                                     | Directory                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| Edit distances from the truth              | edlib-scores                                                                          |
| Predicted sequences                        | predicted-sequences/*experiment-identifier*/predicted.*workflow*.*variant-caller*.txt |
| Variants called with the PanVC workflow    | call/*experiment-identifier*/ext\_vc/pg\_variants.*variant-caller*.vcf                |
| Variants called with the baseline workflow | call/*experiment-identifier*/baseline\_vc/variants.*variant-caller*.vcf               |

#### Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archive itself has not been re-compressed.)

| Reads | Coverage | Note |
| ----- | -------- | ---- |
| [genreads-cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov10.tar) | 10 | |
| [genreads-cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov20.tar) | 20 | |
| [genreads-cov10-renamed.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov10-renamed.tar) | 10 | All reads in one file |
| [genreads-cov20-renamed.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov20-renamed.tar) | 20 | All reads in one file |

#### Variants

The following archives contain the actual (not predicted) variants in the generated samples. The identifier of the removed sample in all cases is `SAMPLE0`.

| Description | File |
| ----------- | ---- |
| Samples removed in the experiments | [variants-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/variants-truth.tar.gz) |
| All samples | [variants-all.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/variants-all.tar.gz) |

#### Sequences of the removed samples

The following archives contain the actual sequences of the samples that were removed in the experiments.

| Sequences |
| --------- |
| [sequences-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/sequences-truth.tar.gz) |

#### Indices for use with `Snakefile.call`

Archives that contain the pregenerated indices have been listed [on a separate page](experiments-with-artificial-mutations/e-coli-indices.md).

#### Founder sequences used when generating the indices

| All sequences in one archive |
| ---------------------------- |
| [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2) |

Individual sequence files have been listed [on a separate page](experiments-with-artificial-mutations/e-coli-index-inputs.md).

---

### Take-one-out experiment with human chromosome 21

#### Running the experiment

 1. `cd take-one-out-experiment-with-human-chr-21`
 2. Download (some of) the reads used in the experiment and extract. Please see the commands below. The reads should be automatically placed in a subdirectory called *reads*.
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/reads/cov10.tar`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/reads/cov20.tar`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/reads/cov50.tar`
    * `tar xf cov10.tar`
    * `tar xf cov20.tar`
    * `tar xf cov50.tar`
 3. Download (some of) the indices used in the experiment and extract. Please see the commands below. Each index should be automatically placed in its own subdirectory under *indices*.
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/index-no-HG00513.tar.bz2`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/index-no-HG00731.tar.bz2`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/index-no-NA12273.tar.bz2`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/index-no-NA18954.tar.bz2`
    * `wget https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/index-no-NA19238.tar.bz2`
    * `tar xjf index-no-HG00513.tar.bz2`
    * `tar xjf index-no-HG00731.tar.bz2`
    * `tar xjf index-no-NA12273.tar.bz2`
    * `tar xjf index-no-NA18954.tar.bz2`
    * `tar xjf index-no-NA19238.tar.bz2`
 4. Download the [hs37d5 reference](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz) and extract. The provided Snakefile will extract the chromosome in question to a file called chr21.fa with the identifier chr21.
 5. Download the [reference dataset](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz) and extract. The provided Snakefile will extract the tested samples.
 6. Run the variant calling workflow with the following commands.
    * `snakemake --configfile config-common-call.yaml config-call/HG00513-cov10.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/HG00731-cov10.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA12273-cov10.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA18954-cov10.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA19238-cov10.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/HG00513-cov20.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/HG00731-cov20.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA12273-cov20.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA18954-cov20.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA19238-cov20.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/HG00513-cov50.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/HG00731-cov50.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA12273-cov50.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA18954-cov50.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
    * `snakemake --configfile config-common-call.yaml config-call/NA19238-cov50.yaml --snakefile ../panvc-sample-workflow/Snakefile.call --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=100000`
 7. Run Snakemake to compare the results to the truthset variants with e.g. `snakemake --cores 32 --printshellcmds --use-conda --conda-prefix ../conda-env`. The comparison results will be placed to a subdirectory called *hap.py*.
 8. Run `python3 summarize.py > summary.csv` to create a summary from the results.


#### Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archives themselves have not been re-compressed.)

| File | Coverage |
| ---- | -------- |
| [cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/reads/cov10.tar) | 10x |
| [cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/reads/cov20.tar) | 20x |
| [cov50.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/reads/cov50.tar) | 50x |

#### Indices for use with `Snakefile.call`

The following archives contain indices generated with `Snakefile.index`.

| Index file |
| ---------- |
| [no-HG00513.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/no-HG00513.tar.bz2) |
| [no-HG00731.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/no-HG00731.tar.bz2) |
| [no-NA12273.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/no-NA12273.tar.bz2) |
| [no-NA18954.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/no-NA18954.tar.bz2) |
| [no-NA19238.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/panvc-indices/no-NA19238.tar.bz2) |

#### Founder sequences used when generating the indices

| Sequence file |
| ------------- |
| [no-HG00513.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/founder-sequences/no-HG00513.tar.bz2) |
| [no-HG00731.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/founder-sequences/no-HG00731.tar.bz2) |
| [no-NA12273.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/founder-sequences/no-NA12273.tar.bz2) |
| [no-NA18954.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/founder-sequences/no-NA18954.tar.bz2) |
| [no-NA19238.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr21/founder-sequences/no-NA19238.tar.bz2) |

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
