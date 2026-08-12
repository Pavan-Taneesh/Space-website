-- Seven fixed categories, per project spec
INSERT INTO categories (name, color_hex) VALUES
    ('Space Stations', '#FFD700'),
    ('Navigation',      '#00BFFF'),
    ('Communication',   '#FF6347'),
    ('Weather',         '#32CD32'),
    ('Scientific',      '#9370DB'),
    ('Rocket Bodies',   '#FF8C00'),
    ('Space Debris',    '#808080');

-- Known data sources
INSERT INTO sources (name, url) VALUES
    ('CelesTrak',   'https://celestrak.org'),
    ('Space-Track', 'https://www.space-track.org'),
    ('SatNOGS',     'https://satnogs.org'),
    ('ESA DISCOS',  'https://discosweb.esoc.esa.int');