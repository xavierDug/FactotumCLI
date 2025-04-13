from questionary import Style

custom_style = Style([
    ('qmark', 'fg:#00c0ff bold'),     # Question mark
    ('question', 'bold'),             # Question text
    ('answer', 'fg:#00c0ff bold'),    # User's answer
    ('pointer', 'fg:#00c0ff bold'),   # Pointer for select
    ('highlighted', 'fg:#00c0ff bold'), # Highlighted choice
    ('selected', 'fg:#00ff00'),       # Style for a selected item
    ('separator', 'fg:#4AF626'),
    ('instruction', ''),              # User instructions
    ('text', ''),                     # Plain text
    ('disabled', 'fg:#858585 italic') # Disabled choices
])