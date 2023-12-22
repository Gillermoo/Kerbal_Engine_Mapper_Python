# Kerbal_Engine_Mapper_Python
This tool visualizes the optimal cost and optimal mass rockets for Kerbal Space Program. 
It is intended to serve the same purposes as the original Matlab tool but be more open source.
The tool also has a Rocket Stage Planner that allows you to plan stages of a rocket.  
The optimizer finds all best cost and best mass options and constructs a pareto frontier of best case rockets.  
It then uses the masses of those rocket to determine the best one to be used on the next stage.  
This is an exponential process so adding more stages greatly increases computation time.

![alt text](https://private-user-images.githubusercontent.com/89491478/292497707-293c00d5-5718-464e-a489-8b92f3df4af6.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDMyNTIzNDMsIm5iZiI6MTcwMzI1MjA0MywicGF0aCI6Ii84OTQ5MTQ3OC8yOTI0OTc3MDctMjkzYzAwZDUtNTcxOC00NjRlLWE0ODktOGI5MmYzZGY0YWY2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMjIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjIyVDEzMzQwM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTQ5ZDFjZTUxMjEwMDExOThkM2M0M2E1NDI3YWQwMGY0NGM2ZTk0ODcwYmNlZjNiMDUzNDU4NDI2MTIwMDExODAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.getllPGStGp7dbzvQOn36jUa9xHUJHe-XsLilALUFxE)
