from importlib import import_module

from time import time


CONCLUSION_PASS = 'pass'
CONCLUSION_GO = 'go'

FB_PAGE_FOUND = 'known_page'
FB_PAGE_NOT_FOUND = 'wrong_page'

POST_TO_ANALYZE = 'analyze_it'
POST_TO_IGNORE = 'ignore_this_shit'

ARSENAL = {'hashtags_per_post',
'hashtags_per_post_caption',
'key_phrases_per_post',
'key_phrases_per_post_caption',
'sentiment_per_post',
'emojis_per_post',
'emojis_per_post_caption',
}



def Scout(target,tools):
	# Maps each facebook page of the target
	report = {}
	month = 60*60*24*30
	report['conclusion'] = CONCLUSION_PASS

	if not 'facebook' in target:
		print('No facebook presence for this target. No scouting needed')
	else:
		params = {}
		report['pages'] = []
		for page in target['facebook']:

			current_page = {'id':page['id']}

			print('Mapping page id: '+str(page['id']))
			params['fb_page_id'] = page['id']
			params['since'] = 0
			
			cmd = {'command':'map_page','parameters':params}
			redacted,current_page['mapping'] = ExecuteAction(cmd,tools)

			if not redacted:
				current_page['page_status'] = FB_PAGE_FOUND
				report['conclusion'] = CONCLUSION_GO

				for post in current_page['mapping']:
					print(post)
					if post['created_time'] > time()-month:
						cmd = {'command':'metrics_per_post','parameters':{'fb_post_id':post['id']}}
						redacted,results = ExecuteAction(cmd,tools)
						if redacted:
							results = []
						post['metrics'] = results
			else:
				current_page['page_status'] = FB_PAGE_NOT_FOUND

			report['pages'].append(current_page)

	print('Scout report: '+str(report))
	return report



def CompareMaps(new_map,old_map):
	month = 60*60*24*30
	results = []
	for post in new_map:
		try:
			if post['created_time'] > time()-month:
				results.append(post)
		except Exception as exc:
			print('Error while comparing: '+str(exc))

	print('Comparison: '+str(results))
	return results



def Define(target,new_report,old_report):
	todolist = []

	#if the scouting didn't go well
	if (new_report is None) or (new_report['conclusion'] == CONCLUSION_PASS):
		print('The scouting didn\'t proceed as expected')
		return todolist

	for page in new_report['pages']:
		if page['page_status'] == FB_PAGE_FOUND: 
			try:
				# compare the two reports in order to define the strategy 
				evolution = CompareMaps(page['mapping'],old_report)
				for post_changed in evolution:
					for analysis_type in ARSENAL:
						todolist.append({'command':analysis_type,'parameters':{'fb_post_id':post_changed['id']}})
			except:
				print('Wierd stuff is going on. No facebook page ? Wrong report format?')

	print('Strategy: '+str(todolist))
	return todolist



def ExecuteAction(action,tools):
	analyze = action['command']
	parameters = action['parameters']
	parameters.update(tools)

	try :
		# Instanciate an analysis class
		package = import_module('analyze.facebook.'+str(analyze))
		analysis_class = getattr(package,analyze)
		instance = analysis_class()
	except AttributeError:
		return True,'Error: Unknown analysis '+ analyze

	# get analysis response
	redacted = True
	results = {}

	try:
		redacted,results = instance.execute(**parameters)
	except:
		return True,'Full Facebook Analysis : error in analysis : '+ analyze

	return redacted,results