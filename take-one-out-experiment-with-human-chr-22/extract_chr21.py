# Copyright (c) Tuukka Norri 2020
# Licenced under the MIT licence.


import sys

sys.path.append(f"{snakemake.scriptdir}/..")
from extract_fasta import extract_fasta


assert 1 == len(snakemake.input)
assert 1 == len(snakemake.output)
with open(snakemake.input[0], "r") as src, open(snakemake.output[0], "w") as dst:
	if not extract_fasta(src, dst, "21", "chr21", False, False, False):
		print(f"Sequence with identifier “21” not found in {snakemake.input}.", file = sys.stderr)
		sys.exit(1)
