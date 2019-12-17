Developer Guide
===============

Database Design
---------------

**We have 6 tables. 2 of them saves earthquake data's and 4 of them includes person,comments,essays,announcements.Person includes user's data which has logged in the application. Comments,essays and announcements are the data which can be submitted by users.**



Code
----

**Technical structure is depending on flask.We have sql queries in tables.py and we implemented operations in server.app. In that implementation we used the functions in tables.py and made changes in our database persistently. We used elephantsql for this**

**to include a code listing, use the following example**::

   .. code-block:: python

      class Foo:

         def __init__(self, x):
            self.x = x

.. toctree::

   member1
   member2
   member3
   member4
   member5
