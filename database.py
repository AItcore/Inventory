import sqlite3


class Database:

    def __init__(self):
        self.comm = sqlite3.connect('inventory.db')
        self.cursor = self.comm.cursor()
        self.create_db()
        self.types = self.get_types()

    def __create_responsible_person(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS responsible_person (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name_responsible_person VARCHAR(128) NOT NULL
                )
                """)
            self.comm.commit()
        except:
            pass

    def __create_type(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS type (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name_type VARCHAR(64) NOT NULL
            )
            """)
            self.comm.commit()
        except Exception:
            pass

    def __create_location(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS location (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            location VARCHAR(128) NOT NULL
            )
            """)
            self.comm.commit()
        except:
            pass

    def __create_characteristic(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS characteristic (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name_characteristic VARCHAR(64) NOT NULL,
            id_type INTEGER,
            FOREIGN KEY (id_type) REFERENCES type(id)
            )
            """)
            self.comm.commit()
        except:
            pass

    def __create_items(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
            id VARCHAR(9) PRIMARY KEY NOT NULL,
            type INTEGER,
            characteristic TEXT,
            serial_number VARCHAR(128),
            location INTEGER,
            responsible_person INTEGER,
            FOREIGN KEY (type) REFERENCES type(id),
            FOREIGN KEY (location) REFERENCES location(id),
            FOREIGN KEY (responsible_person) REFERENCES responsible_person(id)
            )
            """)
            self.comm.commit()
        except:
            pass

    def create_db(self):
        self.__create_type()
        self.__create_characteristic()
        self.__create_location()
        self.__create_responsible_person()
        self.__create_items()

    def get_types(self):
        try:
            return self.cursor.execute("SELECT * FROM type").fetchall()
        except:
            pass

    def get_items(self):
        try:
            return self.cursor.execute("SELECT * FROM items").fetchall()
        except:
            pass

    def get_responsible_person(self):
        try:
            return self.cursor.execute("SELECT * FROM responsible_person").fetchall()
        except:
            pass

    def search_items(self, text, type, location, resPers):
        try:
            if (text, type, location, resPers) == ('', '', '', ''):
                return []
            elif (type, location, resPers) == ('', '', ''):
                item = self.cursor.execute(f"""
                                SELECT * FROM items WHERE id='{text}'
                                """).fetchall()
                if len(item) == 0:
                    item = self.cursor.execute(f"""
                                SELECT * FROM items WHERE characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%'
                                """).fetchall()
                return item
            elif (location, resPers) == ('', ''):
                return self.cursor.execute(f"""
                SELECT * FROM items WHERE type='{str(type)}'
                AND (characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%') 
                """).fetchall()
            elif (type, resPers) == ('', ''):
                return self.cursor.execute(f"""
                SELECT * FROM items WHERE location='{location}'
                AND (characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%') 
                """).fetchall()
            elif (type, location) == ('', ''):
                return self.cursor.execute(f"""
                SELECT * FROM items WHERE responsible_person='{resPers}'
                AND (characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%') 
                """).fetchall()
            elif type == '':
                return self.cursor.execute(f"""
                SELECT * FROM items WHERE (location='{location}' AND responsible_person='{resPers}') 
                AND (characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%') 
                """).fetchall()
            elif location == '':
                return self.cursor.execute(f"""
                SELECT * FROM items WHERE (type='{str(type)}' AND responsible_person='{resPers}') 
                AND (characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%') 
                """).fetchall()
            elif resPers == '':
                return self.cursor.execute(f"""
                SELECT * FROM items WHERE (type='{str(type)}' AND location='{location}') 
                AND (characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%') 
                """).fetchall()
            else:
                return self.cursor.execute(f"""
                SELECT * FROM items WHERE (type='{str(type)}' AND location='{location}' AND responsible_person='{resPers}') 
                AND (characteristic LIKE '%{text}%' OR serial_number LIKE '%{text}%') 
                """).fetchall()
        except Exception as e:
            print(e)
            pass

    def get_location(self):
        try:
            return self.cursor.execute("SELECT * FROM location").fetchall()
        except Exception as e:
            pass

    def insert_item(self, item):
        try:
            self.cursor.execute(f"""
                INSERT INTO items(id, type, characteristic, serial_number, location, responsible_person) 
                VALUES ('{item['id']}','{item['type']}','{item['characteristic']}', '{item['serial_number']}',
                '{item['location']}','{item['responsible_person']}')
                """)
            self.comm.commit()
        except Exception as e:
            print(e)
            pass

    def insert_characteristic(self, name, id_type):
        try:
            self.cursor.execute(f"""INSERT INTO characteristic(name_characteristic, id_type)\
             VALUES ('{name}','{id_type}')""")
            self.comm.commit()
        except:
            pass

    def insert_res_pers(self, name):
        try:
            self.cursor.execute(f"INSERT INTO responsible_person(name_responsible_person) VALUES ('{name}')")
            self.comm.commit()
        except:
            pass

    def insert_location(self, name):
        try:
            self.cursor.execute(f"INSERT INTO location(location) VALUES ('{name}')")
            self.comm.commit()
        except Exception as e:
            pass

    def insert_type(self, name):
        try:
            self.cursor.execute(f"INSERT INTO type(name_type) VALUES ('{name}')")
            self.comm.commit()
        except:
            pass

    def delete_item(self, id):
        try:
            self.cursor.execute(f"DELETE FROM items WHERE id='{id}'")
            self.comm.commit()
        except:
            pass

    def delete_res_pers(self, id):
        try:
            self.cursor.execute(f"DELETE FROM responsible_person WHERE id={id}")
            self.comm.commit()
        except:
            pass

    def delete_location(self, id):
        try:
            self.cursor.execute(f"DELETE FROM location WHERE id={id}")
            self.comm.commit()
        except:
            pass

    def delete_type(self, id_type):
        try:
            self.cursor.executescript(f"""
            DELETE FROM characteristic WHERE id_type={id_type};
            DELETE FROM type WHERE id={id_type};
            """)
            self.comm.commit()
        except:
            pass

    def count_item_type(self, id):
        try:
            return self.cursor.execute(f"SELECT COUNT(*) FROM items WHERE type={id}").fetchone()[0]
        except:
            pass

    def count_item_res_pers(self, id_res_pers):
        try:
            return self.cursor.execute(f"SELECT COUNT(*) FROM items WHERE responsible_person={id_res_pers}").fetchone()[
                0]
        except:
            pass

    def count_item_location(self, id_location):
        try:
            return self.cursor.execute(f"SELECT COUNT(*) FROM items WHERE location={id_location}").fetchone()[0]
        except:
            pass

    def exist_type(self, name):
        try:
            if self.cursor.execute(f"SELECT COUNT(*) FROM type WHERE name_type='{name}'").fetchone()[0] == 1:
                return True
            else:
                return False
        except:
            pass

    def count_type(self):
        try:
            return self.cursor.execute(f"SELECT COUNT(*) FROM type").fetchone()[0]
        except:
            pass

    def count_location(self):
        try:
            return self.cursor.execute(f"SELECT COUNT(*) FROM location").fetchone()[0]
        except:
            pass

    def count_res_pers(self):
        try:
            return self.cursor.execute(f"SELECT COUNT(*) FROM responsible_person").fetchone()[0]
        except:
            pass

    def update_item(self, item):
        try:
            self.cursor.execute(f"""UPDATE items SET characteristic='{item['characteristic']}', 
            serial_number='{item['serial_number']}', location='{item['location']}', 
            responsible_person='{item['responsible_person']}' WHERE id='{item['id']}'""")
            self.comm.commit()
        except:
            pass

    def get_characteristics(self, id_type):
        try:
            return self.cursor.execute(f"SELECT * FROM characteristic WHERE id_type='{id_type}'").fetchall()
        except:
            pass

    def get_type_id(self, type):
        try:
            return self.cursor.execute(f"SELECT id FROM type WHERE name_type='{type}'").fetchone()[0]
        except:
            pass

    def get_location_id(self, location):
        try:
            return self.cursor.execute(f"SELECT id FROM location WHERE location='{location}'").fetchone()[0]
        except:
            pass

    def get_res_pers_id(self, res_pers):
        try:
            return self.cursor.execute(f"SELECT id FROM responsible_person \
                                        WHERE name_responsible_person='{res_pers}'").fetchone()[0]
        except:
            pass

    def get_location_name(self, id):
        try:
            return self.cursor.execute(f"SELECT location FROM location WHERE id={id}").fetchone()[0]
        except:
            pass

    def get_res_pers_name(self, id):
        try:
            return \
                self.cursor.execute(f"SELECT name_responsible_person FROM responsible_person WHERE id={id}").fetchone()[
                    0]
        except:
            pass

    def get_last_item_id(self, id):
        try:
            return self.cursor.execute(f"SELECT count(*) FROM items WHERE id LIKE '%{id}%'").fetchone()[0]
        except Exception as e:
            print(e)
            pass

    def get_item_by_id(self, id):
        try:
            return self.cursor.execute(f"SELECT * FROM items WHERE id='{id}'").fetchall()
        except:
            pass
