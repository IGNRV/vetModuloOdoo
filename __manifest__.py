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

        # === Reportes ===
        'report/sterilization_report.xml',
        'report/visit_report.xml',
        'report/exam_order_report.xml',
        # === NUEVO: Reporte PDF de Vacunación ===
        'report/vaccination_report.xml',

        # === Vistas base ===
        'views/animals_views.xml',
        'views/medicines_views.xml',
        'views/allergies_views.xml',
        'views/surgeries_views.xml',
        'views/vaccines_views.xml',
        'views/visits_views.xml',
        'views/species_views.xml',
        'views/breeds_views.xml',
        'views/tags_views.xml',
        'views/animal_partner_views.xml',

        # Vistas de Seguros
        'views/insurances_views.xml',

        # Vistas de Esterilizaciones
        'views/sterilizations_views.xml',

        # Vistas de Órdenes de Exámenes
        'views/exam_orders_views.xml',

        # === NUEVO: Vistas de REGISTROS de Vacunación ===
        'views/vaccinations_views.xml',

        # Menús
        'views/animals_menus.xml',

        # Secuencias/otros
        'views/visit_sequence.xml',
        'views/animals_identification.xml',
        'views/exam_order_sequence.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "images": [
        "static/images/banner.png",
        "static/description/icon.png",
        "static/src/img/visita_header.png",
        "static/src/img/visita_divider.png",
        "static/src/img/sterilizacion_header.png"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}