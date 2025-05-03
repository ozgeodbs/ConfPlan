from datetime import datetime, timedelta, time
from models import Conference, Paper, Similarity, Hall

def schedule_papers(conference_id: int):
    # Konferansı getir
    conference = Conference.query.filter(
        Conference.Id == conference_id,
        Conference.IsDeleted == False
    ).first()
    if not conference:
        raise ValueError("Conference not found")

    # Konferansa ait paper'ları getir
    papers = Paper.query.filter(
        Paper.ConferenceId == conference_id,
        Paper.IsDeleted == False
    ).all()

    paper_ids = [p.Id for p in papers]
    # Similarity sadece PaperId üzerinden filtrelenecek
    similarities = Similarity.query.filter(
        Similarity.PaperId.in_(paper_ids),
        Similarity.IsDeleted == False
    ).all()

    halls = Hall.query.filter(
        Hall.ConferenceId == conference_id,
        Hall.IsDeleted == False
    ).all()

    # Gruplama (benzerlik bazlı) – mevcut algoritmadan aynen alınmış
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

    # Her odanın (hall) günlük başlangıç ve bitiş zamanları
    # Konferans modelinizde StartTime ve EndTime alanları odak için konfigürasyon sağlayacak (örneğin, 09:00 ve 17:00)
    daily_start = time(conference.StartDate.hour, conference.StartDate.minute)
    daily_end = time(conference.EndDate.hour, conference.EndDate.minute)
    # Konferansın ilk günü için başlangıç datetime'ı
    first_day_start = datetime.combine(conference.StartDate, daily_start)

    # Her odanın (hall) müsaitlik takvimi: { hall_id: next_available_datetime }
    hall_schedule = { hall.Id: first_day_start for hall in halls }

    # Yeni planlama algoritması: Her paper'ı, en erken müsait odaya yerleştir.
    for group in groups:
        # Aynı gruptaki paper'ları sırayla planlıyoruz.
        group_papers = [p for p in papers if p.Id in group]
        for paper in group_papers:
            # En erken müsait odayı seç: key, hall_id; value, next available time
            chosen_hall_id = min(hall_schedule, key=lambda h: hall_schedule[h])
            chosen_time = hall_schedule[chosen_hall_id]
            current_day = chosen_time.date()
            # O günün bitiş zamanını hesapla
            current_day_end = datetime.combine(current_day, daily_end)
            duration = timedelta(minutes=paper.Duration or 30)
            # Eğer seçilen oda için müsait zaman + paper süresi o günün bitişini aşıyorsa,
            # o odanın müsait zamanını bir sonraki güne ayarla.
            if chosen_time + duration > current_day_end:
                next_day = current_day + timedelta(days=1)
                chosen_time = datetime.combine(next_day, daily_start)
            # Paper’ın saatlerini ve salonunu ayarla
            paper.StartTime = chosen_time
            paper.EndTime = chosen_time + duration
            paper.HallId = chosen_hall_id
            paper.save()
            # Odadaki sonraki müsait zamanı güncelle: paper bittiği zamandan itibaren
            new_time = paper.EndTime
            # Eğer yeni zaman yine o günün bitişini aşıyorsa, bir sonraki güne al
            if new_time > current_day_end:
                next_day = new_time.date() + timedelta(days=1)
                new_time = datetime.combine(next_day, daily_start)
            hall_schedule[chosen_hall_id] = new_time

    return f"{len(papers)} papers scheduled and saved."
