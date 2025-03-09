from flask import Blueprint, request, jsonify
from models.paper import Paper
from app import db

paper_routes = Blueprint('paper', __name__)

# Tüm bildirileri listele
@paper_routes.route('/papers', methods=['GET'])
def get_papers():
    papers = Paper.query.all()
    return jsonify([paper.__repr__() for paper in papers])

# Yeni bir bildiri oluştur
@paper_routes.route('/papers', methods=['POST'])
def create_paper():
    data = request.get_json()
    new_paper = Paper(
        Title=data['Title'],
        SpeakerId=data['SpeakerId'],
        CategoryId=data['CategoryId'],
        Duration=data['Duration'],
        Description=data['Description'],
        CreatedDate=data['CreatedDate'],
        CreatedBy=data['CreatedBy']
    )
    db.session.add(new_paper)
    db.session.commit()
    return jsonify(new_paper.__repr__()), 201

# ID'ye göre bildiri getir
@paper_routes.route('/papers/<int:id>', methods=['GET'])
def get_paper(id):
    paper = Paper.query.get(id)
    if paper:
        return jsonify(paper.__repr__())
    return jsonify({"message": "Paper not found"}), 404

# Bildiriyi güncelle
@paper_routes.route('/papers/<int:id>', methods=['PUT'])
def update_paper(id):
    paper = Paper.query.get(id)
    if paper:
        data = request.get_json()
        paper.Title = data.get('Title', paper.Title)
        paper.SpeakerId = data.get('SpeakerId', paper.SpeakerId)
        paper.CategoryId = data.get('CategoryId', paper.CategoryId)
        paper.Duration = data.get('Duration', paper.Duration)
        paper.Description = data.get('Description', paper.Description)
        paper.ChangedDate = data.get('ChangedDate', paper.ChangedDate)
        paper.ChangedBy = data.get('ChangedBy', paper.ChangedBy)

        db.session.commit()
        return jsonify(paper.__repr__())
    return jsonify({"message": "Paper not found"}), 404

# Bildiriyi sil
@paper_routes.route('/papers/<int:id>', methods=['DELETE'])
def delete_paper(id):
    paper = Paper.query.get(id)
    if paper:
        db.session.delete(paper)
        db.session.commit()
        return jsonify({"message": "Paper deleted successfully"})
    return jsonify({"message": "Paper not found"}), 404
