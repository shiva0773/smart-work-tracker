import ollama
from generate_summary import generate_summary
from plyer import notification
import datetime

def format_prompt(summary_data):
    apps = summary_data["apps"]
    idle = summary_data["idle"] // 60
    lock = summary_data["lock"] // 60
    productive = summary_data["productive"] // 60
    total = summary_data["total"] // 60

    app_summary = "\n".join([f"- {app}: {sec//60} min" for app, sec in apps.items()])

    prompt = f"""
You are a friendly productivity assistant. Based on the following daily system usage, generate a short motivational summary:

App Usage:
{app_summary}

Idle Time: {idle} min
Lock Time: {lock} min
Productive Time: {productive} min
Total Time Tracked: {total} min

Respond in a casual and positive tone.
"""
    return prompt.strip()

def save_summary(summary):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("summary_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] {summary}\n\n")

def show_notification(summary):
    notification.notify(
        title="🧠 Your AI Productivity Summary",
        message=summary[:200] + "..." if len(summary) > 200 else summary,
        timeout=10
    )

def get_ai_summary():
    summary_data = generate_summary()
    prompt = format_prompt(summary_data)

    print("\n🤖 Generating AI Summary using 'gemma:2b'...")

    try:
        response = ollama.chat(
            model='gemma:2b',
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes work productivity."},
                {"role": "user", "content": prompt}
            ]
        )

        summary = response['message']['content']
        print("\n🧠 AI Summary:")
        print(summary)

        save_summary(summary)
        show_notification(summary)

    except Exception as e:
        print("❌ Error generating AI summary:", e)

if __name__ == "__main__":
    get_ai_summary()
