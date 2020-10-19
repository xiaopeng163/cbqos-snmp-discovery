class CfgBase:

    cfg_dict = dict()

    @classmethod
    def has_cfg(cls):
        return bool(cls.cfg_dict)

    @classmethod
    def to_dict(cls, cfg_index):
        return {
            'name': cls.cfg_dict.get(cfg_index)
        }
