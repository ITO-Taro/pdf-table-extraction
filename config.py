COLUMNS = [
    'condition',
    'explanation',
    'category',
    'groups',
    '17_19_Co',
    '17_19_Co_95',
    '17_19_Co_CI',
    '17_19_St',
    '17_19_St_95',
    '17_19_St_CI',
    '16_Co',
    '19_Co_St_sig',
    '16_Co_Co_sig',
]

TABLE_SETTINGS = {
    'condition_description': {
        "explicit_horizontal_lines": [45, 80],
        "explicit_vertical_lines": [35, 550],
    },

    'main': {
        "explicit_horizontal_lines": [45],
        "explicit_vertical_lines": [35, 150, 255, 300, 330 ,360, 405, 435, 470, 555],
    },

    'county_name': {
        "explicit_horizontal_lines": [30, 47],
        "explicit_vertical_lines": [470, 550],
    },
}

FIRST_COL_VALS = [
    'ALL',
    'SEX',
    'RACE/ETHNICITY',
    'SEX BY RACE/ETHNICITY',
    'AGE GROUP',
    'EDUCATION LEVEL',
    'ANNUAL INCOME',
    'MARITAL STATUS',
]

ROW_IGNORE = '2017-2019'