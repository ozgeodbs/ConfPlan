from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from models import Conference
from models.db import db
from config import Config
import requests
import similarity
import generate_excel as ge

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

    @app.route('/<int:conference_id>/speakers', defaults={'speaker_id': None})
    @app.route('/<int:conference_id>/speakers/<int:speaker_id>')
    def speakers(conference_id, speaker_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404

        if speaker_id:
            return render_template(
                "speaker.html",
                base_url=base_url,
                conference_id=conference.Id,
                speakerId=speaker_id,
                title="Speaker"
            )
        else:
            return render_template(
                "speakers.html",
                base_url=base_url,
                conference_id=conference.Id,
                title="Speakers"
            )

    @app.route('/<int:conference_id>/partners')
    def partners(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template("partners.html", base_url=base_url, conference_id=conference.Id, title="Partners")

    @app.route('/<int:conference_id>/papers')
    def calendar(conference_id):
        # Konferansı al
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404

        # API'den bildirileri al
        response = requests.get(f'http://127.0.0.1:5000/{conference_id}/papers/get/all')
        if response.status_code != 200:
            return "Error fetching papers", 500
        papers = response.json()

        if not papers:
            return jsonify({"message": "No papers found for this conference"}), 404

        # Benzerlikleri hesapla (similarity.py içindeki fonksiyon kullanılarak)
        similarities = similarity.calculate_similarities(papers)
        events = similarity.create_calendar_events(similarities, papers)

        return render_template(
            "papers.html",
            conference_id=conference.Id,
            title="Calendar",
            events=events,
            papers = papers,
            similarities = similarities
        )

    @app.route('/generate_excel_template')
    def generate_excel_template():
        return ge.generate_excel();
    return app

# Eğer doğrudan çalıştırılıyorsa
if __name__ == '__main__':
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=True)
