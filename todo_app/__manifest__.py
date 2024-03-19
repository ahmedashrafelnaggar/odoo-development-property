{
    'name': " To_Do App ",
    'version': '17.0.0.1.0',
    'depends': ['base','mail',
                ],
    'author': "Ahmad EL Naggar ",
    'category': '',
    # data files always loaded at installation and all files xml and csv write here
    'data': [

        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'reports/todo_task_report.xml',

    ],

    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    'application':True,

}
