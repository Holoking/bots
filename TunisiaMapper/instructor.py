import translator

##########################
	# GENERAL
##########################
BLOC_FOR = 0

def enter_bloc(bloc_type,memory):
	bloc = {}
	bloc['type'] = bloc_type
	bloc['idle'] = True
	memory['cursor']['blocs'].insert(0,bloc)

def exit_bloc(bloc_type,memory):
	if memory['cursor']['blocs'][0]['type'] == bloc_type:
		memory['cursor']['blocs'].pop(0)
	else:
		raise Exception('Unexpected bloc end')


##########################
	# MISC
##########################
def dict_to_list(some_dict):
	containerList = []
	for key in some_dict.keys():
		containerList.append(some_dict[key])
	return containerList


##########################
	# FOR
##########################
def is_for_instruction(instruction):
	instr = instruction['instr']
	if instr.startswith("<for ") and instr.endswith(">"):
		return True

	return False


def parse_for_instruction(instruction):
	instr = instruction['instr'][5:-1]
	return instr.split(':')


def execute_for_instruction(instruction,memory):
	enter_bloc(BLOC_FOR,memory)
	print('entered for : '+str(instruction))
	if memory['cursor']['state'] == 'exec':
		bloc = memory['cursor']['blocs'][0]
		bloc['idle'] = False
		var,container_name = parse_for_instruction(instruction)
		container = translator.translate_parameter(container_name,memory)

		if type(container).__name__ == 'dict':
			container = dict_to_list(container)

		if len(container) > 0:
			bloc['anchor'] = memory['cursor']['position']
			bloc['container'] = container_name
			bloc['vars'] = var
			bloc['pointer'] = 0
			memory[var] = container[0]
		else:
			memory['cursor']['state'] = 'pass'



##########################
	# ROF
##########################
def is_rof_instruction(instruction):
	instr = instruction['instr']
	if instr == "<rof>":
		return True
	return False


def execute_rof_instruction(instruction,memory):
	if memory['cursor']['state'] == 'pass':
		if not memory['cursor']['blocs'][0]['idle']:
			memory['cursor']['state'] = 'exec'
		exit_bloc(BLOC_FOR,memory)
	else:
		bloc = memory['cursor']['blocs'][0]
		container = translator.translate_parameter(bloc['container'],memory)

		if type(container).__name__ == 'dict':
			container = dict_to_list(container)

		pointer = bloc['pointer']
		if pointer < len(container)-1:
			memory['cursor']['position'] = bloc['anchor']
			var = bloc['vars']
			memory[var] = container[pointer+1]
			bloc['pointer'] = pointer+1
		else:
			print('exited for : '+str(instruction))
			exit_bloc(BLOC_FOR,memory)


	

def execute_instruction(instruction,memory):
	if is_for_instruction(instruction):
		execute_for_instruction(instruction,memory)
	elif is_rof_instruction(instruction):
		execute_rof_instruction(instruction,memory)
			
