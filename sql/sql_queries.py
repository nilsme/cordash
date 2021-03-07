coronavirus_table_create = ("""
                            CREATE TABLE IF NOT EXISTS coronavirus (
                            date DATE,
                            province VARCHAR,
                            country VARCHAR,
                            lat VARCHAR,
                            long VARCHAR,
                            type VARCHAR,
                            cases NUMERIC);
                            """)

coronavirus_table_drop = "DROP TABLE IF EXISTS coronavirus;"

preview = "SELECT * FROM coronavirus LIMIT 10"

list_tables = ("""
               SELECT table_name 
               FROM information_schema.tables 
               WHERE table_schema='public' AND table_type='BASE TABLE'
               """)

coronavirus_insert = ("""
                     INSERT INTO coronavirus (
                     country,
                     lat,
                     long,
                     date,
                     type,
                     cases)
                     VALUES (%s, %s, %s, %s, %s, %s);
                     """)
