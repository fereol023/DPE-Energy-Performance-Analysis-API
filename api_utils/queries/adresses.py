create_table = f"""
CREATE TABLE "adresses" (
	"id_ban" VARCHAR(255) NOT NULL UNIQUE,
	"full_adress_ban" TEXT,
	"label_ban" TEXT,
	"complement_d_adresse_batiment_ademe" TEXT,
	"complement_d_adresse_logement_ademe" TEXT,
	PRIMARY KEY("id_ban")
);
"""
