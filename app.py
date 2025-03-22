from flask import Flask
from flask_migrate import migrate, Migrate

from models.db import db
from config import Config
from flask_restx import Api  # Flask-RESTPlus import

def create_app():
    # Flask uygulamasını başlat
    app = Flask(__name__)

    # Konfigürasyonu uygula
    app.config.from_object(Config)

    # Veritabanı başlat
    db.init_app(app)

    # Swagger dokümantasyonu için Api sınıfını başlat
    api = Api(app, version='1.0', title='Conference API', description='A simple Conference management API')

    # Routes dosyasını import et ve uygulamaya ekle
    from routes import speaker_routes, paper_routes, conference_routes, category_routes, hall_routes
    app.register_blueprint(speaker_routes)
    app.register_blueprint(paper_routes)
    app.register_blueprint(conference_routes)
    app.register_blueprint(category_routes)
    app.register_blueprint(hall_routes)

    return app

# Eğer doğrudan çalıştırılıyorsa
if __name__ == '__main__':
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=True)
