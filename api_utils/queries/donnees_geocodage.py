create_table = f"""
CREATE TABLE "donnees_geocodage" (
	"id_ban" VARCHAR(255) NOT NULL UNIQUE,
	"lon_ban" DECIMAL,
	"lat_ban" DECIMAL,
	"score_ban_ademe" DECIMAL,
	"statut_geocodage_ademe" TEXT,
	PRIMARY KEY("id_ban")
);
"""