import argparse
import sys


if __name__ == "__main__":
	reference = "index/std_ref.fa"
	known_variants = "/home/wrk/gsa/tnorri/genome-data-files/1000g-phase-3/founders-3/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.selected_samples.no_svs.vcf.gz"
	vcf_filter_py = "/home/tnorri/.local/bin/vcf_filter.py"

	parser = argparse.ArgumentParser(description = "Output commands for running GraphTyper")
	parser.add_argument("mode", choices = ["index", "call", "combine", "normalize", "filter"], help = "1. index alignments, 2. call variants, 3. combine BCF files, 4. split multiallelics, 5. Filter by AAScore")
	args = parser.parse_args()

	if args.mode in ["index", "call"]:
		for bam_input, wf in [("call/baseline_vc/sorted-alns2.samtools.bam", "bwa-for-samtools"), ("call/baseline_vc/aligned_deduplicated_sorted.gatk.bam", "bwa-for-gatk")]:
			if "index" == args.mode:
				print(f"samtools index {bam_input}")
			elif "call" == args.mode:
				print(f"~/Checkout/graphtyper/build/bin/graphtyper genotype '{reference}' --sam='{bam_input}' --prior_vcf='{known_variants}' --region=1:1-249250621 --output=graphtyper/{wf} --threads=80")
				print(f"~/Checkout/graphtyper/build/bin/graphtyper genotype_sv '{reference}' '{known_variants}' --sam='{bam_input}' --region=1:1-249250621 --output=graphtyper/{wf}-sv --threads=80")
	elif "combine" == args.mode:
		print("# Remember to cd graphtyper first.", file = sys.stderr)
		for subdir in ["bwa-for-gatk", "bwa-for-gatk-sv", "bwa-for-samtools", "bwa-for-samtools-sv"]:
			print(f'find {subdir}/1 -name "*.vcf.gz" | sort > {subdir}.list.txt && bcftools concat --naive --file-list {subdir}.list.txt -Ob -o {subdir}.bcf')
	elif "normalize" == args.mode:
		for wf in ["bwa-for-gatk", "bwa-for-gatk-sv", "bwa-for-samtools", "bwa-for-samtools-sv"]:
			print(f"bcftools norm --multiallelics - -Oz -o graphtyper/{wf}.split.vcf.gz graphtyper/{wf}.bcf")
	elif "filter" == args.mode:
		# SV pipeline does not set AAScore.
		for wf in ["bwa-for-gatk", "bwa-for-samtools"]:
			print(f"{vcf_filter_py} --local-script filter_graphtyper_output.py graphtyper/{wf}.split.vcf.gz AAScore --aa-score 0.5 | bgzip > graphtyper/{wf}.filtered.vcf.gz")
