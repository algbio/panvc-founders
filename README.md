# PanVC Experiments with Founder Sequences

We provide the following data files for testing PanVC.

To build PanVC, please follow the instructions on the [repository page of PanVC](https://gitlab.com/dvalenzu/PanVC/-/tree/PanVC-2.0-rc-tsnorri).

To run any of the experiments, please download and unarchive the reads in question and do one of the following:

* Download and unarchive the pre-generated indices and run `panvc_call_variants` with the reads and each of the indices.
* Download and decompress the founder sequences, prepare input for `panvc_index`, generate the index and run `panvc_call_variants` with the reads and each of the indices.

### Generating indices with PanVC

We provide pregenerated indices for each experiment. In case you would like to prepare the index yourself, please follow these steps. The subdirectories in this repository also contain sample scripts for generating the indices. In general, PanVC’s indexing input consists of a directory with two files: `chr_list.txt` and `pangenome1.a2m`. The index consists of various files that `panvc_index` places in a given directory.

1. Download the compressed founder sequences for the experiment in question. One sequence file corresponds to one index.
2. Decompress the file with e.g. `pbzip2` or `bzip2`.
3. Create a directory for the index in question.
4. Move the decompressed A2M file to the new directory and rename it `pangenome1.a2m`.
5. Create a text file called `chr_list.txt` alongside the A2M file. The contents of the file should be the number `1` followed by a newline.
6. Run `panvc_index`. Please see [PanVC’s README](https://gitlab.com/dvalenzu/PanVC/-/blob/PanVC-2.0-rc-tsnorri/README.md) for details. The read length parameter should be set to a value greater than the read length used in the experiment in question. For the maximum edit distance, we used the value 10.

## Experiment data

### Experiments with artificial mutations

See [experiments-with-artificial-mutations](experiments-with-artificial-mutations) for sample scripts.

#### Reads used in the experiment

The following archive contains the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archive itself has not been re-compressed.)

| Reads |
| ----- |
| [genreads.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/genreads.tar) |

#### Founder sequences used when generating the indices

| Sequence archive |
| ---------------- |
| [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2) |

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
