from datetime import date, timedelta

def get_current_week_dates():
    today = date.today()

    week_dates = [
        (today - timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(7)
    ]
    return set(week_dates)
