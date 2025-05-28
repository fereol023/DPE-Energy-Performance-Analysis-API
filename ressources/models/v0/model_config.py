model_config = {
    'apports_solaires_saison_chauffe_ademe': {
        'min': 0.0,
        'max': 1_500,
        'def': 150,
        'dtype': 'float32',
        'desc': 'Apports solaires totaux durant la saison de chaude (kWh)'
    },
    'besoin_chauffage_ademe': {
        'min': 0.4,
        'max': 8_000,
        'def': 342,
        'dtype': 'float32',
        'desc': 'Besoin de chauffage annuel total du logement ou immeuble (kWh)'
    },
    'conso_5_usages_e_finale_energie_ndeg2_ademe': {
        'min': 0.7,
        'max': 1_000,
        'def': 437, 
        'dtype': 'float32',
        'desc': 'Consommation annuelle finale 5 usages (kwh/an)'
    },
    'conso_5_usages_m2_e_finale_ademe': {
        'min': 0.5,
        'max': 7_690.9,
        'def': 78,
        'dtype': 'float32',
        'desc': 'Conso. annuelle finale 5 usages par m2 (kwh/an/m2)'
    },
    'conso_5_usages_par_m2_e_primaire_ademe': {
        'min': 13.9,
        'max': 8_083.9,
        'def': 180,
        'dtype': 'float32',
        'desc': 'Conso. annuelle primaire 5 usages (kwh/an)'
    },
    'conso_auxiliaires_e_primaire_ademe': {
        'min': 0.0,
        'max': 8_517.8,
        'def': 339,
        'dtype': 'float32',
        'desc': "Conso. de l'ensemble des auxiliaires en energie primaire (kwh/an)"
    },
    'conso_e_finale_depensier_installation_ecs_ademe': {
        'min': 0.0,
        'max': 3_039.2,
        'def': 1_500.8,
        'dtype': 'float32',
        'desc': "Conso. de chauffage en energie primaire pour le scénario dépensier (kWh/an)"
    },
    'conso_ecs_depensier_e_primaire_ademe': {
        'min': 0.0,
        'max': 3_039.2,
        'def': 2760,
        'dtype': 'float32',
        'desc': "Conso. d'ECS en énergie primaire pour le scénario dépensier (kWh/an)"
    },
    'conso_ecs_e_finale_energie_ndeg2_ademe': {
        'min': 0.0,
        'max': 605.4,
        'def': 0,
        'dtype': 'float32',
        'desc': "Conso. d'ecs en énergie finale pour la source d'énergie considérée (kWh/an)"
    },
    'consommation_annuelle_totale_de_l_adresse_mwh_enedis_with_ban': {
        'min': 2.166,
        'max': 1_218.589,
        'def': 85.1,
        'dtype': 'float32',
        'desc': "Conso. annuelle totale de l'adresse (mWh)"
    },
    'cout_auxiliaires_ademe': {
        'min': 0.0,
        'max': 287.0,
        'def': 51.2,
        'dtype': 'float32',
        'desc': "Coût des auxilliaires de l'ensemble des auxiliaires (€)"
    },
    'deperditions_baies_vitrees_ademe': {
        'min': 0.0,
        'max': 58.0,
        'def': 3.09,
        'dtype': 'float32',
        'desc': 'Déperdition par les baies vitrées (W/K)'
    },
    'deperditions_planchers_hauts_ademe': {
        'min': 0.0,
        'max': 130.001,
        'def': 0,
        'dtype': 'float32',
        'desc': 'Déperdition par les baies vitrées (W/K)'
    },
    'emission_ges_5_usages_energie_ndeg2_ademe': {
        'min': 0.0,
        'max': 166.49,
        'def': 27.7,
        'dtype': 'float32',
        'desc': 'Estimation GES totale 5 usages (kgCO2/an)'
        },
    'emission_ges_5_usages_par_m2_ademe': {
        'min': 0.0,
        'max': 17.00,
        'def': 5.0,
        'dtype': 'float32',
        'desc': 'Estimation GES totale 5 usages rapportée à la surface m2 (kgCO2/an)'
        },
    'etiquette_dpe_ademe': {
        'min': 1,
        'max': 7,
        'dtype': 'int32',
        'mapping': {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'NA': -1},
        'desc': 'Etiquette DPE'
        },
    'surface_habitable_logement_ademe': {
        'min': 2,
        'max': 1_500.0,
        'def': 22.2,
        'dtype': 'float32',
        'desc': 'Surface totale habitable du logement (m2)'
        },
    'type_energie_generateur_ndeg1_installation_ndeg1_ademe': {
        'min': 1,
        'max': 12,
        'dtype': 'int32',
        'mapping': {
            'Gaz naturel': 1,
            'Électricité': 2,
            'Fioul domestique': 3,
            'Réseau de Chauffage urbain': 4,
            'GPL': 5,
            'Bois – Bûches': 6,
            'Propane': 7,
            'Bois – Plaquettes forestières': 8,
            'Butane': 9,
            'Charbon': 10,
            'Bois – Granulés (pellets) ou briquettes': 11,
            'NA': 12,
            },
        'desc': "Type d'énergie consommée par le générateur de chauffage"
        },
    'type_energie_ndeg1_ademe': {
        'min': 1,
        'max': 11,
        'dtype': 'int32',
        'mapping': {
            'Gaz naturel': 1,
            'Électricité': 2,
            'Fioul domestique': 3,
            'Réseau de Chauffage urbain': 4,
            'GPL': 5,
            'Bois – Bûches': 6,
            'Butane': 7,
            'Charbon': 8,
            'Bois – Granulés (pellets) ou briquettes': 9,
            'Propane': 10,
            'Réseau de Froid Urbain': 11,
            'NA': -2
            },
        'desc': "Type énergie 1 du logement"
        },
    'type_energie_ndeg2_ademe': {
        'min': 1,
        'max': 12,
        'dtype': 'int32',
        'mapping': {
            'Électricité': 1,      
            'Gaz naturel': 2,                                                    
            'Réseau de Chauffage urbain': 3,                                      
            'Bois – Bûches': 4,                                                  
            'Fioul domestique': 5,                                                
            'GPL': 6,                                                             
            "Électricité d'origine renouvelable utilisée dans le bâtiment": 7,    
            'Bois – Plaquettes d’industrie': 8,                                   
            'Bois – Granulés (pellets) ou briquettes': 9,                          
            'Bois – Plaquettes forestières': 10,                                  
            'Réseau de Froid Urbain': 11,                                         
            'NA': 12                                                            
            },
        'desc': 'Type énergie 2 du logement'
        },
    'type_installation_ecs_general_ademe': {
        'min': 1,
        'max': 4,
        'dtype': 'int32',
        'mapping': {
            'individuel': 1,
            'collectif': 2,              
            'mixte (collectif-individuel)': 3,
            'NaN': 4
            },
        'desc': 'Type énergie eau chaude sanitaire'
        },
    'ubat_w_m2_k_ademe': {
        'min': 0.0,
        'max': 25.43,
        'def': 1.059,
        'dtype': 'float32',
        'desc': "Coeff. de déperdition thermique du bâtiment (W/m2/Kelvin)"
        },
    'usage_generateur_ecs_ndeg1_ademe': {
        'min': 1,
        'max': 4,
        'dtype': 'int32',
        'mapping': {
            'chauffage + ecs': 1,
            'ecs': 2, 
            'chauffage': 3,
            'NA': 4
            },
        'desc': 'Usage du générateur ECS'
        },
    'volume_stockage_generateur_ecs_ndeg1_ademe': {
        'min': 0.0,
        'max': 65.0,
        'def': 65,
        'dtype': 'float32',
        'desc': "Volume de stockage associé au générateur d'ECS"
        }
}