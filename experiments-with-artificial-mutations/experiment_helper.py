# Copyright (c) Tuukka Norri 2020
# Licenced under the MIT licence.

import argparse
import sys
import yaml
from panvc_experiment_tools import list_experiment_names, list_index_names


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Print file URLs and commands needed to run the experiment.")

	parser.add_argument("--experiment-list", type = str, required = True, help = "List of experiment names to run as a plain text file, one per line")

	group = parser.add_mutually_exclusive_group(required = True)
	group.add_argument("--print-index-input-urls", action = "store_true", help = "Print URLs for founder sequences needed to generate the indices")
	group.add_argument("--print-index-urls", action = "store_true", help = "Print URLs for pregenerated indices needed to run the listed experiments")
	group.add_argument("--print-indexing-commands", action = "store_true", help = "Print commands for generating the indices needed for variant calling")
	group.add_argument("--print-variant-calling-commands", action = "store_true", help = "Print commands for running the variant calling workflow")
	group.add_argument("--print-predicted-sequence-generation-commands", action = "store_true", help = "Print commands for generating the predicted sequences from the variant calling results")
	group.add_argument("--print-sequence-comparison-commands", action = "store_true", help = "Print commands for comparing the predicted sequences to the hidden truth")

	parser.add_argument("--snakemake-arguments", type = str, required = False, default = "", help = "Additional arguments to pass to Snakemake, e.g. --snakemake-arguments '--conda-prefix /path/to/conda/environment'")

	args = parser.parse_args()

	if args.print_index_input_urls:
		index_names = list_index_names(args.experiment_list)
		input_file_names = map(lambda x: f"{x}.a2m.bz2", index_names)
		input_file_urls = map(lambda x: f"https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/index-input/{x}", input_file_names)
		for url in input_file_urls:
			print(url)
	elif args.print_index_urls:
		index_names = list_index_names(args.experiment_list)
		index_file_names = map(lambda x: f"{x}.tar.bz2", index_names)
		index_file_urls = map(lambda x: f"https://cs.helsinki.fi/group/gsa/panvc-founders/e-coli-experiment/indices/{x}", index_file_names)
		for url in index_file_urls:
			print(url)
	elif args.print_indexing_commands:
		index_names = list_index_names(args.experiment_list)
		for index_name in index_names:
			cmd = f"snakemake --snakefile ../panvc-sample-workflow/Snakefile.index --configfile config-common-index.yaml config-index/{index_name}.yaml --use-conda {args.snakemake_arguments}"
			print(cmd)
	elif args.print_variant_calling_commands:
		exp_names = list_experiment_names(args.experiment_list)
		for exp_name in exp_names:
			cmd = f"snakemake --snakefile ../panvc-sample-workflow/Snakefile.call --configfile config-common-call.yaml config-call/{exp_name}.yaml --use-conda {args.snakemake_arguments}"
			print(cmd)
	elif args.print_predicted_sequence_generation_commands:
		cmd = f"snakemake --config experiment_list={args.experiment_list} --configfile config-common-call.yaml --use-conda {args.snakemake_arguments} -- predicted_sequences"
		print(cmd)
	elif args.print_sequence_comparison_commands:
		cmd = f"snakemake --config experiment_list={args.experiment_list} --configfile config-common-call.yaml --use-conda {args.snakemake_arguments} -- edit_distances"
		print(cmd)
