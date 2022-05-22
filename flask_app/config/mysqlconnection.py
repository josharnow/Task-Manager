import pymysql.cursors  # a cursor is the object we use to interact with the database

class MySQLConnection:  # this class will give us an instance of a connection to our database
    def __init__(self, db):
        """Constructor function

        Args:
            db (str): The name of the database passed in from a function in user.py
        """        
        
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
            user = 'root', 
            password = 'root', 
            db = db,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query, data=None):
        """Queries the database

        Args:
            query (str): mySQL query passed in from a function in user.py
            data (dict of {str : str}, optional): Data passed in from a function in user.py. Defaults to None.

        Returns:
            int or list of dict of {str : int, str : str, str : str, str : str, datetime.datetime, datetime.datetime} or bool: Information returned from the mySQL database when a query is performed
        """        
        
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
    
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    """Connects to the specified mySQL database

    Args:
        db (str): The name of the database passed in from a function in user.py

    Returns:
        int or list of dict of {str : int, str : str, str : str, str : str, datetime.datetime, datetime.datetime} or bool: The result of instantiating the MySQLConnection class
    """    
    return MySQLConnection(db)