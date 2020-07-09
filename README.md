# PanVC Experiments with Founder Sequences

We provide the following data files for use with PanVC.

To build PanVC, please follow the instructions on the [repository page of PanVC](https://gitlab.com/dvalenzu/PanVC/-/tree/PanVC-2.0-rc-tsnorri).

### Generating indices with PanVC

We provide pregenerated indices for each experiment. In case you would like to prepare the index yourself, please follow these instructions.

1. Download the compressed founder sequences for the experiment in question. One sequence file corresponds to one index.
2. Decompress the file with e.g. `pbzip2` or `bzip2`.
3. Create a directory for the index in question.
4. Move the decompressed A2M file to the new directory and rename it `pangenome1.a2m`.
5. Create a text file called `chr_list.txt` alongside the A2M file. The contents of the file should be the number `1` followed by a newline.
6. Run `panvc_index`. Please see [PanVC’s README](https://gitlab.com/dvalenzu/PanVC/-/blob/PanVC-2.0-rc-tsnorri/README.md) for details. The read length parameter should be set to a value greater than the read length used in the experiment in question. For the maximum edit distance, we used the value 10.

## Take-one-out experiment with human chromosome 22

To do the experiment, please download the reads listed below and do one of the following:

* Download pre-generated indices (below) and run `panvc_call_variants`
* Download the founder sequences (below), prepare input for `panvc_index`, generate the index and run `panvc_call_variants`.

### Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archives themselves have not been re-compressed.)

| File | Coverage |
| ---- | -------- |
| [cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov10.tar) | 10x |
| [cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov20.tar) | 20x |
| [cov50.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/reads/cov50.tar) | 50x |

### Indices for use with `panvc_call_variants`

The following archives contain indices generated with `panvc_index`.

| Index file |
| ---------- |
| [no-HG00513.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-HG00513.tar.bz2) |
| [no-HG00731.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-HG00731.tar.bz2) |
| [no-NA12273.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-NA12273.tar.bz2) |
| [no-NA18954.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-NA18954.tar.bz2) |
| [no-NA19238.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/panvc-indices/no-NA19238.tar.bz2) |

### Founder sequences used when generating the indices

| Sequence file |
| ------------- |
| [no-HG00513.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-HG00513.tar.bz2) |
| [no-HG00731.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-HG00731.tar.bz2) |
| [no-NA12273.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-NA12273.tar.bz2) |
| [no-NA18954.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-NA18954.tar.bz2) |
| [no-NA19238.a2m.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/take-one-out-experiment-with-human-chr22/founder-sequences/no-NA19238.tar.bz2) |
