import py_sched.utils as utils

class Pysched:
    '''Class to hold details of scheduled job'''

    def __init__(self, def_file=None):
        '''Initialise schedule object.

        Optionally with `def_file` containing the job's schedule definition
        '''

        if def_file is not None:
            self.set_def_file(def_file)

    def set_def_file(self, def_file):
        '''Set definition file and read in the dictionary it contains

        sets self._def_file to passed argument, expected to be definition filename

        and calls self._read_yaml(self_def_file)
        '''
        
        self._def_file = def_file

        self._def = utils.read_yaml(self._def_file)

    def get_def_file(self):
        '''Return def_file name'''

        try:
            return self._def_file
        except AttributeError:
            raise AttributeError('Pysched definition file: def_file not set')
      
    def get_def(self):
        '''Return definition dictionary'''

        try:
            return self._def
        except AttributeError:
            raise AttributeError('Pysched definition: def not set')
        
