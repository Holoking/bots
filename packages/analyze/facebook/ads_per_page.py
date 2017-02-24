from facebookads.exceptions import (
    FacebookBadObjectError,
)

import facebook
import json
import time
import time
from facebookads.api import (
    FacebookAdsApi,
    Cursor,
    FacebookRequest,
)
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet

from facebookads.adobjects.abstractobject import AbstractObject
from facebookads.adobjects.objectparser import ObjectParser
from facebookads.adobjects.targetingsearch import TargetingSearch
from operator import itemgetter


class ads_per_page:

	def execute(self,**params):
		"""parse the parameters"""
		if ('fb_app_access_token' in params) and ('fb_token_version' in params) and ('fb_app_account_id' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_app_access_token'],version=params['fb_token_version'])
				FacebookAdsApi.init(access_token=params['fb_app_access_token'])
				account = AdAccount(params['fb_app_account_id'])
			except:
				return True, "[facebook_ads_page_analysis]:Error while accessing Facebook GraphAPI or ads api"
		else:
			return True, "[facebook_ads_page_analysis]:Missing facebook token information or fb_app_account_id"

		if ('fb_page_id' in params):
			page_id = params['fb_page_id']
		else:
			return True, "[facebook_ads_page_analysis]:Missing facebook page identifier"

		if ('country' in params):
			country=params['country']
		else:
			return True, "[facebook_ads_page_analysis]:Missing country"

		return self.facebook_ads_page_analysis(graph,account,page_id,country)


		
	def facebook_ads_page_analysis(self,FBgraph,account,page_id,country):
		output=[]
		try:
			name = FBgraph.get_object(id=page_id,fields='name')['name']

			params = {
				'q': name,
				'type': 'adinterest',
			}

			resp = TargetingSearch.search(params=params)
			if len(resp)==0:
				return True,'no interest for this page'
			
			listresult=sorted(resp, key=itemgetter('audience_size'), reverse=True) 

			targeting_spec1=targeting_spec1 = {
					'geo_locations': {
								   'countries':country,
								},

				'flexible_spec': [ 
			  {

				'interests':[ 
				  {'id':listresult[0]['id']},],  
			  }, 

			], 


			}
			params1 = {
				'currency': 'USD',
				'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
				'targeting_spec': targeting_spec1,
			}

			reach_estimate1 = account.get_reach_estimate(params=params1)
			total={}
			total['key']=country[0]
			total['count']=reach_estimate1[0]['users']
			gender1=[[1],[2]]
			age1=[[18,24],[25,34],[35,44],[45,54],[55,64]]
			relation1=['single','in_relationship','married','engaged','not specified','in a civil union','in a domestic partnership','In an open relationship',"It's complicated",'Separated','Divorced','Widowed']
			education_status=['HIGH_SCHOOL','UNDERGRAD','ALUM','HIGH_SCHOOL_GRAD','SOME_COLLEGE','ASSOCIATE_DEGREE','IN_GRAD_SCHOOL','SOME_GRAD_SCHOOL','MASTER_DEGREE','PROFESSIONAL_DEGREE','DOCTORATE_DEGREE','UNSPECIFIED','SOME_HIGH_SCHOOL']
			gender_analys=[]
			for c in gender1:
				gender={}
				targeting_spec2 = {
					'geo_locations': {

										'countries':country, },
					
					'genders':c,
					'flexible_spec': [ 
										  {

											'interests':[ 
											  {'id':listresult[0]['id']},],  
										  }, 

									], 


									}
				params2 = {
				'currency': 'USD',
				'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
				'targeting_spec':targeting_spec2
				}

				reach_estimate2 = account.get_reach_estimate(params=params2)
				gender['Total']=reach_estimate2[0]["users"]
				if c[0]==1 :
					gender['key']='Male'


				else:
					gender['key']='Female'
				age_analys=[]
				for d in age1:
					age={}

					age['key']=str(d[0])+'-'+str(d[1])


					targeting_spec3= {        
						'geo_locations': {

										'countries':country,
											},
						

						'age_min': d[0],
						'age_max': d[1],
						'genders':c,
						'flexible_spec': [ 
										  {

											'interests':[ 
											  {'id':listresult[0]['id']},],  
										  }, 

									], 

								}
					params3 = {
					'currency': 'USD',
					'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
					'targeting_spec':targeting_spec3
					}
					reach_estimate3 = account.get_reach_estimate(params=params3)
					age['Total']=reach_estimate3[0]["users"]
					relation_analys=[]
					i=1
					for r in relation1:
						try:
							relation={}
							relation['key']=r
							targeting_spec4= {        
							'geo_locations': {

										'countries':country,
											},

							'age_min': d[0],
							'age_max': d[1],
							'genders':c,
							'flexible_spec': [ 
									  {'relationship_statuses':[i],},
										{

											'interests':[ 
											  {'id':listresult[0]['id']},],  
										  },
								   ],

									}
							i+=1
							params4 = {
							'currency': 'USD',
							'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
							'targeting_spec':targeting_spec4
							}
							reach_estimate4 = account.get_reach_estimate(params=params4)
							relation['Total']=reach_estimate4[0]["users"]
							time.sleep(3)


							relation_analys.append(relation)
						except:
							continue
					j=0
					education_status_analysis=[]
					for s in education_status:
						try:
							education={}
							education['key']=s
							targeting_spec6= {        
							'geo_locations': {

										'countries':country,
											},
							'age_min': d[0],
							'age_max': d[1],
							'genders':c,
							'flexible_spec': [ 
									{'education_statuses':[j],},
									{

											'interests':[ 
											  {'id':listresult[0]['id']},],  
										  },
								   ],

									}
							j+=1
							params6 = {
							'currency': 'USD',
							'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
							'targeting_spec':targeting_spec6
							}
							reach_estimate6 = account.get_reach_estimate(params=params6)
							education['Total']=reach_estimate6[0]["users"]
							education_status_analysis.append(education)
							time.sleep(5)
						except:
							continue
					age['education_status_analysis']= education_status_analysis
					age['relation_analys']=relation_analys
					age_analys.append(age)
					print age_analys
				gender['age_analys']=age_analys
				gender_analys.append(gender)
				print gender_analys
				time.sleep(30)
			total['gender_analys']=gender_analys
			output.append(total)
			return False, output

		except Exception as er:
			return True,str(er)
