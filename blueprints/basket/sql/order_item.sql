select *
from flights.departure
join flights.flight
using (idFlight)
where idDeparture = '$idDeparture'