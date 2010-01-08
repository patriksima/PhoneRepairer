#!/usr/bin/env python
# coding: utf-8

class SingletonException(Exception):
    pass

class MetaSingleton(type):
    def __new__(metaclass, strName, tupBases, dict):
        if dict.has_key('__new__'):
            raise SingletonException, 'Can not override __new__ in a Singleton'
        return super(MetaSingleton,metaclass).__new__(metaclass, strName, tupBases, dict)

    def __call__(cls, *lstArgs, **dictArgs):
        raise SingletonException, 'Singletons may only be instantiated through getInstance()'

class Singleton(object):
    __metaclass__ = MetaSingleton

    def getInstance(cls, *lstArgs):
        """
        Call this to instantiate an instance or retrieve the existing instance.
        If the singleton requires args to be instantiated, include them the first
        time you call getInstance.
        """
        if cls._isInstantiated():
            if len(lstArgs) != 0:
                raise SingletonException, 'If no supplied args, singleton must already be instantiated, or __init__ must require no args'
        else:
            if len(lstArgs) != cls._getConstructionArgCountNotCountingSelf():
                raise SingletonException, 'If the singleton requires __init__ args, supply them on first instantiation'
            instance = cls.__new__(cls)
            instance.__init__(*lstArgs)
            cls.cInstance = instance
        return cls.cInstance
    getInstance = classmethod(getInstance)

    def _isInstantiated(cls):
        return hasattr(cls, 'cInstance')
    _isInstantiated = classmethod(_isInstantiated)

    def _getConstructionArgCountNotCountingSelf(cls):
        return cls.__init__.im_func.func_code.co_argcount - 1
    _getConstructionArgCountNotCountingSelf = classmethod(_getConstructionArgCountNotCountingSelf)

    def _forgetClassInstanceReferenceForTesting(cls):
        """
        This is designed for convenience in testing -- sometimes you
        want to get rid of a singleton during test code to see what
        happens when you call getInstance() under a new situation.

        To really delete the object, all external references to it
        also need to be deleted.
        """
        delattr(cls,'cInstance')
    _forgetClassInstanceReferenceForTesting = classmethod(_forgetClassInstanceReferenceForTesting)

if __name__ == '__main__':
	class A(Singleton):
		def __init__(self, arg1, arg2):
			super(A, self).__init__()
			self.arg1 = arg1
			self.arg2 = arg2

	a1 = A.getInstance('arg1 value', 'arg2 value')
	a2 = A.getInstance()
	print a1, a2
	print a1.arg1, a1.arg2
	print a2.arg1, a2.arg2
	print a1.arg1 is a2.arg1
	print a1 is a2
