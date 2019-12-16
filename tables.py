import psycopg2 as dbapi2
from datetime import datetime

url = "postgres://ysgegrjn:ootmjPwTp-y8BaY1tPlyaVy-vTxDJDm_@rajje.db.elephantsql.com:5432/ysgegrjn"

class database:
    def __init__(self):
        self.is_a_try = 1

    def delete_all(self):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """
                    DROP TABLE COMMENTS;
                    DROP TABLE ESSAYS;
                    DROP TABLE ANNOUNCEMENTS;
                    DROP TABLE PERSON;
                    DROP TABLE EARTHQUAKES;
                    DROP TABLE OLD_EARTHQUAKES; 
                    """
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        connection.close()
        return


    def create_tables(self):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        # old earthquake tables will be added
        statement = """CREATE TABLE PERSON(
                            PERSON_ID SERIAL PRIMARY KEY,
                            NAME VARCHAR(50),
                            PASSWORD VARCHAR(1000),
                            TYPE VARCHAR(6),
                            PERSON_DATE DATE
                        );
                    CREATE TABLE COMMENTS(
                            COMMENT_ID SERIAL PRIMARY KEY,
                            COMMENT_WHICH_ID INTEGER REFERENCES PERSON(PERSON_ID),
                            COMMENT VARCHAR(100000),
                            COMMENT_TOPIC VARCHAR(1000),
                            COMMENT_DATE DATE  
                        );
                        CREATE TABLE ESSAYS(
                            ESSAY_ID SERIAL PRIMARY KEY,
                            ESSAY_WHICH_ID INTEGER REFERENCES PERSON(PERSON_ID),
                            ESSAY_HEADER VARCHAR(1000),
                            ESSAY VARCHAR(10000000),
                            ESSAY_DATE DATE
                        );    
                        CREATE TABLE ANNOUNCEMENTS(
                            ANNOUNCEMENT_ID SERIAL PRIMARY KEY,
                            ANNOUNCEMENT_HEADER VARCHAR(1000),
                            ANNOUNCEMENT VARCHAR(1000000),
                            ANNOUNCEMENT_WHICH_ID INTEGER REFERENCES PERSON(PERSON_ID),
                            ANNOUNCEMENT_DATE DATE         
                        );
                        CREATE TABLE EARTHQUAKES(
                            EVENTID SERIAL PRIMARY KEY,
                            AGENCY VARCHAR(100),
                            DATE_TIME VARCHAR(100),
                            LATITUDE FLOAT,
                            LONGITUDE FLOAT,
                            DEPTH FLOAT,
                            RMS FLOAT,
                            KIND VARCHAR(100),
                            MAGNITUDE FLOAT,
                            COUNTR VARCHAR(100),
                            CITY VARCHAR(100),
                            VILLAGE VARCHAR(100),
                            OTHER1 VARCHAR(100),
                            OTHER2 VARCHAR(100),
                            OTHER3 VARCHAR(100)
                        );
                        CREATE TABLE OLD_EARTHQUAKES(
                            EARTHQUAKE_ID NUMERIC PRIMARY KEY,
                            TIMEUTC VARCHAR(100),
                            LATITUDE NUMERIC(7,4),
                            LONGTITUDE NUMERIC(7,4),
                            DEPTH NUMERIC(6,2),
                            SOURCE_NO INTEGER,
                            SOURCE1 VARCHAR(100),
                            TYPE VARCHAR(100),
                            MAGNITUDE NUMERIC(3,1),
                            SOURCE_NO2 NUMERIC,
                            SOURCE2 VARCHAR(100)
                        );
                            """
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        connection.close()
        return

    ######### PERSON METHODS ##########

    def create_person(self, name, password):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        today = datetime.today()

        
        statement = """INSERT INTO PERSON (NAME, PASSWORD, TYPE, PERSON_DATE)
                        VALUES ( %s, %s, %s, %s)            
                            """
        cursor.execute(statement, [name, password, "user", today])
        connection.commit()
        cursor.close()
        connection.close()
        return

    def get_password(self, name):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """SELECT PASSWORD FROM PERSON
                    WHERE( NAME = (%(id)s) )           
                            """
        cursor.execute(statement, {'id' : name})
        password = cursor.fetchall()
        cursor.close()
        connection.close()
        return password

    def get_type(self, name):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """SELECT TYPE FROM PERSON
                    WHERE( NAME = (%(id)s) )           
                            """
        cursor.execute(statement, {'id' : name})
        type = cursor.fetchall()
        if(type == "user"):
            is_admin = False
        is_admin = True
        cursor.close()
        connection.close()
        return is_admin

    def get_user_id(self, name):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """SELECT PERSON_ID FROM PERSON
                    WHERE( NAME = (%(id)s) )           
                            """
        cursor.execute(statement, {'id' : name})
        user_id = cursor.fetchall()
        cursor.close()
        connection.close()
        return user_id

    def get_person(self, id):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """SELECT NAME FROM PERSON
                    WHERE( PERSON_ID = (%(id)s))           
                            """
        cursor.execute(statement, {'id' : id})
        person = cursor.fetchall()
        cursor.close()
        connection.close()
        return person

    def get_people(self):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """SELECT PASSWORD, NAME, PERSON_DATE FROM PERSON           
                            """
        cursor.execute(statement)
        people = cursor.fetchall()
        cursor.close()
        connection.close()
        return people

    def delete_person(self,id):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        database.delete_comments(self, id, 0)
        database.delete_essays(self, id, 0)
        database.delete_announcements(self,id,0)
        
        statement = """DELETE FROM PERSON
                        WHERE ( PERSON_ID = (%(id)s) )           
                            """

        cursor.execute(statement, {'id' : id})

        connection.commit()
        cursor.close()
        connection.close()
        return

    ##################################

    ####### COMMENT METHODS ##########

    def create_comment(self, header, comment, which):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        today = datetime.today()
        
        statement = """INSERT INTO COMMENTS (COMMENT_TOPIC, COMMENT, COMMENT_WHICH_ID, COMMENT_DATE)
                        VALUES ( %s, %s, %s, %s)            
                            """
        cursor.execute(statement, [header, comment, which, today])
        connection.commit()
        cursor.close()
        connection.close()
        return

    def delete_comments(self, id, check):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        if(check == 0):
            statement = """DELETE FROM COMMENTS
                        WHERE ( COMMENT_WHICH_ID = (%(id)s) )           
                            """
        #### With this statement, we can delete a spesific user's all comments. Useful when an account gets deleted.
        else:
            statement = """DELETE FROM COMMENTS
                        WHERE ( COMMENT_ID = (%(id)s) )           
                            """                
        #### With this statement, we can delete a specific comment.

        cursor.execute(statement, {'id' : id})
        connection.commit()
        cursor.close()
        connection.close()
        return

    def get_comment(self, id):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """SELECT * FROM COMMENTS
                        WHERE ( COMMENT_WHICH_ID = (%(id)s) )
                            """

        cursor.execute(statement, {'id' : id})
        comments = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return comments
    
    def get_comments(self):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """SELECT COMMENT_WHICH_ID, COMMENT_TOPIC, COMMENT, COMMENT_DATE FROM COMMENTS
                            """

        cursor.execute(statement)
        comments = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return comments
        
    def get_comment_id(self, comment):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """SELECT COMMENT_ID FROM COMMENTS
                        WHERE ( COMMENT = (%(id)s) )
                            """

        cursor.execute(statement, {'id' : comment})
        comment_id = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return comment_id

    ###############################

    ##### ANNOUNCEMENT METHODS ####

    def create_announcement(self,header,announcement,which):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """ INSERT INTO ANNOUNCEMENTS (ANNOUNCEMENT_HEADER, ANNOUNCEMENT, ANNOUNCEMENT_WHICH_ID)
                            VALUES ( %s, %s, %s)
                                """
        cursor.execute(statement, [header, announcement, which])
        connection.commit()
        cursor.close()
        connection.close()
        return

    def get_announcement(self):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """SELECT ANNOUNCEMENT_WHICH_ID,ANNOUNCEMENT_HEADER, ANNOUNCEMENT, ANNOUNCEMENT_DATE FROM ANNOUNCEMENTS
                            """

        cursor.execute(statement)
        announcements = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return announcements

    def delete_announcements(self, id, check):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        if(check == 0):
            statement = """DELETE FROM ANNOUNCEMENTS
                        WHERE ( ANNOUNCEMENT_WHICH_ID = (%(id)s) )           
                            """
        #### With this statement, we can delete a spesific user's all comments. Useful when an account gets deleted.
        else:
            statement = """DELETE FROM ANNOUNCEMENTS
                        WHERE ( ANNOUNCEMENT_ID = (%(id)s) )           
                            """                
        #### With this statement, we can delete a specific comment.

        cursor.execute(statement, {'id' : id})
        connection.commit()
        cursor.close()
        connection.close()
        return
    
    def get_announcement_id(self, announcement):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """SELECT ANNOUNCEMENT_ID FROM ANNOUNCEMENTS
                        WHERE ( ANNOUNCEMENT = (%(id)s) )
                            """

        cursor.execute(statement, {'id' : announcement})
        announcement_id = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return announcement_id

    

    ###############################

    ######## ESSAY METHODS ########

    def create_essay(self, header, essay, which):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """INSERT INTO ESSAYS (ESSAY_HEADER, ESSAY, ESSAY_WHICH_ID)
                        VALUES ( %s, %s, %s)            
                            """
        cursor.execute(statement, [header, essay, which])
        connection.commit()
        cursor.close()
        connection.close()
        return

    def delete_essays(self, id, check):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        if(check == 0):
            statement = """DELETE FROM ESSAYS
                        WHERE ( ESSAY_WHICH_ID = (%(id)s) )           
                            """
        #### With this statement, we can delete a spesific user's all essays. Useful when an account gets deleted.
        else:
            statement = """DELETE FROM ESSAYS
                        WHERE ( ESSAY_ID = (%(id)s) )           
                            """                
        #### With this statement, we can delete a specific essay.

        cursor.execute(statement, {'id' : id})
        connection.commit()
        cursor.close()
        connection.close()
        return


    def get_essay(self):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """SELECT ESSAY_WHICH_ID,ESSAY_HEADER, ESSAY, ESSAY_DATE FROM ESSAYS
                            """

        cursor.execute(statement)
        essays = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return essays
    
    def get_essay_id(self, essay):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        statement = """SELECT ESSAY_ID FROM ESSAYS
                        WHERE ( ESSAY = (%(id)s) )
                            """

        cursor.execute(statement, {'id' : essay})
        essay_id = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return essay_id


   # def get_essay(self, id, check):
    #    connection = dbapi2.connect(url)
     #   cursor = connection.cursor()

#        if(check == 0):
 #           statement = """SELECT * FROM ESSAYS
  #                      WHERE ( ESSAY_WHICH_ID = (%(id)s) )
   #                         """
    #    else:
     #       statement = """SELECT * FROM ESSAYS
      #                  WHERE ( ESSAY_ID = (%(id)s) )
       #                     """

        #cursor.execute(statement, {'id' : id})
        #essays = cursor.fetchall()
       # connection.commit()
        #cursor.close()
        #connection.close()
        #return essays

    ###################################
    ######### earthquakes #############

    def create_earthquakes(self, file):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        with open(file, 'r')as file:
            data = file.read()
            statement = data

            cursor.execute(statement)
            connection.commit()
            cursor.close()
            connection.close()
        return

    def get_earthquakes(self, id, check):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        if(check == 0):
            statement = """SELECT * FROM EARTHQUAKES
                        """
        else:
            statement = """SELECT * FROM EARTHQUAKES
                        WHERE ( EARTHQUAKE_ID = (%(id)s) )
                        """

        cursor.execute(statement, {'id' : id})
        earthquakes = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return earthquakes

    def create_earthquake(self, agency, date_time, latitude, longtitude, depth, kind, magnitude,  rms = '-',country = '-', city = '-', village = '-', other1 = '-', other2 = '-', other3='-'):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
            
        statement = """INSERT INTO EARTHQUAKES (AGENCY, DATE_TIME, LATITUDE, LONGITUDE, DEPTH, RMS, KIND, MAGNITUDE, COUNTR, CITY, VILLAGE, OTHER1, OTHER2, OTHER3)
                            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """          
                                
        cursor.execute(statement, [agency, date_time, latitude, longtitude, depth, rms, kind, magnitude, country, city, village, other1, other2, other3])
        connection.commit()
        cursor.close()
        connection.close()
        return

    def delete_earthquake(self, id):
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        
        statement = """DELETE FROM EARTHQUAKES
                        WHERE ( EVENTID = (%(id)s) )
                        """

        cursor.execute(statement, {'id' : id})
        connection.commit()
        cursor.close()
        connection.close()
        return
        
