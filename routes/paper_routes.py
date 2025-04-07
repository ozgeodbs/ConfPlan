from flask import Blueprint, request, jsonify
from models.paper import Paper

paper_routes = Blueprint('paper', __name__)

# Tüm bildirileri listele
@paper_routes.route('/papers', methods=['GET'])
def get_papers():
    papers = Paper.query.filter_by(IsDeleted=False).all()  # Assuming IsDeleted field exists
    return jsonify([paper.to_dict() for paper in papers]), 200

# Yeni bir bildiri oluştur
@paper_routes.route('/papers', methods=['POST'])
def create_paper():
    data = request.get_json()
    new_paper = Paper(
        Title=data['Title'],
        SpeakerId=data['SpeakerId'],
        CategoryId=data['CategoryId'],
        Duration=data['Duration'],
        Description=data.get('Description', '')
    )
    new_paper.save()  # Assuming save() is defined in your base model
    return jsonify(new_paper.to_dict()), 201

# ID'ye göre bildiri getir
@paper_routes.route('/papers/<int:id>', methods=['GET'])
def get_paper(id):
    paper = Paper.query.get(id)
    if paper and not paper.IsDeleted:
        return jsonify(paper.to_dict())
    return jsonify({"message": "Paper not found"}), 404

# Bildiriyi güncelle
@paper_routes.route('/papers/<int:id>', methods=['PUT'])
def update_paper(id):
    paper = Paper.query.get(id)
    if paper and not paper.IsDeleted:
        data = request.get_json()
        paper.Title = data.get('Title', paper.Title)
        paper.SpeakerId = data.get('SpeakerId', paper.SpeakerId)
        paper.CategoryId = data.get('CategoryId', paper.CategoryId)
        paper.Duration = data.get('Duration', paper.Duration)
        paper.Description = data.get('Description', paper.Description)

        paper.update()  # Assuming update() is defined in your base model
        return jsonify(paper.to_dict())
    return jsonify({"message": "Paper not found"}), 404

# Bildiriyi sil
@paper_routes.route('/papers/<int:id>', methods=['DELETE'])
def delete_paper(id):
    paper = Paper.query.get(id)
    if paper and not paper.IsDeleted:
        paper.delete()  # Assuming delete() is defined in your base model
        return jsonify({"message": "Paper deleted successfully"})
    return jsonify({"message": "Paper not found"}), 404

# 📌 Belirli bir konferansa ait bildirileri getir
@paper_routes.route('/<int:conference_id>/papers/get/all', methods=['GET'])
def get_papers_by_conference(conference_id):
    papers = Paper.query.filter_by(ConferenceId=conference_id, IsDeleted=False).all()
    if papers:
        return jsonify([paper.to_dict() for paper in papers]), 200
    return jsonify({"message": "No papers found for this conference"}), 404

# 📌 Belirli bir konferans ve konuşmacıya ait bildirileri getir
@paper_routes.route('/<int:conference_id>/papers/speaker/<int:speaker_id>/get/all', methods=['GET'])
def get_papers_by_conference_and_speaker(conference_id, speaker_id):
    papers = Paper.query.filter_by(ConferenceId=conference_id, SpeakerId=speaker_id, IsDeleted=False).all()
    if papers:
        return jsonify([paper.to_dict() for paper in papers]), 200
    return jsonify({"message": "No papers found for this conference and speaker"}), 404
