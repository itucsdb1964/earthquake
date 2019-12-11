import psycopg2 as dbapi2

 

dsn = """user='postgres' password='1864'

         host='localhost' port=5432 dbname='postgres'"""

 

def delete_all():

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

   

    statement = """

                   DROP TABLE COMMENTS;

                   DROP TABLE ESSAYS;

                   DROP TABLE ANNOUNCEMENTS;

                   DROP TABLE PERSON;

                """

    cursor.execute(statement)

    connection.commit()

    cursor.close()

    connection.close()

    return

 

 

def create_tables():

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

    # old earthquake tables will be added

    statement = """CREATE TABLE PERSON(

                        PERSON_ID SERIAL PRIMARY KEY,

                        NAME VARCHAR(50),

                        PASSWORD VARCHAR(10),

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

 

def create_person(name):

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

   

    statement = """INSERT INTO PERSON (NAME)

                    VALUES ( %s )           

                        """

    cursor.execute(statement, [name])

    connection.commit()

    cursor.close()

    connection.close()

    return

 

def get_people():

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

   

    statement = """SELECT PERSON_ID, NAME FROM PERSON          

                        """

    cursor.execute(statement)

    people = cursor.fetchall()

    cursor.close()

    connection.close()

    return people

 

def delete_person(id):

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

   

    statement = """DELETE FROM PERSON

                    WHERE ( PERSON_ID = (%(id)s) )          

                        """

 

    cursor.execute(statement, {'id' : id})

    check = 0

    delete_comments(id, check)

    connection.commit()

    cursor.close()

    connection.close()

    return

 

##################################

 

####### COMMENT METHODS ##########

 

def create_comment(header, comment, which):

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

   

    statement = """INSERT INTO COMMENTS (COMMENT_TOPIC, COMMENT, COMMENT_WHICH_ID)

                    VALUES ( %s, %s, %s)           

                        """

    cursor.execute(statement, [header, comment, which])

    connection.commit()

    cursor.close()

    connection.close()

    return

 

def delete_comments(id, check):

    connection = dbapi2.connect(dsn)

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

 

def get_comment(id):

    connection = dbapi2.connect(dsn)

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

 

###############################

 

######## ESSAY METHODS ########

 

def create_essay(header, essay, which):

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

   

    statement = """INSERT INTO ESSAYS (ESSAY_TOPIC, ESSAY, ESSAY_WHICH_ID)

                    VALUES ( %s, %s, %s)           

                        """

    cursor.execute(statement, [header, essay, which])

    connection.commit()

    cursor.close()

    connection.close()

    return

 

def delete_essays(id, check):

    connection = dbapi2.connect(dsn)

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

 

def get_essay(id, check):

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

 

    if(check == 0):

        statement = """SELECT * FROM ESSAYS

                    WHERE ( ESSAY_WHICH_ID = (%(id)s) )

                        """

    else:

        statement = """SELECT * FROM ESSAYS

                    WHERE ( ESSAY_ID = (%(id)s) )

                        """

 

    cursor.execute(statement, {'id' : id})

    essays = cursor.fetchall()

    connection.commit()

    cursor.close()

    connection.close()

    return essays

 

###################################

######### earthquakes #############

 

def create_earthquakes(file):

    connection = dbapi2.connect(dsn)

    cursor = connection.cursor()

 

    with open(file, 'r')as file:

        data = file.read()

        statement = data

 

        cursor.execute(statement)

        connection.commit()

        cursor.close()

        connection.close()

    return

 

def get_earthquakes(id, check):

    connection = dbapi2.connect(dsn)

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
