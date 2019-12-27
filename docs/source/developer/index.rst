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

As an example, here is the code for login page. It checks the username and password and directs to related html part.

.. code-block:: python
      @app.route("/login",methods=["GET", "POST"])
      def login_page():
          form = LoginForm()
          if form.validate_on_submit():
              username = form.data["username"]
              user = get_user(username)
              if user is not None:
                  password = form.data["password"]
                  if pbkdf2_sha256.verify(password, user.password[0][0] ):
                      login_user(user)
                      flash("You have logged in.")
                      next_page = request.args.get("next", url_for("home_page"))
                      return redirect(next_page)
              flash("Invalid credentials.")
          return render_template("login.html", form=form)
          
        

.. toctree::

   member1
   member2
   member3
   member4
   member5
