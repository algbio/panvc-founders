from Bio import SeqIO
import gzip
import sys

# Output maximum read lengths for given accessions.

if __name__ == "__main__":
	for acc in sys.stdin:
		acc = acc.rstrip("\n")
		for rid in [1, 2]:
			fname = f"reads/{acc}_{rid}.fastq.gz"
			max_len = 0
			with gzip.open(fname, "rt") as infile:
				for rec in SeqIO.parse(infile, "fastq"):
					length = len(rec.seq)
					max_len = max(max_len, length)
			print(f"{fname}\t{max_len}")
