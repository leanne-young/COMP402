#Plot DLC results

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np

#import csv
data = pd.read_csv (r"C:\Users\Leanne\Desktop\School\Lab_2022\DLC\dlc-models\iteration-0\trainset95shuffle1\train\learning_stats.csv")
 
# make dataframe from data
df = pd.DataFrame(data, columns=["Iteration", "Loss"])

x = df["Iteration"]
y = df["Loss"]

#Line plot -------------------
plt.plot(x,y, color="dodgerblue")

#customizing plot
plt.suptitle('Loss Over Iterations of Network Training', fontsize=25, fontfamily='fantasy')
plt.ylabel('Loss', fontsize=14, fontfamily='sans-serif', weight="bold") #add and customize y axis label
plt.xlabel('Iteration', fontsize=14, fontfamily='sans-serif', weight="bold") #customize x axis label
#legend
#line 2D uses a line marker object of our choice for the legend, here I used a square marker
#legend_elements = [Line2D([0], [0], marker='s', color='w', label='Right Paw',
#                          markerfacecolor='blueviolet', markersize=10),
#                    Line2D([0], [0], marker='s', color='w', label='Left Paw',
#                          markerfacecolor='springgreen', markersize=10),
#                    Line2D([0], [0], marker='s', color='w', label='Pellet',
#                          markerfacecolor='orangered', markersize=10)]

#plt.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(1.15, 1), borderaxespad=0)
# display plot
plt.show()



