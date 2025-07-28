# Auto-Start Work Tracker

## 🎯 **What This Does**

This tracker automatically starts when you turn on your laptop and tracks your 9-hour workday from that moment.

## ⏰ **How It Works**

1. **Auto-Start**: When you turn on your laptop and log in to Windows, the tracker starts automatically
2. **Login Time**: The exact time you turn on your laptop becomes your login time
3. **Logout Time**: 9 hours from your login time
4. **Progress Tracking**: Shows workday progress and countdown timer

## 🚀 **Setup (Already Done!)**

✅ Auto-start has been configured! The tracker will start automatically when you log in to Windows.

## 📱 **What You'll See**

A clean desktop window showing:
- 👤 **Your name** with weather (Hyderabad temperature)
- 🔓 **Login time** (when you turned on laptop)
- 🔒 **Logout time** (9 hours later)
- 📊 **Progress bar** (workday completion)
- ⏳ **Countdown timer** (time remaining)
- 📊 **Status** (hours completed)

## 🛠️ **Manual Control**

### To start the tracker manually:
```bash
python auto_start_tracker.py
```

### To remove auto-start:
```bash
.\remove_auto_start.bat
```

### To re-enable auto-start:
```bash
.\setup_auto_start.bat
```

## 📁 **Files Created**

- `auto_start_tracker.py` - The main tracker application
- `setup_auto_start.bat` - Sets up auto-start
- `remove_auto_start.bat` - Removes auto-start
- `logs/auto_login.json` - Saves your login/logout times

## 🎉 **Ready to Use!**

The tracker is now set up and will automatically start tomorrow when you turn on your laptop. No more manual starting needed! 