import datetime

def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

a = datetime.datetime.now().time()
c = 0.2
b = addSecs(a, c)
print a
print b
