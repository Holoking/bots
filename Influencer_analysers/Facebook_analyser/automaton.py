import importlib
import yaml
import sys
import os
import io

import instructor
import translator


env = {}
me = {}


def setup_environnement():
	global env
	global me

	# get spider own path
	own_path = os.path.dirname(os.path.abspath(__file__))

	# verify it
	if not os.path.isdir(own_path):
		raise Exception('Error while setting up spider\'s own path')

	env['own_path'] = own_path

	env['errors_path'] = env['own_path']+"/memory/exceptions.mem"
	env['state_path'] = env['own_path']+"/memory/state.mem"
	env['memory_path'] = env['own_path']+"/memory/memory.mem"
	env['script_path'] = env['own_path']+"/config/script"
	
	# Read the configuration file
	config_file = own_path+"/config/automaton.conf"
	if not os.path.isfile(config_file):
		raise Exception('Config file can not be found')

	with io.open(config_file,"r") as stream:
			loaded = yaml.load(stream)

	env.update(loaded['env'])
	me.update(loaded['me'])



def import_packages():
	global env

	if not env['own_path'] in sys.path:
		sys.path.append(env['own_path'])
	if not env['own_path']+"/own_lib" in sys.path:
		sys.path.append(env['own_path']+"/own_lib")
	if not env['packages_path'] in sys.path:
		sys.path.append(env['packages_path'])

	# Read the import file
	import_file = env['own_path']+"/config/import.conf"
	import_list = []
	if os.path.isfile(import_file):
		with io.open(import_file,"r") as stream:
			try :
				import_list = yaml.load(stream)
			except yaml.YAMLError as error:
				raise error

	packages = {}
	for element in import_list:
		packages[element]=importlib.import_module(element)

	return packages



##########################
	# Script
##########################
def load_script(script_file=""):
	if script_file == "":
		script_file = env['script_path']

	script = {}
	if os.path.isfile(script_file):
		with io.open(script_file,"r") as stream:
			try :
				script = yaml.load(stream)
			except Exception as error:
				raise error

	return script


def reset_mem_files():
	global env

	for key in env.keys():
		if '.mem' in env[key]:
			io.open(env[key],"w")



##########################
	# Memory
##########################
def init_memory_from_script(memory,script):
	if 'init' in script:
		memory.update(script['init'])

	if 'on_except' in script:
		memory['on_except'] = script['on_except']

	return memory

	

def init_memory_from_file(memory,file_name=""):
	if file_name == "":
		file_name = env['memory_path']

	if os.path.isfile(file_name):
		with io.open(file_name,"r") as stream:
				memory = yaml.load(stream)
	else:
		raise Exception('Can\'t find memory file.')

	return memory


def save_memory(memory,file_name=""):
	if file_name == "":
		file_name = env['memory_path']

	print("saving memory in "+str(file_name))

	with io.open(file_name,'wb') as outfile:
		try:
			yaml.dump(memory, outfile, default_flow_style=False)
		except Exception as exc:
			#print("memory: "+str(memory))
			print("memory save error: "+str(exc))


def reset_memory(memory):
	memory['cursor'] = {}
	memory['cursor']['state'] = 'exec'
	memory['cursor']['position'] = 0
	memory['cursor']['blocs'] = []

	return memory


##########################
	# Errors Handling
##########################
def save_error(step,exception,file_name=""):
	if file_name == "":
		file_name = env['errors_path']

	exception_list = []
	if os.path.isfile(file_name):
		with io.open(file_name, 'r') as outfile:
			try:
				exception_list = yaml.load(outfile)
				if exception_list is None:
					exception_list = []
			except Exception as exc:
				exception_list = False
				print("Exception save error: "+str(exc))
	
	if exception_list != False:
		with io.open(file_name, 'wb') as outfile:
			to_write = {}

			to_write['class'] = exception.__class__.__name__
			to_write['msg'] = str(exception)

			if 'name' in step:
				to_write['at_step'] = step['name']
			elif 'function' in step:
				to_write['at_step'] = step['function']
			elif 'instr' in step:
				to_write['at_step'] = step['instr']

			exception_list.append(to_write)

			try:
				yaml.dump(exception_list, outfile, default_flow_style=False)
			except Exception as exc:
				print("Exception save error: "+str(exc))


def on_except(action,exception,memory):
	# Mark return vars as None (function)
	if 'function' in action and 'return' in action['function']:
		nonelist = []
		for var in action['function']['return']:
			nonelist.append(None)
		memory.update(parse_results(action['function']['return'],None))

	# Try to correct errors
	correction_tries(action,exception,memory)


def correction_tries(action,exception,memory):
	if 'on_except' in memory and not memory['on_except'] is None:
		print('Searching for appropriate reaction to: '+str(exception))
		for reaction in memory['on_except']:
			if 'exception' in reaction and 'class' in reaction['exception']:
				if reaction['exception']['class'] == exception.__class__.__name__:
					if not 'tries' in memory:
						memory['tries'] = 0

					if memory['tries'] == 3:
						raise Exception('Could\'t correct the error: '+str(exception))
					else:
						memory['tries'] += 1

					try:
						execute_step(reaction['handler'],memory)
						save_memory(memory)
						execute_step(action,memory)
					except:
						on_except(action,exception,memory)

	elif 'optionnal' in action and action['optionnal']:
		repr(exception)
		raise exception
	else:
		pass



##########################
	# Spider State
##########################
def clear_state():
	state = {}
	state['running'] = True
	return state

def error_state(exception):
	state = {}
	state['running'] = False
	state['exception-type'] = type(exception).__name__
	state['exception-msg'] = str(exception)
	return state
 
def change_state(state,current_step,file_name=""):
	if file_name == "":
		file_name = env['state_path']
	to_write = {}
	to_write['state'] = state
	to_write['current_step'] = current_step
	with io.open(file_name, 'w') as outfile:
		try:
			yaml.dump(to_write, outfile, default_flow_style=False)
		except Exception as exc:
			raise exc


##########################
	# Execution
##########################
def execute_function(module,function,parameters,options):
	with_options = False

	if not options is None and len(options) >= 1:
		with_options = True

	if parameters is None or len(parameters) == 0:
		if with_options:
			return getattr(module,function)(**options)

		return getattr(module,function)()

	if len(parameters) == 1:
		if with_options:
			return getattr(module,function)(parameters[0],**options)

		return getattr(module,function)(parameters[0])

	if len(parameters) == 2:
		if with_options:
			return getattr(module,function)(parameters[0],parameters[1],**options)

		return getattr(module,function)(parameters[0],parameters[1])
	

	if len(parameters) == 3:
		if with_options:
			return getattr(module,function)(parameters[0],parameters[1],parameters[2],**options)

		return getattr(module,function)(parameters[0],parameters[1],parameters[2])

	if len(parameters) == 4:
		if with_options:
			return getattr(module,function)(parameters[0],parameters[1],parameters[2],parameters[3],**options)

		return getattr(module,function)(parameters[0],parameters[1],parameters[2],parameters[3])

	if len(parameters) == 5:
		if with_options:
			return getattr(module,function)(parameters[0],parameters[1],parameters[2],parameters[3],parameters[4],**options)

		return getattr(module,function)(parameters[0],parameters[1],parameters[2],parameters[3],parameters[4])



def execute_step(step,memory):
	# define steps' parameters
	parameters = []
	if 'parameters' in step['function'] and not step['function']['parameters'] is None:
		parameters =  translator.translate_parameters(step['function']['parameters'],memory)
	
	# define steps' optionnal parameters
	options = {}
	if 'options' in step['function']:
		options =  step['function']['options']

	# define steps' return var
	return_vars = []
	if 'return' in step['function']:
		return_vars =  step['function']['return']

	# define function location
	package = step['function']['name'].split('.')[:-1]
	package = '.'.join(package)

	function = step['function']['name'].split('.')[-1]

	package = importlib.import_module(package)

	memory.update(parse_results(return_vars,execute_function(package,function,parameters,options)))
	


def execute_action(action,memory):
	try:
		print('')
		print('On step: '+str(action['name']))
	except:
		pass

	try:
		change_state(clear_state(),action)
		execute_step(action,memory)
		save_memory(memory)
	except Exception as exc:
		save_error(action,exc)
		save_memory(memory)
		change_state(error_state(exc),action)
		on_except(action,exc,memory)


def execute_script(script,memory,**options):
	# Load the script file
	global env

	# Go step by step
	while memory['cursor']['position'] < len(script['steps']):
		step = script['steps'][memory['cursor']['position']]
		if 'function' in step and not memory['cursor']['state'] == 'pass':
			execute_action(step,memory)
		if 'instr' in step:
			instructor.execute_instruction(step,memory)
		memory['cursor']['position'] += 1


def parse_results(var_list,result):
	parsed = {}
	if not var_list is None and len(var_list) > 0:
		
		if len(var_list) == 1:
			parsed[var_list[0]] = result
		elif len(var_list) == 2:
			parsed[var_list[0]] = result[0]
			parsed[var_list[1]] = result[1]	
		elif len(var_list) == 3:
			parsed[var_list[0]] = result[0]
			parsed[var_list[1]] = result[1]
			parsed[var_list[2]] = result[2]
		else:
			raise Exception('Too many return values')

	return parsed		



##########################
	# Start, pause, resume
##########################
def start_automaton():
	memory = {}
	script = load_script()

	reset_mem_files()
	memory = reset_memory(memory)
	memory = init_memory_from_script(memory,script)

	execute_script(script,memory)




def resume_automaton():	
	memory = {}
	script = load_script()

	memory = init_memory_from_script(memory,script)
	memory = init_memory_from_file(memory)

	print("resuming from step :")
	print(script['steps'][memory['cursor']['position']])

	execute_script(script,memory)