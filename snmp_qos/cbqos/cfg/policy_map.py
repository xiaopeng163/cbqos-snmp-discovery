
from snmp_qos.cbqos.qos_object import QosObject
from snmp_qos.cbqos.cfg.base import CfgBase


@QosObject.register
class PolicyMap(CfgBase):

    TYPE = '1'
    TYPE_STR = 'policymap'
