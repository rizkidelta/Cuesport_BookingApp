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

    # ✅ Serve React build folder
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        root_dir = os.path.join(os.getcwd(), "build")
        if path != "" and os.path.exists(os.path.join("build", path)):
            return send_from_directory("build", path)
        else:
            return send_from_directory("build", "index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
