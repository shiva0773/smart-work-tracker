import json
from datetime import datetime
from collections import defaultdict

LOG_FILE = "logs/structured_log.json"

def load_logs():
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def generate_summary():
    logs = load_logs()
    app_usage = defaultdict(int)
    idle_time = 0
    lock_time = 0

    for entry in logs:
        duration = entry["duration_seconds"]
        if entry["event"] == "active_app":
            app_usage[entry["title"]] += duration
        elif entry["event"] == "idle":
            idle_time += duration
        elif entry["event"] == "lock":
            lock_time += duration

    total_tracked = sum(app_usage.values()) + idle_time + lock_time
    productive_time = sum(app_usage.values())

    print("\n📊 DAILY WORK SUMMARY")
    print("--------------------------")
    for app, seconds in sorted(app_usage.items(), key=lambda x: x[1], reverse=True):
        mins = seconds // 60
        print(f"🖥️  {app}: {mins} min")

    print(f"\n💤 Idle Time: {idle_time // 60} min")
    print(f"🔒 Lock Time: {lock_time // 60} min")
    print(f"\n✅ Productive Time: {productive_time // 60} min")
    print(f"⏱️  Total Tracked Time: {total_tracked // 60} min")
    print("--------------------------")

    return {
        "apps": app_usage,
        "idle": idle_time,
        "lock": lock_time,
        "productive": productive_time,
        "total": total_tracked
    }

if __name__ == "__main__":
    generate_summary()
