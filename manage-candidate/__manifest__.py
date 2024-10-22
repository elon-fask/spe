# By Atman Boulaajaili
# https://github.com/elon-fask

{
    "name": "Manage Candidate",
    "version": "18.0.1.0",
    "license": "LGPL-3",
    "category": "Education",
    "sequence": 1,
    "summary": "Manage Candidate",
    "complexity": "easy",
    "author": "Atman Boulaajaili",
    "website": "https://github.com/elon-fask",
    "depends": ["mail", "base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/candidate_view.xml",
        "views/candidate_session_view.xml",
        "views/session_view.xml",
        "views/application_view.xml",
        "menu/core_menu.xml",
    ],
    "demo": [],
    "images": ["static/description/icon-crane.png"],
    "installable": True,
    "auto_install": False,
    "application": True,
}
