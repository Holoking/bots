######################
	# Parameters Translating
######################
def translate_parameter(parameter,memory):
	if parameter.startswith("$"):
		if not parameter[1:] in memory.keys():
			raise Exception('Can\'t find parameter '+str(parameter))

		return memory[parameter[1:]]

	return parameter


def translate_parameters(parameters,memory):
	# Two kinds of parameters : direct parameters or vars
	translated = []
	for parameter in parameters:
		translated.append(translate_parameter(parameter,memory))

	return translated