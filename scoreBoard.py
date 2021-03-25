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
        self.topScores.clear()
        cursor = self.conn.cursor(buffered=True)
        cursor.execute("SELECT name,score,date FROM hiscores ORDER BY score DESC")

        for x in range(10):
            row = cursor.fetchone()
            if row == None:
                break
            sL = scoreLine(row[0],row[1],row[2])
            self.topScores.append(sL)
            print(row)
        #self.topScores.sort(key= lambda x:x.score, reverse = True)

        cursor.close()

    def close(self):
        self.conn.close()

    def getTopScores(self):
        """TODO: unsure yet, depends on how the graphics handles multi-line strings"""
        return self.topScores

    def addTopScore(self, name="MaXx_2",score=0,date="03/24/2021"):
        if self.connect():
            print(f"attempt to write hiscore:{score}, {self.topScores[-1].score}")
            if score > self.topScores[-1].score:
                
                query = "INSERT INTO hiscores(name,score,date) " \
                        "VALUES(%s,%s,%s)"
                print(query)
                cursor = self.conn.cursor()
                cursor.execute(query,[name,score,date])
                self.conn.commit()
                cursor.close()

                #write new score to DB!
            self.fetchTopScores()
            self.close()
        else:
            pass

    


            
class scoreLine:
    def __init__(self,name:str,score:int,date:str):
        self.name=name
        self.score=score
        self.date=date
