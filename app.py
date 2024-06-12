from flask import Flask, request, jsonify, send_file,render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import secrets
import qrcode
import io
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    api_key = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    return "API de Geração de QR Code"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    data.get('password')  

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already taken!"}), 400

    api_key = secrets.token_hex(16)
    new_user = User(username=username, api_key=api_key)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"username": username, "api_key": api_key})

@app.route('/protected', methods=['GET'])
def protected():
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "API key missing!"}), 401
    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        return jsonify({"message": "Invalid API key!"}), 401

    return jsonify({"message": "Welcome to the protected route, " + user.username})

@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "API key missing!"}), 401
    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        return jsonify({"message": "Invalid API key!"}), 401

    data = request.get_json()
    qr_content = data.get('content')
    if not qr_content:
        return jsonify({"message": "Content for QR code missing!"}), 400

    img = qrcode.make(qr_content)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    message = None
    api_key = None

    if request.method == 'POST':
        username = request.form.get('username')
        request.form.get('password') 
        if User.query.filter_by(username=username).first():
            message = "Nome de usuário já existe!"
        else:
            api_key = secrets.token_hex(16)
            new_user = User(username=username, api_key=api_key)
            db.session.add(new_user)
            db.session.commit()
            message = "Usuário registrado com sucesso!"

    return render_template('dashboard.html', message=message, api_key=api_key)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Geração de QR Code"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
