from datetime import date

def string2date(dateString):
    result = date.strptime(dateString, "%Y-%m-%d")
    return result