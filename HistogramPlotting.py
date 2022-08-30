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
from scipy.interpolate import interp1d

#import csv
data = pd.read_csv (r"C:\Users\Leanne\Desktop\School\Lab_2022\S2022\COMP402\Python_Files\DLC_Plots\DLC_Data.csv")
 
# make dataframe from data
df = pd.DataFrame(data, columns=["Frame", "X_RH", "Y_RH", "Likelihood_RH", "X_LH", "Y_LH", "Likelihood_LH", "X_Nose", "Y_Nose", "Likelihood_Nose", "X_Pellet", "Y_Pellet", "Likelihood_Pellet"])

#frame bounds
firstframe = 12540;  #3:29
lastframe = 13140;   #3:39

df_RH_filtered = df[df['Frame'] > firstframe]
df_RH_filtered = df_RH_filtered[df_RH_filtered['Frame'] < lastframe]
df_LH_filtered = df[df['Frame'] > firstframe]
df_LH_filtered = df_LH_filtered[df_LH_filtered['Frame'] < lastframe]
df_Pel_filtered = df[df['Frame'] > firstframe]
df_Pel_filtered = df_Pel_filtered[df_Pel_filtered['Frame'] < lastframe]
df_Nose_filtered = df[df['Frame'] > firstframe]
df_Nose_filtered = df_Nose_filtered[df_Nose_filtered['Frame'] < lastframe]

#calculating values ------------------------------
x = list(range(firstframe+1, lastframe))
#x = df['Frame'].values.tolist()
X_RH = df_RH_filtered['X_RH'].values.tolist()
Y_RH = df_RH_filtered['Y_RH'].values.tolist()
X_LH = df_LH_filtered['X_LH'].values.tolist()
Y_LH = df_LH_filtered['Y_LH'].values.tolist()
X_Pel = df_Pel_filtered['X_Pellet'].values.tolist()
Y_Pel = df_Pel_filtered['Y_Pellet'].values.tolist()
X_Nose = df_Pel_filtered['X_Nose'].values.tolist()
Y_Nose = df_Pel_filtered['Y_Nose'].values.tolist()

delta_X_RH = []
delta_X_LH = []
delta_X_Pel = []
delta_X_Nose = []
delta_Y_RH = []
delta_Y_LH = []
delta_Y_Pel = []
delta_Y_Nose = []

delta = 0
for i in range(0,len(x)-1):
    delta_X_RH.append(abs(X_RH[i] - X_RH[i+1]))
    delta_Y_RH.append(abs(Y_RH[i] - Y_RH[i+1]))
    delta_X_LH.append(abs(X_LH[i] - X_LH[i+1]))
    delta_Y_LH.append(abs(Y_LH[i] - Y_LH[i+1]))
    delta_X_Pel.append(abs(X_Pel[i] - X_Pel[i+1]))
    delta_Y_Pel.append(abs(Y_Pel[i] - Y_Pel[i+1]))
    delta_X_Nose.append(abs(X_Nose[i] - X_Nose[i+1]))
    delta_Y_Nose.append(abs(Y_Nose[i] - Y_Nose[i+1]))

RH_binCount = len(delta_X_RH)
LH_binCount = len(delta_X_LH)
Pel_binCount = len(delta_X_Pel)
Nose_binCount = len(delta_X_Nose)

#Hist plots -------------------
#plotting each line separately to manually change colors and properties easily
plt.hist(delta_X_RH, color="blueviolet", histtype="step", bins=RH_binCount, alpha=1, linewidth=1.3)
plt.hist(delta_X_LH, color="springgreen", histtype="step", bins=LH_binCount, alpha=1, linewidth=1.3)
plt.hist(delta_X_Pel, color="orangered", histtype="step", bins=Pel_binCount, alpha=1, linewidth=1.3)
plt.hist(delta_X_Nose, color="gold", histtype="step", bins=Nose_binCount, alpha=1, linewidth=1.3)
plt.hist(delta_Y_RH, color="blueviolet", histtype="step", bins=RH_binCount, alpha=1, linewidth=1.3)
plt.hist(delta_Y_LH, color="springgreen", histtype="step", bins=LH_binCount, alpha=1, linewidth=1.3)
plt.hist(delta_Y_Pel, color="orangered", histtype="step", bins=Pel_binCount, alpha=1, linewidth=1.3)
plt.hist(delta_Y_Nose, color="gold", histtype="step", bins=Nose_binCount, alpha=1, linewidth=1.3)


#customizing plot
plt.suptitle(r"$\Delta$ X and $\Delta$ Y of Tracked Coordinates", fontsize=25, fontfamily='fantasy')
plt.ylabel('Frequency', fontsize=14, fontfamily='sans-serif', weight="bold") #add and customize y axis label
plt.xlabel(r"$\Delta$ X and $\Delta$ Y", fontsize=14, fontfamily='sans-serif', weight="bold") #customize x axis label

plt.xlim(13, 600)
plt.ylim(0, 11)

#legend
#line 2D uses a line marker object of our choice for the legend, here I used a square marker
legend_elements = [Line2D([0], [0], marker='s', color='w', label='Right Paw',
                          markerfacecolor='blueviolet', markersize=10),
                    Line2D([0], [0], marker='s', color='w', label='Left Paw',
                          markerfacecolor='springgreen', markersize=10),
                    Line2D([0], [0], marker='s', color='w', label='Nose',
                          markerfacecolor='gold', markersize=10),
                    Line2D([0], [0], marker='s', color='w', label='Pellet',
                          markerfacecolor='orangered', markersize=10)]

plt.legend(handles=legend_elements, loc="upper right")
fig = plt.gcf()
fig.set_size_inches(13,5)

# display plot
plt.show()