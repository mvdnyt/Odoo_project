{
    'name': 'Tourism Management',
    'depends': ['base', 'sale', 'fleet'], 
    'application': True,
    'data': [
        "security/ir.model.access.csv",
        
        # Load Views (and Actions) FIRST
        "views/tourism_package_views.xml",
        "views/tourism_booking_views.xml",
        "views/tourism_package_type_views.xml",
        "views/tourism_package_tag_views.xml",
        "views/res_users_views.xml",
        
        # Load Menus SECOND
        "views/tourism_menus.xml",
    ]
}