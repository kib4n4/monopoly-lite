from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session management

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(150), unique=True, nullable=False)  # Unique username
    password_hash = db.Column(db.String(150), nullable=False)  # Hashed password

    # Method to set the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Routes
@app.route('/')
def home():
    return render_template('index.html')  # Render the home page

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username  # Set the session
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error='Invalid credentials')
    return render_template('index.html')

# Register
@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return
