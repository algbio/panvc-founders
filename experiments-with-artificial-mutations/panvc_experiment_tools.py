# Copyright (c) Tuukka Norri 2020
# Licenced under the MIT licence.

def remove_prefix(s, prefix):
	"""Remove the given prefix from s"""
	if s.startswith(prefix):
		return s[len(prefix):]
	else:
		return s


def list_experiment_names(exp_file_path):
	"""Retrieve experiment names from the given file."""
	def helper():
		with open(exp_file_path, "r") as ef:
			for line in ef:
				exp_name = line.rstrip("\n")
				yield exp_name
	return [x for x in helper()]


def list_index_names(exp_file_path):
	"""List index names needed for the given experiments."""
	exp_names = list_experiment_names(exp_file_path)
	index_names = set()
	for exp_name in exp_names:
		with open(f"config-call/{exp_name}.yaml", "r") as cf:
			config = yaml.safe_load(cf)
			index_root = config["index_root"]
			index_name = remove_prefix(index_root, "indices/")
			index_names.add(index_name)
	return list(sorted(index_names))
