select *
from flights.departure
join flights.flight
using (idFlight)
where date_dep>current_date()
group by (idFlight)