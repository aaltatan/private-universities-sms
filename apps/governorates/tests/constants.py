DIRTY_DATA = [
    {
        "data": {
            "name": "Ha",
            "description": "google",
            "save": "true",
        },
        "error": "the field must be at least 4 characters long",
    },
    {
        "data": {
            "name": "",
            "description": "",
            "save": "true",
        },
        "error": "This field is required.",
    },
    {
        "data": {
            "name": "a" * 265,
            "description": "",
            "save": "true",
        },
        "error": "Ensure this value has at most 255 characters (it has 265).",
    },
    {
        "data": {
            "name": "Governorate 1",
            "description": "google",
            "save": "true",
        },
        "error": "Governorate with this Name already exists.",
    },
]