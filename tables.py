import psycopg2 as dbapi2

dsn = """user='postgres' password='docker'
         host='localhost' port=5432 dbname='postgres'"""

def create_tables():
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    
    statement = """CREATE TABLE PERSON(
                        PERSON_ID SERIAL PRIMARY KEY,
                        NAME VARCHAR(50)
                        );
                   CREATE TABLE USER(
                        USER_ID PRIMARY KEY FOREIGN KEY REFERENCES TO PERSON(PERSON_ID)
                        );
                   CREATE TABLE ADMIN(
                        ADMIN_ID PRIMARY KEY FOREIGN KEY REFERENCES TO PERSON(PERSON_ID)
                        );
                   CREATE TABLE EXPERT(
                        EXPERT_ID PRIMARY KEY FOREIGN KEY REFERENCES TO PERSON(PERSON_ID)
                        );
                   CREATE TABLE COMMENTS(
                        COMMENT_ID SERIAL PRIMARY KEY,
                        WHICH_ID INTEGER REFERENCES PERSON(PERSON_ID),
                        COMMENT VARCHAR(100000),
                        COMMENT_TOPIC VARCHAR(1000);
                        COM_DATE DATE,  
                        )
                    CREATE TABLE ESSAYS(
                        ESSAY_ID SERIAL PRIMARY KEY,
                        WHICH_ID INTEGER FOREIGN KEY REFERENCES TO EXPERT(EXPERT_ID),
                        ESSAY_HEADER VARCHAR(1000);
                        ESSAY VARCHAR(100000000),
                        ES_DATE DATE,
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

def get_persons():
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    
    statement = """SELECT PERSON_ID, NAME FROM CUSTOMER           
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
