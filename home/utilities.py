from datetime import datetime, time, date, timedelta
import pytz


def localNow():
    return datetime.now(pytz.utc)


def endOfTomorrow():
    #TODO: take off the time to turn it into midnight
    return date.today() + timedelta(days=2)
