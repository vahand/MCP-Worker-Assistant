from mcp.server import FastMCP

from apple_scripts import get_calendar_names, get_today_calendar, get_open_reminders, get_note_content

mcp = FastMCP("apple-daily-planning")

@mcp.tool()
def calendar_today(calendar_names: list[str] = ["Personal"]) -> list[dict]:
    """Return today's events of the specified calendars"""
    output = get_today_calendar(calendar_names)
    events = []
    for line in output.splitlines():
        if " | " in line:
            title, start_date, end_date, calendar_name = line.split(" | ", 3)
            events.append({"title": title, "start_date": start_date, "end_date": end_date, "calendar_name": calendar_name})
    return events

@mcp.tool()
def calendar_names() -> str:
    """Return the names of all calendars"""
    calendar_names = get_calendar_names()
    if isinstance(calendar_names, list):
        return ",".join(calendar_names)
    return str(calendar_names)

@mcp.tool()
def open_for_today_tasks() -> str:
    """Return open reminders for today"""
    return get_open_reminders("For Today")

@mcp.tool()
def open_weekend_tasks() -> str:
    """Return open reminders for the weekend"""
    return get_open_reminders("Week-End")

@mcp.tool()
def say_good_morning() -> str:
    """Return a good morning message"""
    return "Good morning Vahan! Think to read Bible before all."

@mcp.tool()
def current_work_note() -> str:
    """Return the current work content"""
    return get_note_content("👨🏻‍💻 Current Work")

if __name__ == "__main__":
    mcp.run()