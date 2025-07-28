import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime, timedelta

LOG_FILE = os.path.join("logs", "structured_log.json")

# Helper to get last 7 days' idle, lock, and active times
def get_weekly_stats():
    today = datetime.now().date()
    stats = []
    if not os.path.exists(LOG_FILE):
        return stats
    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except Exception:
            return stats
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        idle = lock = active = 0
        login_time = None
        logout_time = None
        for entry in logs:
            if entry.get('start_time', '').startswith(day_str):
                if entry.get('event') == 'idle':
                    idle += entry.get('duration_seconds', 0)
                elif entry.get('event') == 'lock':
                    lock += entry.get('duration_seconds', 0)
                elif entry.get('event') == 'login':
                    login_time = datetime.strptime(entry['start_time'], "%Y-%m-%d %H:%M:%S")
                elif entry.get('event') == 'logout':
                    logout_time = datetime.strptime(entry['start_time'], "%Y-%m-%d %H:%M:%S")
        # Calculate active time
        if login_time and logout_time:
            total = (logout_time - login_time).total_seconds()
            active = max(0, total - idle - lock)
        stats.append({
            'date': day.strftime('%a %d'),
            'idle': idle/60,  # minutes
            'lock': lock/60,  # minutes
            'active': active/60 if login_time and logout_time else 0  # minutes
        })
    return stats

def show_dashboard():
    stats = get_weekly_stats()
    dates = [d['date'] for d in stats]
    idle = [d['idle'] for d in stats]
    lock = [d['lock'] for d in stats]
    active = [d['active'] for d in stats]

    # AI-powered insights
    most_productive_idx = max(range(len(active)), key=lambda i: active[i]) if active else None
    least_productive_idx = max(range(len(idle)), key=lambda i: idle[i] + lock[i]) if idle and lock else None
    summary = ""
    if most_productive_idx is not None:
        summary += f"Your most productive day was {dates[most_productive_idx]} with {int(active[most_productive_idx])} active minutes.\n"
    if least_productive_idx is not None:
        summary += f"You had the most idle/lock time on {dates[least_productive_idx]} (Idle+Lock: {int(idle[least_productive_idx]+lock[least_productive_idx])} min)."
    if not summary:
        summary = "No data available for insights."

    # --- Personalized Recommendations ---
    recommendations = []
    if len(stats) >= 2:
        # Find the day with the highest idle time (excluding today)
        max_idle_idx = max(range(len(idle)), key=lambda i: idle[i])
        if idle[max_idle_idx] > 30:
            recommendations.append(f"Try to reduce idle time on {dates[max_idle_idx]}.")
        # Find the day with the highest lock time
        max_lock_idx = max(range(len(lock)), key=lambda i: lock[i])
        if lock[max_lock_idx] > 30:
            recommendations.append(f"Avoid long screen locks on {dates[max_lock_idx]}.")
        # If active time is low on any day
        min_active_idx = min(range(len(active)), key=lambda i: active[i])
        if active[min_active_idx] < 60:
            recommendations.append(f"Try to stay more active on {dates[min_active_idx]}.")
    if not recommendations:
        recommendations.append("Keep up the good work!")
    recommendations_text = "\n".join(recommendations)

    # --- Trend Analysis ---
    trend_text = ""
    if len(stats) >= 14:
        # Compare this week to previous week
        this_week = sum(active[-7:])
        last_week = sum(active[-14:-7])
        if this_week > last_week:
            trend_text = f"Great! Your active time increased by {int(this_week - last_week)} minutes compared to last week."
        elif this_week < last_week:
            trend_text = f"Your active time decreased by {int(last_week - this_week)} minutes compared to last week."
        else:
            trend_text = "Your active time is the same as last week."
    elif len(stats) >= 2:
        if active[-1] > active[-2]:
            trend_text = "Nice! You were more active today than yesterday."
        elif active[-1] < active[-2]:
            trend_text = "You were less active today than yesterday."
        else:
            trend_text = "Your activity was the same as yesterday."

    # --- Motivational Message ---
    import random
    motivational_quotes = [
        "Every day is a new opportunity to improve yourself.",
        "Stay positive, work hard, make it happen!",
        "Small steps every day lead to big results.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Don't watch the clock; do what it does. Keep going.",
        "Success is not for the lazy.",
        "Your only limit is you."
    ]
    motivational_message = random.choice(motivational_quotes)

    root = tk.Tk()
    root.title("Productivity Dashboard - Smart Work Tracker")
    root.geometry("700x540")
    root.configure(bg="#23272e")

    # Smart summary label
    summary_label = tk.Label(root, text=summary, font=("Arial", 13, "bold"), fg="#fff", bg="#23272e", justify="center")
    summary_label.pack(pady=(10, 0))

    # Recommendations section
    rec_label = tk.Label(root, text="Recommendations:", font=("Arial", 12, "bold"), fg="#4fc3f7", bg="#23272e", anchor="w")
    rec_label.pack(pady=(8,0), anchor="w", padx=20)
    rec_text = tk.Label(root, text=recommendations_text, font=("Arial", 12), fg="#fff", bg="#23272e", justify="left", anchor="w")
    rec_text.pack(pady=(0,0), anchor="w", padx=40)

    # Trend analysis section
    if trend_text:
        trend_label = tk.Label(root, text=trend_text, font=("Arial", 12, "italic"), fg="#81c784", bg="#23272e")
        trend_label.pack(pady=(4,0))


    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=100)
    bar1 = ax.bar(dates, active, label='Active (min)', color='#81c784')
    bar2 = ax.bar(dates, idle, bottom=active, label='Idle (min)', color='#4fc3f7')
    bar3 = ax.bar(dates, lock, bottom=[a+i for a,i in zip(active, idle)], label='Lock (min)', color='#ff6b6b')

    # Highlight bars for most/least productive days
    if most_productive_idx is not None:
        bar1[most_productive_idx].set_edgecolor('#ffd700')
        bar1[most_productive_idx].set_linewidth(3)
    if least_productive_idx is not None:
        bar2[least_productive_idx].set_edgecolor('#ff9800')
        bar2[least_productive_idx].set_linewidth(3)
        bar3[least_productive_idx].set_edgecolor('#ff9800')
        bar3[least_productive_idx].set_linewidth(3)

    ax.set_ylabel('Minutes')
    ax.set_title('Work Activity (Past 7 Days)')
    ax.legend()
    ax.set_facecolor('#23272e')
    fig.patch.set_facecolor('#23272e')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_color('white')

    # Save chart as image for email attachment
    chart_path = os.path.join(os.path.dirname(LOG_FILE), 'weekly_productivity_chart.png')
    fig.savefig(chart_path, bbox_inches='tight', facecolor=fig.get_facecolor())

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True, pady=(10,0))

    # Motivational message at the bottom
    mot_label = tk.Label(root, text=motivational_message, font=("Arial", 12, "italic"), fg="#ffd700", bg="#23272e")
    mot_label.pack(pady=(8, 12))

    root.mainloop()

if __name__ == "__main__":
    show_dashboard()
