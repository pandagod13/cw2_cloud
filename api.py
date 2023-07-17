from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data for demonstration purposes
menu_items = [
    {"id": 1, "name": "Burger", "price": 9.99},
    {"id": 2, "name": "Pizza", "price": 12.99},
    {"id": 3, "name": "Salad", "price": 8.99}
]

orders = []


# Authentication and Authorization
def authenticate(username, password):
    # Replace with your authentication logic
    if username == "waiter" and password == "password":
        return True
    else:
        return False


def authorize(token):
    # Replace with your authorization logic
    # Here, we assume the token is valid if it matches the hardcoded value
    return token == "valid_token"


# API Endpoints
@app.route("/api/waitstaff/login", methods=["POST"])
def waitstaff_login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if authenticate(username, password):
        token = "valid_token"  # Generate a secure token
        return jsonify({"success": True, "token": token})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})


@app.route("/api/waitstaff/menu", methods=["GET"])
def get_menu_items():
    # Ensure only authenticated waitstaff can access this endpoint
    token = request.headers.get("Authorization")
    if not authorize(token):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    return jsonify(menu_items)


@app.route("/api/waitstaff/orders", methods=["GET"])
def get_orders():
    # Ensure only authenticated waitstaff can access this endpoint
    token = request.headers.get("Authorization")
    if not authorize(token):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    return jsonify(orders)


@app.route("/api/waitstaff/orders", methods=["POST"])
def create_order():
    # Ensure only authenticated waitstaff can access this endpoint
    token = request.headers.get("Authorization")
    if not authorize(token):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()
    items = data["items"]

    # Add order to the list of orders
    order = {"items": items}
    orders.append(order)

    return jsonify({"success": True, "message": "Order created successfully"})


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"success": False, "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"success": False, "message": "Internal server error"}), 500


if __name__ == "__main__":
    app.run()
