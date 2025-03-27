import mysql.connector
from mysql.connector import Error


class MySQLConnection:
    _instance = None

    def __new__(cls, host='localhost', port=3306, user='root', password='', database='testdb'):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
            cls._instance._connection = None
            cls._instance._host = host
            cls._instance._port = port
            cls._instance._user = user
            cls._instance._password = password
            cls._instance._database = database
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        try:
            self._connection = mysql.connector.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database
            )
            if self._connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self._connection = None

    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            self._connect()
        return self._connection

    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("MySQL connection closed")
            self._connection = None
            MySQLConnection._instance = None

    def get_cursor(self):
        """Lấy cursor với dictionary=True để trả về kết quả dạng dict"""
        if self._connection is None or not self._connection.is_connected():
            self._connect()
        return self._connection.cursor(dictionary=True)


# check connection
if __name__ == "__main__":
    db = MySQLConnection(
        host="123.31.12.175",
        user="rd_user",
        password="rduser@123",
        database="RD"
    )
    connection = db.get_connection()
    print(connection)

    cursor = db.get_cursor()
    cursor.execute("SELECT * FROM experience LIMIT 5;")
    results = cursor.fetchall()
    for row in results:
        print(row)
    db.close_connection()
