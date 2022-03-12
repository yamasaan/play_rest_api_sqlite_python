from src.api.items import create_table, delete_all_item, delete_item, get_item_by_id, get_items, insert_item, update_item

from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
# from flask_cors import CORS
# CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/items', methods=['GET'])
def api_get_items():
    return jsonify(get_items())


@app.route('/api/items/<int:id>', methods=['GET'])
def api_get_item(id):
    return jsonify(get_item_by_id(id))


@app.route('/api/items/add', methods=['POST'])
def api_add_item():
    item = request.get_json()
    return jsonify(insert_item(item))


@app.route('/api/items/update/<int:id>', methods=['PUT'])
def api_update_item(id):
    item = {
        'id': id,
        'userid': request.json['userid'],
        'itemid': request.json['itemid'],
        'shopid': request.json['shopid'],
        'schedule': request.json['schedule'],
    }
    return jsonify(update_item(item))


@app.route('/api/items/delete/<id>', methods=['DELETE'])
def api_delete_item(id):
    return jsonify(delete_item(id))


@app.route('/api/items/deleteall', methods=['DELETE'])
def api_delete_all_item():
    return jsonify(delete_all_item())


def main():
    create_table()
    app.run(debug=True)
    app.run()


if __name__ == "__main__":
    main()
