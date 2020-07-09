import sys

# Create Slurm job files for generating the indices.

panvc_index_cmd = "/proj/tnorri/Checkout/git/panvc-test-version/panvc_index -t 16 -d 10 -l 105 -p 1 -i A2M --max_open_files 1000 --max_mem_MB 15000 input output log"

def output_job_script(basename):
	global panvc_index_cmd

	dst = f"indices/{basename}"

	with open(f"jobs/{basename}.job", "w") as f:
		print("#!/bin/bash", file = f)
		print("#SBATCH -c 16", file = f)
		print("#SBATCH -t 0:45:00", file = f)
		print("#SBATCH --mem=16G", file = f)
		print("module purge", file = f)
		print("module load GCCcore/8.2.0", file = f)
		print("module load Python/3.7.2-GCCcore-8.2.0", file = f)
		print("source /proj/tnorri/python3.7.2-GCCcore-8.2.0/bin/activate", file = f)
		print("ulimit -n 8192", file = f)
		print(f"cd {dst}", file = f)
		print(f"srun {panvc_index_cmd}", file = f)

for gen in [5, 7, 10]:
	for mrate in [0.001, 0.002, 0.004, 0.008, 0.016]:
		basename = f"e-coli-g{gen}-p{mrate}"
		output_job_script(basename)

for seg in range(0, 7):
	basename = f"e-coli-g5-m0.016-s{seg}"
	output_job_script(basename)
