from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager, login_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# In-memory user storage for simplicity
users = {
    'testuser': generate_password_hash('password123')  # username: password hash
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def home():
    return "Hello World!"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_password_hash = users.get(username)
        if user_password_hash and check_password_hash(user_password_hash, password):
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password', 401
    return render_template('login.html')

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


if __name__ == '__main__':
    app.run(debug=True)
