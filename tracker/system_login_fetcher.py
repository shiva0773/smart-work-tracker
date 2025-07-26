# tracker/system_login_fetcher.py

import win32evtlog
from datetime import datetime, timedelta

def get_latest_login_time():
    server = 'localhost'
    log_type = 'Security'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    login_event_id = 4624  # Successful login

    hand = win32evtlog.OpenEventLog(server, log_type)
    events = win32evtlog.ReadEventLog(hand, flags, 0)

    for ev_obj in events:
        if ev_obj.EventID == login_event_id:
            return ev_obj.TimeGenerated

    return None
