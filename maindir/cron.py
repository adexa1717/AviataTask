import json
import pprint
from datetime import datetime, timedelta

import requests
from redis import Redis

from constants import *
from helpers import key_names, redis


def main():
    print('start', flush=True)
    flag = datetime.now()
    second_flag = datetime.now()
    count = 1
    second_count = 1

    while True:
        if flag <= datetime.now():
            print("flights LOOP", count, flush=True)
            flag = datetime.now() + timedelta(hours=24)
            count += 1
            for flight in flights:
                flights_params = {
                    'fly_from': flight['from'],
                    'fly_to': flight['to'],
                    'adults': 1,
                    'curr': 'USD',
                    'partner': 'picky',
                    'adult_hold_bag': 1
                }
                for i in range(days + 1):
                    print('in process', flush=True)
                    day = (datetime.now() + timedelta(days=i)).strftime('%d/%m/%Y')
                    flights_params.update({'date_from': day, 'date_to': day, })
                    day_flight_data = get_flights_and_return_cheapest(url=flights_url, params=flights_params)
                    redis.set(f'{cheapest_day_fly_redis_key}_{i}_from_{flight["from"]}_to_{flight["to"]}',
                              json.dumps(day_flight_data))
        if second_flag <= datetime.now():
            second_flag = datetime.now() + timedelta(hours=1)
            second_count += 1
            print("check_flights LOOP", second_count, flush=True)
            check_flights_params = {
                'v': 2,
                'bnum': 1,
                'pnum': 1,
                'affily': 'picky_{market}',
                'currency': 'USD',
                'visitor_uniqid': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                'adults': 1,
            }
            flight_keys_for_check = key_names(days=days, flights=flights, suffix=cheapest_day_fly_redis_key)
            print('in first loop', flush=True)
            for key in flight_keys_for_check:
                print('in second loop', flush=True)
                redis_data = redis.get(key)
                if redis_data is not None:
                    redis_json_data = json.loads(redis_data)
                    if redis_json_data != 'empty':
                        check_flights_params.update({'booking_token': redis_json_data['booking_token']})
                        if check_flight(url=check_flights_url, params=check_flights_params):
                            data_to_redis = update_cheapest_flight(url=flights_url,
                                                                   fly_from=redis_json_data['fly_from'],
                                                                   fly_to=redis_json_data['fly_to'],
                                                                   day=redis_json_data['departure_date'])
                            data_to_redis.update({'checked': True})
                            redis.set(key, json.dumps(data_to_redis))


def get_flights_and_return_cheapest(url, params):
    flights_response = requests.get(url=url, params=params)
    data = flights_response.json()['data']
    return minimum_of_flight_response(data)


def minimum_of_flight_response(data):
    if len(data) > 0:
        minimum_cost_flight = min(data, key=lambda y: y['price'])
        cheapest_flight = {
            'fly_from': minimum_cost_flight['flyFrom'],
            'city_from': minimum_cost_flight['cityFrom'],
            'fly_to': minimum_cost_flight['flyTo'],
            'city_to': minimum_cost_flight['cityTo'],
            'fly_duration': minimum_cost_flight['fly_duration'],
            'airlines': minimum_cost_flight['airlines'],
            'booking_token': minimum_cost_flight['booking_token'],
            'departure_date': datetime.utcfromtimestamp(minimum_cost_flight['dTime']).strftime(
                '%d/%m/%Y'),
            'departure_datetime': datetime.utcfromtimestamp(minimum_cost_flight['dTime']).strftime(
                '%d/%m/%YT%H:%M:%S'),
            'arrival_datetime': datetime.utcfromtimestamp(minimum_cost_flight['aTime']).strftime(
                '%d/%m/%YT%H:%M:%S'),
        }
    else:
        cheapest_flight = 'empty'
    return cheapest_flight


def update_cheapest_flight(url, fly_from, fly_to, day):
    params = {
        'fly_from': fly_from,
        'fly_to': fly_to,
        'adults': 1,
        'curr': 'USD',
        'partner': 'picky',
        'adult_hold_bag': 1,
        'date_from': day,
        'date_to': day,
    }
    flights_response = requests.get(url=url, params=params)
    data = flights_response.json()['data']
    return minimum_of_flight_response(data)


def check_flight(url, params):
    check_flight_response = requests.get(url=url, params=params)
    return check_flight_response.json()['flights_invalid']


if __name__ == '__main__':
    main()
