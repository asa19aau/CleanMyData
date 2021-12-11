DATA_CHOICES = [
    ('non', 'None'),
    ('Temperature', (
            ('C', 'Celsius'),
            ('F', 'Fahrenheit'),
            ('K', 'Kelvin'),
        )
    ),
    ('Distance', (
            ('KM', 'Kilometer'),
            ('MI', 'Mile'),
        )
    ),
    ('Weight', (
            ('KG', 'Kilogram'),
            ('LB', 'Pound')
        )
    ),
]


NULL_CHOICES_NUM = [
    ('nothing', 'Nothing'),
    ('remove-tuples', 'Remove tuples'),

    # Replace
    ('Avg', 'Average'),
    ('Med', 'Median'),
    ('Min', 'Minimum'),
    ('Max', 'Maximum'),
    ('Cus', 'Custom value'),
]


NULL_CHOICES_STRING = [
    ('nothing', 'Nothing'),
    ('remove-tuples', 'Remove tuples'),

    # Replace
    ('Cus', 'Custom string'),

]


NULL_CHOICES_DATE = [
    ('nothing', 'Nothing'),
    ('remove-tuples', 'Remove tuples'),

    # Replace
    ('Now', 'Current date'),
    ('Cus', 'Custom date'),
]

#The files types allowed to be uploaded
valid_extensions = ['.csv', '.json', '.tsv', '.xml', '.yaml']