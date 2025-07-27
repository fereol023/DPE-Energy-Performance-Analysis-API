CREATE TABLE "logements" (
	"id_ademe" VARCHAR(255) NOT NULL UNIQUE,
	"id_ban" VARCHAR(255) NOT NULL,
	"apports_solaires_saison_chauffe_ademe" DECIMAL,
	"besoin_chauffage_ademe" DECIMAL,
	"conso_5_usages_e_finale_energie_ndeg2_ademe" DECIMAL,
	"conso_5_usages_par_m2_e_primaire_ademe" DECIMAL,
	"conso_auxiliaires_e_primaire_ademe" DECIMAL,
	"conso_chauffage_e_primaire_ademe" DECIMAL,
	"conso_e_finale_depensier_installation_ecs_ademe" DECIMAL,
	"conso_ecs_depensier_e_primaire_ademe" DECIMAL,
	"conso_kwh_m2" DECIMAL,
	"cout_auxiliaires_ademe" DECIMAL,
	"deperditions_baies_vitrees_ademe" DECIMAL,
	"deperditions_planchers_hauts_ademe" DECIMAL,
	"emission_ges_5_usages_energie_ndeg2_ademe" DECIMAL,
	"emission_ges_5_usages_par_m2_ademe" DECIMAL,
	"etiquette_dpe_ademe" VARCHAR(1),
	"etiquette_ges_ademe" VARCHAR(1),
	"qualite_isolation_menuiseries_ademe" VARCHAR(255),
	"type_energie_ndeg2_ademe" VARCHAR(255),
	"type_installation_ecs_general_ademe" VARCHAR(255),
	"ubat_w_m2_k_ademe" DECIMAL,
	"usage_generateur_ecs_ndeg1_ademe" VARCHAR(255),
	"usage_generateur_ndeg1_installation_ndeg1_ademe" VARCHAR(255),
	"volume_stockage_generateur_ecs_ndeg1_ademe" DECIMAL,
	"code_postal_ban_ademe" VARCHAR(255),
	"absolute_diff_conso_prim_fin" DECIMAL,
	"absolute_diff_conso_fin_act" DECIMAL,
	"periode_construction_ademe" VARCHAR(255),
	PRIMARY KEY("id_ademe")
);




CREATE TABLE "adresses" (
	"id_ban" VARCHAR(255) NOT NULL UNIQUE,
	"full_adress_ban" TEXT,
	"label_ban" TEXT,
	"complement_d_adresse_batiment_ademe" TEXT,
	"complement_d_adresse_logement_ademe" TEXT,
	PRIMARY KEY("id_ban")
);




CREATE TABLE "donnees_climatiques" (
	"id_ban" VARCHAR(255) NOT NULL UNIQUE,
	"zone_climatique_ademe" CHAR(1),
	PRIMARY KEY("id_ban")
);




CREATE TABLE "ville" (
	"code_postal_ban_ademe" VARCHAR(255) NOT NULL UNIQUE,
	"city_ban" TEXT,
	"code_departement_enedis" VARCHAR(255),
	PRIMARY KEY("code_postal_ban_ademe")
);




CREATE TABLE "donnees_geocodage" (
	"id_ban" VARCHAR(255) NOT NULL UNIQUE,
	"lon_ban" DECIMAL,
	"lat_ban" DECIMAL,
	"score_ban_ademe" DECIMAL,
	"statut_geocodage_ademe" TEXT,
	PRIMARY KEY("id_ban")
);




CREATE TABLE "tests_statistiques_dpe" (
	"etiquette_dpe_ademe" VARCHAR(1) NOT NULL UNIQUE,
	"stat_t_student" DECIMAL,
	"p_value_student" DECIMAL,
	"stat_wilcoxon" DECIMAL,
	"p_value_wilcoxon" DECIMAL,
	"sample_size" INTEGER,
	PRIMARY KEY("etiquette_dpe_ademe")
);



ALTER TABLE "donnees_geocodage"
ADD FOREIGN KEY("id_ban") REFERENCES "logements"("id_ban")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "adresses"
ADD FOREIGN KEY("id_ban") REFERENCES "logements"("id_ban")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "donnees_climatiques"
ADD FOREIGN KEY("id_ban") REFERENCES "logements"("id_ban")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "ville"
ADD FOREIGN KEY("code_postal_ban_ademe") REFERENCES "logements"("code_postal_ban_ademe")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "tests_statistiques_dpe"
ADD FOREIGN KEY("etiquette_dpe_ademe") REFERENCES "logements"("etiquette_dpe_ademe")
ON UPDATE NO ACTION ON DELETE NO ACTION;