# Kerbal_Engine_Mapper_Python
This tool visualizes the optimal cost and optimal mass rockets for Kerbal Space Program. 
It is intended to serve the same purposes as the original Matlab tool but be more open source.
The tool also has a Rocket Stage Planner that allows you to plan stages of a rocket.  
The optimizer finds all best cost and best mass options and constructs a pareto frontier of best case rockets.  
It then uses the masses of those rocket to determine the best one to be used on the next stage.  
This is an exponential process so adding more stages greatly increases computation time.
