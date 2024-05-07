from datetime import datetime, timedelta

def month_to_number(month):
    match month:
        case "gen":
            return 1
        case "feb":
            return 2
        case "mar":
            return 3
        case "apr":
            return 4
        case "mag":
            return 5
        case "giu":
            return 6
        case "lug":
            return 7
        case "ago":
            return 8
        case "sep":
            return 9
        case "ott":
            return 10
        case "nov":
            return 11
        case "dic":
            return 12

# Scrivo l'orario nel formato
def subitotime_to_datetime(subitotime):
    subitotime = subitotime.lower()
    parts = subitotime.split()
    today = datetime.today()

    if parts[0] == "ieri":
        hour_min = parts[2].split(":")
        offer_time = today - timedelta(days=1)
    elif parts[0] =="oggi":
        hour_min = parts[2].split(":")
        offer_time = today
    else:
        hour_min = parts[3].split(":")
        # print(month_to_number(parts[1]) - 1)
        offer_time = today.replace(day=int(parts[0]), month=month_to_number(parts[1]))
    offer_time = offer_time.replace(hour=int(hour_min[0]), minute=int(hour_min[1]))
    return offer_time
