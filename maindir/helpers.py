from redis import Redis

redis = Redis(host='redis', port=6379, db=0)


def key_names(days, flights, suffix):
    keys = list()
    for i in range(days + 1):
        for flight in flights:
            keys.append(f'{suffix}_{i}_from_{flight["from"]}_to_{flight["to"]}')
    return keys
