#Plot DLC results

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure
import numpy as np

#import csv (w = working, nw = non-working)
data_w = pd.read_csv (r"C:\Users\Leanne\Desktop\School\Lab_2022\DLC\Trial9_DCohort-LY-2022-03-27\results\2022-03-17_F2-WT-C61DLC_resnet50_Trial9_DCohortMar27shuffle1_250000_filtered.csv")
data_nw = pd.read_csv (r"C:\Users\Leanne\Desktop\School\Lab_2022\S2022\COMP402\Python_Files\DLC_Plots\DLC_Data.csv")
 
# make dataframes from data
df_w = pd.DataFrame(data_w, columns=["Frame", "X_RH", "Y_RH", "Likelihood_RH", "X_LH", "Y_LH", "Likelihood_LH", "X_Pellet", "Y_Pellet", "Likelihood_Pellet"])
df_nw = pd.DataFrame(data_nw, columns=["Frame", "X_RH", "Y_RH", "Likelihood_RH", "X_LH", "Y_LH", "Likelihood_LH", "X_Pellet", "Y_Pellet", "Likelihood_Pellet"]) #not including nose data since first one doesn't have it

#easy frame bound change:
firstframe_w = 3210;
lastframe_w = 3420;
firstframe_nw = 12540;
lastframe_nw = 13140;

df_RH_filtered_w = df_w[df_w['Frame'] > firstframe_w]
df_RH_filtered_w = df_RH_filtered_w[df_RH_filtered_w['Frame'] < lastframe_w]
df_LH_filtered_w = df_w[df_w['Frame'] > firstframe_w]
df_LH_filtered_w = df_LH_filtered_w[df_LH_filtered_w['Frame'] < lastframe_w]
df_Pel_filtered_w = df_w[df_w['Frame'] > firstframe_w]
df_Pel_filtered_w = df_Pel_filtered_w[df_Pel_filtered_w['Frame'] < lastframe_w]

df_RH_filtered_nw = df_nw[df_nw['Frame'] > firstframe_nw]
df_RH_filtered_nw = df_RH_filtered_nw[df_RH_filtered_nw['Frame'] < lastframe_nw]
df_LH_filtered_nw = df_nw[df_nw['Frame'] > firstframe_nw]
df_LH_filtered_nw = df_RH_filtered_nw[df_RH_filtered_nw['Frame'] < lastframe_nw]
df_Pel_filtered_nw = df_nw[df_nw['Frame'] > firstframe_nw]
df_Pel_filtered_nw = df_RH_filtered_nw[df_RH_filtered_nw['Frame'] < lastframe_nw]

#calculating values ------------------------------
x_w = list(range(firstframe_w+1, lastframe_w))
x_nw = list(range(firstframe_nw+1, lastframe_nw))
#x = df['Frame'].values.tolist()
X_RH_w = df_RH_filtered_w['X_RH'].values.tolist()
Y_RH_w = df_RH_filtered_w['Y_RH'].values.tolist()
X_LH_w = df_LH_filtered_w['X_LH'].values.tolist()
Y_LH_w = df_LH_filtered_w['Y_LH'].values.tolist()
X_Pel_w = df_Pel_filtered_w['X_Pellet'].values.tolist()
Y_Pel_w = df_Pel_filtered_w['Y_Pellet'].values.tolist()

X_RH_nw = df_RH_filtered_nw['X_RH'].values.tolist()
Y_RH_nw = df_RH_filtered_nw['Y_RH'].values.tolist()
X_LH_nw = df_LH_filtered_nw['X_LH'].values.tolist()
Y_LH_nw = df_LH_filtered_nw['Y_LH'].values.tolist()
X_Pel_nw = df_Pel_filtered_nw['X_Pellet'].values.tolist()
Y_Pel_nw = df_Pel_filtered_nw['Y_Pellet'].values.tolist()

delta_X_RH_w = []
delta_X_LH_w = []
delta_X_Pel_w = []
delta_Y_RH_w = []
delta_Y_LH_w = []
delta_Y_Pel_w = []

delta_X_RH_nw = []
delta_X_LH_nw = []
delta_X_Pel_nw = []
delta_Y_RH_nw = []
delta_Y_LH_nw = []
delta_Y_Pel_nw = []

delta = 0
for i in range(0,len(x_w)-1):
    delta_X_RH_w.append(abs(X_RH_w[i] - X_RH_w[i+1]))
    delta_Y_RH_w.append(abs(Y_RH_w[i] - Y_RH_w[i+1]))
    delta_X_LH_w.append(abs(X_LH_w[i] - X_LH_w[i+1]))
    delta_Y_LH_w.append(abs(Y_LH_w[i] - Y_LH_w[i+1]))
    delta_X_Pel_w.append(abs(X_Pel_w[i] - X_Pel_w[i+1]))
    delta_Y_Pel_w.append(abs(Y_Pel_w[i] - Y_Pel_w[i+1]))

for i in range(0,len(x_nw)-1):
    delta_X_RH_nw.append(abs(X_RH_nw[i] - X_RH_nw[i+1]))
    delta_Y_RH_nw.append(abs(Y_RH_nw[i] - Y_RH_nw[i+1]))
    delta_X_LH_nw.append(abs(X_LH_nw[i] - X_LH_nw[i+1]))
    delta_Y_LH_nw.append(abs(Y_LH_nw[i] - Y_LH_nw[i+1]))
    delta_X_Pel_nw.append(abs(X_Pel_nw[i] - X_Pel_nw[i+1]))
    delta_Y_Pel_nw.append(abs(Y_Pel_nw[i] - Y_Pel_nw[i+1]))

# reliability function;
def reliabilityFunction(deltaList):
    sum = 0
    for i in range(0, len(deltaList)):
        #if deltaList[i] > 10:
        sum = sum + ((i * deltaList[i]))**2
    return (sum)

deltaRH_w = reliabilityFunction(delta_X_RH_w) + reliabilityFunction(delta_Y_RH_w)
deltaRH_nw = reliabilityFunction(delta_X_RH_nw) + reliabilityFunction(delta_Y_RH_nw)
deltaLH_w = reliabilityFunction(delta_X_LH_w) + reliabilityFunction(delta_Y_LH_w)
deltaLH_nw = reliabilityFunction(delta_X_LH_nw) + reliabilityFunction(delta_Y_LH_nw)
deltaPel_w = reliabilityFunction(delta_X_Pel_w) + reliabilityFunction(delta_Y_Pel_w)
deltaPel_nw = reliabilityFunction(delta_X_Pel_nw) + reliabilityFunction(delta_Y_Pel_nw)

#reciprocal after sum
w = (deltaRH_w + deltaLH_w + deltaPel_w)
nw = (deltaRH_nw + deltaLH_nw + deltaPel_nw)

print(w)
print(nw)
#delta_X_RH_w.sort()
#print(delta_X_RH_w)

#std dev
delta_w = np.array([deltaRH_w, deltaLH_w, deltaPel_w])
delta_nw = np.array([deltaRH_nw, deltaLH_nw, deltaPel_nw])
w_std = np.std(delta_w)
nw_std = np.std(delta_nw)
error = [w_std, nw_std]
toPlot = [w, nw]

print(error)

#plot graph
x = np.arange(2)
fig, ax = plt.subplots()
ax.bar(x, toPlot, color="blue", yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_xticks(x)

#set bar colors
barlist = plt.bar(x, toPlot)
barlist[0].set_color('dodgerblue')
barlist[1].set_color('orangered')

#labels
labels = ['Good Trial', 'Bad Trial']
ax.set_title('uR Score of 1 Working vs. Erroneous Trial: Cohort 1', fontsize=20, fontfamily='fantasy')
ax.set_ylabel('uR Score', fontsize=14, fontfamily='sans-serif', weight="bold")
ax.set_xticks(x, labels, fontsize=14, fontfamily='sans-serif', weight="bold")

#plt.xlim(0,1200)
#plt.ylim(0,1*(10**11))

fig.tight_layout()
fig.set_size_inches(8,5)

# display plot
plt.show()