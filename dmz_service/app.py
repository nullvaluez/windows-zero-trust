from flask import Flask, request, jsonify
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

@app.route('/dmz-data', methods=['GET'])
def dmz_data():
    logger.info('Accessing DMZ data.')
    return jsonify({'data': 'This is DMZ data'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
