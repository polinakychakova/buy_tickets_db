SELECT *
FROM flights.ticket
join flights.departure
using (iddeparture)
JOIN flights.flight
using (idflight)
WHERE (flight_num='$flight_num')