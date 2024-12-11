from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []


@app.route("/todos", methods=["GET"])
def get_todos():
    """Get all todos."""
    print("Hit")
    return jsonify(todos), 200


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """Get a specific todo by ID."""
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    """Create a new todo."""
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_todo = {"id": len(todos) + 1, "title": data["title"], "completed": False}

    todos.append(new_todo)
    return jsonify(new_todo), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a specific todo."""
    data = request.get_json()
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    if "title" in data:
        todo["title"] = data["title"]
    if "completed" in data:
        todo["completed"] = data["completed"]

    return jsonify(todo), 200


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a specific todo."""
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]

    return jsonify({"message": "Todo deleted"}), 200


if __name__ == "__main__":
    app.run()
