from pydantic import BaseModel

class InputModel(BaseModel):
    besoin_ecs_ademe: float
    emission_ges_5_usages_par_m2_ademe: float
    emission_ges_chauffage_ademe: float
    emission_ges_ecs_ademe: float
    etiquette_dpe_ademe: int
    etiquette_ges_ademe: int
    periode_construction_ademe: int
    type_energie_generateur_n1_installation_n1_ademe: int
    type_energie_principale_chauffage_ademe: int
    type_energie_principale_ecs_ademe: int
    ubat_w_par_m2_k_ademe: float


model_config = {
    'besoin_ecs_ademe': {
        'min': 0,
        'max': 800,
        'def': 100,
        'dtype': 'float32',
        'desc': 'Besoin ECS annuel total du logement (kWh)'
    },
    'emission_ges_5_usages_par_m2_ademe': {
        'min': 0.0,
        'max': 17.00,
        'def': 5.0,
        'dtype': 'float32',
        'desc': 'Emission GES totale 5 usages rapportée à la surface m2 (kgCO2/an)'
        },
    'emission_ges_chauffage_ademe': {
        'min': 0.0,
        'max': 17.00,
        'def': 5.0,
        'dtype': 'float32',
        'desc': 'Emission GES du chauffage totale (kgCO2/an)'
        },
    'emission_ges_ecs_ademe': {
        'min': 0.0,
        'max': 17.00,
        'def': 5.0,
        'dtype': 'float32',
        'desc': 'Emission GES ECS totale (kgCO2/an)'
        },
    'etiquette_ges_ademe': {
        'min': 1,
        'max': 7,
        'def': 5,
        'dtype': 'int32',
        'mapping': {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'NA': -1},
        'desc': 'Etiquette GES'
        },
    'etiquette_dpe_ademe': {
        'min': 1,
        'max': 7,
        'def': 3,
        'dtype': 'int32',
        'mapping': {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'NA': -1},
        'desc': 'Etiquette DPE'
        },
    'periode_construction_ademe': {
        'min': 1,
        'max': 7,
        'dtype': 'int32',
        'mapping': {'avant 1948': 1, '1948-1974': 2, '1975-1977': 3, '1978-1982': 4, '1983-1988': 5, '1989-2000': 6, '2001-2005': 7, '2006-2012': 8, '2013-2021': 9, 'après 2021': 10, 'NA': -1},
        'desc': 'Période de construction du logement'
        },
    'type_energie_generateur_n1_installation_n1_ademe': {
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
            'Non affecté': 12,
            'NA': 12,
            },
        'desc': "Type d'énergie principale consommée par les installations du logement"
        },
    'type_energie_principale_chauffage_ademe': {
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
            'Non affecté': 12,
            'NA': 12,
            },
        'desc': "Type d'énergie principale pour le chauffage"
        },
    'type_energie_principale_ecs_ademe': {
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
            'Non affecté': 12,
            'NA': 12,
            },
        'desc': "Type d'énergie principale consommée pour les besoins ECS"
        },
    'ubat_w_par_m2_k_ademe': {
            'min': 0.0,
            'max': 25.43,
            'def': 1.059,
            'dtype': 'float32',
            'desc': "Coeff. de déperdition thermique du bâtiment (W/m2/Kelvin)"
            },
    'surface_habitable_logement_ademe': {
        'min': 4,
        'max': 1000,
        'def': 50,
        'dtype': 'float32',
        'desc': 'Surface habitable du logement'
    }
}