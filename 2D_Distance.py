# Kinematics
# 2D
# distance vs. time

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure
import numpy as np
import math

#import csv
data = pd.read_csv (r"C:\Users\Leanne\Desktop\School\Lab_2022\DLC\results\2020-11-30_F2-KODLC_resnet50_Trial8_DLCMar27shuffle1_200000_filtered.csv")
 
# make dataframe from data
df = pd.DataFrame(data, columns=["Frame", "X_RH", "Y_RH", "Likelihood_RH", "X_LH", "Y_LH", "Likelihood_LH", "X_Pellet", "Y_Pellet", "Likelihood_Pellet", "X_Nose", "Y_Nose", "Likelihood_Nose"])

#only keep rows with a likelihood higher than the p_cutoff we set
p_cutoff = 0.8

#frame bounds
# firstframe = when the pellet disk starts
# lastframe = when the last trial ends
firstframe = 11190;
lastframe = 11490;

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

#put all the values into a list that you can use to calculate stuff
X_RH = df_RH_filtered['X_RH'].values.tolist()
Y_RH = df_RH_filtered['Y_RH'].values.tolist()
X_LH = df_LH_filtered['X_LH'].values.tolist()
Y_LH = df_LH_filtered['Y_LH'].values.tolist()
X_Pel = df_Pel_filtered['X_Pellet'].values.tolist()
Y_Pel = df_Pel_filtered['Y_Pellet'].values.tolist()
X_Nose = df_Nose_filtered['X_Nose'].values.tolist()
Y_Nose = df_Nose_filtered['Y_Nose'].values.tolist()

#df_subset1 = df[df['Frame'] < firstframe] #upper frame bound
#df_subset2 = df_subset1[df_subset1['Frame'] > lastframe] #lower frame bound

#idea
#split the trials first
#list of lists (list of all the trial data)
#then bring in the deltas
#       trial 1                                                         trial 2
#[ [[x_paw points], [y_paw points], [Lpaw_points], [Rpaw_points] ], [(1,2,3), (1,2,3), (1,2,3)] ]
#because the idexes are the same, iterate through them to calculate delta (just like before but nested lists)

# -------- auto split the trials ---------
frames = df_RH_filtered['Frame'].values.tolist() #it doesn't really matter which df to use here, they should all have the same frames column
#convert frames to time
#videos recorded in 120 fps, we can set this as a variable
#so frame / 120 = time in seconds
fps = 120
time = []
for i in range(0,len(frames)-1):
    time.append(frames[i]/fps)

#actually for the sake of keeping them whole numbers, do the calculations (splitting) by frames and then convert them to time for plots after

#now to actually split the trials by time
temp = 0
init_wait = 9.5 #time for pellet to start moving from stop to the first part of the trial zone
                #when you first start the system, the pellet starts from the paused stop at the dispenser
                #so it's a little more time than later on when you're still counting the trial zone, and
                #the pellet has already started moving towards the next trial zone, hence a little less general wait time
gen_wait = 9 #wait time in between all the trials after the first one

#do it by frame instead
init_wait = 9.5 * fps
gen_wait = 9 * fps
len_pause = 3
len_bufferTime = 1 #0.5s before and after the trial itself
trial_frames = (len_pause + len_bufferTime) * fps

start_frame = 0
end_frame = 0
trial_times = [] #will be 2D
trial_data = [] #will be 3D

#idea:
#get a list with tuples (2) of all the start and end times of the trials
#index will then give you the trial number
#and then loop through each frame between (with a nested loop) to append each data point into the list

#----------------- getting trial bounds -----------------------
#initial trial
start_frame = init_wait
end_frame = start_frame + trial_frames
trial_times.append([start_frame, end_frame])

#all other trials after first one
loopStarter = end_frame
for i in range(loopStarter, len(frames)):
    start_frame = end_frame + gen_wait
    end_frame = start_frame + trial_frames
    trial_times.append([start_frame, end_frame])

#some print statements to help double check things look good
print (trial_times)
print ("total # of trials: " + str(len(trial_times)))

#*********************
#looping through all the time stamps to get the data into a nested list
for i in range(0, len(trial_times)):
    start_frame = trial_times[i][0]
    end_frame = trial_times[i][1]
    trial_toAdd = [[],[],[],[],[],[],[],[]]
    #nested loop to get all the data in between those frames (the "trial zone")
    for j in range(start_frame, end_frame):
        trial_toAdd[0].append(X_RH[j])
        trial_toAdd[1].append(Y_RH[j])
        trial_toAdd[2].append(X_LH[j])
        trial_toAdd[3].append(Y_LH[j])
        trial_toAdd[4].append(X_Pel[j])
        trial_toAdd[5].append(Y_Pel[j])
        trial_toAdd[6].append(X_Nose[j])
        trial_toAdd[7].append(Y_Nose[j])
        #i is the trial index
        trial_data.append(trial_toAdd) #add the entire trial to the mega list

# ------------- Calculate Distance to Pellet -----------

#function to calculate the distance (hypotenuse between X and Y)
def distance(x, y):
      d = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
      return d

#loop through each trial and calculate the delta values and store in a delta values list
RHdist_allTrials = [] #will be 2D
LHdist_allTrials = [] #2D
for trial in range(0, len(trial_data)):
    # get delta values
    for i in range(0, len(trial_data[trial])):
        #new lists that you can store the calculated values to be plotted later
        delta_X_RH = []
        delta_X_LH = []
        delta_X_Pel = []
        delta_Y_RH = []
        delta_Y_LH = []
        delta_Y_Pel = []

        #calculate the delta values
        # *** need to double check this
        for datapoint_index in range(0,len(trial_data[trial][0])-1):
            delta_X_RH.append(abs(trial_data[trial][0][datapoint_index] - trial_data[trial][0][datapoint_index+1]))
            delta_Y_RH.append(abs(trial_data[trial][1][datapoint_index] - trial_data[trial][1][datapoint_index+1]))
            delta_X_LH.append(abs(trial_data[trial][2][datapoint_index] - trial_data[trial][2][datapoint_index+1]))
            delta_Y_LH.append(abs(trial_data[trial][3][datapoint_index] - trial_data[trial][3][datapoint_index+1]))
            delta_X_Pel.append(abs(trial_data[trial][4][datapoint_index] - trial_data[trial][4][datapoint_index+1]))
            delta_Y_Pel.append(abs(trial_data[trial][5][datapoint_index] - trial_data[trial][5][datapoint_index+1]))
            #we don't really need to calclate the delta values of the nose, we just need the nose values for the reach detection later

    #calculate distance between paw and pellet using delta values for current trial (at trial index)
    #variable naming note: d for delta
    RH_distances = []
    LH_distances = []
    for i in range(0, len(delta_X_RH)):
        #RH
        dRH_X = delta_X_RH[i] - delta_X_Pel[i]
        dRH_Y = delta_Y_RH[i] - delta_Y_Pel[i]
        RH_distances.append(distance(dRH_X, dRH_Y))
        #LH
        dLH_X = delta_X_LH[i] - delta_X_Pel[i]
        dLH_Y = delta_Y_LH[i] - delta_Y_Pel[i]
        LH_distances.append(distance(dLH_X, dLH_Y))

    #after the loop is complete, add all the list of all dists from this trial into the mega list
    #you can then have all the dists by trial (trial by index #)
    RHdist_allTrials.append(RH_distances)
    LHdist_allTrials.append(LH_distances)
    #these are 2D arrays

#notes:
#make sure to plot RH and LH in 2 diff color 
#overlap RH and LH as 2 separate plots?


# ------------ Calculating the average distance for the line plots ----------------
# idea: loop through the mega list and add all the values at the same index across all the trial lists
# then divide by the total number of trials len(of trial list)
# store this value into an averages list that you can use to plot as Y value
RH_averages = [] #average by frame/time, no distinction between trials anymore (1D array)
LH_averages = []
#RH
sum = 0
for i in range(0, len(RHdist_allTrials)-1):
    for j in range(0, len(RHdist_allTrials[i])-1):
        sum = sum + RHdist_allTrials[i][j]
RH_averages.append(sum)
#LH
sum = 0
for i in range(0, len(LHdist_allTrials)-1):
    for j in range(0, len(LHdist_allTrials[i])-1):
        sum = sum + LHdist_allTrials[i][j]
LH_averages.append(sum)

#this may not work well because sometimes the mouse reaches multiple times in this window. so the averages won't work out
#revisit this during the Fall

# ----------------- Reach isolation --------------------
#Threshold detection
#SET THRESHOLD VALUES
up_threshold_Y = 0  #this threshold is to prevent the case where the mouse is chewing at the slit higher up
low_threshold_Y = 0 #this is the threshold across which the mouse reaches
L_threshold_X = 0 # X threshold further reduces probability of inaccurate reach identification
R_threshold_X = 0

#SET TEMPORAL LENGTH OF PAW REACH in ms (e.g. 300 for 300ms)
reachTime = 300

#idea: loop through the list of data and extract the reaches, store reach data points as separate lists

#check if the paw is within threshold
#RH
for i in range(0, len(trial_data)): #to loop through the trials in the list
    for j in range(0, 8): #within each trial there are 8 sublists w all the values separated by axis
        #condition 1: check if current value is inside the threshold
        #recall: within trial_data[i][j]: [xRH, yRH, xLH, yLH, XPel, yPel, xNose, yNose]
        #if either the LH or RH is within the threshold:
        if ((trial_data[i][j][1] < up_threshold_Y and trial_data[i][j][1] > low_threshold_Y) or (trial_data[i][j][3] < up_threshold_Y and trial_data[i][j][3] > low_threshold_Y)): #starting point
            #check x thresholds next:
            if ((trial_data[i][j][0] > L_threshold_X and trial_data[i][j][0] < R_threshold_X) or (trial_data[i][j][2] > L_threshold_X and trial_data[i][j][2] < R_threshold_X)):
                
                #see where the nose is, and if it's within range
                #if (nose in range):
                    #then set reach boolean to true
                #if nose is within x and y thresholds
                if ((trial_data[i][j][6] > L_threshold_X and trial_data[i][j][6] < R_threshold_X) and (trial_data[i][j][7] < up_threshold_Y and trial_data[i][j][7] > low_threshold_Y)):

                    reach_likelihood_score = 0 #if this is > 4 then it's probably good - use this to mitigate incorrect DLC points
                    #check succesing 
                    

            #reach_likelihood_score = reach_likelihood_score + 1


            #********
            #Note: this algorithm is on pause due to the quality of the available data. 
            # The current dataset is from a model that performs too poorly for this algorithm to be effective
            # This will be revisited during the Fall semester once we can get recordings to be optimal
            #********


            #for succeding points, just check if they're in the same direction
            #if (RHdist_allTrials[i][j+1] ):
            #    reach_likelihood_score = reach_likelihood_score + 1
            #    
            #    if (RHdist_allTrials[i][j+2]):
            #        reach_likelihood_score = reach_likelihood_score + 1
            #        if (RHdist_allTrials[i][j+3]):
            #            reach_likelihood_score = reach_likelihood_score + 1



# ***************************************************************
# ----------------------- Line plots ----------------------------
# ***************************************************************
#notes: alpha = transparency
# s = size

#things to think about:
#do I want to also plot every single trial? I feel like there's too many trials for this to be effective
# -> average per trial?

#convert frames to time in seconds
xAxis_frames = list(range(0, trial_frames, 1)) # (start, end, interval)
xAxis_time = []
for i in range(0, len(xAxis_frames)-1):
    xAxis_time.append(xAxis_frames[i]/120)

#Now to plot ------------
#RH
plt.plot(xAxis_time, RH_averages, color="blueviolet", s=5, alpha=0.5)
#LH
plt.plot(xAxis_time, LH_averages, color="springgreen", s=5, alpha=0.5)

#customizing plot
plt.suptitle('Distance Between Paws & Pellet', fontsize=25, fontfamily='fantasy', y=0.96)
plt.ylabel('Distance (pixels)', fontsize=14, fontfamily='sans-serif', weight="bold") #add and customize y axis label
plt.xlabel('Time (s)', fontsize=14, fontfamily='sans-serif', weight="bold") #customize x axis label
#plt.xlim(0,1200)

plt.ylim(500,750)
#legend
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Right Paw',
                          markerfacecolor='blueviolet', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Left Paw',
                          markerfacecolor='springgreen', markersize=10)]

plt.legend(handles=legend_elements, loc="upper right")
fig = plt.gcf()
fig.set_size_inches(7,5)
 
# display plot
plt.show()
