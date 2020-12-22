#!/bin/bash

set -e

benchmark_dir="$1"

process_one_panvc() {
	benchmark_path="${benchmark_dir}/${1}"
	if [ -f "${benchmark_path}" ]
	then
		printf "${1}\tpanvc\t"
		tail -n +2 "${benchmark_path}"
	fi
}

process_group_panvc() {
	benchmark_path="${benchmark_dir}/${1}"
	if [ -d "${benchmark_path}" ]
	then
		ls "${benchmark_path}" | sort -n | while read x
		do
			printf "${1}\tpanvc\t"
			tail -n +2 "${benchmark_path}/${x}"
		done
	fi
}

process_group() {
	benchmark_path="${benchmark_dir}/${1}"
	if [ -d "${benchmark_path}" ]
	then
		ls "${benchmark_path}" | sort -n | while read x
		do
			printf "${1}\t${x}\t"
			tail -n +2 "${benchmark_path}/${x}"
		done
	fi
}


printf "step\tgroup\ts\th:m:s\tmax_rss\tmax_vms\tmax_uss\tmax_pss\tio_in\tio_out\tmean_load\n"


# Handle indexing benchmarks.
# We can handle both indexing and variant calling in one script b.c. the step names are unique.

process_group_panvc a2m_prepare

for x in all_sequences_file chic_align
do
	process_one_panvc "${x}"
done

process_group_panvc gap_positions


# Variant calling. This also involves indexing steps for baseline.

for x in panvc_generate_reads_all panvc_align_reads panvc_convert_alignments panvc_sam_to_positions
do
	process_one_panvc "${x}"
done

for x in panvc_pileup panvc_pileup_sums panvc_heaviest_paths
do
	process_group_panvc "${x}"
done

for x in panvc_combine_adhoc_ref
do
	process_one_panvc "${x}"
done

for x in bwa_index_ref samtools_align_reads gatk_align_reads gatk_sort_aligned_reads 
do
	process_group "${x}"
done

process_group mark_duplicates

for x in samtools_sort_aligned samtools_pileup 
do
	process_group "${x}"
done

# FIXME: Continue from gatk_fastq_to_unaligned
