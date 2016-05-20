# PythonScripts

This repository will contain python scripts developed/modified for specific purposes, 
which I found particularly useful or which functionalities where difficoult to find elsewer. 

## CategoricalScatterPlot

This script was developed to address a very specific scenario: to plot a scatter point graph 
with data points consisting in couples of categorical coordinates (string, string).
This particular situation generates the problem of visualizing the points when their number is high.
To address this issue a small amount of randomization in the position of the points is introduced. In this
way coinciding points will be visualized as clusters of adjacents points instead of a single point.
Of course this representation is just a visualization tool, since it inheerently modifies the real position of the points.

