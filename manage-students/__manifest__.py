{
    "name": "Manage Students",
    "version": "18.0.0.0",
    "license": "LGPL-3",
    "category": "Education",
    "sequence": 1,
    "summary": "Manage Students",
    "complexity": "easy",
    "author": "Atman Boulaajaili",
    "website": "https://github.com/elon-fask",
    "description": """Manage Students""",
    "depends": ["base", "mail"],
    "data": [
        # "views/student_view.xml",
        "security/ir.model.access.csv",
        "views/op_student_views.xml",
        "menu/manage_student_menu.xml",
        # "menu/student_menu.xml"
        # "views/op_course_views.xml"
    ],
    "demo": [],
    "images": [
        "static/description/icon.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
