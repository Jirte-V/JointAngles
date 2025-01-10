# JointAngles

Joint angle script
Functions
Angle Calculation (calculate_angle)
•	calculates the angle at the middle joint formed by two vectors: one from the start joint to the middle joint and another from the middle joint to the end joint.
•	How does it work?
1.	Gets the world-space positions of the three selected joints using cmds.xform.
2.	Constructs two vectors using maya.api.OpenMaya.MVector.
3.	Calculates the angle between these vectors in radians using the angle method.
4.	Converts the angle to degrees using math.degrees.
Text Annotation (update_text_annotation)
•	Creates/updates text object in the viewport to show the angle.
•	How does it work?
1.	If a text group with the name angle_annotation already exists, it deletes it.
2.	Creates a new text curve using cmds.textCurves and groups it into a named group (angle_annotation).
3.	Positions the text slightly offset from the middle joint (8 units on the Z-axis) for visibility. This is easy to change if necessary.
4.	Scales the text by a factor of 2 to make it more readable. This is also easy to change if necessary.
5.	Rotates the text -90 degrees along the Y-axis to ensure proper orientation in the viewport. This is also easy to change if necessary.
Dynamic Updates During Animation (update_angle)
•	The angle text updates when the scene's time changes.
•	How does it work?
1.	Calculate the current angle between the three joints by calling calculate_angle.
2.	Returns the middle joint's position and passes it, along with the calculated angle, to update_text_annotation.
UI
•	A window with instructions to select three joints in the proper order. With buttons for starting and stopping the visualisation.
Visualisation 
Start Visualization (start_visualization): 
•	Sets up a scriptJob to dynamically update the angle text during animation playback.
•	Make sure exactly three joints are selected. Otherwise, shows an error.
•	Stops any previously running visualization (calls stop_visualization).
•	Creates a scriptJob bound to the timeChanged event, which calls update_angle to update the text annotation on each frame.
Stop Visualization (stop_visualization)
•	Checks if a scriptJob (tracked via the global variable angle_job_id) exists. If it does, the job is terminated.
•	Deletes the angle_annotation text group if it exists.
•	Displays a message confirming the cleanup.

How to use
1.	Run the Script
2.	Select Joints
o	Select three joints in the order:
1.	Start Joint: The joint at the start of the chain.
2.	Middle Joint: The joint where the angle is calculated.
3.	End Joint: The joint at the end of the chain.
3.	Start Visualization:
o	click "Start Visualizing Angles".
o	The angle will appear dynamically updated near the middle joint during animation playback.
4.	Stop Visualization:
o	Click "Stop Visualization" to stop updates and clean up the text.
This script is useful for animators and riggers to analyze joint behavior and ensure proper motion or deformation. Could also be useful in medical applications for motion analysis.

