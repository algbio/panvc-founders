# 
# Copyright (c) 2018-2020 Tuukka Norri
# This code is licensed under MIT license (see LICENSE for details).
# 

import argparse
import os
import sys

from Bio import SeqIO

# Input: FASTA.
# Output: The specified sequence.


def extract_fasta(fh, dst, seq_id, new_id, reverse_complement, remove_gaps, log):
	if log:
		print("Reading FASTA…", file = sys.stderr)
	seq = None
	for rec in SeqIO.parse(fh, format = "fasta"):
		if log:
			print("Found record: %s" % rec.id, file = sys.stderr)
		if rec.id == seq_id:
			print(">%s" % new_id, file = dst)
			if reverse_complement:
				table = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', '-': '-', 'N': 'N'}
				for i in reversed(range(len(rec.seq))):
					if remove_gaps and '-' == rec.seq[i]:
						continue
					dst.write(table[rec.seq[i]])
			else:
				# FIXME: this is really inefficient.
				for i in range(len(rec.seq)):
					if remove_gaps and '-' == rec.seq[i]:
						continue
					dst.write(rec.seq[i])
			dst.write("\n")
			return True
	
	return False

	print("Sequence identifier not found in FASTA.", file = sys.stderr)
	sys.exit(os.EX_DATAERR)


if __name__ == "__main__":
	parser = argparse.ArgumentParser("Output the specified sequence in a FASTA file.")
	parser.add_argument('--fasta', required = True, type = argparse.FileType('rU'))
	parser.add_argument('--seq-id', required = True)
	parser.add_argument('--reverse-complement', action = "store_true")
	parser.add_argument('--remove-gaps', action = "store_true")
	args = parser.parse_args()

	if not extract_fasta(args.fasta, sys.stdout, args.seq_id, args.reverse_complement, args.remove_gaps, True):
		print("Sequence identifier not found in FASTA.", file = sys.stderr)
		sys.exit(os.EX_DATAERR)
