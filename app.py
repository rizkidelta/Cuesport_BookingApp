from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from extensions import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    from routes.bookings import bookings_bp
    from routes.admin import admin_bp
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)

    # Serve React build
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        root_dir = os.path.join(os.getcwd(), "build")
        file_path = os.path.join(root_dir, path)

        if path != "" and os.path.exists(file_path):
            return send_from_directory(root_dir, path)
        else:
            return send_from_directory(root_dir, "index.html")

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
