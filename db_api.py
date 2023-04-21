import psycopg2

db_name = "railway"
db_user = "postgres"
db_password = "Q9KQON3sAe744O7b0fRD"
db_host = "containers-us-west-48.railway.app"
db_port = "7276"

db_connection_config = {
    "dbname": db_name,
    "password": db_password,
    "user": db_user,
    "port": db_port,
    "host": db_host
}


class DataBaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def set_connection(self):
        self.connection = psycopg2.connect\
            (
                f"""
                    dbname={self.config['dbname']}
                    user={self.config['user']}
                    password={self.config['password']}
                    host={self.config['host']}
                    port={self.config['port']}
                """
            )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()


class PostgresDataBaseManager(DataBaseManager):

    def add_user(self, user):
        self.set_connection()
        sql_add_user = \
            f"""
                INSERT INTO users(user_id, username, first_name) 
                VALUES('{user.id}', '{user.username}', '{user.first_name}')
            """
        self.cursor.execute(sql_add_user)
        self.connection.commit()
        self.close_connection()

    def get_user(self, user):
        self.set_connection()
        sql_get_user = f"SELECT * FROM users WHERE user_id = '{user.id}'"
        self.cursor.execute(sql_get_user)
        result = self.cursor.fetchall()
        self.close_connection()
        return result

    def get_all_users(self):
        self.set_connection()
        sql_get_user = f"SELECT * FROM users"
        self.cursor.execute(sql_get_user)
        result = self.cursor.fetchall()
        self.close_connection()
        return result

    def check_user(self, user):
        user_data = self.get_user(user)
        if not user_data:
            self.add_user(user=user)
