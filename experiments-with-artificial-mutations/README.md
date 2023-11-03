# Experiments with Artificial Mutations

This directory contains the scripts needed to run the experiments with artificial mutations.

## Running the experiment

The experiment consists of running the workflow with 192 different inputs. For testing purposes, a subset of the inputs may be used. To run the experiment, please follow these steps.

To simplify running the experiment, the repository contains a helper script, [experiment\_helper.py](experiment_helper.py). All its available options may be listed with `python3 experiment_helper.py --help`.

 1. `cd experiments-with-artificial-mutations`
 2. The identifiers of the inputs are listed in [all-experiment-names.txt](all-experiment-names.txt). Decide with which inputs to run the experiment, copy the list with e.g. `cp -i all-experiment-names.txt experiment-names.txt` and possibly remove some of the lines in order to run the experiment with fewer inputs.
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
 4. Download [the reads used in the experiment](#reads-used-in-the-experiment) and extract. Please see the commands below. The compressed FASTQ files should be automatically placed in a subdirectory called *genreads*. (In addition to the separate read files, some parts of the workflow require all the reads in one file. The file is automatically generated as part of the workflow but we also provide the generated files.)
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

## Reads used in the experiment

The following archives contain the reads used in the experiment in gzip-compressed FASTQ format. (Hence the archive itself has not been re-compressed.)

| Reads | Coverage | Note |
| ----- | -------- | ---- |
| [genreads-cov10.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov10.tar) | 10 | |
| [genreads-cov20.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov20.tar) | 20 | |
| [genreads-cov10-renamed.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov10-renamed.tar) | 10 | All reads in one file |
| [genreads-cov20-renamed.tar](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/reads/genreads-cov20-renamed.tar) | 20 | All reads in one file |

## Variants

The following archives contain the actual (not predicted) variants in the generated samples. The identifier of the removed sample in all cases is `SAMPLE0`.

| Description | File |
| ----------- | ---- |
| Samples removed in the experiments | [variants-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/variants-truth.tar.gz) |
| All samples | [variants-all.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/variants-all.tar.gz) |

## Sequences of the removed samples

The following archives contain the actual sequences of the samples that were removed in the experiments.

| Sequences |
| --------- |
| [sequences-truth.tar.gz](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/sequences-truth.tar.gz) |

## Indices for use with `Snakefile.call`

Archives that contain the pregenerated indices have been listed [on a separate page](e-coli-indices.md).

## Founder sequences used when generating the indices

| All sequences in one archive |
| ---------------------------- |
| [founder-sequences-a2m.tar.bz2](https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/founder-sequences-a2m.tar.bz2) |

Individual sequence files have been listed [e-coli-index-inputs.md](e-coli-index-inputs.md).

