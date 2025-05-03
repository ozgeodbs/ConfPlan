from datetime import datetime, timedelta
from models import Conference, Paper, Similarity, Hall


def schedule_papers(conference_id: int):
    conference = Conference.query.filter(Conference.Id == conference_id, Conference.IsDeleted == False).first()
    if not conference:
        raise ValueError("Conference not found")

    papers = Paper.query.filter(Paper.ConferenceId == conference_id, Paper.IsDeleted == False).all()

    paper_ids = [p.Id for p in papers]
    similarities = Similarity.query.filter(Similarity.PaperId.in_(paper_ids), Similarity.IsDeleted == False).all()
    halls = Hall.query.filter(Hall.ConferenceId == conference_id, Hall.IsDeleted == False).all()

    from collections import defaultdict

    similarity_threshold = 0.7
    groups = []
    visited = set()

    paper_graph = defaultdict(set)
    for sim in similarities:
        if sim.SimilarityScore >= similarity_threshold:
            paper_graph[sim.PaperId].add(sim.SimilarPaperId)
            paper_graph[sim.SimilarPaperId].add(sim.PaperId)

    def dfs(paper_id, group):
        if paper_id in visited:
            return
        visited.add(paper_id)
        group.add(paper_id)
        for neighbor in paper_graph[paper_id]:
            dfs(neighbor, group)

    for paper in papers:
        if paper.Id not in visited:
            group = set()
            dfs(paper.Id, group)
            groups.append(group)

    remaining = {p.Id for p in papers} - visited
    for paper_id in remaining:
        groups.append({paper_id})

    start_datetime = datetime.combine(conference.StartDate, datetime.min.time()) + timedelta(hours=9)
    end_datetime = datetime.combine(conference.EndDate, datetime.min.time()) + timedelta(hours=17)

    current_time = start_datetime
    hall_index = 0

    for group in groups:
        group_papers = [p for p in papers if p.Id in group]
        for paper in group_papers:
            duration = timedelta(minutes=paper.Duration or 30)
            hall = halls[hall_index % len(halls)]

            # Zaman ve salon ata
            paper.StartTime = current_time
            paper.EndTime = current_time + duration
            paper.HallId = hall.Id

            # Kaydet
            paper.save()

            current_time += duration

            # Eğer gün sonuna geldiysek bir sonraki gün ve salona geç
            if current_time + duration > end_datetime:
                current_time = start_datetime + timedelta(days=1)
                hall_index += 1

    return f"{len(papers)} papers scheduled and saved."
