{
    'name': 'Tourism Vehicle Management',
    'depends': ['base', 'mail'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/tourism_vehicle_views.xml',
        'views/tourism_vehicle_type_views.xml',
        'views/tourism_trip_views.xml',
        'views/tourism_menus.xml',
    ]
}
