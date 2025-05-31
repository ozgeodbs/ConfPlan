from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from models import Conference, Paper
from models.db import db
from config import Config
import generate_excel as ge

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    from routes import speaker_routes, paper_routes, conference_routes, category_routes, hall_routes,similarity_routes
    app.register_blueprint(speaker_routes)
    app.register_blueprint(paper_routes)
    app.register_blueprint(conference_routes)
    app.register_blueprint(category_routes)
    app.register_blueprint(hall_routes)
    app.register_blueprint(similarity_routes)

    base_url = "http://127.0.0.1:5000"
    @app.route('/<int:conference_id>', methods=['GET'])
    def get_conference(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template('main.html', base_url = base_url, conference_id=conference.Id, title = "Home")

    @app.route('/<int:conference_id>/about')
    def about(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template("about.html", base_url = base_url, conference_id=conference.Id, title="About")

    @app.route('/<int:conference_id>/admin')
    def admin(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404
        return render_template("admin.html", base_url = base_url, conference_id=conference.Id, title="Admin")

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

    @app.route('/<int:conference_id>/papers')
    def calendar(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404

        papers = Paper.query.filter(Paper.ConferenceId == conference.Id).all()
        if not papers:
            return jsonify({"message": "No papers found for this conference"}), 404

        return render_template(
            "papers.html",
            conference_id=conference.Id,
            title="Calendar",
            papers = [paper.to_dict() for paper in papers],
        )

    @app.route('/<int:conference_id>/similarities')
    def similarities(conference_id):
        conference = Conference.query.get(conference_id)
        if not conference:
            return "Conference not found", 404

        papers = Paper.query.filter(Paper.ConferenceId == conference.Id).all()
        if not papers:
            return jsonify({"message": "No papers found for this conference"}), 404

        return render_template(
            "similarities.html",
            conference_id=conference.Id,
            title="Calendar",
            papers = [paper.to_dict() for paper in papers],
        )

    @app.route('/generate_excel_template')
    def generate_excel_template():
        return ge.generate_excel();
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
