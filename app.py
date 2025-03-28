from flask import Flask, render_template
from flask_migrate import Migrate
from models import Conference
from models.db import db
from config import Config

def create_app():
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

    base_url = "http://127.0.0.1:5000"
    @app.route('/<int:conference_id>', methods=['GET'])
    def get_conference(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template('main.html', base_url = base_url, conference_id=conference.Id, title = "Home")

    @app.route('/<int:conference_id>/contact')
    def contact(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404

        return render_template("contact.html", base_url = base_url, conference_id=conference.Id, title="Contact")

    @app.route('/<int:conference_id>/about')
    def about(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template("about.html", base_url = base_url, conference_id=conference.Id, title="About")

    @app.route('/<int:conference_id>/speakers')
    def speakers(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template("speakers.html", base_url=base_url, conference_id=conference.Id, title="Speakers")

    @app.route('/<int:conference_id>/partners')
    def partners(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template("partners.html", base_url=base_url, conference_id=conference.Id, title="Partners")

    @app.route('/<int:conference_id>/papers')
    def calender(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template("papers.html", base_url=base_url, conference_id=conference.Id, title="Calender")

    return app

# Eğer doğrudan çalıştırılıyorsa
if __name__ == '__main__':
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=True)
