# Copyright (C) 2006-2007 Dan Pascu. See LICENSE for details.
#

"""Miscellaneous utility functions and classes"""

__all__ = ['Singleton', 'Null']

from new import instancemethod
from application.python.decorator import preserve_signature

class Singleton(type):
    """Metaclass for making singletons"""
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls._instances = {}
    def __call__(cls, *args, **kw):
        if not hasattr(cls, '_instance_creator'):
            @preserve_signature(cls.__init__)
            def instance_creator(cls, *args, **kwargs):
                key = (args, tuple(sorted(kwargs.iteritems())))
                try:
                    hash(key)
                except TypeError:
                    raise TypeError("cannot have singletons for classes with unhashable arguments")
                if key not in cls._instances:
                    cls._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)
                return cls._instances[key]
            cls._instance_creator = instancemethod(instance_creator, cls, type(cls))
        return cls._instance_creator(*args, **kw)

class Null(object):
    """Instances of this class always and reliably "do nothing"."""
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return self
    def __repr__(self): return self.__class__.__name__
    def __nonzero__(self): return 0
    def __eq__(self, other): return isinstance(other, self.__class__)
    def __ne__(self, other): return not isinstance(other, self.__class__)
    def __getattr__(self, name): return self
    def __setattr__(self, name, value): return self
    def __delattr__(self, name): return self
    __str__ = __repr__

