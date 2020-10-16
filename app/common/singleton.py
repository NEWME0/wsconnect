

class SingletonMeta(type):
    """
        Meta class for singletons
        Usage:
            class MySingleton(metaclass=SingletonMeta):
                pass

            instance_1 = MySingleton()
            instance_2 = MySingleton()
            instance_3 = MySingleton()

            is_single = instance_1 is instance_2 is instance_3
            is_single => True
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
