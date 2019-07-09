import py_sched.py_sched as pys
import py_sched.utils as utils
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

        my_sched = pys.Pysched()
        my_sched.set_def_file(def_file)

        expect = def_file
     
        assert my_sched.get_def_file() == expect

    def test_get_notset_def_file(self):
        '''Get unset def_file'''

        my_sched = pys.Pysched()

        self.assertRaises(AttributeError, lambda: my_sched.get_def_file())
        
    def test_read_yaml(self):
        '''Read valid definition yaml dictionary'''

        def_file = 'data/valid.yaml'

        my_sched = pys.Pysched()
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

        my_sched = pys.Pysched()
        self.assertRaises(ScannerError,lambda: my_sched.set_def_file(def_file))

    @pytest.mark.skip(reason="Test fail due to exception chaining")                   
    def test_read_not_file(self):
        '''Read valid definition yaml dictionary'''

        def_file= ''

        my_sched = pys.Pysched()
        self.assertRaises(ScannerError,lambda: my_sched.set_def_file(def_file))

    def test_load_def_file(self):
        '''Test load def file and all dependencies.'''

        def_file = 'data/valid.yaml'

        my_sched = pys.Pysched()
        my_sched.load_def_file(def_file)

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

    def test_load_dep_files(self):
        '''Test load def file and all dependencies.'''

        def_file = 'data/depends.yaml'

        my_sched = pys.Pysched()
        my_sched.load_def_file(def_file)

        expect = { 'system':{
                       'launch': 'aprun',
                       'tasks': '-n',
                       'ppn': '-N',
                       'threads': '-d'},
                   'account':{
                       'queue': 'arm',
                       'email': 'rjg20@bath.ac.uk',
                       'project': None},
                   'map':{
                       'info':{
                           'scheduler': 'PBSPRO',
                           'version': '18.2'},
                       'format':{
                     #  'shebang': '#!/bin/bash', should be system dependent rather than scheduler?
                           'hash': '#PBS'},
                       'map':{
                           '$SEPARATOR': '=',
                           'general':{
                               'name': '-N'},
                           'accounting':{
                               'queue': '-q',
                               'project': '-P',
                               'email': '-M'},
                           'resource':{
                               '$SUFFIX': '-l',
                               'nodes': 'select',
                               'ncpus': 'ncpus',
                               'ppn': None,
                               'tasks': None,
                               'threads': None,
                               'walltime': 'walltime',
                               'memory': 'mem'},
                           'io':{
                               'stdout': None,
                               'stderr': None}}},
                   'mod':{
                       'file': 'isambard-gnu-vasp.sh',
                       'script':[
                           'module swap PrgEnv-cray PrgEnv-gnu',
                           'module swap gcc/8.2.0 gcc/7.3.0']},
                   'pre':{
                       'file': 'pre-script.sh',
                       'script':[
                           'echo "Jobscript generated with py_sched"']},
                   'post':{
                       'file': 'post-script.sh',
                       'script':[
                           'echo "Thank you for using py_sched! Please shed with us again soon!"']}
                   }
        assert my_sched.get_def() == expect

    def test_dupl_def(self):
        '''Create a dupl definition and verify deep copy'''

        def_file = 'data/depends.yaml'

        my_sched = pys.Pysched()
        my_sched.load_def_file(def_file)

        my_sched.dupl_def()

        my_sched.dupl['system']=None

        assert my_sched.get_def() != my_sched.dupl

    def test_write_jobscript(self):
        '''Iteratively write and test jobscript'''

        def_file = 'data/balena_vasp.yaml'

        my_sched = pys.Pysched()
        my_sched.load_def_file(def_file)
        my_sched.dupl_def()

        expect_file = 'data/jobscripts/balena-vasp-full.sub'
        expect = utils.read_script(expect_file)

        my_sched.write_header()
        assert my_sched.get_job() == expect[0:4]

        my_sched.write_general()
        assert my_sched.get_job() == expect[0:7]

        my_sched.write_accounting()
        assert my_sched.get_job() == expect[0:12]

        my_sched.write_resource()
        assert my_sched.get_job() == expect[0:18]

        my_sched.write_io()
        assert my_sched.get_job() == expect[0:22]

        my_sched.write_modules()
        assert my_sched.get_job() == expect[0:29]

        my_sched.write_threads()
        assert my_sched.get_job() == expect[0:32]

        my_sched.write_proc()
        assert my_sched.get_job() == expect[0:35]

@pytest.mark.parametrize('nodes,ppn,threads,tasks',[
        (1,24,1,24),
        (2,24,1,48),
        (3,12,2,36)])
def test_set_tasks(nodes, ppn, threads, tasks):
    '''Check that tasks is automatically generated correctly'''

    def_file = 'data/balena_vasp.yaml'

    my_sched = pys.Pysched()
    my_sched.load_def_file(def_file)
    my_sched.dupl_def()

    my_sched.dupl['resource']['nodes'] = nodes
    my_sched.dupl['resource']['ppn'] = ppn
    my_sched.dupl['resource']['threads'] = threads

    my_sched._set_tasks()

    assert  my_sched.dupl['resource']['tasks'] == tasks



         


