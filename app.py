"""Minimal JSON API for the Flask Micro-API assignment."""

from flask import Flask, abort, jsonify, request
from werkzeug.exceptions import HTTPException


def create_app():
    """Create an app with an independent, in-memory sample collection."""
    app = Flask(__name__, static_folder=None)
    items = [
        {"id": 1, "name": "Notebook", "category": "school"},
        {"id": 2, "name": "Water bottle", "category": "everyday"},
    ]

    @app.get("/hello")
    def hello():
        """Return a welcome message as JSON."""
        return jsonify(message="Welcome to the Flask Micro-API!"), 200

    @app.get("/data")
    def get_data():
        """Return the current sample items and their count."""
        return jsonify(items=items, count=len(items)), 200

    @app.post("/data")
    def add_data():
        """Validate a JSON object and add a sample item."""
        if not request.is_json:
            abort(
                415,
                description="Send JSON with Content-Type application/json.",
            )

        payload = request.get_json()
        if not isinstance(payload, dict):
            abort(400, description="The JSON body must be an object.")

        for field in ("name", "category"):
            value = payload.get(field)
            if not isinstance(value, str) or not value.strip():
                abort(
                    400,
                    description=f"'{field}' must be a non-empty string.",
                )

        # IDs are assigned by the server; caller-supplied IDs are ignored.
        item = {
            "id": max(entry["id"] for entry in items) + 1,
            "name": payload["name"].strip(),
            "category": payload["category"].strip(),
        }
        items.append(item)
        return jsonify(item=item), 201

    @app.errorhandler(HTTPException)
    def json_http_error(error):
        """Keep HTTP errors in JSON while preserving status and headers."""
        response = error.get_response()
        response.data = app.json.dumps(
            {"error": error.name, "message": error.description}
        )
        response.content_type = "application/json"
        return response

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
