from configparser import ConfigParser
from psycopg2 import connect, DatabaseError


class base:
    def init(self):
        pass

    def term(self):
        pass

    def getConnString(
        self,
        filename="/home/u/idapro-7.7/plugins/local_types/localTypes.toml",
        section="database",
        param="connection_info",
    ) -> dict:
        parser = ConfigParser()
        parser.read(filename)
        connString = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                connString[param[0]] = param[1]
        else:
            raise Exception(
                "Section {0} not found in the {1} file".format(section, filename)
            )
        return connString

    def insertIntoDB(self, type_name: str, typedef: str, file_path: str) -> None:
        conn = None
        try:
            params = self.getConnString()
            print("Connecting to the PostgreSQL database...")
            conn = connect(**params)
            cur = conn.cursor()
            req = (
                "INSERT INTO types (file_path, typedef, name) VALUES ('"
                + file_path
                + "', '"
                + typedef
                + "', '"
                + type_name
                + "');"
            )
            print(req)
            cur.execute(req)
            conn.commit()
            cur.close()
        except (Exception, DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("Database connection closed.")

    def getTypedefFromDB(self, type_name: str) -> str:
        conn = None
        try:
            params = self.getConnString()
            print("Connecting to the PostgreSQL database...")
            conn = connect(**params)
            cur = conn.cursor()
            req = "SELECT typedef FROM types WHERE name='" + type_name + "';"
            print(req)
            cur.execute(req)
            r = cur.fetchone()[0]
            cur.close()
            return r
        except (Exception, DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("Database connection closed.")
