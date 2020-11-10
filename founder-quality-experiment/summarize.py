import sys

sys.stdout.write("Coverage,Index,Variant caller,Workflow,Type,Filter,TRUTH.TOTAL,TRUTH.TP,TRUTH.FN,QUERY.TOTAL,QUERY.FP,QUERY.UNK,FP.gt,FP.al,METRIC.Recall,METRIC.Precision,METRIC.Frac_NA,METRIC.F1_Score,TRUTH.TOTAL.TiTv_ratio,QUERY.TOTAL.TiTv_ratio,TRUTH.TOTAL.het_hom_ratio,QUERY.TOTAL.het_hom_ratio\n")
for cov in [10, 20, 50]:
	for index in ["Founders", "Predicted"]:
		for vc in ["GATK", "Samtools"]:
			for workflow in ["Baseline", "PanVC"]:
				# baseline-predicted-cov10-gatk.summary.csv
				with open(f"hap.py/{workflow.lower()}-{index.lower()}-cov{cov}-{vc.lower()}.summary.csv", "r") as f:
					next(f)
					for line in f:
						sys.stdout.write("%d,%s,%s,%s," % (cov, index, vc, workflow))
						sys.stdout.write(line)
