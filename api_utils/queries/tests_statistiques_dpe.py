create_table = f"""
CREATE TABLE "tests_statistiques_dpe" (
	"batch_id" VARCHAR(255) NOT NULL,
	"etiquette_dpe_ademe" VARCHAR(1) NOT NULL,
	"sample_size" INTEGER,
	"paired_t_test_t_statistic" DECIMAL,
	"paired_t_test_p_value" DECIMAL,
	"wilcoxon_statistic" DECIMAL,
	"wilcoxon_p_value" DECIMAL,
	PRIMARY KEY("batch_id", "etiquette_dpe_ademe")
);
"""