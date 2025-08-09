# -*- coding: utf-8 -*-
{
    'name': "Veterinary management",

    'summary': "Manage the animals that visit our veterinarian",

    'description': """
Manage the animals that visit our veterinarian
    """,

    'author': "Javier Diez",
    'website': "https://javierdiez.netlify.app/",
    'license': 'AGPL-3',
    'category': 'Animales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # === Reportes (deben cargarse ANTES de las vistas que referencian sus acciones) ===
        'report/sterilization_report.xml',
        'report/visit_report.xml',          # <-- acción + plantilla PDF de Visitas

        # === Vistas base ===
        'views/animals_views.xml',
        'views/medicines_views.xml',
        'views/allergies_views.xml',
        'views/surgeries_views.xml',
        'views/vaccines_views.xml',
        'views/insurances_views.xml',
        'views/visits_views.xml',           # <-- ahora viene DESPUÉS del reporte
        'views/species_views.xml',
        'views/breeds_views.xml',
        'views/tags_views.xml',
        'views/animal_partner_views.xml',

        # IMPORTANTE: acción de Esterilizaciones ya está arriba; aquí la vista que la usa
        'views/sterilizations_views.xml',

        # Menús (usa acciones ya definidas arriba)
        'views/animals_menus.xml',

        # Secuencias/otros
        'views/visit_sequence.xml',
        'views/animals_identification.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "images": ['static/images/banner.png', 'static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
