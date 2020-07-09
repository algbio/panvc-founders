#!/bin/bash

## Prepares index input from A2M files.

set -e

for gen in 5 7 10
do
	for mrate in 0.001 0.002 0.004 0.008 0.016
	do
		basename="e-coli-g${gen}-p${mrate}"
		src="founder-sequences-a2m/${basename}.a2m"
		dst="indices/${basename}"
		mkdir -p "${dst}"
		mkdir -p "${dst}/input"
		mkdir -p "${dst}/output"
		mkdir -p "${dst}/log"
		ln "${src}" "${dst}/input/pangenome1.a2m"
		echo 1 > "${dst}/input/chr_list.txt"
	done
done

for seg in {0..6}
do
	basename="e-coli-g5-m0.016-s${seg}"
	src="founder-sequences-a2m/${basename}.a2m"
	dst="indices/${basename}"
	mkdir -p "${dst}"
	mkdir -p "${dst}/input"
	mkdir -p "${dst}/output"
	mkdir -p "${dst}/log"
	ln "${src}" "${dst}/input/pangenome1.a2m"
	echo 1 > "${dst}/input/chr_list.txt"
done
