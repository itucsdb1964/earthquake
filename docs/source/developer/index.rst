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


   .. code-block:: python
   class Foo:
      @app.route("/signup",methods=["GET", "POST"])
      def signup_page():
          form = LoginForm()
          if form.validate_on_submit():
              username = form.data["username"]
              password = form.data["password"]
              next_page = request.args.get("next", url_for("login_page"))
              db = current_app.config["db"]
              db.create_person(username, pbkdf2_sha256.hash(password))
              flash("You signed up, you can enjoy our website now :)")
              return redirect(next_page)
          flash("Invalid credentials.")
          return render_template("signup.html", form=form)

.. toctree::

   member1
   member2
   member3
   member4
   member5
