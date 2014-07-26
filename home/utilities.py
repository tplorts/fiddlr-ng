from datetime import datetime, time, date, timedelta
import pytz
from models import Uzer

def localNow():
    return datetime.now(pytz.utc)


def endOfTomorrow():
    return localNow().date() + timedelta(days=2)



def getUzer(request):
    if request.user.is_authenticated:
        return Uzer.objects.get(user=request.user.pk)
    return None
