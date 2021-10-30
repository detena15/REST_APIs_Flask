"""
AL hacer peticiones REST API a una web, lo haces a un servidor. Para que este servidor entienda las peticiones y
pueda procesarlas, debe tener una aplicación Flask (en este caso).
"""
from flask import Flask, jsonify, request, render_template

# Crear un objeto de clase Flask
app = Flask(__name__)  # __name__ gives each file an unique name


# data
stores = [
    {
        'name': 'My Wonderful Store',
        'items':
            [
                 {
                     'name': 'My Item',
                     'price': 19.99
                 }
            ]
     }
]


# What requests is going to understand
@app.route('/')  # '/' es el endpoint, la petición que debe entender: 'https://www.google.com/'
def home():
    # Lo que haga aqui la funcion, debe devolver una respuesta al navegador. Asi el navegador recibe algo
    # y puede mostrarlo en el navegador

    return render_template('index.html')


# POST - used to recieve data
# GET - used to use data back only

# ---Crear los ENDPOINTS----------------------------------
# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()  # get_json converts the JSON string into a python dictionary

    new_store = {
        'name': request_data['name'],
        'items': []
    }

    stores.append(new_store)

    return jsonify(new_store)


# GET /store/<string: name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if name == store['name']:
            return jsonify(store)

        else:
            return jsonify({'message': 'The store does not exist.'})


# GET /store
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string: name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {}

    for store in stores:
        if name == store['name']:
            new_item = {'name': request_data['name'],
                        'price': request_data['price']}

        store['items'].append(new_item)

        return jsonify(new_item)

    # solo se envia este return en el caso en el que el otro no se envie. Estos metodos solo pueden enviar un return.
    return jsonify({'message': 'Store not found'})


# GET /store/<string: name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_item_in_store(name):
    for store in stores:
        if name == store['name']:
            return jsonify({'items': store['items']})

        else:
            return jsonify({'message': 'The store does not exist.'})


# Hay que decirle a la app que se ejecute. En los parentesis se puede incluir el puerto: is just a sort of area
# in the computer where your app is going to be receiving your requests and returning your responses through
app.run(port=5000)
