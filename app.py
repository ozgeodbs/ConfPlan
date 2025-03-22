from flask import Flask, render_template
from flask_migrate import Migrate

from models.db import db
from config import Config

def create_app():
    # Flask uygulamasını başlat
    app = Flask(__name__)

    # Konfigürasyonu uygula
    app.config.from_object(Config)

    # Veritabanı başlat
    db.init_app(app)

    # Routes dosyasını import et ve uygulamaya ekle
    from routes import speaker_routes, paper_routes, conference_routes, category_routes, hall_routes
    app.register_blueprint(speaker_routes)
    app.register_blueprint(paper_routes)
    app.register_blueprint(conference_routes)
    app.register_blueprint(category_routes)
    app.register_blueprint(hall_routes)

    @app.route('/')
    def index():
        return render_template('get.html')  # HTML sayfası burada döndürülür

    return app

# Eğer doğrudan çalıştırılıyorsa
if __name__ == '__main__':
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=True)
