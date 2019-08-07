"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie

from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=['GET'])
def register_form():

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():

    email = request.form.get('email')
    password = request.form.get('password')

    user = User()
    user.email = email
    user.password = password

    # We need to add to the session or it won't ever be stored
    db.session.add(user)
    # Once we're done, we should commit our work
    db.session.commit()


    return redirect('/')

@app.route('/login', methods=['GET'])
def login_form():

    return render_template('login_form.html')

@app.route('/logged', methods=['GET'])
def logged_in():
    print("\n\n\n\n\n\n\n\n******inside function")
    email = request.args.get('email')
    password = request.args.get('password')
    print("\n\n\nUSERS INPUT", email, password)
    try:
        user = User.query.filter(User.email == email).one()
        print("USER INSTANCE EMAIL", user.email)
        print("USER INSTANCE PASSWORD", user.password)

        # NEEDS DEBUGGIN
        if user.password == password:
        #flash message about success
            session['logged_in'] = True
            flash("Login Successful")
            flash("hoorayy!!!")
            return redirect('/')
        else:
            session['logged_in'] = False
            flash("Login Failed, invalid email or PASSWORD")
            return redirect('/login')
    except NoResultFound:
        flash("Login Failed, invalid EMAIL or password")
        return redirect('/login')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
