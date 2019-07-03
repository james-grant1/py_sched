from ruamel.yaml import YAML 
import ruamel.yaml

ScannerError = ruamel.yaml.error.MarkedYAMLError

yaml=YAML(typ="safe")

def read_yaml(filename):
    ''' Try to read passed filename as yaml'''

    try:
        with open(filename, 'r') as fp:
            return yaml.load(fp)
    except ScannerError:
        raise ScannerError
    except FileNotFoundError:
        raise FileNotFoundError
    except:
        raise Exception

def read_script(filename):
    '''Read script line by line and return as list'''

    try:
        with open(filename, 'r') as fp:
            return( fp.read().splitlines() )
    except FileNotFoundError:
        raise FileNotFoundError
    except:
        raise Exception

