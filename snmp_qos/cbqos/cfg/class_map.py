
from snmp_qos.cbqos.qos_object import QosObject
from snmp_qos.cbqos.cfg.base import CfgBase


@QosObject.register
class ClassMap(CfgBase):

    TYPE = '2'
    TYPE_STR = 'classmap'
