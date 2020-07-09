#!/bin/bash

# Output commands for generating the indices.

set -e


panvc_index="/proj/tnorri/Checkout/git/panvc-test-version/panvc_index -t 28 -d 10 -l 105 -p 1 -i A2M --max_open_files 1000 --max_mem_MB 16000 input output log"

for gen in 5 7 10
do
	for mrate in 0.001 0.002 0.004 0.008 0.016
	do
		basename="e-coli-g${gen}-p${mrate}"
		dst="indices/${basename}"
		echo "pushd ${dst} && ${panvc_index} input output log"
	done
done

for seg in {0..6}
do
	basename="e-coli-g5-m0.016-s${seg}"
	dst="indices/${basename}"
	echo "pushd ${dst} && ${panvc_index} input output log"
done
