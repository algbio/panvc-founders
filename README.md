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

1. Download the [index files](#indices-for-use-with-panvc_call_variants-1). For downloading all (or some) of the files, download [all-index-files.txt](experiments-with-artificial-mutations/all-index-files.txt), modify the file if need be, and do `wget --content-disposition --trust-server-names -i all-index-files.txt`.
   * The indices may also be generated with `Snakefile.index`. The input files are listed under [Founder sequences used when generating the indices](#founder-sequences-used-when-generating-the-indices). Please see [experiments-with-artificial-mutations](experiments-with-artificial-mutations) for scripts for processing the files in [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2).
2. Extract the contents of the archives. Each of the indices will be placed in a subdirectory called `indices`.
3. Download [genreads.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads.tar) for the reads used in the experiment and extract.
4. Download [call_cmds.py](experiments-with-artificial-mutations/call_cmds.py). Modify the first lines to set the path to `PanVC` and the amount of memory and number of threads used.
6. Download [edlib-cmds.sh](experiments-with-artificial-mutations/edlib-cmds.sh). Modify the first lines to set the path to `Edlib`.
5. Run `call_cmds.py` with Python (e.g. `python3.7 call_cmds.py`) to get a list of commands to run.
6. XXX generate predicted sequences
7. After running PanVC, run `edlib-cmds.sh` to get a list of commands to run.

#### Reads used in the experiment

The following archive contains the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archive itself has not been re-compressed.)

| Reads |
| ----- |
| [genreads.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads.tar) |

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

The following archives contain indices generated with `Snakefile.index`.

| Indices with all samples except the tested one | Generation | Mutation probability | Minimum subgraph distance |
| ---------------------------------------------- | ---------- | -------------------- | ------------------------- |
| [e-coli-g5-p0.001-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.001-msd25-precalc.tar.bz2)     | 5  | 0.001 | 25  |
| [e-coli-g5-p0.001-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.001-msd50-precalc.tar.bz2)     | 5  | 0.001 | 50  |
| [e-coli-g5-p0.001-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.001-msd100-precalc.tar.bz2)   | 5  | 0.001 | 100 |
| [e-coli-g5-p0.002-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.002-msd25-precalc.tar.bz2)     | 5  | 0.002 | 25  |
| [e-coli-g5-p0.002-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.002-msd50-precalc.tar.bz2)     | 5  | 0.002 | 50  |
| [e-coli-g5-p0.002-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.002-msd100-precalc.tar.bz2)   | 5  | 0.002 | 100 |
| [e-coli-g5-p0.004-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.004-msd25-precalc.tar.bz2)     | 5  | 0.004 | 25  |
| [e-coli-g5-p0.004-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.004-msd50-precalc.tar.bz2)     | 5  | 0.004 | 50  |
| [e-coli-g5-p0.004-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.004-msd100-precalc.tar.bz2)   | 5  | 0.004 | 100 |
| [e-coli-g5-p0.008-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.008-msd25-precalc.tar.bz2)     | 5  | 0.008 | 25  |
| [e-coli-g5-p0.008-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.008-msd50-precalc.tar.bz2)     | 5  | 0.008 | 50  |
| [e-coli-g5-p0.008-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.008-msd100-precalc.tar.bz2)   | 5  | 0.008 | 100 |
| [e-coli-g5-p0.016-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.016-msd25-precalc.tar.bz2)     | 5  | 0.016 | 25  |
| [e-coli-g5-p0.016-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.016-msd50-precalc.tar.bz2)     | 5  | 0.016 | 50  |
| [e-coli-g5-p0.016-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.016-msd100-precalc.tar.bz2)   | 5  | 0.016 | 100 |
| [e-coli-g7-p0.001-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.001-msd25-precalc.tar.bz2)     | 7  | 0.001 | 25  |
| [e-coli-g7-p0.001-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.001-msd50-precalc.tar.bz2)     | 7  | 0.001 | 50  |
| [e-coli-g7-p0.001-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.001-msd100-precalc.tar.bz2)   | 7  | 0.001 | 100 |
| [e-coli-g7-p0.002-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.002-msd25-precalc.tar.bz2)     | 7  | 0.002 | 25  |
| [e-coli-g7-p0.002-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.002-msd50-precalc.tar.bz2)     | 7  | 0.002 | 50  |
| [e-coli-g7-p0.002-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.002-msd100-precalc.tar.bz2)   | 7  | 0.002 | 100 |
| [e-coli-g7-p0.004-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.004-msd25-precalc.tar.bz2)     | 7  | 0.004 | 25  |
| [e-coli-g7-p0.004-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.004-msd50-precalc.tar.bz2)     | 7  | 0.004 | 50  |
| [e-coli-g7-p0.004-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.004-msd100-precalc.tar.bz2)   | 7  | 0.004 | 100 |
| [e-coli-g7-p0.008-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.008-msd25-precalc.tar.bz2)     | 7  | 0.008 | 25  |
| [e-coli-g7-p0.008-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.008-msd50-precalc.tar.bz2)     | 7  | 0.008 | 50  |
| [e-coli-g7-p0.008-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.008-msd100-precalc.tar.bz2)   | 7  | 0.008 | 100 |
| [e-coli-g7-p0.016-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.016-msd25-precalc.tar.bz2)     | 7  | 0.016 | 25  |
| [e-coli-g7-p0.016-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.016-msd50-precalc.tar.bz2)     | 7  | 0.016 | 50  |
| [e-coli-g7-p0.016-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.016-msd100-precalc.tar.bz2)   | 7  | 0.016 | 100 |
| [e-coli-g10-p0.001-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.001-msd25-precalc.tar.bz2)   | 10 | 0.001 | 25  |
| [e-coli-g10-p0.001-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.001-msd50-precalc.tar.bz2)   | 10 | 0.001 | 50  |
| [e-coli-g10-p0.001-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.001-msd100-precalc.tar.bz2) | 10 | 0.001 | 100 |
| [e-coli-g10-p0.002-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.002-msd25-precalc.tar.bz2)   | 10 | 0.002 | 25  |
| [e-coli-g10-p0.002-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.002-msd50-precalc.tar.bz2)   | 10 | 0.002 | 50  |
| [e-coli-g10-p0.002-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.002-msd100-precalc.tar.bz2) | 10 | 0.002 | 100 |
| [e-coli-g10-p0.004-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.004-msd25-precalc.tar.bz2)   | 10 | 0.004 | 25  |
| [e-coli-g10-p0.004-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.004-msd50-precalc.tar.bz2)   | 10 | 0.004 | 50  |
| [e-coli-g10-p0.004-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.004-msd100-precalc.tar.bz2) | 10 | 0.004 | 100 |
| [e-coli-g10-p0.008-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.008-msd25-precalc.tar.bz2)   | 10 | 0.008 | 25  |
| [e-coli-g10-p0.008-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.008-msd50-precalc.tar.bz2)   | 10 | 0.008 | 50  |
| [e-coli-g10-p0.008-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.008-msd100-precalc.tar.bz2) | 10 | 0.008 | 100 |
| [e-coli-g10-p0.016-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.016-msd25-precalc.tar.bz2)   | 10 | 0.016 | 25  |
| [e-coli-g10-p0.016-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.016-msd50-precalc.tar.bz2)   | 10 | 0.016 | 50  |
| [e-coli-g10-p0.016-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.016-msd100-precalc.tar.bz2) | 10 | 0.016 | 100 |

| Indices with nearest samples removed | Minimum subgraph distance |
| ------------------------------------ | ------------------------- |
| [e-coli-g5-m0.016-s0-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s0-msd25-precalc.tar.bz2)   | 25  |
| [e-coli-g5-m0.016-s0-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s0-msd50-precalc.tar.bz2)   | 50  |
| [e-coli-g5-m0.016-s0-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s0-msd100-precalc.tar.bz2) | 100 |
| [e-coli-g5-m0.016-s1-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s1-msd25-precalc.tar.bz2)   | 25  |
| [e-coli-g5-m0.016-s1-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s1-msd50-precalc.tar.bz2)   | 50  |
| [e-coli-g5-m0.016-s1-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s1-msd100-precalc.tar.bz2) | 100 |
| [e-coli-g5-m0.016-s2-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s2-msd25-precalc.tar.bz2)   | 25  |
| [e-coli-g5-m0.016-s2-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s2-msd50-precalc.tar.bz2)   | 50  |
| [e-coli-g5-m0.016-s2-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s2-msd100-precalc.tar.bz2) | 100 |
| [e-coli-g5-m0.016-s3-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s3-msd25-precalc.tar.bz2)   | 25  |
| [e-coli-g5-m0.016-s3-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s3-msd50-precalc.tar.bz2)   | 50  |
| [e-coli-g5-m0.016-s3-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s3-msd100-precalc.tar.bz2) | 100 |
| [e-coli-g5-m0.016-s4-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s4-msd25-precalc.tar.bz2)   | 25  |
| [e-coli-g5-m0.016-s4-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s4-msd50-precalc.tar.bz2)   | 50  |
| [e-coli-g5-m0.016-s4-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s4-msd100-precalc.tar.bz2) | 100 |
| [e-coli-g5-m0.016-s5-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s5-msd25-precalc.tar.bz2)   | 25  |
| [e-coli-g5-m0.016-s5-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s5-msd50-precalc.tar.bz2)   | 50  |
| [e-coli-g5-m0.016-s5-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s5-msd100-precalc.tar.bz2) | 100 |
| [e-coli-g5-m0.016-s6-msd25-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s6-msd25-precalc.tar.bz2)   | 25  |
| [e-coli-g5-m0.016-s6-msd50-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s6-msd50-precalc.tar.bz2)   | 50  |
| [e-coli-g5-m0.016-s6-msd100-precalc.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s6-msd100-precalc.tar.bz2) | 100 |


#### Founder sequences used when generating the indices

| All sequences in one archive |
| ---------------------------- |
| [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2) |

| Individual input files | Generation | Mutation probability | Minimum subgraph distance |
| ---------------------- | ---------- | -------------------- | ------------------------- |
| [e-coli-g5-p0.001-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.001-msd25-precalc.a2m.bz2)     | 5  | 0.001 | 25  |
| [e-coli-g5-p0.001-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.001-msd50-precalc.a2m.bz2)     | 5  | 0.001 | 50  |
| [e-coli-g5-p0.001-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.001-msd100-precalc.a2m.bz2)   | 5  | 0.001 | 100 |
| [e-coli-g5-p0.002-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.002-msd25-precalc.a2m.bz2)     | 5  | 0.002 | 25  |
| [e-coli-g5-p0.002-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.002-msd50-precalc.a2m.bz2)     | 5  | 0.002 | 50  |
| [e-coli-g5-p0.002-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.002-msd100-precalc.a2m.bz2)   | 5  | 0.002 | 100 |
| [e-coli-g5-p0.004-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.004-msd25-precalc.a2m.bz2)     | 5  | 0.004 | 25  |
| [e-coli-g5-p0.004-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.004-msd50-precalc.a2m.bz2)     | 5  | 0.004 | 50  |
| [e-coli-g5-p0.004-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.004-msd100-precalc.a2m.bz2)   | 5  | 0.004 | 100 |
| [e-coli-g5-p0.008-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.008-msd25-precalc.a2m.bz2)     | 5  | 0.008 | 25  |
| [e-coli-g5-p0.008-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.008-msd50-precalc.a2m.bz2)     | 5  | 0.008 | 50  |
| [e-coli-g5-p0.008-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.008-msd100-precalc.a2m.bz2)   | 5  | 0.008 | 100 |
| [e-coli-g5-p0.016-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.016-msd25-precalc.a2m.bz2)     | 5  | 0.016 | 25  |
| [e-coli-g5-p0.016-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.016-msd50-precalc.a2m.bz2)     | 5  | 0.016 | 50  |
| [e-coli-g5-p0.016-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.016-msd100-precalc.a2m.bz2)   | 5  | 0.016 | 100 |
| [e-coli-g7-p0.001-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.001-msd25-precalc.a2m.bz2)     | 7  | 0.001 | 25  |
| [e-coli-g7-p0.001-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.001-msd50-precalc.a2m.bz2)     | 7  | 0.001 | 50  |
| [e-coli-g7-p0.001-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.001-msd100-precalc.a2m.bz2)   | 7  | 0.001 | 100 |
| [e-coli-g7-p0.002-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.002-msd25-precalc.a2m.bz2)     | 7  | 0.002 | 25  |
| [e-coli-g7-p0.002-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.002-msd50-precalc.a2m.bz2)     | 7  | 0.002 | 50  |
| [e-coli-g7-p0.002-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.002-msd100-precalc.a2m.bz2)   | 7  | 0.002 | 100 |
| [e-coli-g7-p0.004-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.004-msd25-precalc.a2m.bz2)     | 7  | 0.004 | 25  |
| [e-coli-g7-p0.004-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.004-msd50-precalc.a2m.bz2)     | 7  | 0.004 | 50  |
| [e-coli-g7-p0.004-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.004-msd100-precalc.a2m.bz2)   | 7  | 0.004 | 100 |
| [e-coli-g7-p0.008-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.008-msd25-precalc.a2m.bz2)     | 7  | 0.008 | 25  |
| [e-coli-g7-p0.008-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.008-msd50-precalc.a2m.bz2)     | 7  | 0.008 | 50  |
| [e-coli-g7-p0.008-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.008-msd100-precalc.a2m.bz2)   | 7  | 0.008 | 100 |
| [e-coli-g7-p0.016-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.016-msd25-precalc.a2m.bz2)     | 7  | 0.016 | 25  |
| [e-coli-g7-p0.016-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.016-msd50-precalc.a2m.bz2)     | 7  | 0.016 | 50  |
| [e-coli-g7-p0.016-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.016-msd100-precalc.a2m.bz2)   | 7  | 0.016 | 100 |
| [e-coli-g10-p0.001-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.001-msd25-precalc.a2m.bz2)   | 10 | 0.001 | 25  |
| [e-coli-g10-p0.001-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.001-msd50-precalc.a2m.bz2)   | 10 | 0.001 | 50  |
| [e-coli-g10-p0.001-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.001-msd100-precalc.a2m.bz2) | 10 | 0.001 | 100 |
| [e-coli-g10-p0.002-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.002-msd25-precalc.a2m.bz2)   | 10 | 0.002 | 25  |
| [e-coli-g10-p0.002-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.002-msd50-precalc.a2m.bz2)   | 10 | 0.002 | 50  |
| [e-coli-g10-p0.002-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.002-msd100-precalc.a2m.bz2) | 10 | 0.002 | 100 |
| [e-coli-g10-p0.004-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.004-msd25-precalc.a2m.bz2)   | 10 | 0.004 | 25  |
| [e-coli-g10-p0.004-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.004-msd50-precalc.a2m.bz2)   | 10 | 0.004 | 50  |
| [e-coli-g10-p0.004-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.004-msd100-precalc.a2m.bz2) | 10 | 0.004 | 100 |
| [e-coli-g10-p0.008-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.008-msd25-precalc.a2m.bz2)   | 10 | 0.008 | 25  |
| [e-coli-g10-p0.008-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.008-msd50-precalc.a2m.bz2)   | 10 | 0.008 | 50  |
| [e-coli-g10-p0.008-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.008-msd100-precalc.a2m.bz2) | 10 | 0.008 | 100 |
| [e-coli-g10-p0.016-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.016-msd25-precalc.a2m.bz2)   | 10 | 0.016 | 25  |
| [e-coli-g10-p0.016-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.016-msd50-precalc.a2m.bz2)   | 10 | 0.016 | 50  |
| [e-coli-g10-p0.016-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.016-msd100-precalc.a2m.bz2) | 10 | 0.016 | 100 |

| Individual input files, nearest samples removed | Minimum subgraph distance |
| ----------------------------------------------- | ------------------------- |
| [e-coli-g5-m0.016-s0-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s0-msd25-precalc.a2m.bz2)   | 25  |
| [e-coli-g5-m0.016-s0-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s0-msd50-precalc.a2m.bz2)   | 50  |
| [e-coli-g5-m0.016-s0-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s0-msd100-precalc.a2m.bz2) | 100 |
| [e-coli-g5-m0.016-s1-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s1-msd25-precalc.a2m.bz2)   | 25  |
| [e-coli-g5-m0.016-s1-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s1-msd50-precalc.a2m.bz2)   | 50  |
| [e-coli-g5-m0.016-s1-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s1-msd100-precalc.a2m.bz2) | 100 |
| [e-coli-g5-m0.016-s2-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s2-msd25-precalc.a2m.bz2)   | 25  |
| [e-coli-g5-m0.016-s2-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s2-msd50-precalc.a2m.bz2)   | 50  |
| [e-coli-g5-m0.016-s2-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s2-msd100-precalc.a2m.bz2) | 100 |
| [e-coli-g5-m0.016-s3-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s3-msd25-precalc.a2m.bz2)   | 25  |
| [e-coli-g5-m0.016-s3-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s3-msd50-precalc.a2m.bz2)   | 50  |
| [e-coli-g5-m0.016-s3-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s3-msd100-precalc.a2m.bz2) | 100 |
| [e-coli-g5-m0.016-s4-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s4-msd25-precalc.a2m.bz2)   | 25  |
| [e-coli-g5-m0.016-s4-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s4-msd50-precalc.a2m.bz2)   | 50  |
| [e-coli-g5-m0.016-s4-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s4-msd100-precalc.a2m.bz2) | 100 |
| [e-coli-g5-m0.016-s5-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s5-msd25-precalc.a2m.bz2)   | 25  |
| [e-coli-g5-m0.016-s5-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s5-msd50-precalc.a2m.bz2)   | 50  |
| [e-coli-g5-m0.016-s5-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s5-msd100-precalc.a2m.bz2) | 100 |
| [e-coli-g5-m0.016-s6-msd25-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s6-msd25-precalc.a2m.bz2)   | 25  |
| [e-coli-g5-m0.016-s6-msd50-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s6-msd50-precalc.a2m.bz2)   | 50  |
| [e-coli-g5-m0.016-s6-msd100-precalc.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s6-msd100-precalc.a2m.bz2) | 100 |

---

### Take-one-out experiment with human chromosome 22

#### Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archives themselves have not been re-compressed.)

| File | Coverage |
| ---- | -------- |
| [cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov10.tar) | 10x |
| [cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov20.tar) | 20x |
| [cov50.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov50.tar) | 50x |

#### Indices for use with `panvc_call_variants`

The following archives contain indices generated with `panvc_index`.

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

#### Indices for use with `panvc_call_variants`

The following archives contain indices generated with `panvc_index`.

| Index file |
| ---------- |
| [chr1-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr1-index.tar.bz2) |
| [chr2-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr2-index.tar.bz2) |
| [chr3-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr3-index.tar.bz2) |
| [chr4-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr4-index.tar.bz2) |
| [chr5-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr5-index.tar.bz2) |
| [chr6-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr6-index.tar.bz2) |
| [chr7-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr7-index.tar.bz2) |
| [chr8-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr8-index.tar.bz2) |
| [chr9-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr9-index.tar.bz2) |
| [chr10-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr10-index.tar.bz2) |
| [chr11-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr11-index.tar.bz2) |
| [chr12-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr12-index.tar.bz2) |
| [chr13-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr13-index.tar.bz2) |
| [chr14-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr14-index.tar.bz2) |
| [chr15-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr15-index.tar.bz2) |
| [chr16-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr16-index.tar.bz2) |
| [chr17-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr17-index.tar.bz2) |
| [chr18-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr18-index.tar.bz2) |
| [chr19-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr19-index.tar.bz2) |
| [chr20-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr20-index.tar.bz2) |
| [chr21-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr21-index.tar.bz2) |
| [chr22-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chr22-index.tar.bz2) |
| [chrX-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/indices/chrX-index.tar.bz2) |

#### Founder sequences used when generating the indices

| Sequence file |
| ------------- |
| [chr1.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr1.a2m.bz2) |
| [chr2.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr2.a2m.bz2) |
| [chr3.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr3.a2m.bz2) |
| [chr4.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr4.a2m.bz2) |
| [chr5.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr5.a2m.bz2) |
| [chr6.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr6.a2m.bz2) |
| [chr7.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr7.a2m.bz2) |
| [chr8.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr8.a2m.bz2) |
| [chr9.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr9.a2m.bz2) |
| [chr10.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr10.a2m.bz2) |
| [chr11.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr11.a2m.bz2) |
| [chr12.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr12.a2m.bz2) |
| [chr13.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr13.a2m.bz2) |
| [chr14.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr14.a2m.bz2) |
| [chr15.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr15.a2m.bz2) |
| [chr16.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr16.a2m.bz2) |
| [chr17.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr17.a2m.bz2) |
| [chr18.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr18.a2m.bz2) |
| [chr19.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr19.a2m.bz2) |
| [chr20.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr20.a2m.bz2) |
| [chr21.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr21.a2m.bz2) |
| [chr22.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chr22.a2m.bz2) |
| [chrX.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/scalability-experiment/index-input/chrX.a2m.bz2) |
