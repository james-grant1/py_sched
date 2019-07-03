from py_sched import py_sched
import unittest
import pytest
import ruamel.yaml

ScannerError = ruamel.yaml.error.MarkedYAMLError

class Test_Pysched_read(unittest.TestCase):
    """
    The class inherits from unittest
    """
    def test_get_set_def_file(self):
        '''Set and get def_file'''

        def_file = 'data/valid.yaml'

        my_sched = py_sched.Pysched()
        my_sched.set_def_file(def_file)

        expect = def_file
     
        assert my_sched.get_def_file() == expect

    def test_get_notset_def_file(self):
        '''Get unset def_file'''

        my_sched = py_sched.Pysched()

        self.assertRaises(AttributeError, lambda: my_sched.get_def_file())
        
    def test_read_yaml(self):
        '''Read valid definition yaml dictionary'''

        def_file = 'data/valid.yaml'

        my_sched = py_sched.Pysched()
        my_sched.set_def_file(def_file)

        expect = { 'name':'test',
                   'queue':'default',
                   'project':'my_project',
                   'email':'rjg20@bath.ac.uk',
                   'nodes':4,
                   'ppn':16,
                   'tasks':64,
                   'threads':1,
                   'walltime':'12:0:0',
                   'memory':'20gb',
                   'stdout':'StdOut.o.%j',
                   'stderr':'StdEdd.e.%j',
                 }

        assert my_sched.get_def() == expect
                   
    def test_read_not_yaml(self):
        '''Read valid definition yaml dictionary'''

        def_file = 'data/not_valid.yaml'

        my_sched = py_sched.Pysched()
        self.assertRaises(ScannerError,lambda: my_sched.set_def_file(def_file))

    @pytest.mark.skip(reason="Test fail due to exception chaining")                   
    def test_read_not_file(self):
        '''Read valid definition yaml dictionary'''

        def_file= ''

        my_sched = py_sched.Pysched()
        self.assertRaises(ScannerError,lambda: my_sched.set_def_file(def_file))
