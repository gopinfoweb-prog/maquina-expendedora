from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Máquina expendedora funcionando'

@app.route('/webhook', methods=['POST'])
def webhook():
    # Aquí vas a recibir la confirmación de MercadoPago
    return 'Webhook recibido', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
