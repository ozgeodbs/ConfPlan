# similarity.py
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta

def round_to_nearest_5_minutes(dt):
    # Round the given datetime to the nearest 5-minute mark
    return dt + timedelta(minutes=(5 - dt.minute % 5)) if dt.minute % 5 != 0 else dt


def create_calendar_events(similarities, papers):
    events = []
    start_date = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)  # Start at 10 AM
    end_of_day = start_date.replace(hour=18, minute=0)  # End at 6 PM

    # Networking and lunch break times (you can adjust the timings as per the schedule)
    networking_start = start_date + timedelta(hours=2)  # First networking break at 12 PM
    networking_start = round_to_nearest_5_minutes(networking_start)  # Round to nearest 5 minutes
    networking_end = networking_start + timedelta(minutes=30)  # Networking break for 30 minutes
    networking_end = round_to_nearest_5_minutes(networking_end)  # Round to nearest 5 minutes

    lunch_start = networking_end  # Lunch break immediately after networking
    lunch_start = round_to_nearest_5_minutes(lunch_start)  # Round to nearest 5 minutes
    lunch_end = lunch_start + timedelta(minutes=60)  # Lunch break for 1 hour
    lunch_end = round_to_nearest_5_minutes(lunch_end)  # Round to nearest 5 minutes

    afternoon_networking_start = lunch_end + timedelta(hours=2)  # Afternoon networking break at 3:30 PM
    afternoon_networking_start = round_to_nearest_5_minutes(afternoon_networking_start)  # Round to nearest 5 minutes
    afternoon_networking_end = afternoon_networking_start + timedelta(minutes=30)  # Networking break for 30 minutes
    afternoon_networking_end = round_to_nearest_5_minutes(afternoon_networking_end)  # Round to nearest 5 minutes

    # Add networking and lunch events
    events.append({
        "title": "Networking Session",
        "start_date": networking_start,
        "end_date": networking_end,
        "similar_papers": []
    })
    events.append({
        "title": "Lunch Break",
        "start_date": lunch_start,
        "end_date": lunch_end,
        "similar_papers": []
    })
    events.append({
        "title": "Afternoon Networking Session",
        "start_date": afternoon_networking_start,
        "end_date": afternoon_networking_end,
        "similar_papers": []
    })

    # Create events for papers
    for paper in papers:
        # Ensure the event does not extend past the end of the day
        event_end_time = start_date + timedelta(minutes=paper['Duration'])
        event_end_time = round_to_nearest_5_minutes(event_end_time)  # Round to nearest 5 minutes

        # If the event end time exceeds the end of the day, stop scheduling further
        if event_end_time > end_of_day:
            break

        # Avoid scheduling events during breaks
        if (start_date >= networking_end and start_date < lunch_start) or \
                (start_date >= lunch_end and start_date < afternoon_networking_start):
            event = {
                "title": paper['Title'],
                "start_date": start_date,
                "end_date": event_end_time,
                "similar_papers": []
            }

            # Add similar papers to the event
            for similarity in similarities:
                if similarity['paper_id'] == paper['Id']:
                    similar_paper = next(p for p in papers if p['Id'] == similarity['other_paper_id'])
                    event['similar_papers'].append({
                        "title": similar_paper['Title'],
                        "similarity_score": similarity['similarity_score']
                    })

            events.append(event)
            start_date = event_end_time + timedelta(minutes=5)  # Add a 5-minute gap between events

    return events
