from flask import Flask, request, jsonify
from functools import wraps
import jwt
import logging
import colorlog

# Configure colored logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
SECRET_KEY = 'your_secret_key'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.warning('Token is missing!')
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            logger.warning('Invalid token provided.')
            return jsonify({'message': 'Token is invalid!'}), 403
        logger.info('Token verified successfully.')
        return f(*args, **kwargs)
    return decorated

@app.route('/secure-data', methods=['GET'])
@token_required
def secure_data():
    logger.info('Accessing secure data.')
    return jsonify({'data': 'This is secured data'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
