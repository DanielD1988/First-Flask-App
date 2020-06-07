import mysql.connector

class UseDatabase:

    def __init__(self,config: dict) -> 'none':
        self.configuration = config

    def __enter__(self) -> 'Cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, exc_trace) -> 'none':
        self.conn.commit()
        self.cursor.close
        self.conn.close()

