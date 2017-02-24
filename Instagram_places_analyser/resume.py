##################################
	# Default autonaton resume file #
##################################

import automaton


# setup the spider
env = automaton.setup_environnement()
packages = automaton.import_packages()


# execute the bahavior script
results = automaton.resume_automaton()

