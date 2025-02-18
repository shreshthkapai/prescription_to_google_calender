import json
import re
from datetime import datetime, timedelta

DEFAULT_DURATION_DAYS = 365  

def assign_time(timing):
    time_mappings = {
        "random": "09:00 AM",
        "daily": "09:00 AM",
        "before breakfast": "07:00 AM",
        "after breakfast": "08:30 AM",
        "before lunch": "12:00 PM",
        "after lunch": "01:30 PM",
        "before dinner": "07:00 PM",
        "after dinner": "08:30 PM",
    }
    return time_mappings.get(timing.lower(), timing)

def get_recurrence_interval(timing):
    timing = timing.lower().strip()

    if "every alternate day" in timing:
        return 2  
    elif match := re.search(r"every (\d+) days", timing):
        return int(match.group(1))  
    elif "once a week" in timing:
        return 7  
    elif "once a month" in timing:
        return "monthly"  
    elif timing in ["daily", "every day"]:
        return 1  
    else:
        return None  

def convert_to_24hr(time_str):
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

def format_calendar_events(processed_data):
    events = []
    start_date = datetime.today().date()

    if "medicines" in processed_data:
        for med in processed_data["medicines"]:
            if med.get("name"):
                event_time = assign_time(med.get("timing", "09:00 AM"))
                interval_days = get_recurrence_interval(med["timing"])
                
                if interval_days is None:
                    interval_days = 1  

                event_date = start_date
                for _ in range(365 if interval_days != "monthly" else 12):  
                    if interval_days == "monthly":
                        event_date = (event_date.replace(day=1) + timedelta(days=32)).replace(day=1)  
                    else:
                        event_date += timedelta(days=interval_days)
                    
                    event = {
                        "summary": f"Take {med['name']} ({med.get('dosage', 'Dosage not specified')})",
                        "start": {
                            "dateTime": f"{event_date.isoformat()}T{convert_to_24hr(event_time)}:00",
                            "timeZone": "Asia/Kolkata"
                        },
                        "end": {
                            "dateTime": f"{event_date.isoformat()}T{convert_to_24hr(event_time)}:59",
                            "timeZone": "Asia/Kolkata"
                        }
                    }
                    events.append(event)

    if "tests" in processed_data:
        for test in processed_data["tests"]:
            if test.get("name") and test.get("dueDate"):  
                event = {
                    "summary": f"Medical Test: {test['name']}",
                    "start": {"date": test["dueDate"]},  
                    "end": {"date": test["dueDate"]},  
                    "timeZone": "Asia/Kolkata"
                }
                events.append(event)

    if "follow_ups" in processed_data:
        for follow_up in processed_data["follow_ups"]:
            if follow_up.get("date"):
                event = {
                    "summary": "Doctor Follow-up Appointment",
                    "start": {"date": follow_up["date"]},
                    "end": {"date": follow_up["date"]},
                    "timeZone": "Asia/Kolkata"
                }
                events.append(event)

    return events

def validate_event(event):
    required_fields = {
        "summary": "Untitled Event",
        "start": {"dateTime": datetime.today().isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": (datetime.today() + timedelta(minutes=30)).isoformat(), "timeZone": "Asia/Kolkata"}
    }

    for field, default_value in required_fields.items():
        if field not in event or event[field] is None:
            event[field] = default_value

    return event
