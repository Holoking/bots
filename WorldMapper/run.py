##################################
	# Default spider run file #
##################################

import automaton


# setup the spider
env = automaton.setup_environnement()
packages = automaton.import_packages()


# execute the bahavior script
results = automaton.start_automaton()

