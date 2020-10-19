import json


class ServicePolicy:

    direction_map = {
        '1': 'input',
        '2': 'output'
    }

    def __init__(self, policy_index, direction, interface, qos_root_obj):
        self.policy_index = policy_index
        self.direction = direction
        self.interface = interface
        self.qos_root_obj = qos_root_obj

    def to_dict(self):
        return {
            'policy_index': self.policy_index,
            'direction': self.direction_map[self.direction],
            'interface': self.interface,
            'qos_obj': self.qos_root_obj.to_dict() if self.qos_root_obj else {}
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def class_map_dict(self, level=1):
        # level 1 class-map
        # cbQosCMPrePolicyByte64  1.3.6.1.4.1.9.9.166.1.15.1.1.6
        # cbQosCMPostPolicyByte64  1.3.6.1.4.1.9.9.166.1.15.1.1.10
        # cbQosCMDropByte64 1.3.6.1.4.1.9.9.166.1.15.1.1.17
        result = {
            'policy_index': self.policy_index,
            'direction': self.direction_map[self.direction],
            'interface': self.interface,
            'policy_name': self.qos_root_obj.obj_cfg()['name'],
            'classmap': []
        }
        for qos_obj in self.qos_root_obj.children:
            if qos_obj.obj_type == '2':
                result['classmap'].append(
                    {
                        'object_index': qos_obj.obj_index,
                        'cfg_name': qos_obj.obj_cfg()['name']
                    }
                )
        return result
