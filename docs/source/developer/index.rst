Developer Guide
===============

Database Design
---------------

We have 6 tables. 2 of them saves earthquake data's and 4 of them includes person,comments,essays,announcements.Person includes user's data which has logged in the application. Comments,essays and announcements are the data which can be submitted by users.

   .. figure:: diagram.png
      :scale: 50 %
      :alt: map to buried treasure

      Database diagram.



Code
----

Technical structure is depending on flask.We have sql queries in tables.py and we implemented operations in server.app. In that implementation we used the functions in tables.py and made changes in our database persistently. We used elephantsql for this.



   .. figure:: codeexample.png
      :scale: 50 %
      :alt: map to buried treasure

      As an example, here is the code for login page and signup page.
      
Like it is mentioned, tables.py has functions that makes necessary changes in database. We used dbapi2(library: pscycopg2) for these functions
   
   .. figure:: sqlcodeexample.png
      :scale: 50 %
      :alt: map to buried treasure

      As an example, here is the code for deleting comments from database.
      
      
   .. figure:: elephantsql.png
      :scale: 50 %
      :alt: map to buried treasure
      
      Users data's can be observed in elephantsql server more clearly.
          
        

.. toctree::

   member1
   member2
 
