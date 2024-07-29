#imports - things we need in the code and are ready to use.
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session 
import pyrebase

#app load - loading the app.
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'Adminsecretkey'


#Firebase configuration
firebaseConfig = {
  "apiKey": "AIzaSyBcnAhKn3K6t7eOu-5TE3AjOU4as-_9fMM",
  "authDomain": "calander-d12ed.firebaseapp.com",
  "projectId": "calander-d12ed",
  "storageBucket": "calander-d12ed.appspot.com",
  "messagingSenderId": "319275616286",
  "appId": "1:319275616286:web:42b2f118ed53df43d3860f",
  "measurementId": "G-VJ1ZPQ17FS",
  "databaseURL": "https://calander-d12ed-default-rtdb.europe-west1.firebasedatabase.app/"
};

#Initialize firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

events = {
    "CAS": []
}


#app route main
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")
 

#app route - login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html") 
    else: 
        email = request.form['email']
        password = request.form['password']

        try:
            if username == 'admin':
                login_session['admin'] = True
                return redirect(url_for('admin'))           
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('event'))

        except Exception as e:
            error = "login failed, try again."
            print(e)
            return render_template("login.html", error=error)


#app route - signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html") 
    else: 
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email": email, "password": password, "username": username}
            db.child("users").child(UID).set(user)
            return redirect(url_for('event'))
        except Exception as e:
            error = "Authentication error"
            print(e)
            return render_template("signup.html",error=error)

        
#app route - events
@app.route('/event', methods= ['GET', 'POST'])
def event():
    if request.method == 'GET':
        return render_template("event.html") 
    else: 
        UID = login_session['user']['localId']
        return redirect(url_for('thanks'))


#app route - thanks
@app.route('/thanks<event>', methods= ['GET', 'POST'])
def thanks(event):
    if username == 'admin':
        login_session['admin'] = True
        return redirect(url_for('admin')) 
    if request.method == 'POST':
        events[event].append(login_session['user']['email'])
        db.child("events").push(events)
        return render_template("thanks.html")
    return render_template("event.html")


#app route - admin
@app.route('/admin', methods= ['GET', 'POST'])
def admin():
    if request.method == 'GET':

        return render_template("admin.html" , events=events)


#app route - signout
@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('home'))


#run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
