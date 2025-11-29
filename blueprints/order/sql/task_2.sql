SELECT date_dep, time, Aeroport_DEPART, Aeroport_DEST, day_of_week, flight_num
from flights.departure
join flights.flight
using (idFlight)
where date_dep between '$from_date' and '$to_date'