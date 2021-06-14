import argparse
import gzip
import sys
from bit_vector import BitVector

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Convert aligned positions")
	parser.add_argument("--alignment-positions", type = str, required = True, metavar = "path", help = "Alignment positions (gzipped, one per line)")
	parser.add_argument("--reference-positions", type = str, required = True, metavar = "path", help = "Reference gap positions")
	parser.add_argument("--ad-hoc-reference-positions", type = str, required = True, metavar = "path", help = "Ad-hoc reference gap positions")
	args = parser.parse_args()

	ref_positions = BitVector()
	ad_hoc_ref_positions = BitVector()

	ref_positions.load_from_file(args.reference_positions)
	ad_hoc_ref_positions.load_from_file(args.ad_hoc_reference_positions)

	with gzip.open(args.alignment_positions, mode = "rt") as f:
		for line in f:
			pos_ = line.rstrip("\n")
			pos = int(pos_)

			aln_pos = ad_hoc_ref_positions.select_0(1 + pos)
			ref_pos = ref_positions.rank_0(1 + aln_pos)
			sys.stdout.write(f"{ref_pos}\n")
