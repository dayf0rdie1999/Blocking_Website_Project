import mysql.connector


def main():
    mydb = UserDB()
    mydb.Clear_Data()



class UserDB():
    def __init__(self):
        self.mydb = mysql.connector.connect(host="localhost", user="root", passwd="Relive19$", database="websites")
        self.mycursor = self.mydb.cursor()
        self.arrayData = None
        self.data = []

    def insertURL(self, URL):
        sqlform = "INSERT INTO porn(URL) VALUES (\""+URL+"\")"
        self.mycursor.execute(sqlform)
        self.mydb.commit()

    def insertURL_multiple(self, URL_List):
        for URL in URL_List:
            sqlform = "INSERT INTO porn(URL) VALUES (\""+URL+"\")"
            self.mycursor.execute(sqlform)

        self.mydb.commit()

    def readURL(self):
        self.data.clear()
        self.mycursor.execute("SELECT * FROM porn")
        self.arrayData = self.mycursor.fetchall()
        for x in self.arrayData:
            for a in x:
                self.data.append(a)

    def printUser(self):
        for row in self.arrayData:
            print(row)

    def Clear_Data(self):
        self.readURL();
        if len(self.data) > 0:
            sqlForm = "DELETE FROM porn";
            self.mycursor.execute(sqlForm)
            self.mydb.commit()
        elif len(self.data) == 0:
            pass

    # Don't need to update
    #def updateURL(self, URL):
        #sqlForm = "UPDATE user SET URL= %s WHERE URL= %s"
        #user = URL
        #self.mycursor.execute(sqlForm, user)
        #self.mydb.commit()

    def deleteURL(self, URL):
        sqlForm = "DELETE FROM porn WHERE URL = \""+URL+"\" "
        self.mycursor.execute(sqlForm)
        self.mydb.commit()

    def checkURL(self, URL):
        self.readURL()
        for row in self.arrayData:
            if row[0] == URL:
                return True
            else:
                pass
        return False


if __name__ == "__main__":
    main()