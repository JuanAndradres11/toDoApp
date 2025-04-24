from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from config import DATABASE_URL  # <-- Imported from your config file
import os

client_secret='ubr51ltdjasp1fg1mevk200pests1r0bsshoo95fqdnvsuqs7ap',

# Initialize the Flask app and configurations
app = Flask(__name__, static_folder="static")
CORS(app)

# Set up Flask secret key (in production, use a more secure key)
app.secret_key = os.urandom(24)

# Initialize OAuth
oauth = OAuth(app)

# Amazon Cognito OAuth Setup
oauth.register(
    name='oidc',
    authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_wlNiP83wU',
    client_id='1edh81k4oh52ie444ioerjluqo',
    client_secret='ubr51ltdjasp1fg1mevk200pests1r0bsshoo95fqdnvsuqs7ap',
    server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_wlNiP83wU/.well-known/openid-configuration',
    client_kwargs={'scope': 'email openid phone'}
)

# Use PostgreSQL database (AWS RDS)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your database model for Todo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "task": self.task, "completed": self.completed}

# Initialize the database
with app.app_context():
    db.create_all()

# Home page route
@app.route('/')
def home():
    user = session.get('user')
    if user:
        return render_template('index.html', user=user)
    else:
        return f'Welcome! Please <a href="/login">Login</a>.'

# Todos API routes
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    data = request.get_json()
    todo.task = data.get('task', todo.task)
    todo.completed = data.get('completed', todo.completed)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted successfully"})

# Login page route
@app.route('/login')
def login():
    return render_template('login.html')

# Cognito login redirect route
@app.route('/login/redirect')
def login_redirect():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)

# Cognito authorize route
@app.route('/authorize')
def authorize():
    try:
        print("OAuth Response:", request.args)  # Print full OAuth response
        token = oauth.oidc.authorize_access_token()
        user = token['userinfo']
        session['user'] = user
        return redirect(url_for('home'))
    except Exception as e:
        print("OAuth Error:", str(e))
        return f"OAuth failed: {str(e)}", 500


# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
