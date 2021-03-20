{
    "name" : "Group Expand Buttons",
    "category": "Hidden",
    "version" : '1.0',
    "author" : 'OpenERP SA',
    "description":
        """
A group by list can be expanded and collapased with buttons
===============================================================
You'll see two buttons appear on top right corner of the list when you perform a group by with which you can expand and collapse grouped records by level.
        """,
    "depends" : ["web"],
    "data": ['view.xml'],
    'qweb' : ["static/src/xml/expand_buttons.xml"],
    'installable': True,
    'auto_install': False,
}

