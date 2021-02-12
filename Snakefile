# Copyright (c) Tuukka Norri 2020
# Licenced under the MIT licence.

include: "panvc-sample-workflow/Snakefile.install"

rule conda_environment_edlib:
	conda:					"envs/edlib.yaml"
	shell:					'echo "Done"'

rule conda_environment_happy:
	conda:					"envs/happy.yaml"
	shell:					'echo "Done"'

rule conda_environment_vcfcat:
	conda:					"envs/vcfcat.yaml"
	shell:					'echo "Done"'
