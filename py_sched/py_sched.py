from py_sched import utils
import os
from copy import deepcopy

class Pysched:
    '''Class to hold details of scheduled job'''

    def __init__(self, def_file=None):
        '''Initialise schedule object.

        Optionally with `def_file` containing the job's schedule definition
        '''

        self._js_comps = {}
        self._js_sections = [ 'header',
                            'general',
                            'accounting',
                            'resource',
                            'io',
                            'mod',
                            'threads',
                            'pre',
                            'proc',
                            'post']
        self._jobscript = []

        self._pys_short = '# Created with py_sched using template:'

        if def_file is not None:
            self.set_def_file(def_file)

        self._initialise_sections()

    def _initialise_sections(self):
        '''Initiase _js_comps with sections defined in _js_sections'''

        for section in self._js_sections:
            self._js_comps[section] = []

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
        
        Componenets are written to _js_sections['header']

        Adds shebang and optional (verbose) py_sched header and template title
        '''

        this_list = []
        this_key = 'header'

        self._js_comps[this_key] = []

        # All systems currently use bash
        this_list.append('#!/bin/bash')

        # options/verbose does not need to be specified so default False
        try:
            if self.dupl['options']['verbose']:
                this_list.append(self._pys_short)
                this_list.append('# '+self.dupl['title'])
        except:
            pass

        if len(this_list) > 0:
            self._js_comps[this_key] = this_list

    def write_general(self):
        '''Write general parameters for jobscript
        
        Componenets are written to _js_sections['general']

        Write optional verbose section header and jobname
        '''
       
        this_list = []
        this_key = 'general'

        self._js_comps[this_key] = []

        try:
            if self.dupl['options']['verbose']:
                this_list.append('# General job parameters')
        except:
            pass

        for sub_key in self.dupl[this_key]:
            if ( ( self.dupl['map']['map'][this_key][sub_key] )
               and
               ( self.dupl[this_key][sub_key] != None ) ):
                this_list.append( self._generate_shed(this_key, sub_key) )

        if len(this_list) > 0:
            self._js_comps[this_key] = this_list

    def write_accounting(self):
        '''Write accounting parameters for jobscript
        
        Componenets are written to _js_sections['accounting']

        Write optional verbose section header and jobname
        '''

        this_list = []
        this_key = 'accounting'
       
        self._js_comps[this_key] = []

        try:
            if self.dupl['options']['verbose']:
                this_list.append('# Specify accounting details')
        except:
            pass

        for sub_key in self.dupl[this_key]:
            if ( ( self.dupl['map']['map'][this_key][sub_key] )
               and
               ( self.dupl[this_key][sub_key] != None ) ):
                this_list.append( self._generate_shed(this_key, sub_key) )

        if len(this_list) > 0:
            self._js_comps[this_key] = this_list

    def write_resource(self):
        '''Write resource parameters for jobscript
        
        Componenets are written to _js_sections['resource']

        Write optional verbose section header and jobname
        '''

        this_list = []
        this_key = 'resource'
       
        self._js_comps[this_key] = []

        try:
            if self.dupl['options']['verbose']:
                this_list.append('# Specify job resources')
        except:
            pass

        for sub_key in self.dupl[this_key]:
            if ( ( self.dupl['map']['map'][this_key][sub_key] )
               and
               ( self.dupl[this_key][sub_key] != None ) ):
                this_list.append( self._generate_shed(this_key, sub_key) )

        if len(this_list) > 0:
            self._js_comps[this_key] = this_list

    def write_io(self):
        '''Write resource parameters for jobscript
        
        Componenets are written to _js_sections['io']

        Write optional verbose section header and jobname
        '''

        this_list = []
        this_key = 'io'
       
        self._js_comps[this_key] = []

        try:
            if self.dupl['options']['verbose']:
                this_list.append('# Specify io redirects')
        except:
            pass

        for sub_key in self.dupl[this_key]:
            if ( ( self.dupl['map']['map'][this_key][sub_key] )
               and
               ( self.dupl[this_key][sub_key] != None ) ):
                this_list.append( self._generate_shed(this_key, sub_key) )

        if len(this_list) > 0:
            self._js_comps[this_key] = this_list

    def write_modules(self):
        '''Write modules for jobscript
        
        Componenets are written to _js_sections['mod']

        Write optional verbose section header and jobname
        '''

        this_list = []
        this_key = 'mod'
       
        self._js_comps[this_key] = []

        try:
            if self.dupl['options']['verbose']:
                this_list.append('# Load modules for job')
        except:
            pass

        try:
            if len(self.dupl[this_key]['script'])>0:
                this_list.extend(self.dupl[this_key]['script'])
        except:
            pass

        if len(this_list) > 0:
            self._js_comps[this_key] = this_list

    def write_threads(self):
        '''Write threads for jobscript
        
        Componenets are written to _js_sections['threads']

        Write optional verbose section header and jobname
        '''

        this_list = []
        this_key = 'threads'
       
        self._js_comps[this_key] = []

        try:
            if self.dupl['options']['verbose']:
                this_list.append('# Set number threads')
        except:
            pass

        if this_key in self.dupl['resource']:
            instruction = "export OMP_NUM_THREADS="
            instruction = instruction + str( self.dupl['resource'][this_key] )
        else:
            instruction = "export OMP_NUM_THREADS=1"

        this_list.append(instruction)

        self._js_comps[this_key] = this_list

    def write_proc(self):
        '''Write execition line for jobscript
        
        Componenets are written to _js_sections['exec']

        Write optional verbose section header and jobname
        '''

        this_list = []
        this_key = 'proc'
       
        self._js_comps[this_key] = []

        try:
            if self.dupl['options']['verbose']:
                this_list.append('# Execute process')
        except:
            pass

        sub_keys = list(self.dupl['system'].keys())

        instruction = self.dupl['system']['launch']
        instruction = instruction + ' '

        sub_keys.remove('launch')

        for process in self.dupl[this_key]:
            for key in sub_keys:
                if self.dupl['system'][key] != None:
                    instruction = instruction + self.dupl['system'][key]
                    instruction = instruction + ' '
                    instruction = instruction + str(self.dupl['resource'][key])
                    instruction = instruction + ' '

            instruction = instruction + process['exec']
            instruction = instruction + ' '
            instruction = instruction + process['args']

            this_list.append(instruction)

        self._js_comps[this_key] = this_list

    def _generate_shed(self, key1, key2):
        '''Generate a scheduler instruction'''

        instruction = self.dupl['map']['format']['hash']
        instruction = instruction + ' '
        if '$SUFFIX' in self.dupl['map']['map'][key1]:
            instruction = instruction + self.dupl['map']['map'][key1]['$SUFFIX']
            instruction = instruction + ' '

        instruction = instruction + self.dupl['map']['map'][key1][key2]

        instruction = instruction + self.dupl['map']['map']['$SEPARATOR']

        # In some cases the value may not be a string, so convert
        instruction = instruction + str( self.dupl[key1][key2] )

        return instruction 

    def _generate_jobscript(self):
        '''Generates jobscript from the entries in _js_sections'''

        self._jobscript = []

        for section in self._js_sections:
            if len(self._js_comps[section]) > 0:
                self._jobscript.extend(self._js_comps[section])
                self._jobscript.append('')

    def get_job(self):
        '''Return the jobscript list'''

        self._generate_jobscript()

        return self._jobscript

    def _set_tasks(self):
        '''Overide user number of tasks'''

        self.dupl['resource']['tasks'] = (
            self.dupl['resource']['nodes']
          * self.dupl['resource']['ppn'])

