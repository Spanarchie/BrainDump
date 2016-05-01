
import json
listr = []
with open('API_Perf_Rec.dat') as data_file:
    data = json.load(data_file)

listr.append(data)

listr.append(data)

# print("Results : {}".format(data["results"][0][0]))
#
# print ("Resp times : {}".format(data["results"][0][1]))




with open('API_Perf_Rec.dat', 'w') as outfile:
    json.dump(listr, outfile)