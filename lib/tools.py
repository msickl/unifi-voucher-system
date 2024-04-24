from datetime import datetime, timedelta

def ToUnifyTime(unit):
    if unit == 'minutes':
        return 1
    elif unit == 'hours':
        return 60
    elif unit == 'days':
        return 1440
    else:
        return 1440

def GetExpireDate(client):
    timespan = client['expire'] * ToUnifyTime(client['expire_unit'])

    if client.get('lastcreationdate'):
        date = client['lastcreationdate']
    else:
        date = datetime.now().isoformat()

    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f") + timedelta(minutes=timespan)

def IsVoucherExpired(client):
    if client.get('lastcreationdate'):
        expire_date = GetExpireDate(client)
        if datetime.now() < expire_date:
            return 0
        else:
            return 1
    else:
        return 1

def DateTimeNowToISODate():
    current_date_time = datetime.now()
    return current_date_time.isoformat()