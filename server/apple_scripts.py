import subprocess


def get_calendar_names():
    script = """tell application "Calendar"
    set calendarNames to name of every calendar
    return calendarNames
end tell"""
    result = subprocess.run(["osascript", "-e", script],
                            capture_output=True, text=True)
    print("Calendar names script output:\n", result.stdout)  # Debugging line
    return [name.strip() for name in result.stdout.strip().split(",") if name.strip()]


def get_today_calendar(calendar_names=["Personal"]):
    script = f"""tell application "Calendar"
    set output to ""
    set calendarNames to {{{",".join(f'"{name}"' for name in calendar_names)}}}

    set todayDate to (current date)
    set todayStart to todayDate
    set hours of todayStart to 0
    set minutes of todayStart to 0
    set seconds of todayStart to 0
    set todayEnd to todayStart + (1 * days)

    repeat with calName in calendarNames
        try
            set calRef to calendar calName
            set todayEvents to events of calRef whose start date ≥ todayStart and start date < todayEnd
            repeat with e in todayEvents
                set output to output & summary of e & " | " & (start date of e as string) & " | " & (end date of e as string) & " | " & (calName) & "\n"
            end repeat
        on error
            -- Skip calendar if it doesn't exist or has access issues
        end try
    end repeat
    return output
end tell"""
    result = subprocess.run(["osascript", "-e", script],
                            capture_output=True, text=True)
    print("Calendar script output:\n", result.stdout)  # Debugging line
    return result.stdout.strip()


def get_open_reminders(list_name="For Today"):
    script = f"""tell application "Reminders"
    set output to ""
    repeat with r in reminders of list "{list_name}" whose completed is false
        set output to output & name of r & "\n"
    end repeat
    return output
end tell"""
    result = subprocess.run(["osascript", "-e", script],
                            capture_output=True, text=True)
    print("Reminders script output:\n", result.stdout)  # Debugging line
    return result.stdout.strip()


def get_note_content(note_name):
    script = f"""tell application "Notes"
    set output to ""
    repeat with n in notes
        if name of n is "{note_name}" then
            set output to body of n
            exit repeat
        end if
    end repeat
    return output
end tell"""
    result = subprocess.run(["osascript", "-e", script],
                            capture_output=True, text=True)
    print("Note script output:\n", result.stdout)  # Debugging line
    return result.stdout.strip()


if __name__ == "__main__":
    calendar_names = get_calendar_names()
    get_today_calendar(calendar_names)
    get_open_reminders()
    get_note_content("👨🏻‍💻 Current Work")
