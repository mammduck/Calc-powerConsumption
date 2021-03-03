import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


#data-logger(TsDMMViewer) column. Make sure to choose either of below
"""
column_name1 =   'voltage'  #check
column_name2 =   'current'  #check
"""
column_name1 =  'current'  #check
column_name2 =  'voltage'   #check


MeasurementTargetName = 'photography'    #check

#import the measured value by DMM   #check csv-name
data = pd.read_csv('2021-02-15-0010_5領域撮影.csv', names=('time',column_name1, column_name2), skiprows=2,header=None,usecols=[0,2,5], dtype={'time': str, column_name1: float, column_name2: float})
data = data.loc[:,['time','current','voltage']]


#remove outliers
data=data[data.current > 0]

cutOffCurrentValue = 0.0  #unit [A]    #check




#remove safe mode part 


while data.iloc[0,1] < cutOffCurrentValue:
    data.drop(data.index[0],inplace=True)
    data.reset_index(inplace=True,drop=True)


#remove last redundant part 

while data.iloc[len(data)-1,1] < cutOffCurrentValue:
    data.drop(data.index[len(data)-1],inplace=True)
    data.reset_index(inplace=True,drop=True)

#upper part has filtered out redundant part

# initialization of time array
passedTime = [0.0]*len(data)    #unit:[sec]
powerConsumption = 0.0  #unit:[J]
measuredTimeSum = 0.0

#assign time of each row
for i in range(len(passedTime)):
    passedTime[i]+=(float(data.iloc[i,0][3:4]))*3600
    passedTime[i]+=(float(data.iloc[i,0][5:7]))*60.0
    passedTime[i]+=(float(data.iloc[i,0][8:10]))*1.0
    passedTime[i]+=(float(data.iloc[i,0][11:13]))/100.0
measuredTimeSum = passedTime[len(passedTime)-1]-passedTime[0]

#The product of the average current of [i,i+1] and the average voltage of [i,i+i]
for i in range(len(passedTime)-1):
    powerConsumption += (passedTime[i+1]-passedTime[i])*(data.iloc[i,1]*data.iloc[i,2]+data.iloc[i+1,1]*data.iloc[i+1,2])/2


#print(powerConsumption/measuredTimeSum) #unit[W]
#print(powerConsumption/3600.0) #unit[Wh]
#print(measuredTimeSum) #unit[s]
text = f"Power Consumption = {powerConsumption/measuredTimeSum} [W]\nConsumption = {powerConsumption/3600.0} [Wh]\nMeasurment Time = {measuredTimeSum} [s]"
print(text)


############
#↓graph plot

x_list = passedTime
y1_list = data['voltage'].tolist()
y2_list = data['current'].tolist()

fig = plt.figure()
fig.suptitle(MeasurementTargetName)

# row:2 column:1 upper
ax1 = fig.add_subplot(211, xlabel = 'passed time [s]', ylabel = 'Voltage [V]')
ax1.plot(x_list, y1_list, marker=".", color = "cornflowerblue")
plt.grid()

# row:2 column:1 lower
ax2 = fig.add_subplot(212,  xlabel = 'passed time [s]', ylabel = 'Current [A]')
ax2.plot(x_list, y2_list, marker=".", color = "orangered");
plt.grid()
plt.show()
