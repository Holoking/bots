import time

def get_state_name(state,states,counter):
	print(state)
	name = states.keys()[counter]
	counter += 1
	print('state = '+str(name))
	time.sleep(15)
	return counter,name
def get_place_info(dict_):
	return dict_['Name'],dict_['lng'],dict_['lat']
