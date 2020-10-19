import os
import json
from pathlib import Path

import yaml

from snmp_qos.qos_poller import CiscoQoSPoller
from snmp_qos.table import print_table


def main():
    OUTPUT = Path('.') / 'output'
    if not os.path.exists(OUTPUT):
        os.mkdir(OUTPUT)
    with open("device.yml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            community = data.get('community')
            inventory_list = data.get('inventory_list')
        except yaml.YAMLError as exc:
            print(exc)
            return
    for hostname in inventory_list:
        host = {
            'hostname': hostname,
            'community': community
        }
        print('host=', hostname)
        poller = CiscoQoSPoller(**host)
        service_policy_obj_list = poller.discovery()
        # class-map table
        print_table(service_policy_obj_list)
        file_name = os.path.join(OUTPUT, f'{hostname}.json')
        json_result = [item.to_dict() for item in service_policy_obj_list]
        with open(file_name, 'w') as fp:
            json.dump(json_result, fp, indent=4)


if __name__ == "__main__":
    main()
