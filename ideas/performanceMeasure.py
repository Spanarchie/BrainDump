# -*- coding: utf-8 -*-
import json
import requests
import logging
import time
import pygal

def generatePerfChart(data, title):
    maxLen = 0
    bar_chart = pygal.Line()
    bar_chart.title = 'API sequential page request durations (in ms)'
    bar_chart.x_title='Initial & Page number'
    bar_chart.y_title='Duration in ms'
    for x in data['results']:
        bar_chart.add(x[0],x[1])
        curLen = len(x[1])
        if maxLen < curLen:
            maxLen = len(x[1])
    bar_chart.x_labels = map(str, range(0, maxLen))
    bar_chart.render_to_file('{}_chart2.svg'.format(title))



current_milli_time = lambda: int(round(time.time() * 1000))
result = []

targetURL = "api.demo.trialreach.com" 

base_trial = """https://{}/trial""".format(targetURL)
base_protocol = """https://{}/protocol""".format(targetURL)
base_annotation = """https://{}/annotation""".format(targetURL)

req_include_P_A = """https://{}/trial?include=protocol,annotation""".format(targetURL)
req_include_P = """https://{}/trial?include=protocol""".format(targetURL)
req_include_A = """https://{}/trial?include=annotation""".format(targetURL)

req_include_P_A_with_lstChange_Range = """http://{}/trial\
?include=protocol,annotation&fields[trial]=attributes.lastchanged_date\
&filter[trial]=attributes.lastchanged_date.value:[2016-04-14T20:34:36.034865+00:00+TO+2016-04-14T20:31:59.047674+00:00]""".format(targetURL)

req_include_P_A_with_lstChange_Range = """http://{}/trial\
?include=annotation\
&fields[trial]=attributes.lastchanged_date\
&filter[trial]=attributes.lastchanged_date.value:[2016-04-14T20:34:36.034865+00:00+TO+2016-04-14T20:31:59.047674+00:00]""".format(targetURL)
req_include_P_with_lstChange_Range = """http://{}/trial\
?include=protocol\
&fields[trial]=attributes.lastchanged_date\
&filter[trial]=attributes.lastchanged_date.value:[2016-04-14T20:34:36.034865+00:00+TO+2016-04-14T20:31:59.047674+00:00]""".format(targetURL)

trial_req_LT_Date = """http://{}/trial\
?include=protocol,annotation\
&fields[trial]=attributes.lastchanged_date\
&filter[trial]=attributes.lastchanged_date.value:[LT+2016-04-14T20:34:36.034865+00:00]""".format(targetURL)

protocol_req_LT_Date = """http://{}/protocol\
?fields[protocol]=attributes.lastchanged_date\
&filter[protocol]=attributes.lastchanged_date.value:[LT+2016-04-14T20:34:36.034865+00:00]""".format(targetURL)

annotation_req_LT_Date = """http://{}/annotation\
?fields[annotation]=attributes.lastchanged_date\
&filter[annotation]=attributes.lastchanged_date.value:[LT+2016-04-14T20:34:36.034865+00:00]""".format(targetURL)

req_LE_Date = """http://{}/trial\
?include=protocol,annotation\
&fields[trial]=attributes.lastchanged_date\
&filter[trial]=attributes.lastchanged_date.value:[LE+2016-04-14T20:34:36.034865+00:00]""".format(targetURL)


req_GT_Date = """http://{}/trial\
?include=protocol,annotation\
&fields[trial]=attributes.lastchanged_date\
&filter[trial]=attributes.lastchanged_date.value:[GT+2016-04-14T20:34:36.034865+00:00]""".format(targetURL)

req_GE_Date = """http://{}/trial\
?include=protocol,annotation\
&fields[trial]=attributes.lastchanged_date\
&filter[trial]=attributes.lastchanged_date.value:[GE+2016-04-14T20:34:36.034865+00:00]""".format(targetURL)

req_OR_with_Ampersand = """http://{}/trial\
?fields[trial]=attributes.eligibility.gender\
&filter[trial]=attributes.eligibility.gender:(Male Female)&attributes.eligibility.healthy_volunteers:No""".format(targetURL)

req_OR_same_fields = """https://{}/trial\
?fields[trial]=attributes.eligibility.gender\
&filter[trial]=attributes.eligibility.gender:Male OR attributes.eligibility.gender:Female""".format(targetURL)

OR_country_List_fields = """https://{}/trial\
?filter[trial]=attributes.location_countries.country:(United States+Australia)\
&fields[trial]=attributes.location_countries.country""".format(targetURL)

OR_keyword_List_fields = """https://{}/trial\
?filter[trial]=attributes.keyword:(psoriasis meta-analyses)\
&fields[trial]=attributes.keyword""".format(targetURL)

req_OR_diff_fields = """https://{}/trial\
?filter[trial]=attributes.eligibility.gender:Male%20OR%20attributes.eligibility.healthy_volunteers:No\
&fields[trial]=attributes.eligibility.gender,attributes.eligibility.healthy_volunteers""".format(targetURL)

req_AND_diff_fields = """https://{}/trial\
?filter[trial]=attributes.eligibility.gender:Male%20AND%20attributes.eligibility.healthy_volunteers:No\
&fields[trial]=attributes.eligibility.gender,attributes.eligibility.healthy_volunteers""".format(targetURL)

lsting=[ ["base_trial", base_trial],["base_protocol", base_protocol],["base_annotation", base_annotation],['req_OR_same_fields', req_OR_same_fields], ['OR_country_List_fields', OR_country_List_fields], ['OR_keyword_List_fields', OR_keyword_List_fields], ['req_OR_diff_fields',req_OR_diff_fields], ['req_AND_diff_fields', req_AND_diff_fields], #, ['req_OR_with_Ampersand',req_OR_with_Ampersand],
         ['req_include_P_A', req_include_P_A], ['req_include_P', req_include_P], ['req_include_A', req_include_A]
       ]

with open('API_Perf_Rec.dat') as data_file:
    data = json.load(data_file)



timestr = time.strftime("%Y%m%d-%H%M%S")
jsonObj= {}
jsonObj["date"] = timestr
jsonObj["results"]=[]

for indx, reqst in enumerate(lsting):
    resList = [] # To record the request durations

    strtTime = current_milli_time()
    r = requests.get(reqst[1], auth=('qEZxd3bC707QtFLCrBLP6DhDvHVALcJP', 'BtMPHHrOrAqFReGz'))
    endTime = current_milli_time()
    durTime = endTime - strtTime
    resList.append(durTime)
    print ("{} : {} took {}ms".format(reqst[0], "Initial request", durTime))

    resp = r.json()
    pgs = resp['meta']['total-pages']
    lstPg = pgs+1

    # Make a request for each page & measure the duration.
    for p in range(1, lstPg):
        req = "{}&page[number]={}".format(reqst[1], str(p))
        strtTime = current_milli_time()
        r = requests.get(req, auth=('qEZxd3bC707QtFLCrBLP6DhDvHVALcJP', 'BtMPHHrOrAqFReGz'))
        endTime = current_milli_time()
        durTime = endTime - strtTime
        print ("{} : pg{} took {}ms".format(reqst[0], str(p), durTime))
        resList.append(durTime)
    jsonObj["results"].append([reqst[0], resList])

data.append(jsonObj)

generatePerfChart(jsonObj, reqst[0])


with open('API_Perf_Rec.dat', 'w') as outfile:
    json.dump(data, outfile)











