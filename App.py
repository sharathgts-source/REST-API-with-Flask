from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory storage for users
users = {}

# Sample user format:
# {
#     "1": {"name": "Alice", "email": "alice@example.com"},
#     "2": {"name": "Bob", "email": "bob@example.com"}
# }

# GET /users - get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET /users/<user_id> - get user by ID
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user), 200

# POST /users - create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'id' not in data or 'name' not in data or 'email' not in data:
        abort(400, description="Missing required fields: id, name, email")
    
    user_id = str(data['id'])
    if user_id in users:
        abort(409, description="User with this ID already exists")

    users[user_id] = {
        "name": data['name'],
        "email": data['email']
    }
    return jsonify({"message": "User created", "user": users[user_id]}), 201

# PUT /users/<user_id> - update user by ID
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        abort(404, description="User not found")
    
    data = request.get_json()
    user = users[user_id]

    # Only update provided fields
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])

    return jsonify({"message": "User updated", "user": user}), 200

# DELETE /users/<user_id> - delete user by ID
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        abort(404, description="User not found")
    
    del users[user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
