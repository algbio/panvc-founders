#!/bin/bash

set -e

v2m_path="/proj/tnorri/local/vcf2multialign-DEV-68e94a9"	# Path to vcf2multialign executables
reference_path="e-coli.fa"
call_root="output-panvc-call"								# Workflow output path
output_root="output-predicted-sequences"
minimum_subgraph_distances="25 50 100"						# Indices with the minimum subgraph distances used
coverages="10 20"											# Reads with the coverages used
variant_callers="gatk samtools"								# Variant callers run
handle_panvc=1												# Output predicted sequences from PanVC’s variants
handle_baseline=1											# Output predicted sequences from baseline’s variants


function output_cmd
{   
	experiment="${1}"
	chr_name="${2}"
	exp_path="${call_root}/${experiment}"
	
	for vc in ${variant_callers}
	do  
		if (( 1 == ${handle_panvc} ))
		then
			input_vcf="${exp_path}/ext_vc/pg_variants.${vc}.vcf"
			output_name="${experiment}-${vc}-panvc.txt"
			output_path="${output_root}/${output_name}"
			echo "'${v2m_path}/vcf_to_unaligned' --reference='${reference_path}' --variants='${input_vcf}' --output='${output_path}' -s 0 -p 0 -c '${chr_name}'"
		fi
		
		if (( 1 == ${handle_baseline} ))
		then
			input_vcf="${exp_path}/baseline_vc/variants.${vc}.vcf"
			output_name="${experiment}-${vc}-baseline.txt"
			output_path="${output_root}/${experiment}-${vc}-baseline.txt"
			echo "'${v2m_path}/vcf_to_unaligned' --reference='${reference_path}' --variants='${input_vcf}' --output='${output_path}' -s 0 -p 0 -c '${chr_name}'"
		fi
	done
}

echo "mkdir -p ${output_root}"
for msd in minimum_subgraph_distances
do
	for cov in coverages
	do
		# Reads aligned to the index generated from samples from the same generation.
		for gen in 5 7 10
		do
			for mrate in 0.001 0.002 0.004 0.008 0.016
			do  
				experiment="g${gen}-p${mrate}-cov${cov}-msd${msd}"
				chr_name="e-coli-g${gen}-p${mrate}-msd${msd}-precalc"
				output_cmd "${experiment}" "${chr_name}"
			done
		done

		# Reads aligned to the index generated from samples from a previous generation.
		for gen in 5 7
		do
			experiment="g${gen}-p${mrate}-cov${cov}-read_g10-msd${msd}"
			chr_name="e-coli-g${gen}-p${mrate}-msd${msd}-precalc"
			output_cmd "${experiment}" "${chr_name}"
		done

		# Reads aligned to an index with some samples removed.
		for seg in {0..6}
		do
			experiment="g${gen}-p${mrate}-cov${cov}-s${seg}-msd${msd}"
			chr_name="e-coli-g${gen}-m${mrate}-s${seg}-msd${msd}-precalc"
			output_cmd "${experiment}" "${chr_name}"
		done
	done
done
