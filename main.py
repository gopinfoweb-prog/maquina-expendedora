from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Access Token de prueba de MercadoPago
ACCESS_TOKEN = 'APP_USR-344671403748175-090500-0879682d53527925d0da86937cb842c0-2673317468'

# Variable para guardar el estado del último pago
estado_pago = 'pendiente'

@app.route('/')
def home():
    return 'Máquina expendedora funcionando'

@app.route('/crear_pago', methods=['GET'])
def crear_pago():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "items": [
            {
                "title": "Producto expendedor",
                "quantity": 1,
                "unit_price": 100
            }
        ],
        "payer": {
            "email": "test_user@test.com"
        },
        "back_urls": {
            "success": "https://api.goprevencion.com.ar/success",
            "failure": "https://api.goprevencion.com.ar/failure",
            "pending": "https://api.goprevencion.com.ar/pending"
        },
        "notification_url": "https://api.goprevencion.com.ar/webhook",
        "auto_return": "approved"
    }

    response = requests.post(
        'https://api.mercadopago.com/checkout/preferences',
        headers=headers,
        json=data
    )

    result = response.json()
    return jsonify({
        "init_point": result.get("init_point", "Error al generar pago")
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    global estado_pago
    data = request.json
    print("Webhook recibido:", data)

    if data and 'data' in data and 'id' in data['data']:
        payment_id = data['data']['id']
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}'
        }
        payment_response = requests.get(
            f'https://api.mercadopago.com/v1/payments/{payment_id}',
            headers=headers
        )
        payment_data = payment_response.json()
        estado_pago = payment_data.get('status', 'pendiente')
        print("Estado actualizado:", estado_pago)

    return '', 200

@app.route('/estado', methods=['GET'])
def estado():
    return estado_pago

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
