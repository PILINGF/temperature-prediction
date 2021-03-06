import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import mainfile1

alldata = pd.read_csv('GlobalLandTemperaturesByCountry.csv')
data = alldata[(alldata['Country'] == 'India')]
# data = data[(data['AverageTemperatureUncertainty'] < 1)]
data = data[np.isfinite(data['AverageTemperature'])] # or data[pd.notnull(data['AverageTemperature'])]
data = data[np.isfinite(data['AverageTemperatureUncertainty'])]
# print(data)
avg = data['AverageTemperature'].tolist()
err = data['AverageTemperatureUncertainty'].tolist()
# print(err)
date = data['dt'].tolist()

years = []
months = []
winter = []
summer = []
monsoon = []
yw = []
ys = []
ym = []
mw = []
ms = []
mm = []
for i in date:
    years.append(i[:4])
    months.append(i[5:7])

for c, i in enumerate(months):
    if 11 <= int(i) <= 12 or 1 <= int(i) <= 2:
        winter.append(avg[c])
        yw.append(years[c])
        mw.append(months[c])
    elif 3 <= int(i) <= 6:
        summer.append(avg[c])
        ys.append(years[c])
        ms.append(months[c])
    else:
        monsoon.append(avg[c])
        ym.append(years[c])
        mm.append(months[c])


plt.xlabel('years')
plt.ylabel('temperature')
plt.title('Temperature of India within 215 years')
w, = plt.plot(yw, winter, '+', label='Winter', color='b')
s, = plt.plot(ys, summer, '.', label='Summer', color='r')
m, = plt.plot(ym, monsoon, '*', label='Monsoon', color='g')
# plt.plot(yw, winter, '+', ys, summer, '.', ym, monsoon, '*')
plt.legend(handles=[w, s, m])
plt.grid = True
plt.show()


dataw = []
ywin = []
for i in range(len(winter)):
    p = []
    p.append(yw[i])
    p.append(mw[i])
    dataw.append(p)
    ywin.append(winter[i])

datas = []
ysum = []
for i in range(len(summer)):
    p = []
    p.append(ys[i])
    p.append(ms[i])
    datas.append(p)
    ysum.append(summer[i])

datam = []
ymon = []
for i in range(len(monsoon)):
    p = []
    p.append(ym[i])
    p.append(mm[i])
    datam.append(p)
    ymon.append(monsoon[i])

pre = []
yearspre = []
for i in range(2015, 2030):
    yearspre.append(i)
    for j in range(1, 12):
        p = []
        p.append(i)
        p.append(j)
    pre.append(p)
'''
pre = np.array(pre, dtype='float64')
dataw = np.array(dataw, dtype='float64')
datas = np.array(datas, dtype='float64')
datam = np.array(datam, dtype='float64')
ywin = np.array(ywin, dtype='float64')
ysum = np.array(ysum, dtype='float64')
ymon = np.array(ymon, dtype='float64')
'''

dataw = np.array(dataw, dtype='int64')
datas = np.array(datas, dtype='int64')
datam = np.array(datam, dtype='int64')
ywin = np.array(ywin, dtype='int64')
ysum = np.array(ysum, dtype='int64')
ymon = np.array(ymon, dtype='int64')

clf = SVC(kernel='rbf')
clf.fit(dataw, ywin)
ysvc = clf.predict(pre)
print(ysvc)

clfw = linear_model.LinearRegression()
clfw.fit(dataw, ywin)
wpre = clfw.predict(pre)
print(wpre)

clf = SVC(kernel='rbf')
clf.fit(datas, ysum)
ysvc = clf.predict(pre)
print(ysvc)

clfs = linear_model.LinearRegression()
clfs.fit(datas, ysum)
spre = clfs.predict(pre)
print(spre)

clf = SVC(kernel='rbf')
clf.fit(datam, ymon)
ysvc = clf.predict(pre)
print(ysvc)

clfm = linear_model.LinearRegression()
clfm.fit(datam, ymon)
mpre = clfm.predict(pre)
print(mpre)

print('winter...')
obj = mainfile1.classify(dataw, ywin)
obj.split(testpr=0.25)
obj.getbest()

print('\nsummer...')
obj = mainfile1.classify(datas, ysum)
obj.split(testpr=0.25)
obj.getbest()

print('\nmonsoon...')
obj = mainfile1.classify(datam, ymon)
obj.split(testpr=0.25)
obj.getbest()


plt.figure(1)
plt.xlabel('years')
plt.ylabel('temperature')
plt.subplot(311)
plt.title('Prediction of temperature of India for next 15 years')
w = plt.plot(yearspre, wpre, '+', label='Winter', color='b')
plt.subplot(312)
s = plt.plot(yearspre, spre, '.', label='Summer', color='r')
plt.subplot(313)
m = plt.plot(yearspre, mpre, '*', label='Monsoon', color='g')
# plt.plot(yw, winter, '+', ys, summer, '.', ym, monsoon, '*')
# plt.legend(handles=[w, s, m])
plt.grid = True
plt.show()

