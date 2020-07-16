import sys

threads = 8
max_mem_mb = 15000
panvc_call_cmd = "/proj/tnorri/Checkout/git/panvc-test-version/panvc_call_variants -t {threads} --summarize --baseline_vc -p 1 --ploidy-file 1 -m {max_mem_mb}"

def output_call_cmd(basename, index_dir, reads_1, reads_2, vc):
	global panvc_call_cmd
	print(f"{panvc_call_cmd} --pgindex_dir {index_dir} -r1 {reads_1} -r2 {reads_2} -o panvc-call/{basename} --vc_base_method {vc.upper()} > logs/{basename}.log 2>&1")

for cov in [10, 20]:
	for vc in ["samtools", "gatk"]:
		for gen in [5, 7, 10]:
			for mrate in [0.001, 0.002, 0.004, 0.008, 0.016]:
				basename = f"{vc}-g{gen}-p{mrate}-cov{cov}"
				index = f"indices/e-coli-g{gen}-p{mrate}/output"
				fq1 = f"genreads/e-coli-g{gen}-p{mrate}.fa-cov{cov}_read1.fq.gz"
				fq2 = f"genreads/e-coli-g{gen}-p{mrate}.fa-cov{cov}_read2.fq.gz"
				output_call_cmd(basename, index, fq1, fq2, vc)

		for gen in [5, 7]:
			for mrate in [0.001, 0.002, 0.004, 0.008, 0.016]:
				basename = f"{vc}-g{gen}-p{mrate}-cov{cov}-read_g10"
				index = f"indices/e-coli-g{gen}-p{mrate}/output"
				fq1 = f"genreads/e-coli-g10-p{mrate}.fa-cov{cov}_read1.fq.gz"
				fq2 = f"genreads/e-coli-g10-p{mrate}.fa-cov{cov}_read2.fq.gz"
				output_call_cmd(basename, index, fq1, fq2, vc)

		for seg in range(0, 7):
			basename = f"{vc}-g5-p0.016-cov{cov}-s{seg}"
			index = f"indices/e-coli-g5-m0.016-s{seg}/output"
			fq1 = f"genreads/e-coli-g5-p0.016.fa-cov{cov}_read1.fq.gz"
			fq2 = f"genreads/e-coli-g5-p0.016.fa-cov{cov}_read2.fq.gz"
			output_call_cmd(basename, index, fq1, fq2, vc)
