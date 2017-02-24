import comunicator

######################
	# Parameters Translating
######################
predifined_vars = {"TRUE" : True,
                   "FALSE": False}

def translate_parameter(parameter,memory):
	if parameter.startswith("$"):
		if not parameter[1:] in memory.keys():
			raise Exception('Can\'t find parameter '+str(parameter))

		value = memory[parameter[1:]]

	elif parameter.startswith("{"):
		if ':' in parameter[1:]:
			bot = parameter[1:].split(':',1)[0]
			question = translate_parameter(parameter[1:].split(':',1)[1])
			value = comunicator.AskAndWait(bot,question)
		else:
			raise Exception('not developped yet (Bot Comm)')

	elif parameter in predifined_vars.keys():
			value = predifined_vars[parameter]

	return value


def translate_parameters(parameters,memory):
	# Two kinds of parameters : direct parameters or vars
	translated = []
	for parameter in parameters:
		translated.append(translate_parameter(parameter,memory))

	return translated