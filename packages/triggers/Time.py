import time

def alarmClock(clock,timefilter):
	print("time: "+str(time.strftime(timefilter,time.gmtime())))
	if time.strftime(timefilter,time.gmtime()) == clock:
		return True
	return False

