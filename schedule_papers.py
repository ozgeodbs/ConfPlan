from datetime import datetime, timedelta, time
from models import Conference, Paper, Similarity, Hall

def schedule_papers(conference_id: int):
    conference = Conference.query.filter(
        Conference.Id == conference_id,
        Conference.IsDeleted == False
    ).first()
    if not conference:
        raise ValueError("Conference not found")

    papers = Paper.query.filter(
        Paper.ConferenceId == conference_id,
        Paper.IsDeleted == False
    ).all()

    paper_ids = [p.Id for p in papers]
    similarities = Similarity.query.filter(
        Similarity.PaperId.in_(paper_ids),
        Similarity.IsDeleted == False
    ).all()

    halls = Hall.query.filter(
        Hall.ConferenceId == conference_id,
        Hall.IsDeleted == False
    ).all()

    from collections import defaultdict

    similarity_threshold = 0.8
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

    daily_start = time(conference.StartDate.hour, conference.StartDate.minute)
    daily_end = time(conference.EndDate.hour, conference.EndDate.minute)
    first_day_start = datetime.combine(conference.StartDate, daily_start)

    hall_schedule = { hall.Id: first_day_start for hall in halls }

    speaker_schedule = defaultdict(list)

    for group in groups:
        group_papers = [p for p in papers if p.Id in group]
        for paper in group_papers:
            speaker_id = paper.SpeakerId
            duration = timedelta(minutes=paper.Duration or 30)

            scheduled = False
            while not scheduled:
                chosen_hall_id = min(hall_schedule, key=lambda h: hall_schedule[h])
                chosen_time = hall_schedule[chosen_hall_id]
                current_day = chosen_time.date()
                current_day_end = datetime.combine(current_day, daily_end)

                if chosen_time + duration > current_day_end:
                    next_day = current_day + timedelta(days=1)
                    hall_schedule[chosen_hall_id] = datetime.combine(next_day, daily_start)
                    continue

                speaker_times = speaker_schedule[speaker_id]
                conflict = any(
                    not (chosen_time + duration <= start or chosen_time >= end)
                    for start, end in speaker_times
                )

                if conflict:
                    hall_schedule[chosen_hall_id] = chosen_time + timedelta(minutes=5)
                    continue

                paper.StartTime = chosen_time
                paper.EndTime = chosen_time + duration
                paper.HallId = chosen_hall_id
                paper.save()

                speaker_schedule[speaker_id].append((paper.StartTime, paper.EndTime))
                hall_schedule[chosen_hall_id] = paper.EndTime
                scheduled = True

    return f"{len(papers)} papers scheduled and saved."
