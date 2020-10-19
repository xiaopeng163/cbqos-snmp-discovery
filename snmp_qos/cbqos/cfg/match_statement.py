
from snmp_qos.cbqos.qos_object import QosObject
from snmp_qos.cbqos.cfg.base import CfgBase


@QosObject.register
class MatchStatement(CfgBase):

    TYPE = '3'
    TYPE_STR = 'match statement'
