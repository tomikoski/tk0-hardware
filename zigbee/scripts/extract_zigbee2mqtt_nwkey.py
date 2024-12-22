import yaml

with open("/opt/zigbee2mqtt/data/configuration.yaml") as stream:
    try:
        y = yaml.safe_load(stream)
        print("PLAIN")
        print(y['advanced']['network_key'])
        h = ""
        for x in y['advanced']['network_key']:
            h += f'{x:02x}:'
        print("HEX")
        print(h[:-1])
    except yaml.YAMLError as exc:
        print(exc)

