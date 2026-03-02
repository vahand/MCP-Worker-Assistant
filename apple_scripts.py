import subprocess

def get_today_calendar(calendar_names=["Personal", "EPITECH", "HFT"]):
    script = f"""tell application "Calendar"
    set output to ""
    set calendarNames to {{{", ".join(f'"{name}"' for name in calendar_names)}}}
    repeat with calName in calendarNames
        set todayEvents to events of calendar calName whose start date ≥ (current date) and start date < ((current date) + 1 * days)
        repeat with e in todayEvents
            set output to output & summary of e & " | " & (start date of e as string) & " | " & (end date of e as string) & "\n"
        end repeat
    end repeat
    return output
end tell"""
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
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
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
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
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    print("Note script output:\n", result.stdout)  # Debugging line
    return result.stdout.strip()

get_today_calendar(["HFT", "EPITECH", "Personal"])
# get_open_reminders()
# get_note_content("👨🏻‍💻 Current Work")