from py_sched import utils
import os
from copy import deepcopy

class Pysched:
    '''Class to hold details of scheduled job'''

    def __init__(self, def_file=None):
        '''Initialise schedule object.

        Optionally with `def_file` containing the job's schedule definition
        '''

        self._jobscript = []

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

    def load_dep_yamls(self,):
        '''Load dependent yaml dependencies for:

        keys -> in ['system', 'account', 'map']

        which contain dictionaries with a sole key 'file'
        Load yaml file as new dictionary to replace 'file'
        '''

        yamls = ['system', 'account', 'map']

        for key in yamls:
            if (key in self._def) and (type(self._def[key] == dict)):
                if ('file' in self._def[key]):
                    if len(self._def[key]) == 1:
                        filepath=os.path.join(key,self._def[key]['file'])
                        self._def[key] = utils.read_yaml(filepath)
                    else:
                        raise Exception('File defined in '+key+
                                        ', but other keys present in dict')

    def load_dep_scripts(self):
        '''Load dependent scripts for

        keys -> in ['mod', 'pre', 'post']
        
        which contain dictionaries with a sole key 'file'
        Load script into additional dictionary key 'script' as list.
        '''

        scripts = ['mod', 'pre', 'post']

        for key in scripts:
            if (key in self._def) and (type(self._def[key] == dict)):
                if ('file' in self._def[key]):
                    filepath=os.path.join(key,self._def[key]['file'])
                    self._def[key]['script'] = utils.read_script(filepath)

    def load_def_file(self, def_file):
       '''Set def file and load it and all dependent files'''

       self.set_def_file(def_file)       
       self.load_dep_yamls()
       self.load_dep_scripts()

    def dupl_def(self):
        '''Make a user accessible deep copy of def'''

        self.dupl = deepcopy(self._def)

    def write_header(self):
        '''Write the header of the jobscript

        Adds shebang and optional (verbose) py_sched header and template title
        '''

        # All systems currently use bash
        self._jobscript.append('#!/bin/bash')

        # options/verbose does not need to be specified so default False
        try:
            if self.dupl['options']['verbose']:
                self._jobscript.append('# Created with py_sched using template:')
                self._jobscript.append('# '+self.dupl['title'])
        except:
            return

    def write_general(self):
        '''Write general parameters for jobscript
        
        Write optional verbose section header and jobname
        '''
        
        self._jobscript.append('')

        try:
            if self.dupl['options']['verbose']:
                self._jobscript.append('# General job parameters')
        except:
            pass

        for key in self.dupl['general']:
            self._jobscript.append( self._generate_shed('general', key) )

    def _generate_shed(self, key1, key2):
        '''Generate a scheduler instruction'''

        instruction = self.dupl['map']['format']['hash']
        instruction = instruction + ' '
        if '$SUFFIX' in self.dupl['map']['map'][key1]:
            instruction = instruction + self.dupl['map']['map'][key1]['$SUFFIX']
            instruction = instruction + ' '

        instruction = instruction + self.dupl['map']['map'][key1][key2]

        instruction = instruction + self.dupl['map']['map']['$SEPARATOR']

        instruction = instruction + self.dupl[key1][key2]

        return instruction 

    def get_job(self):
        '''Return the jobscript list'''

        return self._jobscript
