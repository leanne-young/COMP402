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

#import csv
data = pd.read_csv (r"C:\Users\Leanne\Desktop\School\Lab_2022\S2022\COMP402\Python_Files\DLC_Plots\DLC_Data.csv")
 
# make dataframe from data
df = pd.DataFrame(data, columns=["Frame", "X_RH", "Y_RH", "Likelihood_RH", "X_LH", "Y_LH", "Likelihood_LH", "X_Nose", "Y_Nose", "Likelihood_Nose", "X_Pellet", "Y_Pellet", "Likelihood_Pellet"])

#only keep rows with a likelihood higher than the p_cutoff we set
p_cutoff = 0.85

#frame bounds
firstframe = 12540;  #3:29
lastframe = 13140;   #3:39

df_RH_filtered = df[df['Likelihood_RH'] > p_cutoff]
df_LH_filtered = df[df['Likelihood_LH'] > p_cutoff]
df_Pel_filtered = df[df['Likelihood_Pellet'] > p_cutoff]
df_Nose_filtered = df[df['Likelihood_Nose'] > p_cutoff]

df_RH_filtered = df_RH_filtered[df_RH_filtered['Frame'] > firstframe]
df_RH_filtered = df_RH_filtered[df_RH_filtered['Frame'] < lastframe]
df_LH_filtered = df_LH_filtered[df_LH_filtered['Frame'] > firstframe]
df_LH_filtered = df_LH_filtered[df_LH_filtered['Frame'] < lastframe]
df_Pel_filtered = df_Pel_filtered[df_Pel_filtered['Frame'] > firstframe]
df_Pel_filtered = df_Pel_filtered[df_Pel_filtered['Frame'] < lastframe]
df_Nose_filtered = df_Nose_filtered[df_Nose_filtered['Frame'] > firstframe]
df_Nose_filtered = df_Nose_filtered[df_Nose_filtered['Frame'] < lastframe]


#plotting subsets ------------------------------
#plotting each line separately to manually change colors and properties easily
x_pixels = list(range(0, 1080))  #size of video in pixels
y_pixels = list(range(0, 1080))

x1 = df_RH_filtered['X_RH']
y1 = df_RH_filtered['Y_RH']
x2 = df_LH_filtered['X_LH']
y2 = df_LH_filtered['Y_LH']
x3 = df_Pel_filtered['X_Pellet']
y3 = df_Pel_filtered['Y_Pellet']
x4 = df_Nose_filtered['X_Nose']
y4 = df_Nose_filtered['Y_Nose']


# --------- Scatterplots ----------------
#Righthand---------------
plt.scatter(x1,y1, color="blueviolet", s=5, alpha=0.5)
#LH
plt.scatter(x2,y2, color="springgreen", s=5, alpha=0.5)
#Pellet---------------
plt.scatter(x3,y3, color="orangered", s=5, alpha=0.5)
#Nose---------------
plt.scatter(x4,y4, color="gold", s=5, alpha=0.5)


#customizing plot
plt.suptitle('Trajectory of Paws & Pellet', fontsize=25, fontfamily='fantasy', y=0.96)
plt.ylabel('Y Coordinate (pixels)', fontsize=14, fontfamily='sans-serif', weight="bold") #add and customize y axis label
plt.xlabel('X Coordinate (pixels)', fontsize=14, fontfamily='sans-serif', weight="bold") #customize x axis label
#plt.xlim(0,1200)
#plt.ylim(500,750)
#legend
#line 2D uses a line marker object of our choice for the legend, here I used a square marker
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Right Paw',
                          markerfacecolor='blueviolet', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Left Paw',
                          markerfacecolor='springgreen', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Nose',
                          markerfacecolor='gold', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Pellet',
                          markerfacecolor='orangered', markersize=10)]

plt.legend(handles=legend_elements, loc="upper right")
#plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.spring(np.linspace(0, 1, 6)))) #set order of color cycle

#add annotations (arrows and comments) to the plot
#Pellet incorrectly identified at corner of cage
#plt.annotate('A',
#    xy=(260, 743), xycoords='data',
#    xytext=(20, 33), textcoords='offset points',
#    arrowprops=dict(facecolor='black', shrink=0.02),
#    horizontalalignment='right', verticalalignment='bottom')

#Pellet correctly identified in front of slit
#plt.annotate('B',
#    xy=(153, 1050), xycoords='data',
#    xytext=(40, -10), textcoords='offset points',
#    arrowprops=dict(facecolor='black', shrink=0.02),
#    horizontalalignment='right', verticalalignment='bottom')

#invert y axis because Y is inverted on screens
plt.gca().invert_yaxis()
fig = plt.gcf()
#fig.set_size_inches(7,5)
 
# display plot
plt.show()