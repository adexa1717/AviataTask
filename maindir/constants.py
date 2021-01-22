days = 30
cheapest_day_fly_redis_key = 'cheapest_flight_of_day'
flights = [{'from': 'ALA', 'to': 'TSE'},
           {'from': 'TSE', 'to': 'ALA'},
           {'from': 'ALA', 'to': 'MOW'},
           {'from': 'MOW', 'to': 'ALA'},
           {'from': 'ALA', 'to': 'CIT'},
           {'from': 'CIT', 'to': 'ALA'},
           {'from': 'TSE', 'to': 'MOW'},
           {'from': 'MOW', 'to': 'TSE'},
           {'from': 'TSE', 'to': 'LED'},
           {'from': 'LED', 'to': 'TSE'}]
flights_url = 'https://api.skypicker.com/flights'
check_flights_url = 'https://booking-api.skypicker.com/api/v0.1/check_flights'

server_host = '127.0.0.1'
server_port = '8080'
