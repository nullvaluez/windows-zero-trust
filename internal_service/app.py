from flask import Flask, request, jsonify
from functools import wraps
import jwt
import logging
import colorlog
import seal

# Configure colored logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
SECRET_KEY = 'your_secret_key'

# Create encryption parameters
parms = seal.EncryptionParameters(seal.SCHEME_TYPE.CKKS)
poly_modulus_degree = 8192
parms.set_poly_modulus_degree(poly_modulus_degree)
parms.set_coeff_modulus(seal.CoeffModulus.Create(poly_modulus_degree, [60, 40, 40, 60]))

# Create context and keys
context = seal.SEALContext.Create(parms)
keygen = seal.KeyGenerator(context)
public_key = keygen.public_key()
secret_key = keygen.secret_key()
encryptor = seal.Encryptor(context, public_key)
decryptor = seal.Decryptor(context, secret_key)
evaluator = seal.Evaluator(context)
encoder = seal.CKKSEncoder(context)
scale = pow(2.0, 40)

def encrypt_data(data):
    plain = encoder.encode(data, scale)
    encrypted = seal.Ciphertext()
    encryptor.encrypt(plain, encrypted)
    return encrypted

def decrypt_data(encrypted):
    plain = seal.Plaintext()
    decryptor.decrypt(encrypted, plain)
    decoded = encoder.decode(plain)
    return decoded

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

@app.route('/secure-data', methods=['POST'])
@token_required
def secure_data():
    data = request.json.get('data')
    encrypted = encrypt_data(data)
    logger.info('Data encrypted successfully.')
    return jsonify({'encrypted': str(encrypted)})

@app.route('/decrypt-data', methods=['POST'])
@token_required
def decrypt_data_route():
    encrypted_str = request.json.get('encrypted')
    encrypted = seal.Ciphertext()
    encrypted.load(context, encrypted_str)
    decrypted = decrypt_data(encrypted)
    logger.info('Data decrypted successfully.')
    return jsonify({'decrypted': decrypted})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
