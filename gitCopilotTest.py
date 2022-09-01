import datetime

def calculateDaysBetweenDates(startDate, endDate):
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    return (endDate - startDate).days

print(calculateDaysBetweenDates("2020-01-01", "2020-01-06"))
