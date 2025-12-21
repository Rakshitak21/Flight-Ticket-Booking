from datetime import datetime, timedelta
from django.db.models import Count
from flight.models import Week, Place, Flight
from tqdm import tqdm

def get_number_of_lines(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def createWeekDays():
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    for i, day in enumerate(days):
        Week.objects.get_or_create(number=i, defaults={"name": day})


def addPlaces():
    print("Adding Airports...")

    total = get_number_of_lines("./Data/airports.csv")
    with open("./Data/airports.csv") as file:
        for i, line in tqdm(enumerate(file), total=total):
            if i == 0:
                continue
            city, airport, code, country = [x.strip() for x in line.split(",")]

            # Avoid duplicates
            if Place.objects.filter(code=code).exists():
                continue

            Place.objects.create(
                city=city,
                airport=airport,
                code=code,
                country=country,
            )
    print("Done.\n")


def cleanDuplicatePlaces():
    """ Remove duplicate airport entries from DB """
    duplicates = (
        Place.objects.values("code")
        .annotate(c=Count("code"))
        .filter(c__gt=1)
    )
    
    for dup in duplicates:
        code = dup["code"]
        places = Place.objects.filter(code=code)
        # keep first, delete others
        places.exclude(id=places.first().id).delete()


def addDomesticFlights():
    print("Adding Domestic Flights...")
    total = get_number_of_lines("./Data/domestic_flights.csv")
    with open("./Data/domestic_flights.csv") as file:
        for i, line in tqdm(enumerate(file), total=total):
            if i == 0:
                continue

            data = [x.strip() for x in line.split(",")]

            origin = data[1]
            destination = data[2]
            depart_time = datetime.strptime(data[3], "%H:%M:%S").time()
            week_no = int(data[4])
            duration = timedelta(hours=int(data[5][:2]), minutes=int(data[5][3:5]))
            arrive_time = datetime.strptime(data[6], "%H:%M:%S").time()
            flight_no = data[8]
            airline = data[10]
            eco = float(data[11] or 0)
            bus = float(data[12] or 0)
            fst = float(data[13] or 0)

            try:
                a1 = Flight.objects.create(
                    origin=Place.objects.get(code=origin),
                    destination=Place.objects.get(code=destination),
                    depart_time=depart_time,
                    duration=duration,
                    arrival_time=arrive_time,
                    plane=flight_no,
                    airline=airline,
                    economy_fare=eco,
                    business_fare=bus,
                    first_fare=fst,
                )
                a1.depart_day.add(Week.objects.get(number=week_no))
                a1.save()

            except Exception as e:
                print(e)
                continue

    print("Done.\n")


def addInternationalFlights():
    print("Adding International Flights...")
    total = get_number_of_lines("./Data/international_flights.csv")
    with open("./Data/international_flights.csv") as file:
        for i, line in tqdm(enumerate(file), total=total):
            if i == 0:
                continue

            data = [x.strip() for x in line.split(",")]

            origin = data[1]
            destination = data[2]
            depart_time = datetime.strptime(data[3], "%H:%M:%S").time()
            week_no = int(data[4])
            duration = timedelta(hours=int(data[5][:2]), minutes=int(data[5][3:5]))
            arrive_time = datetime.strptime(data[6], "%H:%M:%S").time()
            flight_no = data[8]
            airline = data[10]
            eco = float(data[11] or 0)
            bus = float(data[12] or 0)
            fst = float(data[13] or 0)

            try:
                a1 = Flight.objects.create(
                    origin=Place.objects.get(code=origin),
                    destination=Place.objects.get(code=destination),
                    depart_time=depart_time,
                    duration=duration,
                    arrival_time=arrive_time,
                    plane=flight_no,
                    airline=airline,
                    economy_fare=eco,
                    business_fare=bus,
                    first_fare=fst,
                )
                a1.depart_day.add(Week.objects.get(number=week_no))
                a1.save()

            except Exception as e:
                print(e)
                continue

    print("Done.\n")
