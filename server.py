from flask import Flask, jsonify, abort
import json

app = Flask(__name__)

with open('data.json', 'r') as file:
    data = json.load(file)


@app.route("/all_products/", methods=["GET"])
def get_all_products():
    return jsonify(data)


@app.route("/products/<product_name>", methods=["GET"])
def get_product(product_name):
    for item in data:
        if item.get("name") == product_name:
            return jsonify(item)
    abort(404, description="Product not found")


@app.route("/products/<product_name>/<d_field>", methods=["GET"])
def get_product_field(product_name, d_field):
    for item in data:
        if item.get("name") == product_name:
            field = item.get(f"{d_field}")
            if field:
                return jsonify({d_field: field})
            else:
                abort(404, description="Field not found")
    abort(404, description="Product not found")


if __name__ == "__main__":
    app.run(debug=True)
