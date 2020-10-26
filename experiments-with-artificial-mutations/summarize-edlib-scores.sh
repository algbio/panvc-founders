#!/bin/bash

set -e

printf "Experiment\tWorkflow\tMutation rate\tCoverage\tMinimum subgraph distance\tGeneration\tRead generation\tRead set\tEdit distance\n"

for msd in 25 50 100
do
	for cov in 10 20
	do
		for vc in gatk samtools
		do
			for mrate in 0.001 0.002 0.004 0.008 0.016
			do
				for gen in 5 7 10
				do
					for wf in baseline panvc
					do
						# E.g. edlib-scores/g5-p0.002-cov20-msd50.baseline.gatk.txt
						fn="edlib-scores/g${gen}-p${mrate}-cov${cov}-msd${msd}.${wf}.${vc}.txt"
						if [ -f "${fn}" ]
						then
							#     exp  wf  vc  mr cov  msd gen  rg  rs 
							printf "1\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t-1\t" "${wf}" "${vc}" "${mrate}" "${cov}" "${msd}" "${gen}" "${gen}"
							grep -E "^[#]0" "$fn" | awk '{ print $2 }'
						fi
					done
				done

				for gen in 5 7
				do
					for wf in baseline panvc
					do
						# E.g. edlib-scores/g7-p0.016-cov20-read_g10-msd100.baseline.gatk.txt
						fn="edlib-scores/g${gen}-p${mrate}-cov${cov}-read_g10-msd${msd}.${wf}.${vc}.txt"
						if [ -f "${fn}" ]
						then
							#     exp  wf  vc  mr  cov msd gen rg  rs
							printf "2\t%s\t%s\t%s\t%s\t%s\t%s\t10\t-1\t" "${wf}" "${vc}" "${mrate}" "${cov}" "${msd}" "${gen}"
							grep -E "^[#]0" "$fn" | awk '{ print $2 }'
						fi
					done
				done
			done

			for mrate in 0.016
			do
				for gen in 5
				do
					for wf in baseline panvc
					do
						for seg in {0..6}
						do
							# E.g. edlib-scores/g5-p0.016-cov20-s4-msd100.panvc.samtools.txt
							fn="edlib-scores/g${gen}-p${mrate}-cov${cov}-s${seg}-msd${msd}.${wf}.${vc}.txt"
							if [ -f "${fn}" ]
							then
								#     exp  wf  vc  mr  cov msd gen rg  rs
								printf "3\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" "${wf}" "${vc}" "${mrate}" "${cov}" "${msd}" "${gen}" "${gen}" "${seg}"
								grep -E "^[#]0" "$fn" | awk '{ print $2 }'
							fi
						done
					done
				done
			done
		done
	done
done
