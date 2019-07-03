import py_sched.utils as utils
import unittest
import pytest
import ruamel.yaml

ScannerError = ruamel.yaml.error.MarkedYAMLError

class Test_Pysched_read(unittest.TestCase):
    """
    The class inherits from unittest
    """
    def test_read_not_file(self):
        '''iAttempt load of non-existent file'''

        def_file= ''

        self.assertRaises(FileNotFoundError,lambda: utils.read_yaml(def_file))
