class QosObject:
    """Qos Object with tree format
    """
    object_type_map = {
        '1': 'policymap',
        '2': 'classmap',
        '3': 'matchStatement',
        '4': 'queueing',
        '5': 'randomDetect',
        '6': 'trafficShaping',
        '7': 'police',
        '8': 'set',
        '9': 'compression',
        '10': 'ipslaMeasure',
        '11': 'account'
    }
    obj_cfg_cls = dict()

    def __init__(self, obj_index, obj_type, cfg_index, parent=None):
        self.obj_index = obj_index
        self.parent = parent
        self.obj_type = obj_type
        self.cfg_index = cfg_index
        self.children = []

    @classmethod
    def register(cls, klass):
        """class decorator for automatically register
        object cfg class
        """
        if klass.TYPE in cls.obj_cfg_cls:
            raise RuntimeError('duplicated qos object type')
        cls.obj_cfg_cls[klass.TYPE] = klass
        return klass

    # @property
    # def parent(self):
    #     return self.parent

    # @property
    # def children(self):
    #     return self.children

    def add_child(self, obj):
        self.children.append(obj)

    def obj_cfg(self):
        if self.obj_type in self.obj_cfg_cls:
            return self.obj_cfg_cls[self.obj_type].to_dict(self.cfg_index)

    def to_dict(self):
        return {
            'obj_index': self.obj_index,
            'obj_type': self.object_type_map[self.obj_type],
            'cfg_index': self.cfg_index,
            'cfg': self.obj_cfg(),
            'children': [child.to_dict() for child in self.children]
        }
