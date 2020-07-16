#!/bin/bash

set -e

edlib_aligner=/proj/tnorri/Checkout/git/edlib/build/bin/edlib-aligner

function check_exists
{
	if [ ! -f "$1" ]
	then
		echo "“$1” either does not exists or is not a regular file."
		exit 1
	fi
}


for cov in 10 20
do
	for vc in gatk samtools
	do
		for mrate in 0.001 0.002 0.004 0.008 0.016
		do
			for gen in 5 7 10
			do
				for pl in panvc baseline
				do
					truth="haplotypes-truth/e-coli-g${gen}-p${mrate}-sample0.txt"
					prediction="predicted-haplotypes/${vc}-g${gen}-p${mrate}-cov${cov}-${pl}.txt"
					dst="edlib-scores/exp-1-e-coli-${vc}-g${gen}-p${mrate}-cov${cov}-${pl}.score" 
					check_exists "${truth}"
					check_exists "${prediction}"

					echo "${edlib_aligner} ${prediction} ${truth} > ${dst} 2>&1"
				done
			done

			for gen in 5 7
			do
				for pl in panvc baseline
				do
					truth="haplotypes-truth/e-coli-g10-p${mrate}-sample0.txt"
					prediction="predicted-haplotypes/${vc}-g${gen}-p${mrate}-cov${cov}-read_g10-${pl}.txt"
 					dst="edlib-scores/exp-2-e-coli-${vc}-g${gen}-p${mrate}-cov${cov}-${pl}.score"
					check_exists "${truth}"
					check_exists "${prediction}"

					echo "${edlib_aligner} ${prediction} ${truth} > ${dst} 2>&1"
				done
			done

			for seg in {0..6}
			do
				truth="haplotypes-truth/e-coli-g5-p0.016-sample0.txt"
				prediction="predicted-haplotypes/${vc}-g5-p0.016-cov${cov}-s${seg}-panvc.txt"
				dst="edlib-scores/exp-3-e-coli-${vc}-g5-p0.016-s${seg}-pg.score" 
				check_exists "${truth}"
				check_exists "${prediction}"

				echo "${edlib_aligner} ${prediction} ${truth} > ${dst} 2>&1"
			done
		done
	done
done
