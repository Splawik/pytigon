ACTIONS =  { 
    'django': { 
        'title': 'Action 1',
        'choices': [
            {   'title': 'title1',
                'values': [
                    '1', '2', '3',
                ]
            },
            {   'title': 'title2',
                'values': [
                    '4', '5', '6',
                ],
            },
            {   'title': 'title3',
                'values': [
                    '4', '5', '6',
                ],
            },
            {   'title': 'title4',
                'values': [
                    '14', '15', '16',
                ],
            },
        ],
        'template': """{{choice.0}}{{choice.1}}{{choice.2}}""",
    }
}
