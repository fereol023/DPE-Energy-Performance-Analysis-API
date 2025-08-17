create_table = f"""
CREATE TABLE "donnees_climatiques" (
	"id_ban" VARCHAR(255) NOT NULL UNIQUE,
	"zone_climatique_ademe" VARCHAR(255),
	PRIMARY KEY("id_ban")
);
"""