"""
SNMP Poller for Cisco Devices
"""

from collections import defaultdict

from snmp_qos.poller import BasePoller
from snmp_qos.cbqos.qos_object import QosObject
from snmp_qos.cbqos.service_policy import ServicePolicy


class CiscoQoSPoller(BasePoller):

    def get_interface_descr_alias(self):
        oid_ifdescr = '1.3.6.1.2.1.2.2.1.2'
        oid_alias = '1.3.6.1.2.1.31.1.1.1.18'
        result_if_descr = self.walk(oid_ifdescr)
        result_if_alias = self.walk(oid_alias)

        result_if_descr = self.process_result_with_index(result_if_descr)
        result_if_alias = self.process_result_with_index(result_if_alias)

        # merge
        result = defaultdict(dict)
        for if_index in result_if_descr:
            result[if_index]['name'] = result_if_descr[if_index]
            result[if_index]['description'] = result_if_alias.get(if_index)
        return result

    def get_policy_map_cfg(self):
        oid_qos_policy_map_name = '1.3.6.1.4.1.9.9.166.1.6.1.1.1'
        return self.process_result_with_index(
            result=self.walk(oid_qos_policy_map_name),
            index_level=1
        )

    def get_class_map_cfg(self):
        oid_qos_class_map_name = '1.3.6.1.4.1.9.9.166.1.7.1.1.1'
        return self.process_result_with_index(
            result=self.walk(oid_qos_class_map_name),
            index_level=1
        )

    def get_match_statement(self):
        oid_qos_match_statement_name = '1.3.6.1.4.1.9.9.166.1.8.1.1.1'
        return self.process_result_with_index(
            result=self.walk(oid_qos_match_statement_name),
            index_level=1
        )

    def process_result_with_index(self, result, index_level=1):
        """process snmp walk result and return dict
        for index level 1
             [['1.3.6.1.4.1.9.9.166.1.1.1.1.3.225', '1'], ['1.3.6.1.4.1.9.9.166.1.1.1.1.3.1456', '1']]
        will return
             {
                 '225': 1,
                 '1456': 1
             }
        for index level 2
             [['1.3.6.1.4.1.9.9.166.1.5.1.1.2.225.225', '11335344'], ['1.3.6.1.4.1.9.9.166.1.5.1.1.2.225.659059', '9526675'], 
             ['1.3.6.1.4.1.9.9.166.1.5.1.1.2.225.979395', '10733267'], ['1.3.6.1.4.1.9.9.166.1.5.1.1.2.2912.5242082', '1594']]
        will return
             {
                 '225': {
                     '225': '11335344,
                     '659059': 9526675,
                     '979395': '10733267
                 },
                 '2912': {
                     '5242082': '1594'
                 }
             }
        """
        new_result = defaultdict(dict)
        for oid_index, value in result:
            if index_level == 1:
                new_result[oid_index.split('.')[-1]] = value
            elif index_level == 2:
                index_1, index_2 = oid_index.split('.')[-2:]
                new_result[index_1][index_2] = value
        return new_result

    def discovery(self):

        # get policy map cfg
        QosObject.obj_cfg_cls['1'].cfg_dict = self.get_policy_map_cfg()
        # get class map cfg
        QosObject.obj_cfg_cls['2'].cfg_dict = self.get_class_map_cfg()
        # get match statement cfg
        QosObject.obj_cfg_cls['3'].cfg_dict = self.get_match_statement()

        oid_qos_cfg_index = '1.3.6.1.4.1.9.9.166.1.5.1.1.2'
        oid_qos_object_type = '1.3.6.1.4.1.9.9.166.1.5.1.1.3'
        oid_qos_parent_index = '1.3.6.1.4.1.9.9.166.1.5.1.1.4'
        oid_qos_policy_map_name = '1.3.6.1.4.1.9.9.166.1.6.1.1.1'

        oid_qos_service_policy_if_direction = '1.3.6.1.4.1.9.9.166.1.1.1.1.3'
        oid_qos_service_policy_if_index = '1.3.6.1.4.1.9.9.166.1.1.1.1.4'

        oid_ifdescr = '1.3.6.1.2.1.2.2.1.2'
        oid_alias = '1.3.6.1.2.1.31.1.1.1.18'

        interface_dict = self.get_interface_descr_alias()

        qos_object_cfg_index_dict = self.process_result_with_index(
            result=self.walk(oid=oid_qos_cfg_index),
            index_level=2
        )
        qos_object_type_dict = self.process_result_with_index(
            result=self.walk(oid=oid_qos_object_type),
            index_level=2
        )

        qos_object_parent_index_dict = self.process_result_with_index(
            result=self.walk(oid=oid_qos_parent_index),
            index_level=2
        )
        qos_service_policy_if_direction_dict = self.process_result_with_index(
            result=self.walk(oid_qos_service_policy_if_direction),
            index_level=1
        )
        qos_service_policy_if_index_dict = self.process_result_with_index(
            result=self.walk(oid_qos_service_policy_if_index),
            index_level=1
        )

        service_policy_obj_list = []
        for service_index, value in qos_object_parent_index_dict.items():
            qos_objs_dict = dict()
            value_items_list = list(value.items())
            root_obj_id = [item[0]
                           for item in value_items_list if item[1] == '0'][0]

            def generate_obj_tree(value_items_list):
                for pos, value in enumerate(value_items_list):
                    obj_index, parent_index = value
                    if obj_index in qos_objs_dict:
                        continue
                    if parent_index == '0':  # this is root object
                        qos_obj = QosObject(
                            obj_index=obj_index,
                            obj_type=qos_object_type_dict[service_index][obj_index],
                            cfg_index=qos_object_cfg_index_dict[service_index][obj_index]
                        )
                        qos_objs_dict[obj_index] = qos_obj
                        continue
                    if parent_index not in qos_objs_dict:
                        tmp_items_list = value_items_list[pos+1:]
                        generate_obj_tree(tmp_items_list)
                    if parent_index not in qos_objs_dict:
                        continue
                    # find the parent object, and add children
                    parent_obj = qos_objs_dict[parent_index]
                    qos_obj = QosObject(
                        obj_index=obj_index,
                        obj_type=qos_object_type_dict[service_index][obj_index],
                        cfg_index=qos_object_cfg_index_dict[service_index][obj_index],
                        parent=parent_obj
                    )
                    parent_obj.add_child(qos_obj)
                    qos_objs_dict[obj_index] = qos_obj

            generate_obj_tree(value_items_list)
            service_policy_obj = ServicePolicy(
                policy_index=service_index,
                direction=qos_service_policy_if_direction_dict[service_index],
                interface=interface_dict[qos_service_policy_if_index_dict[service_index]],
                qos_root_obj=qos_objs_dict.get(root_obj_id)
            )
            service_policy_obj_list.append(service_policy_obj)

        return service_policy_obj_list
