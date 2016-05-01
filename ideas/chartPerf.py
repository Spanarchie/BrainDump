import pygal
import json

bar_chart = pygal.Line()

bar_chart.title = 'API request durations  (in ms)'
bar_chart.x_labels = map(str, range(0, 50))

with open('API_Perf_Rec.dat') as data_file:
    data = json.load(data_file)


for x in data[0]['results']:
    print(x[0])
    bar_chart.add(x[0],x[1])

MAX, MIN = [], []
maxm = 750
minm = 550
for itr in range(len(x[1])):
    MAX.append(maxm)
    MIN.append(minm)

bar_chart.add('SLA - MAX',MAX)
bar_chart.add('SLA - MIN',MIN)

bar_chart.render_to_file('bar_chart2.svg')