# By Atman Boulaajaili
# https://github.com/elon-fask


{
    "name": "Manage Sessions",
    "version": "18.0.1.0",
    "license": "LGPL-3",
    "category": "Education",
    "sequence": 3,
    "summary": "Manage Sessions",
    "complexity": "easy",
    "author": "Atman Boulaajaili",
    "website": "https://github.com/elon-fask",
    "depends": ["manage-students"],
    "data": [
        "security/ir.model.access.csv",
        "views/session_view.xml",
        "menus/op_menu.xml",
        "security/security.xml",
    ],
    # "demo": [
    #     "demo/session_demo.xml"
    # ,
    # "demo/facility_line_demo.xml"
    # ],
    "images": [
        "static/description/icon-session.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
