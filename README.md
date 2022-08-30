# COMP 402
Honors Project in Computer Science &amp; Biology

This repository houses all the code and other files that were a part of my project.

## 2D Analysis (DLC)

### uR_Score_Comparison.py
Calculates the uR score of 2 different trials being analyzed using the uR score equations defined in my report. Then plots a bar graph comparing the performance of both.

### HistogramPlotting.py
Calculates delta_X and delta_Y values and plots a histogram of the frequencies of consecutive coordinate differences of a trial. Rerun the script for each trial being analyzed to obtain the histogram for it. Histograms are modeled after the DLC output histograms (Mathis et al., 2018).

### LikelihoodPlotting.py
Plots the network confidence likelihood of a trial. You can isolate each element of interest (i.e. each color line representing a paw or pellet) for easier analysis. Modeled after the DLC output likelihood plot (Mathis et al., 2018).

### LossFunctionPlotting.py
Plots the loss function over iterations of network training.

### TrajectoryPlotting.py
Plots a 2D cumulative trajectory plot of a trial. Points are plotted over the whole duration of the video. Modeled after the DLC output trajectory plot (Mathis et al., 2018).

### XY_CoordinatesPlotting.py
Plots the X and Y coordinates separately over time (in frames). Modeled after the DLC output XY coordinates plot (Mathis et al., 2018).

### 2D_Distance.py
Calculates the distances between the paws (both right and left hands) and the pellet during one extracted reaching movement, and plots them over time.

## 3D Analysis (OptiTrack)
All code files below include trial isolation and reach detection to extract relevant datapoints.

### 3D_TrajectoryPlot.py
Plots a 3D cumulative trajectory plot of a trial. Points are plotted over the whole duration of the video. Plots can be rotated in 3D space, and variables are set in the code to earily save different viewpoints (e.g. frontal view, side view, top down view, etc.)

### 3D_Distance.py
Calculates the distances between the paw and the pellet during one extracted reaching movement, and plots them over time. 

### 3D_Velocity.py
Calculates the average velocities between each datapoint in one extracted reaching movement and plots them over time.

### 3D_Acceleration.py
Calculates the acceleration between each datapoint in one extract reaching movement and plots them over time.


## Other Code & Files

### Food_Delivery.py
Code that controls and automates the experimental apparatus (delivery disk and food dispenser).

### Spherical_w_Base.stl
3D design of a spherical 1.5 mm diameter marker with a circular base for 3D printing.

### Hemispherical.stl
3D design of a hemispherical 1.5 mm diameter marker for 3D printing.


