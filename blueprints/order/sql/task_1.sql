SELECT Passenger_LastName, Passenger_FirstName, Pasport, date_dep
FROM flights.ticket
join flights.departure
using (iddeparture)
JOIN flights.flight
using (idflight)
WHERE (flight_num='$flight_num') and year(DATE_sell)='$year_sell'
