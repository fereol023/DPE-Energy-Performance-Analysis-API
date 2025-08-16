--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: adresses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.adresses (
    id_ban character varying(255) NOT NULL,
    full_adress_ban text,
    label_ban text,
    complement_d_adresse_batiment_ademe text,
    complement_d_adresse_logement_ademe text
);


ALTER TABLE public.adresses OWNER TO postgres;

--
-- Name: donnees_climatiques; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.donnees_climatiques (
    id_ban character varying(255) NOT NULL,
    zone_climatique_ademe character varying(255)
);


ALTER TABLE public.donnees_climatiques OWNER TO postgres;

--
-- Name: donnees_geocodage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.donnees_geocodage (
    id_ban character varying(255) NOT NULL,
    lon_ban numeric,
    lat_ban numeric,
    score_ban_ademe numeric,
    statut_geocodage_ademe text
);


ALTER TABLE public.donnees_geocodage OWNER TO postgres;

--
-- Name: logements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logements (
    batch_id character varying(255) NOT NULL,
    _id_ademe character varying(255) NOT NULL,
    id_ban character varying(255) NOT NULL,
    apports_solaires_saison_chauffe_ademe numeric,
    besoin_chauffage_ademe numeric,
    conso_5_usages_par_m2_ef_ademe numeric,
    conso_5_usages_par_m2_ep_ademe numeric,
    conso_auxiliaires_ep_ademe numeric,
    conso_chauffage_ep_ademe numeric,
    conso_ef_installation_ecs_n1_ademe numeric,
    conso_ecs_depensier_e_primaire_ademe numeric,
    conso_kwh_m2 numeric,
    cout_auxiliaires_ademe numeric,
    deperditions_baies_vitrees_ademe numeric,
    deperditions_planchers_hauts_ademe numeric,
    emission_ges_5_usages_energie_ndeg2_ademe numeric,
    emission_ges_5_usages_par_m2_ademe numeric,
    etiquette_dpe_ademe character varying(1),
    etiquette_ges_ademe character varying(1),
    qualite_isolation_menuiseries_ademe character varying(255),
    type_energie_ndeg2_ademe character varying(255),
    type_installation_ecs_general_ademe character varying(255),
    ubat_w_m2_k_ademe numeric,
    usage_generateur_ecs_ndeg1_ademe character varying(255),
    usage_generateur_ndeg1_installation_ndeg1_ademe character varying(255),
    volume_stockage_generateur_ecs_ndeg1_ademe numeric,
    code_postal_ban_ademe character varying(255),
    absolute_diff_conso_prim_fin numeric,
    absolute_diff_conso_fin_act numeric,
    periode_construction_ademe character varying(255)
);


ALTER TABLE public.logements OWNER TO postgres;

--
-- Name: tests_statistiques_dpe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tests_statistiques_dpe (
    batch_id character varying(255) NOT NULL,
    etiquette_dpe_ademe character varying(1) NOT NULL,
    sample_size integer,
    paired_t_test_t_statistic numeric,
    paired_t_test_p_value numeric,
    wilcoxon_statistic numeric,
    wilcoxon_p_value numeric
);


ALTER TABLE public.tests_statistiques_dpe OWNER TO postgres;

--
-- Name: villes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.villes (
    code_postal_ban_ademe character varying(255) NOT NULL,
    city_ban text,
    code_departement_enedis character varying(255)
);


ALTER TABLE public.villes OWNER TO postgres;

--
-- Name: adresses adresses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adresses
    ADD CONSTRAINT adresses_pkey PRIMARY KEY (id_ban);


--
-- Name: donnees_climatiques donnees_climatiques_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.donnees_climatiques
    ADD CONSTRAINT donnees_climatiques_pkey PRIMARY KEY (id_ban);


--
-- Name: donnees_geocodage donnees_geocodage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.donnees_geocodage
    ADD CONSTRAINT donnees_geocodage_pkey PRIMARY KEY (id_ban);


--
-- Name: logements logements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logements
    ADD CONSTRAINT logements_pkey PRIMARY KEY (_id_ademe);


--
-- Name: tests_statistiques_dpe tests_statistiques_dpe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tests_statistiques_dpe
    ADD CONSTRAINT tests_statistiques_dpe_pkey PRIMARY KEY (batch_id, etiquette_dpe_ademe);


--
-- Name: villes villes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.villes
    ADD CONSTRAINT villes_pkey PRIMARY KEY (code_postal_ban_ademe);


--
-- Name: logements logements_batch_id_etiquette_dpe_ademe_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logements
    ADD CONSTRAINT logements_batch_id_etiquette_dpe_ademe_fkey FOREIGN KEY (batch_id, etiquette_dpe_ademe) REFERENCES public.tests_statistiques_dpe(batch_id, etiquette_dpe_ademe) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: logements logements_code_postal_ban_ademe_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logements
    ADD CONSTRAINT logements_code_postal_ban_ademe_fkey FOREIGN KEY (code_postal_ban_ademe) REFERENCES public.villes(code_postal_ban_ademe) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: logements logements_id_ban_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logements
    ADD CONSTRAINT logements_id_ban_fkey FOREIGN KEY (id_ban) REFERENCES public.donnees_geocodage(id_ban) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: logements logements_id_ban_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logements
    ADD CONSTRAINT logements_id_ban_fkey1 FOREIGN KEY (id_ban) REFERENCES public.adresses(id_ban) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: logements logements_id_ban_fkey2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logements
    ADD CONSTRAINT logements_id_ban_fkey2 FOREIGN KEY (id_ban) REFERENCES public.donnees_climatiques(id_ban) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

