# E.coli experiment with natural reads and known variants

This directory contains the scripts needed to run the E.coli experiment with natural reads.

## Running the experiment

1. Download the [indexing input](https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-index-input.tar.bz2) with e.g. `wget https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-index-input.tar.bz2`. Extract the contents to the `e-coli` directory with e.g. `pbzip2 -dc e-coli-index-input.tar.bz2 | tar x`.
2. Download the [reads used in the experiment](https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-reads.tar) with e.g. `wget https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-reads.tar`. Extract the contents with `tar x e-coli-reads.tar`.
3. Generate an index using the founder sequences with `snakemake --configfile config-common-index.yaml config-index/e-coli-msd5.yaml --snakefile ../panvc-sample-workflow/Snakefile.index --cores 16 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=16384`.
4. Generate an index using the random selection of reference sequences with `snakemake --configfile config-common-index.yaml config-index/e-coli-subset20.yaml --snakefile ../panvc-sample-workflow/Snakefile.index --cores 16 --printshellcmds --use-conda --conda-prefix ../conda-env --resources mem_mb=16384`.
5. The experiments may be run with e.g. <code>./founder-experiment-cmds.sh | parallel -j<i>jobs</i></code> where *jobs* is the number of Snakemake instances. The script allocates 16 GB of memory and 5 CPU cores to each instance of Snakemake. Alternatively the commands may be piped to e.g. bash: `./founder-experiment-cmds.sh | bash -x -e`.
6. The experiments with the random selection of reference sequences may be run similarly with either <code>./subset20-experiment-cmds.sh | parallel -j<i>jobs</i></code> or `./subset20-experiment-cmds.sh | bash -x -e`.
7. To gather statistics with Samtools, run first `mkdir samtools-stats` and then `./run-samtools-stats.sh`. The results will be placed in the aforementioned directory.

## Running the experiment with the comparison to *de novo* sequenced contigs

1. Download the [reads used in the experiment](https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-reads-de-novo-experiment.tar) with e.g. `wget https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-reads-de-novo-experiment.tar`. Extract the contents to the `e-coli` directory with `tar x e-coli-reads-de-novo-experiment.tar`.
2. Download the [contigs used in the experiment](https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-de-novo-contigs.tar) with e.g. `wget https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e-coli-de-novo-contigs.tar`. Extract the contents with `tar x e-coli-de-novo-contigs.tar`.
3. Download the [E.coli K-12 reference without line breaks](https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e.coli-k12-mg1655.no-linebreaks.fa.gz) with e.g. `wget https://cs.helsinki.fi/group/gsa/panvc-founders/natural-e-coli-experiment/e.coli-k12-mg1655.no-linebreaks.fa.gz`. Extract with `gunzip e.coli-k12-mg1655.no-linebreaks.fa.gz`.
4. The indices generated in the previous experiment may be used.
5. Run the following commands where *jobs* is the number of Snakemake instances.
   - <code>./founder-de-novo-experiment-cmds.sh | parallel -j<i>jobs</i></code>
   - <code>./subset20-de-novo-experiment-cmds.sh | parallel -j<i>jobs</i></code>
6. Generate the predicted sequences with `snakemake --printshellcmds --use-conda --conda-prefix ../conda-env`. Here Snakemake is only used to activate the correct Conda environment; the snakefile essentially runs `predicted-sequences.sh`.
7. Run QUAST with `mkdir -p quast && ./quast.sh`. The results will be placed in `quast`.
