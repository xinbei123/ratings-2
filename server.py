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
    if not session['login_status']:
        session['login_status'] = False
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
            session['login_status'] = True
            session['user_id'] = user.user_id
            print("\n\n\n\n", session['user_id'])
            print("\n\n\n\n", session['login_status'])
            flash("Login Successful")
            return redirect('/')
        else:
            session['login_status'] = False
            flash("Login Failed, invalid email or PASSWORD")
            return redirect('/login')
    except NoResultFound:
        session['login_status'] = False
        flash("Login Failed, invalid EMAIL or password")
        return redirect('/login')


@app.route('/logout')
def logout():

    session['login_status'] = False
    del session['user_id']

    return redirect('/')

@app.route('/users/<int:user_id>')
def user_detail(user_id):

    user = User.query.get(user_id)

    return render_template('user_details.html',
                           user=user)

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
