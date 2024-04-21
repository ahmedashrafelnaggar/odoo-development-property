{
    'name': " Hospital Managment",
    'version': '17.0.0.1.0',
    'depends': ['base','mail','website','board',
                ],
    'sequence':-100,
    'author': "Ahmad EL Naggar ",
    'category': 'Hospital',
    'summary': 'Hospital management system',
    'description':""" Hospital management system""" ,
    # data files always loaded at installation and all files xml and csv write here
    'data': [

        'security/security.xml',
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/sequence_data.xml',
        'data/patient.tag.csv',
        'data/appointment_email_template.xml',
        'wizard/cancel_appointment_wizard.xml',
        'views/base_menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/patient_tag_view.xml',
        'views/odoo_playground_view.xml',
        'views/dashboard.xml',
        # 'views/template_controller_patient.xml',
        # 'views/res_config_settings_view.xml',
        'reports/patient_report.xml',
        'reports/appointment_report.xml',


    ],

      'assets':{
          # if for model to do css for it you put it in 'web.assets_backend'
        # 'web.assets_backend':['app_one/static/src/css/property.css'],
        # 'web.assets_backend':['app_one/static/src/css/building.css'],
        #   you take absoulut pathe then start from name of your app /om_hospital/static/src/css/font.css
        'web.report_assets_common':['/om_hospital/static/src/css/font.css'],
    },

    # data files containing optionally loaded demonstration data
    'images': ['/static/description/icon.png'],
    'demo': [],
    'application':True,
    'auto_install':False,
    'license':'LGPL-3',
}
