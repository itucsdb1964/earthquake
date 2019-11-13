import psycopg2 as dbapi2

dsn = """user='postgres' password='docker'
         host='localhost' port=5432 dbname='postgres'"""

def create_tables():
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    
    statement = """CREATE TABLE PERSON(
                        PERSON_ID SERIAL PRIMARY KEY,
                        NAME VARCHAR(50),
                        PASSWORD VARCHAR(10),
                        TYPE VARCHAR(6),
                        DATE DATE,
                        );
                   CREATE TABLE COMMENTS(
                        COMMENT_ID SERIAL PRIMARY KEY,
                        COMMENT_WHICH_ID INTEGER REFERENCES PERSON(PERSON_ID),
                        COMMENT VARCHAR(100000),
                        COMMENT_TOPIC VARCHAR(1000);
                        COMMENT_DATE DATE,  
                        );
                    CREATE TABLE ESSAYS(
                        ESSAY_ID SERIAL PRIMARY KEY,
                        ESSAY_WHICH_ID INTEGER FOREIGN KEY REFERENCES TO PERSON(PERSON_ID),
                        ESSAY_HEADER VARCHAR(1000);
                        ESSAY VARCHAR(100000000),
                        ESSAY_DATE DATE,
                    );    
                    CREATE TABLE ANNOUNCEMENTS(
                        ANNOUNCEMENT_ID SERIAL PRIMARY KEY,
                        ANNOUNCEMENT_HEADER VARCHAR(1000),
                        ANNOUNCEMENT VARCHAR(1000000),
                        ANNOUNCEMENT_WHICH_ID INTEGER FOREIGN KEY REFERENCES TO PERSON(PERSON_ID),
                        ANNOUNCEMENT_DATE DATE,          
                    );
                    
                        """
    cursor.execute(statement)
    connection.commit()
    cursor.close()
    connection.close()
    return

def create_person(name):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    
    statement = """INSERT INTO PERSON (NAME)
                    VALUES ( %s )            
                        """
    cursor.execute(statement, (name))
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

def create_comment(header, comment, which):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    
    statement = """INSERT INTO COMMENTS (COMMENT_TOPIC, COMMENT, WHICH_ID)
                    VALUES ( %s, %s, %s)            
                        """
    cursor.execute(statement, (header, comment, which))
    connection.commit()
    cursor.close()
    connection.close()
    return

def delete_comments(id, check):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    
    if(check == 0):
        statement = """DELETE FROM COMMENTS
                    WHERE ( WHICH_ID = (%(id)s) )           
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
