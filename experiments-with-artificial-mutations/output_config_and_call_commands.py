import sys

output_config = False			# Whether to output configuration files for Snakefile.call
output_call_commands = True		# Whether to output commands for running Snakemake with Snakefile.call

conda_prefix = "/proj/tnorri/panvc-conda"										# Path prefix to the Conda environment
panvc_sample_workflow_path = "/proj/tnorri/Checkout/git/panvc-sample-workflow"	# Path to panvc-sample-worflow repository
threads = 8																		# Number of threads to use
max_memory_gb = 6																# Max. amount of memory to use with (most of the parts of) the workflow
config_root = "config-panvc-call"												# Configuration file output path
output_root = "output-panvc-call"												# Workflow output path
benchmark_root = "benchmark-panvc-call"											# Benchmark output path
minimum_subgraph_distances = [25, 50, 100]										# Indices with the minimum subgraph distances to use
coverages = [10, 20]															# Reads with the coverages to use
variant_callers = ["GATK", "SAMTOOLS"]											# Variant callers to run

max_memory_mb = 1000 * max_memory_gb # Multiply by 1000 (instead of 1024) in order to keep some memory free.


sys.path.append(panvc_sample_workflow_path)
from generate_snakemake_config_for_call import write_config


def handle_experiment(basename, index_path, reads_1, reads_2):
	"""Output the configuration file and commands for running the given experiment."""
	output_path = f"{output_root}/{basename}"
	benchmark_path = f"{benchmark_root}/{basename}"
	config_path = f"{config_root}/{basename}.yaml"
	
	if output_config:
		write_config(config_path, index_path, output_path, reads_1, reads_2, variant_callers, 1, 1, max_memory_mb, True, True, benchmark_dir = benchmark_path)
	
	if output_call_commands:
		print(f"mkdir -p {output_path}")
		print(f"mkdir -p {benchmark_path}")
		print(f"snakemake --configfile {config_path} --snakefile {panvc_sample_workflow_path}/Snakefile.call --cores {threads} -p --use-conda --conda-prefix {conda_prefix} --resources mem_mb={max_memory_mb}")


if __name__ == "__main__":
	for msd in minimum_subgraph_distances:
		for cov in coverages:
			# Align reads to an index generated from samples of the same generation.
			for gen in [5, 7, 10]:
				for mrate in [0.001, 0.002, 0.004, 0.008, 0.016]:
					basename = f"g{gen}-p{mrate}-cov{cov}-msd{msd}"
					index = f"indices/e-coli-g{gen}-p{mrate}-msd{msd}-precalc"
					fq1 = f"genreads/e-coli-g{gen}-p{mrate}.fa-cov{cov}_read1.fq.gz"
					fq2 = f"genreads/e-coli-g{gen}-p{mrate}.fa-cov{cov}_read2.fq.gz"
					handle_experiment(basename, index, fq1, fq2)
			
			# Align reads to an index generated from samples of a previous generation.
			for gen in [5, 7]:
				for mrate in [0.001, 0.002, 0.004, 0.008, 0.016]:
					basename = f"g{gen}-p{mrate}-cov{cov}-read_g10-msd{msd}"
					index = f"indices/e-coli-g{gen}-p{mrate}-msd{msd}-precalc"
					fq1 = f"genreads/e-coli-g10-p{mrate}.fa-cov{cov}_read1.fq.gz"
					fq2 = f"genreads/e-coli-g10-p{mrate}.fa-cov{cov}_read2.fq.gz"
					handle_experiment(basename, index, fq1, fq2)
			
			# Align reads to an index with samples removed.
			for seg in range(0, 7):
				basename = f"g5-p0.016-cov{cov}-s{seg}-msd{msd}"
				index = f"indices/e-coli-g5-m0.016-s{seg}-msd{msd}-precalc"
				fq1 = f"genreads/e-coli-g5-p0.016.fa-cov{cov}_read1.fq.gz"
				fq2 = f"genreads/e-coli-g5-p0.016.fa-cov{cov}_read2.fq.gz"
				handle_experiment(basename, index, fq1, fq2)
