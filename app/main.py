from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import os
import socket
import redis
from .models import Todo
from .storage import TodoStorage

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_DB   = int(os.environ.get("REDIS_DB", "0"))

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=False)
    store = TodoStorage(r)

    # ---------- Health ----------
    @app.route("/health")
    def health():
        try:
            r.ping()
            return jsonify(status="ok", redis=True)
        except Exception as e:
            return jsonify(status="error", redis=False, error=str(e)), 500

    # ---------- Web UI ----------
    @app.route("/", methods=["GET"])
    def index():
        todos = store.list_all()
        hostname = socket.gethostname()
        return render_template("index.html", todos=todos, hostname=hostname)

    @app.route("/add", methods=["POST"])
    def add_todo():
        title = request.form.get("title", "").strip()
        if not title:
            flash("Please enter a todo title.")
            return redirect(url_for("index"))
        t = Todo.new(title)
        store.add(t)
        return redirect(url_for("index"))

    @app.route("/toggle/<todo_id>", methods=["POST"])
    def toggle(todo_id):
        t = store.toggle(todo_id)
        if not t:
            flash("Todo not found.")
        return redirect(url_for("index"))

    @app.route("/delete/<todo_id>", methods=["POST"])
    def delete(todo_id):
        if not store.delete(todo_id):
            flash("Todo not found or could not be deleted.")
        return redirect(url_for("index"))

    @app.route("/clear-completed", methods=["POST"])
    def clear_completed():
        removed = store.clear_completed()
        flash(f"Removed {removed} completed todo(s).")
        return redirect(url_for("index"))

    # ---------- JSON API ----------
    @app.route("/api/todos", methods=["GET"])
    def api_list():
        return jsonify([t.to_dict() for t in store.list_all()])

    @app.route("/api/todos", methods=["POST"])
    def api_add():
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify(error="title is required"), 400
        t = Todo.new(title)
        store.add(t)
        return jsonify(t.to_dict()), 201

    @app.route("/api/todos/<todo_id>/toggle", methods=["POST"])
    def api_toggle(todo_id):
        t = store.toggle(todo_id)
        if not t:
            return jsonify(error="not found"), 404
        return jsonify(t.to_dict())

    @app.route("/api/todos/<todo_id>", methods=["DELETE"])
    def api_delete(todo_id):
        if not store.delete(todo_id):
            return jsonify(error="not found"), 404
        return jsonify(ok=True)

    @app.route("/api/todos/clear-completed", methods=["POST"])
    def api_clear_completed():
        return jsonify(removed=store.clear_completed())

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5005")))
