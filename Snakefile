# Copyright (c) Tuukka Norri 2020
# Licenced under the MIT licence.

include "panvc-sample-workflow/Snakefile.install"

rule conda_environment_experiments:
	conda:					"experiment_env.yaml"
	run:
		print("Done")
