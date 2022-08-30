#Kinematics - 3D (OptiTrack Data)
#Velocity vs Time

import argparse
from calendar import c
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure
from mpl_toolkits import mplot3d
import numpy as np
from scipy.interpolate import make_interp_spline
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.axis3d import Axis
import matplotlib.projections as proj
from matplotlib.colors import colorConverter

#import csv
data = pd.read_csv (r"C:\Users\Leanne\Desktop\School\Lab_2022\S2022\COMP402\Python_Files\Opti_Reach_Simulation.csv")
 
# make dataframe from data
df = pd.DataFrame(data, columns=["Frame", "Time", "X", "Y", "Z"])

#frame bounds
# firstframe = when the pellet disk starts
# lastframe = when the last trial ends
firstframe = 254;
lastframe = 9900;

#filtering by frame bounds:
df_frames = df[df['Frame'] > firstframe]
df_frames = df_frames[df_frames['Frame'] < lastframe]
df_time = df[df['Frame'] > firstframe]
df_time = df_time[df_time['Frame'] < lastframe]
df_x = df[df['Frame'] > firstframe]
df_x = df_x[df_x['Frame'] < lastframe]
df_y = df[df['Frame'] > firstframe]
df_y = df_y[df_y['Frame'] < lastframe]
df_z = df[df['Frame'] > firstframe]
df_z = df_z[df_z['Frame'] < lastframe]

#convert df to list:
frames = df_frames['Frame'].values.tolist()
time = df_time['Time'].values.tolist()
x = df_x['X'].values.tolist()
y = df_y['Y'].values.tolist()
z = df_z['Z'].values.tolist()
#len of sim = 9645

# -------------------------------------------------------------------------
# ------------------ auto split the trials --------------------------------
# -------------------------------------------------------------------------

fps = 120

# init_wait #time for pellet to start moving from stop to the first part of the trial zone
                #when you first start the system, the pellet starts from the paused stop at the dispenser
                #so it's a little more time than later on when you're still counting the trial zone, and
                #the pellet has already started moving towards the next trial zone, hence a little less general wait time
# gen_wait  #wait time in between all the trials after the first one

#do it by frame instead
init_wait = 9.5 * fps
gen_wait = 9 * fps
len_pause = 3
len_bufferTime = 1 #0.5s before and after the trial itself
trial_frames = (len_pause + len_bufferTime) * fps

start_frame = 0
end_frame = 0
trial_markers = [] #will be 2D     -> keeps start and end time stamps of trials in pairs
trial_data = [] #will be 3D        -> keeps actual data points between trial markers


#----------------- getting trial bounds -----------------------
#initial trial
start_frame = int(init_wait)
end_frame = start_frame + trial_frames
trial_markers.append([start_frame, end_frame])

#all other trials after first one
loopStarter = end_frame
while (start_frame < (lastframe-trial_frames)):
    start_frame = end_frame + gen_wait
    end_frame = start_frame + trial_frames
    if (start_frame < (lastframe-trial_frames)):
        trial_markers.append([start_frame, end_frame])


#some print statements to help double check things look good
#print (trial_markers)
#print ("total # of trials: " + str(len(trial_markers)))
#print (trial_markers)

#*********************
#partitioning data points by isolated trial times
#looping through all the time stamps to get the data into a nested list

for i in range(0, len(trial_markers)):
    start_frame = trial_markers[i][0]
    end_frame = trial_markers[i][1]
    trial_toAdd = [[],[],[]] #note: [z, y, x]
    #nested loop to get all the data in between those frames (the "trial zone")
    for j in range(start_frame, end_frame):
        if (x[j] != None): #if one is null, they are all null, and likewise for if it is not null
            trial_toAdd[1].append(x[j])
            trial_toAdd[2].append(y[j])
            trial_toAdd[0].append(z[j])
        #trial_toAdd[0].append(x[j])
        #trial_toAdd[1].append(y[j])
        #trial_toAdd[2].append(z[j])
        #i is the trial index
    trial_data.append(trial_toAdd) #add the entire trial to the mega list



# -------------------------------------------------------------------------
# ------------------------ Reach Isolation --------------------------------
# -------------------------------------------------------------------------
#Threshold detection
#SET THRESHOLD VALUES (all reaches should occur in this specified volume)
# values in cm
lower_threshold_Z = 12  #this threshold is to prevent the case where the mouse is chewing at the slit higher up
higher_threshold_Z = 16 #this is the threshold across which the mouse reaches
lower_threshold_X = 4 # X threshold further reduces probability of inaccurate reach identification
higher_threshold_X = 5.2
lower_threshold_Y = 0
higher_threshold_Y = 3

#SET TEMPORAL LENGTH OF PAW REACH in ms (e.g. 30 for 30ms)
reach_time = 1000   #this number is larger for now because my simulated reaches are much slower than a real mouse reach
reach_duration = math.ceil((reach_time / 1000) * fps)   # reach duration in frames -> *1000 to convert ms to s, *fps to get duration in frames, synonymous to each datapoint

#idea: loop through the list of data and extract the reaches, store reach data points as separate lists

isolated_reach_coordinates = [] #each index is a reach within a trial. Only houses data from 1 trial
isolated_reaches_allTrials = [] #each index is a trial, houses data from all trials
noReach_trials = []

for i in range(0, len(trial_data)): #to loop through the trials in the list   -> trial_data values are: [z, x, y] axes

    reach_bool = False #switch this bool depending on likelihood score

    #for axis in range(0, 3): #within each trial there are 3 sublists w all the values separated by axis
        #condition 1: check if current value is inside the threshold
        # j = 0 -> z values
        # j = 1 -> x values
        # j = 2 -> y values

    #get thresholds for given axis
    def axis_thresholds (axis):
        if (axis == 0):
            lower_threshold = lower_threshold_Z
            higher_threshold = higher_threshold_Z
        elif (axis == 1):
            lower_threshold = lower_threshold_X
            higher_threshold = higher_threshold_X
        elif (axis == 2):
            lower_threshold = lower_threshold_Y
            higher_threshold = higher_threshold_Y
        return (lower_threshold, higher_threshold)

    #check if first 5 datapoints are within threshold:
    def check_thresholds (i, axis, datapoint, lower_threshold, higher_threshold) :
        withinThreshold = False
        if (trial_data[i][axis][datapoint] > lower_threshold and trial_data[i][axis][datapoint] < higher_threshold):
            if (trial_data[i][axis][datapoint+1] > lower_threshold and trial_data[i][axis][datapoint+1] < higher_threshold):
                if (trial_data[i][axis][datapoint+2] > lower_threshold and trial_data[i][axis][datapoint+2] < higher_threshold):
                    if (trial_data[i][axis][datapoint+3] > lower_threshold and trial_data[i][axis][datapoint+3] < higher_threshold):
                        if (trial_data[i][axis][datapoint+4] > lower_threshold and trial_data[i][axis][datapoint+4] < higher_threshold):
                            withinThreshold = True
        return withinThreshold

    #determine if it's likely a reach or not
    def reach_determiner (axis):
        lower_threshold = axis_thresholds(axis)[0]
        higher_threshold = axis_thresholds(axis)[1]
        withinThreshold = check_thresholds(i, axis, datapoint, lower_threshold, higher_threshold)
        reach_axis_likelihood_score = 0

        if (withinThreshold):  
            #check slopes are towards the pellet for 10 points suceeding the first
            for a in range(0, 10):
                if (datapoint+a+1 < len(trial_data[i][axis])-1):
                    if ((trial_data[i][axis][datapoint+a] - trial_data[i][axis][datapoint+a+1]) < 0): #if <0, then slope is positive and in the right direction
                        reach_axis_likelihood_score += 1

            if (reach_axis_likelihood_score >= 7): #70% of points are towards the right direction, considered probable
                reach_axis_bool = True
            if (reach_axis_likelihood_score < 7):
                reach_axis_bool = False
        else:
            reach_axis_bool = False

        return reach_axis_bool


    #loop through all the datapoints in that axis, and compare each sequential 10-points. do this in parallel to the other 2 axes
    #if a reach is detected, it would be the start of that attempt, as datapoints are in order by time
    #so we can extract the reach by the reach duration specified, and jump the iterator variable to the end of that reach so that partial duplicate reaches aren't detected and recorded
    
    # then calculate differences between  point 1 and point 2, for each x y z
    # and if its + or -, can tell which direction in each axis
    # if for 10 consective points it meets the criteria (seeing if things are in the same direction is more obvious with OptiTrack than it is in 2D with DLC)
    #then take the first coordinate of that chain check, and count 30 ms from that point

    #trial_data[i][0] -> length should be the same for [i][0], [i][1], [i][2] so picked one for loop:
    for datapoint in range(0, len(trial_data[i][0])-reach_duration): #subtract duration to prevent out of bounds if a reach is detected towards the end within the specificed duration
        # Z axis first
        z_reach_bool = reach_determiner(0)
        # Y axis
        y_reach_bool = reach_determiner(2)
        # X axis is parallel to the direction of reaching, so it is more effective to check this later
        
        #if both axes are in the right direction:
        if (z_reach_bool and y_reach_bool):
            reach_coords_toAdd = [[],[],[]]

            #get the datapoints from starting point to the end of the specified reach duration
            for p in range(datapoint, (datapoint+reach_duration)):
                reach_coords_toAdd[0].append(trial_data[i][0][p])
                reach_coords_toAdd[1].append(trial_data[i][1][p])
                reach_coords_toAdd[2].append(trial_data[i][2][p])

            #check if points' x coordinates are reasonable:
            #take the min and max x coords, and see if they are greater than 0.4cm
            #during an isolated reach attempt, there is no reason for any of the points to be beyond this range in this axis (and this range is quite generous)
            #if it is beyond this range, then the mouse is probably doing something other than reaching, and thus is not a reach attempt

            valid_x_range = 0.4 #change this as necessary, in cm
            max_x = max(reach_coords_toAdd[1])
            min_x = min(reach_coords_toAdd[1])
            if ((max_x - min_x) < valid_x_range):
                reach_bool = True
                isolated_reach_coordinates.append(reach_coords_toAdd)

            datapoint = datapoint + reach_duration #accelerate iterator
            
    #partitinoing of current trial complete, if a reach attempt exists during the trial, add it to the trials list
    if (reach_bool):
        isolated_reaches_allTrials.append(isolated_reach_coordinates)
    
    #keep track of trials without any reach attempts for record purposes
    else:
        noReach_trials.append(i)
        #to see how many trials had no reach attempts, you can print out the length of this list
        #or print this list to see specific trials. you can also save this to a CSV file with a simple function



# ----------------------------------------------------------------------------------------------------
# ----------------------- Calculating Distance Between Adjacent Datapoints ---------------------------
# ----------------------------------------------------------------------------------------------------

# Note that since the pellet is not tracked in optitrack, for the purposes of comparison and proof of concept for this algorithm, 
# a coordinate point approximately where the pellet should be during a reach trial will be used

# PLaceholder pellet coordinates:
placeholder_pel_X = 15.5
placeholder_pel_Y = 4.5
placeholder_pel_Z = 2
# (values already translated to (z, x, y), so they will correspond with python xyz functions)

#change these to perform analysis on a specified reach
trial_num = 5
reach_num = 220

iso_reach_data = isolated_reaches_allTrials[trial_num][reach_num]

#function to calculate the distance (hypotenuse between X and Y)
def distance(x, y, z):
      d = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
      return d

dist_allTrials = [] #will be 2D
# get delta values
#new lists that you can store the calculated values to be plotted later
delta_X = []
delta_Y = []
delta_Z = []
time_between_points = [] #stores time between points based on detected gaps in data (gaps are NaN values)

#calculate the delta values
point1_x = 0 #temp first point that gets updated to account for marker occlusions - I can't check each point sequentially without removing the time dimension
point1_y = 0 
point1_z = 0 
gap_counter = 0 #to count gaps in the data to determine time between points
gap_counter_temp = 0
for datapoint_index in range(0,len(iso_reach_data[0])-1):
    gap_counter += 1 #always add 1 for every loop, since every loop is advancing to the next point. Then reset it when the point is not null
    gap = True
    #set point1 to current datapoint if not null
    if (math.isnan(iso_reach_data[0][datapoint_index]) == False):
        if (math.isnan(iso_reach_data[1][datapoint_index]) == False):
            if (math.isnan(iso_reach_data[2][datapoint_index]) == False):
                point1_x = iso_reach_data[0][datapoint_index]
                point1_y = iso_reach_data[1][datapoint_index]
                point1_z = iso_reach_data[2][datapoint_index]
    
    if (math.isnan(iso_reach_data[0][datapoint_index+1]) == False):
        delta_X.append(abs(point1_x - iso_reach_data[0][datapoint_index+1]))
        point1_x = iso_reach_data[0][datapoint_index+1] #update temp first point
        gap = False
        gap_counter_temp = gap_counter
        gap_counter = 0
    if (math.isnan(iso_reach_data[1][datapoint_index+1]) == False):
        delta_Y.append(abs(point1_y - iso_reach_data[0][datapoint_index+1]))
        point1_y = iso_reach_data[1][datapoint_index+1]
    if (math.isnan(iso_reach_data[2][datapoint_index+1]) == False):
        delta_Z.append(abs(point1_z - iso_reach_data[0][datapoint_index+1]))
        point1_z = iso_reach_data[2][datapoint_index+1]

    if (gap == False):
        time_between_points.append(gap_counter_temp) #gaps should be uniform across all 3 axes, since if there's an occusion it'd be absent from all axes

    
    #this way if there is a gap, or multiple gaps, it can then compare the difference between the gap rather than just ignoring it, which we don't want

distances = []
for i in range(0, len(delta_X)):
    d_X = delta_X[i]
    d_Y = delta_Y[i]
    d_Z = delta_Z[i]
    distances.append(distance(d_X, d_Y, d_Z))


#distances = []
#calculating distances from reach point to pellet location and adding each distance to a list
#for i in range(0, len(iso_reach_data[0])):
    # using "or" instead of "and" since if one of them is null, it would be true, and neither can be null
#    if ((math.isnan(iso_reach_data[0][i]) or math.isnan(iso_reach_data[0][i+1])) == False):  #if it is not null, then the other axes are also not null
#        d_X = abs(iso_reach_data[0][i] - iso_reach_data[0][i+1])
#        d_Y = abs(iso_reach_data[1][i] - iso_reach_data[1][i+1])
#        d_Z = abs(iso_reach_data[2][i] - iso_reach_data[2][i+1])
#        distances.append(distance(d_X, d_Y, d_Z))


# --------------------------------------------------------------------------------
# ----------------------- Calculating Average Velocity ---------------------------
# --------------------------------------------------------------------------------

#convert time_between_points from gap frames to s
temp = 0
time_between_in_seconds = []
for i in range(0, len(time_between_points)):
    temp = time_between_points[i] / fps
    time_between_in_seconds.append(temp)

#add the gaps to their next gap value for plotting (this is to get the actual time of when the point started in the reach)
time_consecutive = []
temp = 0
for i in range(0, len(time_between_in_seconds)-1):
    if (i == 0):
        time_consecutive.append(time_between_in_seconds[0])
    temp = time_consecutive[i] + time_between_in_seconds[i+1]
    time_consecutive.append(temp)

def velocity (distance, time):
    velocity = distance / time
    return velocity

temp_d = 0
temp_t = 0
velocities = []
for i in range(0, len(distances)):
    temp_d = distances[i]
    temp_t = time_between_in_seconds[i]
    v = velocity(temp_d, temp_t)
    velocities.append(v)
    
np_velocities = np.array(velocities)
#np_times = np.array(time_between_in_seconds)
np_times = np.array(time_consecutive) #np.arange(0, len(velocities))


# -------------------------------------------------------------------------
# ----------------------- Plotting: Line Plots ---------------------------
# -------------------------------------------------------------------------


########### Coloring 1 specific gridline in the scatterplot #################
# I didn't actually end up using this this time, but leaving this here since I will look more into it during the Fall

class axis3d_custom(Axis):
    def __init__(self, adir, v_intervalx, d_intervalx, axes, *args, **kwargs):
        Axis.__init__(self, adir, v_intervalx, d_intervalx, axes, *args, **kwargs)
        self.gridline_colors = []
    def set_gridline_color(self, *gridline_info):
        '''Gridline_info is a tuple containing the value of the gridline to change
        and the color to change it to. A list of tuples may be used with the * operator.'''
        self.gridline_colors.extend(gridline_info)
    def draw(self, renderer):
        # filter locations here so that no extra grid lines are drawn
        Axis.draw(self, renderer)
        which_gridlines = []
        if self.gridline_colors:
            locmin, locmax = self.get_view_interval()
            if locmin > locmax:
                locmin, locmax = locmax, locmin

            # Rudimentary clipping
            majorLocs = [loc for loc in self.major.locator() if
                         locmin <= loc <= locmax]
            for i, val in enumerate(majorLocs):
                for colored_val, color in self.gridline_colors:
                    if val == colored_val:
                        which_gridlines.append((i, color))
            colors = self.gridlines.get_colors()
            for val, color in which_gridlines:
                colors[val] = colorConverter.to_rgba(color)
            self.gridlines.set_color(colors)
            self.gridlines.draw(renderer, project=True)

class XAxis(axis3d_custom):
    def get_data_interval(self):
        'return the Interval instance for this axis data limits'
        return self.axes.xy_dataLim.intervalx

class YAxis(axis3d_custom):
    def get_data_interval(self):
        'return the Interval instance for this axis data limits'
        return self.axes.xy_dataLim.intervaly

class ZAxis(axis3d_custom):
    def get_data_interval(self):
        'return the Interval instance for this axis data limits'
        return self.axes.zz_dataLim.intervalx

class Axes3D_custom(Axes3D):
    """
    3D axes object.
    """
    name = '3d_custom'

    def _init_axis(self):
        '''Init 3D axes; overrides creation of regular X/Y axes'''
        self.w_xaxis = XAxis('x', self.xy_viewLim.intervalx,
                            self.xy_dataLim.intervalx, self)
        self.xaxis = self.w_xaxis
        self.w_yaxis = YAxis('y', self.xy_viewLim.intervaly,
                            self.xy_dataLim.intervaly, self)
        self.yaxis = self.w_yaxis
        self.w_zaxis = ZAxis('z', self.zz_viewLim.intervalx,
                            self.zz_dataLim.intervalx, self)
        self.zaxis = self.w_zaxis

        for ax in self.xaxis, self.yaxis, self.zaxis:
            ax.init3d()
proj.projection_registry.register(Axes3D_custom)

####################################################################################

#x = np.arange(0, len(np_dist_allTrials))
#add the gaps to their next gap value for plotting (this is to get the actual time of when the point started in the reach)
#x = []
#temp = 0
#for i in range(0, len(time_between_points)-1):
#    if (i == 0):
#        x.append(time_between_points[0])
#    temp = x[i] + time_between_points[i+1]
#    x.append(temp)

x = np_times
y = np_velocities

X_Y_Spline = make_interp_spline(x, y)

# Returns evenly spaced numbers
# over a specified interval.
X_ = np.linspace(min(x), max(x), 500)
Y_ = X_Y_Spline(X_)

#plt.plot(x,y)
plt.plot(X_, Y_, color="hotpink")

#customizing plot
plt.suptitle('Velocity vs. Time', fontsize=25, fontfamily='fantasy')
plt.ylabel('Velocity (cm/s)', fontsize=14, fontfamily='sans-serif', weight="bold") #add and customize y axis label
plt.xlabel('Time (s)', fontsize=14, fontfamily='sans-serif', weight="bold") #customize x axis label

# resize figure
#fig = plt.gcf()
#fig.set_size_inches(10,5)

# display plot
plt.show()

#############################################################
###### Additional notes on data structure for clarity #######
#############################################################

#  trial_data = [                                -> 3D
#    [[z_coordinate values], [x_coordinates values], [y_coordinates values]], #trial 0
#    [[z_coordinates values], [x_coordinates values], [y_coordinates values]], #trial 1
#    ...
#    [[z_coordinates values], [x_coordinates values], [y_coordinates values]] #trial n
#  ]
# ________________________________

#  trial_toAdd = trial_data[i]     -> see above
# ________________________________

#  isolated_reach_coordinates = [                -> 3D
#    [[z_coordinate values], [x_coordinates values], [y_coordinates values]], #reach 0
#    [[z_coordinates values], [x_coordinates values], [y_coordinates values]], #reach 1
#    ...
#    [[z_coordinates values], [x_coordinates values], [y_coordinates values]] #reach n
#  ]
# ________________________________

#  isolated_reaches_allTrials = [                -> 4D
#     [ #trial 1
#        [[z_coordinate values], [x_coordinates values], [y_coordinates values]], #reach 0
#        [[z_coordinates values], [x_coordinates values], [y_coordinates values]], #reach 1
#        ...
#        [[z_coordinates values], [x_coordinates values], [y_coordinates values]] #reach n
#     ],
#     [ #trial 2
#        [[z_coordinate values], [x_coordinates values], [y_coordinates values]], #reach 0
#        [[z_coordinates values], [x_coordinates values], [y_coordinates values]], #reach 1
#        ...
#        [[z_coordinates values], [x_coordinates values], [y_coordinates values]] #reach n
#     ]
#        ...   -> to trial n
#  ]
