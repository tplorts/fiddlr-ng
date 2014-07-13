from datetime import datetime, time, date, timedelta
import pytz


def localNow():
    return datetime.now(pytz.utc)


def endOfTomorrow():
    return localNow().date() + timedelta(days=2)
