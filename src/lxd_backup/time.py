from arrow import Arrow

def today():
    return Arrow.utcnow().format('YYYY-MM-DD')

def day():
    return int(Arrow.utcnow().format('DD'))

def weekday():
    return Arrow.utcnow().weekday()

def month():
    return int(Arrow.utcnow().format('MM'))

