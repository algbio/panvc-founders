import sys

# Write Snakemake configuration files for the accessions given in stdin.

if __name__ == "__main__":
	for acc in sys.stdin: # Accession list
		acc = acc.rstrip("\n")
		for ds, suffix in [("subset20", "subset20"), ("founders", "msd5")]:
			with open(f"config-call-{ds}/{acc}.yaml", "w") as f:
				f.write(f"benchmark_dir: benchmark-call/{acc}-{suffix}\n")
				f.write(f"output_root: call/{acc}-{suffix}\n")
				f.write(f"reads_all_path: reads/{acc}.all.fq.gz\n")
				f.write(f"reads_file_1: reads/{acc}_1.fastq.gz\n")
				f.write(f"reads_file_2: reads/{acc}_2.fastq.gz\n")
