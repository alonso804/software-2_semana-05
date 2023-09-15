from flask import Flask
from flask import request, jsonify
# from flask_mongoengine import MongoEngine
import jwt
import hashlib

app = Flask(__name__)

good = hashlib.sha256(b"000000111111")
bad = hashlib.sha256(b"000000111110")

print(f"good: {good.hexdigest()}")
print(f"bad: {bad.hexdigest()}")

JWT_SECRET = "J/xzdVcfP0M="

def get_jwt(payload):
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_jwt(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

print(get_jwt({'api_key': good.hexdigest()}))
print("------")
print(get_jwt({'api_key': bad.hexdigest()}))

def middleware(req, group, correct_api_key):
    authorizarion = req.headers.get('Authorization')

    if not authorizarion or not authorizarion.startswith('Bearer '):
        return jsonify({'result': 'no autorizado'})

    token = authorizarion.split(' ')[1]

    try:
        payload = verify_jwt(token)
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'no autorizado'})

    api_key = payload.get('api_key')

    print(f"api_key: {api_key}")

    if not api_key:
        return jsonify({'result': 'no autorizado'})

    if hashlib.sha256(correct_api_key).hexdigest() == api_key:
        return jsonify({'result': f'este es el grupo {group}'})

    return jsonify({'result': 'no autorizado'})

@app.route('/group01')
def group01():
    return middleware(request, 1, b'000000111111')

@app.route('/group02')
def group02():
    return middleware(request, 2, b'NGTBGjYcdq8=')

@app.route('/group03')
def group03():
    return middleware(request, 3, b'l6AFU7ClqZY=')

@app.route('/group04')
def group04():
    return middleware(request, 4, b'6NI02xDbgG8=')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
