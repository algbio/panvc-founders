# PanVC Experiments with Founder Sequences

PanVC is a variant calling workflow that uses short reads as its input. The reads are aligned to an index generated from a multiple sequence alignment. The newest version of the workflow utilises founder sequences for indexing.

We provide the following data files for testing PanVC.

To build PanVC, please follow the instructions on the [repository page of PanVC](https://gitlab.com/dvalenzu/PanVC/-/tree/PanVC-2.0-rc-tsnorri).

To run any of the experiments, please download and unarchive the reads in question and do one of the following:

* Download and unarchive the pre-generated indices and run `panvc_call_variants` with the reads and each of the indices.
* Download and decompress the founder sequences, prepare input for `panvc_index`, generate the index and run `panvc_call_variants` with the reads and each of the indices.

Each experiment involves aligning different sets of reads to different indices. In the subdirectories of this repository, we have provided some scripts that may be helpful in automatizing the tasks.

The [artificial mutation experiment](#experiments-with-artificial-mutations) should be the fastest one to run.

### Generating indices with PanVC

We provide pregenerated indices for each experiment. In case you would like to prepare the index yourself, please follow these steps. The subdirectories in this repository also contain sample scripts for generating the indices. In general, PanVC’s indexing input consists of a directory with two files: `chr_list.txt` and `pangenome1.a2m`. The index consists of various files that `panvc_index` places in a given directory.

1. Download the compressed founder sequences for the experiment in question. One sequence file corresponds to one index.
2. Decompress the file with e.g. `pbzip2` or `bzip2`.
3. Create a directory for the index in question.
4. Move the decompressed A2M file to the new directory and rename it `pangenome1.a2m`.
5. Create a text file called `chr_list.txt` alongside the A2M file. The contents of the file should be the number `1` followed by a newline.
6. Run `panvc_index`. Please see [PanVC’s README](https://gitlab.com/dvalenzu/PanVC/-/blob/PanVC-2.0-rc-tsnorri/README.md) for details. The read length parameter should be set to a value greater than the read length used in the experiment in question. For the maximum edit distance, we used the value 10.

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

#### Indices for use with `panvc_call_variants`

The following archives contain indices generated with `panvc_index`.

| Index | Index file |
| ----- | ---------- |
| Index generated with founder sequences | [founder-sequence-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/indices/founder-sequence-index.tar.bz2) |
| Index generated with all predicted sequences | [predicted-sequence-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/founder-quality-experiment/indices/predicted-sequence-index.tar.bz2) |

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
   * The indices may also be generated with `panvc_index`. The input files are listed under [Founder sequences used when generating the indices](#founder-sequences-used-when-generating-the-indices). Please see [experiments-with-artificial-mutations](experiments-with-artificial-mutations) for scripts for processing the files in [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2).
2. Move the archives to a directory called `indices` and extract the files.
3. Download [genreads.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads.tar) for the reads used in the experiment and extract.
4. In the working directory, create the subdirectories `panvc` (for PanVC’s output), `logs` and `edlib-scores`. The working directory should now have the following subdirectories:
   * `indices`
   * `genreads`
   * `panvc`
   * `logs`
   * `edlib-scores`
5. Download [call_cmds.py](experiments-with-artificial-mutations/call_cmds.py). Modify the first lines to set the path to `PanVC` and the amount of memory and number of threads used.
6. Download [edlib-cmds.sh](experiments-with-artificial-mutations/edlib-cmds.sh). Modify the first lines to set the path to `Edlib`.
7. Run `call_cmds.py` with Python (e.g. `python3.7 call_cmds.py`) to get a list of commands to run.
8. XXX generate predicted sequences
9. After running PanVC, run `edlib-cmds.sh` to get a list of commands to run.

#### Reads used in the experiment

The following archive contains the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archive itself has not been re-compressed.)

| Reads |
| ----- |
| [genreads.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads.tar) |

#### Variants

The following archives contain the actual (not predicted) variants in the generated samples. The identifier of the removed samples is `SAMPLE0`.

| Description | File |
| ----------- | ---- |
| Samples removed in the experiments | [variants-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/variants-truth.tar.gz) |
| All samples | [variants-all.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/variants-all.tar.gz) |

#### Sequences of the removed samples

The following archives contain the actual sequences of the samples that were removed in the experiments.

| Sequences |
| --------- |
| [sequences-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/sequences-truth.tar.gz) |

#### Indices for use with `panvc_call_variants`

The following archives contain indices generated with `panvc_index`.

| Indices with all samples except the tested one |
| ---------------------------------------------- |
| [e-coli-g5-p0.001-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.001-index.tar.bz2) |
| [e-coli-g5-p0.002-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.002-index.tar.bz2) |
| [e-coli-g5-p0.004-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.004-index.tar.bz2) |
| [e-coli-g5-p0.008-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.008-index.tar.bz2) |
| [e-coli-g5-p0.016-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-p0.016-index.tar.bz2) |
| [e-coli-g7-p0.001-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.001-index.tar.bz2) |
| [e-coli-g7-p0.002-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.002-index.tar.bz2) |
| [e-coli-g7-p0.004-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.004-index.tar.bz2) |
| [e-coli-g7-p0.008-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.008-index.tar.bz2) |
| [e-coli-g7-p0.016-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g7-p0.016-index.tar.bz2) |
| [e-coli-g10-p0.001-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.001-index.tar.bz2) |
| [e-coli-g10-p0.002-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.002-index.tar.bz2) |
| [e-coli-g10-p0.004-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.004-index.tar.bz2) |
| [e-coli-g10-p0.008-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.008-index.tar.bz2) |
| [e-coli-g10-p0.016-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g10-p0.016-index.tar.bz2) |

| Indices with nearest samples removed |
| ------------------------------------ |
| [e-coli-g5-m0.016-s0-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s0-index.tar.bz2) |
| [e-coli-g5-m0.016-s1-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s1-index.tar.bz2) |
| [e-coli-g5-m0.016-s2-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s2-index.tar.bz2) |
| [e-coli-g5-m0.016-s3-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s3-index.tar.bz2) |
| [e-coli-g5-m0.016-s4-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s4-index.tar.bz2) |
| [e-coli-g5-m0.016-s5-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s5-index.tar.bz2) |
| [e-coli-g5-m0.016-s6-index.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/e-coli-g5-m0.016-s6-index.tar.bz2) |


#### Founder sequences used when generating the indices

| All sequences in one archive |
| ---------------------------- |
| [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2) |

| Individual input files |
| ---------------------- |
| [e-coli-g5-p0.001.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.001.a2m.bz2) |
| [e-coli-g5-p0.002.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.002.a2m.bz2) |
| [e-coli-g5-p0.004.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.004.a2m.bz2) |
| [e-coli-g5-p0.008.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.008.a2m.bz2) |
| [e-coli-g5-p0.016.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-p0.016.a2m.bz2) |
| [e-coli-g7-p0.001.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.001.a2m.bz2) |
| [e-coli-g7-p0.002.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.002.a2m.bz2) |
| [e-coli-g7-p0.004.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.004.a2m.bz2) |
| [e-coli-g7-p0.008.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.008.a2m.bz2) |
| [e-coli-g7-p0.016.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g7-p0.016.a2m.bz2) |
| [e-coli-g10-p0.001.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.001.a2m.bz2) |
| [e-coli-g10-p0.002.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.002.a2m.bz2) |
| [e-coli-g10-p0.004.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.004.a2m.bz2) |
| [e-coli-g10-p0.008.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.008.a2m.bz2) |
| [e-coli-g10-p0.016.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g10-p0.016.a2m.bz2) |

| Individual input files, nearest samples removed |
| ----------------------------------------------- |
| [e-coli-g5-m0.016-s0.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s0.a2m.bz2) |
| [e-coli-g5-m0.016-s1.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s1.a2m.bz2) |
| [e-coli-g5-m0.016-s2.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s2.a2m.bz2) |
| [e-coli-g5-m0.016-s3.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s3.a2m.bz2) |
| [e-coli-g5-m0.016-s4.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s4.a2m.bz2) |
| [e-coli-g5-m0.016-s5.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s5.a2m.bz2) |
| [e-coli-g5-m0.016-s6.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/e-coli-g5-m0.016-s6.a2m.bz2) |

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
