# PanVC with Founder Sequences

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

All necessary components for running the experiments from our provided inputs are installed by running Snakemake, which in turn invokes Conda. To install the components to a predefined location, please run the following commands. (By default, i.e. when `--conda-prefix` is not given, the Conda environment is placed in a hidden .snakemake directory in the working directory when Snakemake is run. This may be less convenient for running multiple experiments.)

Please note, however, that prebuilt binaries for some of the software are only available for Linux on x86-64.

 1. Clone the repository with `git clone --recursive https://github.com/algbio/panvc-founders.git`
 2. `cd panvc-founders`
 3. Prepare the Conda environments with the following commands:
    * `snakemake --cores 1 --printshellcmds --use-conda --conda-prefix /path/to/conda/environment conda_environment`
    * `snakemake --cores 1 --printshellcmds --use-conda --conda-prefix /path/to/conda/environment conda_environment_gatk`
    * `snakemake --cores 1 --printshellcmds --use-conda --conda-prefix /path/to/conda/environment conda_environment_experiments`


## Running the experiments

On a high level, the experiments are run as follows:

 1. Decide which experiments to run and modify the configuration files in the subdirectory of the corresponding experiment.
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

#### Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archives themselves have not been re-compressed.)

| File | Coverage |
| ---- | -------- |
| [cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov10.tar) | 10x |
| [cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov20.tar) | 20x |
| [cov50.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/reads/cov50.tar) | 50x |

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

See [experiments-with-artificial-mutations](experiments-with-artificial-mutations) for sample scripts.

#### Running the experiment

The experiment consists of running the workflow with 192 different inputs. For testing purposes, a subset of the inputs may be used. To run the experiment, please follow these steps.

To simplify running the experiment, we provide a helper script, [experiment\_helper.py](experiments-with-artificial-mutations/experiment_helper.py). All its available options may be listed with `python3 experiment_helper.py --help`.

 1. `cd experiments-with-artificial-mutations`
 2. The identifiers of the inputs are listed in [all-experiment-names.txt](experiments-with-artificial-mutations/all-experiment-names.txt). Decide with which inputs to run the experiment, copy the list with e.g. `cp -i all-experiment-names.txt experiment-names.txt` and possibly remove some of the lines in order to run the experiment with fewer inputs.
 3. Do one of the following:
    * Download prepared indices needed to run the experiment as follows:
        1. Create a list of the compressed index URLs with `python3 experiment_helper.py --print-index-urls --experiment-list experiment-names.txt > index-urls.txt`
        2. Download the files with e.g. `wget --content-disposition --trust-server-names -i index-urls.txt`
        3. Extract the contents of the archives. The indices should be automatically placed in a subdirectory called *indices*. The downloaded .tar.gz files are not needed after this step.
    * Download A2M inputs and generate the indices as follows:
        1. Create a list of the corresponding input files with `python3 experiment_helper.py --print-index-input-urls --experiment-list experiment-names.txt > index-input-urls.txt`
        2. Download the files with e.g. `wget --content-disposition --trust-server-names -i index-input-urls.txt`
        3. Extract the contents of the archives to a subdirectory called *a2m*.
        4. Get a list of commands to generate the indices from experiment\_helper.py. These may be piped directly to the shell with e.g. `python3 experiment_helper.py --print-indexing-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 32 --conda-prefix /path/to/conda/environment --resources mem_mb=16000' | bash -x -e`.
 4. Download [the reads used in the experiment](#reads-used-in-the-experiment-1) and extract. The compressed FASTQ files should be automatically placed in a subdirectory called *genreads*. (In addition to the separate read files, some parts of the workflow require all the reads in one file. The file is automatically generated as part of the workflow but we also provide the generated files.)
 5. Download [sequences-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/sequences-truth.tar.gz) and extract. The plain text files should be automatically placed in a subdirectory called *sequences-truth*.
 6. Run the variant calling workflow. To this end, get a list of commands from experiment\_helper.py. These may be piped directly to the shell with e.g. `python3 experiment_helper.py --print-variant-calling-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 32 --conda-prefix /path/to/conda/environment --resources mem_mb=16000' | bash -x -e`.
 7. Generate the predicted sequences from the variants. As the process is rather I/O intensive, we recommend using one core with Snakemake: `python3 experiment_helper.py --print-predicted-sequence-generation-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 1 --conda-prefix /path/to/conda/environment' | bash -x - e`
 8. Compare the predicted sequences to the truth with Edlib: `python3 experiment_helper.py --print-sequence-comparison-commands --experiment-list experiment-names.txt --snakemake-arguments '--cores 32 --conda-prefix /path/to/conda/environment --resources mem_mb=16000' | bash -x -e`

The results are placed in subdirectories as listed in the following table.

| Result                                                    | Directory                                                       |
| --------------------------------------------------------- | --------------------------------------------------------------- |
| Edit distances from the truth                             | edlib-scores                                                    |
| Variants called with the PanVC workflow using GATK        | call/*experiment-identifier*/ext\_vc/pg\_variants.gatk.vcf      |
| Variants called with the PanVC workflow using Samtools    | call/*experiment-identifier*/ext\_vc/pg\_variants.samtools.vcf  |
| Variants called with the baseline workflow using GATK     | call/*experiment-identifier*/baseline\_vc/variants.gatk.vcf     |
| Variants called with the baseline workflow using Samtools | call/*experiment-identifier*/baseline\_vc/variants.samtools.vcf |

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

### Take-one-out experiment with human chromosome 22

#### Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archives themselves have not been re-compressed.)

| File | Coverage |
| ---- | -------- |
| [cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov10.tar) | 10x |
| [cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov20.tar) | 20x |
| [cov50.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov50.tar) | 50x |

#### Indices for use with `Snakefile.call`

The following archives contain indices generated with `Snakefile.index`.

| Index file |
| ---------- |
| [no-HG00513.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-HG00513.tar.bz2) |
| [no-HG00731.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-HG00731.tar.bz2) |
| [no-NA12273.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-NA12273.tar.bz2) |
| [no-NA18954.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-NA18954.tar.bz2) |
| [no-NA19238.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-NA19238.tar.bz2) |

#### Founder sequences used when generating the indices

| Sequence file |
| ------------- |
| [no-HG00513.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-HG00513.tar.bz2) |
| [no-HG00731.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-HG00731.tar.bz2) |
| [no-NA12273.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-NA12273.tar.bz2) |
| [no-NA18954.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-NA18954.tar.bz2) |
| [no-NA19238.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-NA19238.tar.bz2) |

---

### Scalability experiment

#### Indices for use with `Snakefile.call`

Archives that contain the pregenerated indices have been listed [on a separate page](scalability-experiment/scalability-indices.md).

#### Founder sequences used when generating the indices

Individual sequence files have been listed [on a separate page](scalability-experiment/scalability-index-inputs.md).
