create_table = f"""
CREATE TABLE "villes" (
	"code_postal_ban_ademe" VARCHAR(255) NOT NULL UNIQUE,
	"city_ban" TEXT,
	"code_departement_enedis" VARCHAR(255),
	PRIMARY KEY("code_postal_ban_ademe")
);
"""