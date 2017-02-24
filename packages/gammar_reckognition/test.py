from parsley import makeGrammar

Grammar = """
or = Var -> 1
and = Var 'a' 'n' 'd' Var  -> 2
Var = 'A' num | 'A'
num = '1' | '2' | '3'
stuff = (or | and)+
"""

keywords = ['or','and']

sign_operators = ['==','!=','<','>']
keyword_operators = ['in','nin']


def generate_var_name(var_list):
	vr = 'A0'
	i = 0

	while vr in var_list:
		i+=1
		vr='A'+str(i)

	return vr


def regroup_expr(exprs):
	regrouped = []
	i = 0

	while i < len(exprs):
		current = ''

		if exprs[i] in keywords:
			regrouped.append(exprs[i])
			i+=1

		while i < len(exprs) and not exprs[i] in keywords:
			current += str(exprs[i])+' '
			i+=1

		current = current[:-1]
		regrouped.append(current)

	while '' in regrouped:
		regrouped.remove('')

	return regrouped

def match_expr_var(variable,dict__):
	for varname in dict__.keys():
		if dict__[varname] == variable:
			return varname

def abstractItems(string,asList = False):
	operators = []

	# split the string using spaces as separators
	words = string.split(' ')
	print('split = '+str(words))

	#regroup expressions together [Ab,cv,or,fv,and,rc,lkg] -> [Ab cv,or,fv,and,rc lkg]
	if words[0] in keywords or len(words) < 3:
		raise Exception('Wrong query syntax.')

	query = regroup_expr(words)
	print('query = '+str(query))

	# change words (different than or | and) with varible names
	var_dict = {}
	for word in query:
		if not word in keywords:
			if not match_expr_var(word,var_dict):
				var_name = generate_var_name(var_dict.keys())
				var_dict.update({var_name:word})

	# abstract the query into a string
	abstracted_query = []
	for word in query:
		abstracted_query.append((match_expr_var(word,var_dict) or word))

	if not asList:
		abstracted_query = ' '.join(abstracted_query)

	return  abstracted_query,var_dict


'''ex = "place_type not in [af,rg,d] or not (emoji==3 and topics == 2)"
abstracted,var_dict = abstractItems(ex,True)
print('abstracted query = '+str(abstracted))
print('vardict = '+str(var_dict))




Example = makeGrammar(Grammar, {})
g = Example(abstracted)
result = g.stuff()
print result'''


j = {'and':[{},{'or':[{},{'rrf':'ee'}]}]}

def h(dict__):
	for key in dict__.keys():
		if dict__[key] == {}:
			dict__.pop(key)
		elif type(dict__[key]).__name__ == 'list':
			while {} in dict__[key]:
				dict__[key].remove({})
			l = []
			for elem in dict__[key]:
				l.append(h(elem))
			dict__[key] = l

	return dict__

print(h(j))