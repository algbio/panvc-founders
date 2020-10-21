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

## Installing

All necessary components for variant calling from our provided inputs are installed as part of [PanVC sample workflow](https://github.com/algbio/panvc-sample-workflow). Please follow its installation instructions. Given short reads as input, the workflow outputs a set of called variants.

Tools for generating a predicted sequence from variants are provided with [vcf2multialign](https://github.com/tsnorri/vcf2multialign). For determining the edit distances of the predicted sequences to the hidden truth sequences, we recommend [edlib](https://github.com/Martinsos/edlib).

To generate founder sequences from known variants, [vcf2multialign](https://github.com/tsnorri/vcf2multialign) can be used.

## Running the experiments

On a high level, running any of the experiments consists of the following steps:

 1. Download and unarchive the reads provided with the experiment
 2. Do one of the following:
    * Download and unarchive the pre-generated indices provided with the experiment in question and call variants by running Snakemake with `Snakefile.call`
    * Download and decompress the founder sequences provided with the experiment in question, generate the index by running Snakemake with `Snakefile.index` and call variants by running Snakemake with `Snakefile.call` with the reads and each of the indices.

Each experiment involves aligning different sets of reads to different indices. In the subdirectories of this repository, we have provided some scripts that may be helpful in automatizing the tasks.

The [artificial mutation experiment](#experiments-with-artificial-mutations) should be the fastest one to run with one input.

### Generating indices with PanVC

We provide pregenerated indices for each experiment. In case you would like to prepare the index yourself, please follow these steps. The subdirectories in this repository also contain sample scripts for generating the indices.

 1. Download the compressed founder sequences for the experiment in question. In all our experiments, one sequence file corresponds to one index.
 2. Decompress the file with e.g. `pbzip2` or `bzip2`.
 3. Run `python3 generate_snakemake_config_for_index.py`
 4. Run Snakemake with `Snakefile.index`.

Please see [README from the sample workflow](https://github.com/algbio/panvc-sample-workflow/blob/master/README.md#preparing-an-index) for more detailed instructions. The read length parameter should be set to a value greater than the read length used in the experiment in question (e.g. 105). For the maximum edit distance, we used the value 10.

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

1. Download the [index files](#indices-for-use-with-snakefilecall-1). For downloading all (or some) of the files, download [all-index-files.txt](experiments-with-artificial-mutations/all-index-files.txt), modify the file if need be, and do `wget --content-disposition --trust-server-names -i all-index-files.txt`.
   * The indices may also be generated with `Snakefile.index`. The input files are listed under [Founder sequences used when generating the indices](#founder-sequences-used-when-generating-the-indices). Please see [experiments-with-artificial-mutations](experiments-with-artificial-mutations) for scripts for processing the files in [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2).
2. Extract the contents of the archives. Each of the indices will be placed in a subdirectory called `indices`.
3. Download (some of) [the reads used in the experiment](#reads-used-in-the-experiment-1) and extract. In addition to the separate reads, the workflow requires the same reads unpaired and renamed in one input. This is done automatically as part of the workflow but we have also prepared the files in question.
4. Download [output_config_and_call_commands.py](experiments-with-artificial-mutations/output_config_and_call_commands.py). Modify the first lines to set the path to PanVC sample workflow as well as other parameters.
5. Download [gen-predicted-sequences-cmds.sh](experiments-with-artificial-mutations/gen-predicted-sequences-cmds.sh). Modify the first lines to set the path to vcf2multialign as well as other parameters.
6. Download [edlib-cmds.sh](experiments-with-artificial-mutations/edlib-cmds.sh). Modify the first lines to set the path to `Edlib`.
7. Download e-coli.fa.gz. Some of our tools expect the input FASTA not to contain any newlines as part of the sequence; the file in question has been modified accordingly.
8. Run output_config_and_call_commands.py with Python (e.g. `python3 output_config_and_call_commands.py`) to output the configuration files and to get a list of commands for running the variant calling workflow. Run (some of) the commands.
9. Run `gen-predicted-sequences-cmds.sh` to get a list of commands to generate predicted sequences from the variant calling results. Run (some of) the commands.
10. Run `edlib-cmds.sh` to get a list of commands to calculate edit distances of the predicted sequences to the hidden truth.

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
