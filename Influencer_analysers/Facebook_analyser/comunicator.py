import yaml
import io

######################
	# Bot Inter-Comunication
######################

waiting_for_answer = 2

def isHearing(Bot):
	# A bot is hearing if he has a sock by my name
	return True


def AskAndWait(Bot,Question):
	global me

	if isHearing(Bot):
		# Deposit the question
		to_say = {}
		to_say['Q'] = Question

		with io.open(Bot['socks_path']+"/"+str(me['id'])+".sock","w") as sock:
			yaml.dump(to_say, sock, default_flow_style=False)

		forgotten = True
		while forgotten:
			# Wait for the response
			time.sleep(waiting_for_answer)

			# Check if the answer has been given
			with io.open(Bot['socks_path']+"/"+str(me['id'])+".sock","r") as sock:
				loaded = yaml.load(sock)

			if 'A' in loaded:
				forgotten = False

		return loaded['A']

	else:
		# Bot isn't recieving data
		raise Exception("The bot "+str(Bot['id'])+" isn't listening")

