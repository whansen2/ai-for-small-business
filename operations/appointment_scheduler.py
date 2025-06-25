"""
Appointment Scheduler for Small Business
- Accepts working hours and existing bookings via CSV or JSON
- Suggests appointment slots for next 7 days
- Uses OpenAI to format human-friendly responses
- Exports .ics calendar invites
"""
import openai
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from utils.config import OPENAI_API_KEY
from utils.file_io import read_csv, read_json
from ics import Calendar, Event

openai.api_key = OPENAI_API_KEY

def load_bookings(path: str) -> List[Dict[str, str]]:
    """Load bookings from CSV or JSON."""
    if path.endswith('.csv'):
        return read_csv(path)
    elif path.endswith('.json'):
        return read_json(path)
    else:
        raise ValueError("Unsupported file type for bookings.")

def get_available_slots(
    working_hours: Tuple[str, str],
    bookings: List[Dict[str, str]],
    slot_minutes: int = 30,
    days_ahead: int = 7,
    start_date: str = None
) -> List[Tuple[str, str, str]]:
    """Suggest available slots for the next 7 days. Optionally specify start_date as 'YYYY-MM-DD'."""
    if start_date:
        today = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        today = datetime.now().date()
    start_hour, end_hour = [datetime.strptime(h, "%H:%M").time() for h in working_hours]
    slots = []
    for day in range(days_ahead):
        date = today + timedelta(days=day)
        current = datetime.combine(date, start_hour)
        end = datetime.combine(date, end_hour)
        while current + timedelta(minutes=slot_minutes) <= end:
            slot_start = current.time()
            slot_end = (current + timedelta(minutes=slot_minutes)).time()
            overlaps = []
            for b in bookings:
                if b['date'] == str(date):
                    b_start = datetime.strptime(b['start_time'], "%H:%M").time()
                    b_end = datetime.strptime(b['end_time'], "%H:%M").time()
                    overlap = (slot_start < b_end) and (slot_end > b_start)
                    overlaps.append(overlap)
            if not any(overlaps):
                slots.append((str(date), slot_start.strftime("%H:%M"), slot_end.strftime("%H:%M")))
            current += timedelta(minutes=slot_minutes)
    return slots

def format_slots_human(slots: List[Tuple[str, str, str]]) -> str:
    """Format available slots using OpenAI for a human-friendly response."""
    prompt = "List these appointment slots in a friendly, readable way:\n" + \
        "\n".join([f"{d} {s}-{e}" for d, s, e in slots])
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

def export_ics(slots: List[Tuple[str, str, str]], out_path: str) -> None:
    """Export available slots as .ics calendar invites."""
    cal = Calendar()
    for d, s, e in slots:
        event = Event()
        event.name = "Available Appointment"
        event.begin = f"{d} {s}"
        event.end = f"{d} {e}"
        cal.events.add(event)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(cal)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Appointment Scheduler")
    parser.add_argument("--working_hours", type=str, default="09:00-17:00", help="Working hours (e.g., 09:00-17:00)")
    parser.add_argument("--bookings", type=str, default="data/sample_bookings.csv", help="Bookings CSV or JSON file")
    parser.add_argument("--ics", type=str, help="Export available slots to .ics file")
    args = parser.parse_args()
    wh = tuple(args.working_hours.split("-"))
    bookings = load_bookings(args.bookings)
    slots = get_available_slots(wh, bookings)
    print(format_slots_human(slots))
    if args.ics:
        export_ics(slots, args.ics)
        print(f"ICS file saved to {args.ics}")

if __name__ == "__main__":
    main()
