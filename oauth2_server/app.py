from flask import Flask, request, jsonify
from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6749.models import Client, Token
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
authorization = AuthorizationServer(app)

# Mock database
clients = {}
tokens = {}

class ClientCredentialsGrant(grants.ClientCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_basic']

    def authenticate_client(self):
        client_id = request.form.get('client_id')
        client_secret = request.form.get('client_secret')
        client = clients.get(client_id)
        if client and client['client_secret'] == client_secret:
            logger.info(f'Client {client_id} authenticated successfully.')
            return Client(client_id=client_id, client_secret=client_secret)
        logger.warning('Failed client authentication attempt.')
        return None

    def save_token(self, token, request):
        tokens[token['access_token']] = token
        logger.info(f'Token issued: {token["access_token"]}')

authorization.register_grant(ClientCredentialsGrant)

@app.route('/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
