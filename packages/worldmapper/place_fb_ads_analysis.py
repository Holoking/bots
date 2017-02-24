from facebookads.exceptions import (
	FacebookBadObjectError,
)
from matplotlib import gridspec
import matplotlib.pyplot as plt
import pandas as pd
import json
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




def get_place_insights(FBapp_token,FBapp_id,place_name):

	resp = []
	if not place_name is None:
		FacebookAdsApi.init(access_token=FBapp_token)
		account = AdAccount(FBapp_id)
		params = {
			'q': place_name,
			'type': 'adinterest',
		}
	
		resp = TargetingSearch.search(params=params)
		print resp

	country={}
	if len(resp)!=0:
		output={}
		country1=['US']
		name_place=resp[0]['name']
		id_place=resp[0]['id']

		print name_place
		print id_place
		gender1=[[1],[2]]
		age1=[[18,24],[25,34],[35,44],[45,54],[55,64]]
		relation1=['single','in_relationship','married','engaged','not specified','in a civil union','in a domestic partnership','In an open relationship',"It's complicated",'Separated','Divorced','Widowed']
		education_status=['HIGH_SCHOOL','UNDERGRAD','ALUM','HIGH_SCHOOL_GRAD','SOME_COLLEGE','ASSOCIATE_DEGREE','IN_GRAD_SCHOOL','SOME_GRAD_SCHOOL','MASTER_DEGREE','PROFESSIONAL_DEGREE','DOCTORATE_DEGREE','UNSPECIFIED','SOME_HIGH_SCHOOL']
		targeting_spec0={
				'geo_locations': {
								'countries':country1,
							},}
		params0 = {
			'currency': 'USD',
			'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
			'targeting_spec': targeting_spec0,
		}

		reach_estimate0 = account.get_reach_estimate(params=params0)
		
		country['key']=country1[0]
		country['Total']=reach_estimate0[0]["users"]
		place_analys=[]
		place={}
		targeting_spec1=targeting_spec1 = {
				'geo_locations': {
								'countries':country1,
							},

			'flexible_spec': [ 
		  {

			'interests':[ 
			  {'id':id_place, 'name': name_place},],  
		  }, 

		], 

		}
		params1 = {
			'currency': 'USD',
			'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
			'targeting_spec': targeting_spec1,
		}

		reach_estimate1 = account.get_reach_estimate(params=params1)
		place['key']=name_place
		place['Total']=reach_estimate1[0]["users"]
		gender_analys=[]
		for c in gender1:
			gender={}
			targeting_spec2 = {
			'geo_locations': {
							'countries':country1,
						},
			'genders':c,

			'flexible_spec': [ {'interests':[ {'id':id_place, 'name': name_place},], }, ], 
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
							'countries':country1,
						},

					'age_min': d[0],
					'age_max': d[1],
					'genders':c,
					'flexible_spec': [ 
							{'interests':[ {'id':id_place, 'name': name_place},], }, 
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
								'countries':country1,
							},

						'age_min': d[0],
						'age_max': d[1],
						'genders':c,
						'flexible_spec': [ 
								{'interests':[ {'id':id_place, 'name': name_place},], },
								  {'relationship_statuses':[i],}, 
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
						time.sleep(5)


						relation_analys.append(relation)
					except:
						print 'error'
						continue
				j=0
				education_status_analysis=[]
				for s in education_status:
					try:
						education={}
						education['key']=s
						targeting_spec6= {        
						'geo_locations': {
								'countries':country1,
							},

						'age_min': d[0],
						'age_max': d[1],
						'genders':c,
						'flexible_spec': [ 
								{'interests':[ {'id':id_place, 'name': name_place},], },
								{'education_statuses':[j],}, 
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
						print 'error 2'
						continue
				age['education_status_analysis']= education_status_analysis
				age['relation_analys']=relation_analys
				age_analys.append(age)
				print age_analys
			gender['age_analys']=age_analys
			gender_analys.append(gender)


		home_ownership=[]
		targeting_spec5=targeting_spec5 = {
				'geo_locations': {
								'countries':country1,
							},
			'home_ownership':[
					{'id':6006371327132,

						'name': 'Renters',
					},
				],

			'flexible_spec': [ 
		  {

			'interests':[ 
			  {'id':id_place, 'name': name_place},],  
		  }, 

		], 

		}
		params5 = {
			'currency': 'USD',
			'optimize_for': AdSet.OptimizationGoal.offsite_conversions,
			'targeting_spec': targeting_spec5,
		}

		reach_estimate5 = account.get_reach_estimate(params=params5)
		home_rent={}
		home_rent['key']='Renters'
		home_rent['Total']=reach_estimate5[0]["users"]

		home_ownership.append(home_rent)
		home_own={}
		home_own['key']='Owners'
		home_own['Total']=place['Total']-home_rent['Total']
		home_ownership.append(home_own)

		place['gender_analys']=gender_analys
		place['home_ownership']=home_ownership

		place_analys.append(place)
		country['place_analys']=place_analys


	dic_out={'analysis':[country]}
	return dic_out
