import abc
import importlib


class BaseDriver(abc.ABCMeta):
    drivers = {}

    def __new__(cls, name, bases, namespace):
        instance = abc.ABCMeta.__new__(cls, name, bases, namespace)

        if isinstance(instance.name, str):
            cls.drivers[instance.name] = instance

        return instance

    @classmethod
    def get(cls, name):
        if name not in cls.drivers:
            try:
                importlib.import_module('swascale.drivers.%s' % name)
            except ImportError as e:
                print(e)
        return cls.drivers[name]


class Driver(metaclass=BaseDriver):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()
