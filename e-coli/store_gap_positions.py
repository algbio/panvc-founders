import argparse
import functools
import os
import sys
from bit_vector import BitVector

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Store gap positions in a bit vector with rank and select support.')
	parser.add_argument("--input", required = True, type = argparse.FileType('r'), metavar = "path", help = "Input path")
	parser.add_argument("--output", required = True, type = str, metavar = "path", help = "Output path")
	parser.add_argument("--support-rank", action = "store_true", help = "Prepare rank support")
	parser.add_argument("--support-select", action = "store_true", help = "Prepare select support")
	args = parser.parse_args()

	# Determine the input size.
	args.input.seek(0, os.SEEK_END)
	size = args.input.tell()
	args.input.seek(0, os.SEEK_SET)

	bv = BitVector(size)

	# Store the gap positions.
	sys.stderr.write("Reading the input…\n")
	read_ch = functools.partial(args.input.read, 1)
	for i, c in enumerate(iter(read_ch, '')):
		assert i < size
		if '-' == c:
			bv[i] = True

	if args.support_rank:
		sys.stderr.write("Preparing rank support…\n")
		bv.rank_0.prepare()

	if args.support_select:
		sys.stderr.write("Preparing select support…\n")
		bv.select_0.prepare()

	sys.stderr.write("Serializing…\n")
	bv.write_to_file(args.output)
