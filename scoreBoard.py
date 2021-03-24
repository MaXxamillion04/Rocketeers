from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

class scoreBoard:
    def __init__(self):
        self.conn=None
        self.topScores=[]
        if self.connect():
            self.fetchTopScores()
        else:
            print("Unable to connect to database")
            self.topScores = ["Unable to connect to database"]
        self.close()

    def connect(self) -> bool:
        """connect to mySQL database for hiscore retrieval"""
        db_config = read_db_config()
        try:
            print("Connecting to database...")
            self.conn =MySQLConnection(**db_config)
            return self.conn.is_connected()
                
        except Error as error:
            print(error)
            return False
    
    def fetchTopScores(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name,score,date FROM hiscores ORDER BY score DESC")

        for x in range(10):
            row = cursor.fetchone()
            if row == None:
                break
            sL = scoreLine(row[0],row[1],row[2])
            print(row)

        cursor.close()

    def close(self):
        self.conn.close()

    def getTopScores():
        """this will return the scoreboard paragraph actually"""
        """TODO: unsure yet, depends on how the graphics handles multi-line strings"""
        return self.topScores

    def addTopScore(name:str,score:int,date:str):
        pass

    


            
class scoreLine:
    def __init__(self,name:str,score:int,date:str):
        self.name=name
        self.score=score
        self.date=date
