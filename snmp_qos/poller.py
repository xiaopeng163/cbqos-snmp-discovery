import re

from pysnmp.hlapi import \
    bulkCmd, getCmd, nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, \
    ContextData, ObjectType, ObjectIdentity, UsmUserData

from snmp_qos.const import SNMP_VERSION_2C, SNMP_VERSION_3


class BasePoller:
    """
    Snmp Mib Poller
    v2c:
    :hostname: device ip or hostname, string format
    :community: snmp community
    v3:
    :user_name: user name auth
    :auth_key: auth key auth
    :priv_key: privacy key auth
    :version: snmp verison ['2c', '3'], 2c by default
    :snmp_port: default set to be 161
    """

    hostname = None
    community = None
    snmp_port = 161
    user_name = None
    auth_key = None
    priv_key = None
    version = SNMP_VERSION_2C

    def __init__(self, **kwargs):
        super(BasePoller, self).__init__()
        cls_ = type(self)
        for k in kwargs:
            if hasattr(cls_, k):
                setattr(self, k, kwargs[k])

    def _to_list(self, snmp_ret, oid=None):
        """
        parse snmp return & return list
        """
        mib_ret = []
        for (error_indication,
             error_status,
             error_index,
             var_binds) in snmp_ret:
            if error_indication:
                break
            elif error_status:
                print('%s at %s', error_status.prettyPrint(),
                      (error_index and var_binds[int(error_index) - 1][0] or '?'))
                break
            else:
                for var_bind in var_binds:
                    name, value = var_bind
                    name = str(name)
                    value = str(value)
                    if value:
                        mib_ret.append([name, value])
            if oid:
                mib_ret = [mib for mib in mib_ret if re.match(
                    r'%s' % oid, str(mib[-2]))]
        return mib_ret

    def get_auth(self):
        """
        get auth by snmp version
        """
        auth = None
        if self.version == SNMP_VERSION_2C:
            auth = CommunityData(self.community)
        elif self.version == SNMP_VERSION_3:
            auth = UsmUserData(self.user_name,
                               authKey=self.auth_key, privKey=self.priv_key)
        return auth

    def walk(self, oid):
        snmp_ret = nextCmd(SnmpEngine(),
                                CommunityData(self.community),
                                UdpTransportTarget(
                                    (self.hostname, self.snmp_port)),
                                ContextData(),
                                ObjectType(ObjectIdentity(oid)),
                                lexicographicMode=False)
        return self._to_list(snmp_ret=snmp_ret)   

    def get_cmd(self, oid):
        """
        SNMP get
        """
        snmp_ret = getCmd(SnmpEngine(),
                               self.get_auth(),
                               UdpTransportTarget(
                                   (self.hostname, self.snmp_port)),
                               ContextData(),
                               ObjectType(ObjectIdentity(oid)))
        return self._to_list(snmp_ret=snmp_ret)
