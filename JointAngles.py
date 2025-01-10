"""Explanation of the Script:
Angle Calculation:

Uses maya.api.OpenMaya.MVector to calculate the angle between two vectors formed by three joints.
Converts the angle from radians to degrees for better readability.
Dynamic Updates:

Leverages a scriptJob with the timeChanged event to dynamically update angles during animation playback.
"""

"""
How to Use:
Select exactly three joints in Maya's viewport in the correct order: Start joint, Pivot joint (middle), and End joint.
Run the script in Maya's Script Editor.
Play the animation and watch the angles update dynamically in the viewport.
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om
import math

# Function to calculate the angle between three joints
def calculate_angle(joint1, joint2, joint3):
    pos1 = cmds.xform(joint1, query=True, worldSpace=True, translation=True)
    pos2 = cmds.xform(joint2, query=True, worldSpace=True, translation=True)
    pos3 = cmds.xform(joint3, query=True, worldSpace=True, translation=True)

    vec1 = om.MVector(pos1[0] - pos2[0], pos1[1] - pos2[1], pos1[2] - pos2[2])
    vec2 = om.MVector(pos3[0] - pos2[0], pos3[1] - pos2[1], pos3[2] - pos2[2])

    angle_rad = vec1.angle(vec2)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

# Function to create or update text annotation dynamically
def update_text_annotation(text_node, position, angle):
    if not cmds.objExists(text_node):
        # Create new text curve
        text_curve = cmds.textCurves(ch=False, text=f"{angle:.2f}°")
        cmds.move(position[0], position[1], position[2], text_curve)
        cmds.rotate(0, -90, 0, text_curve, relative=True)
        cmds.group(text_curve, name=text_node)
    else:
        # Update existing text
        text_shape = cmds.listRelatives(text_node, shapes=True, fullPath=True)
        if text_shape:
            cmds.delete(text_shape)
        text_curve = cmds.textCurves(ch=False, text=f"{angle:.2f}°")
        cmds.move(position[0], position[1], position[2], text_curve)
        cmds.rotate(0, -90, 0, text_curve, relative=True)
        cmds.parent(cmds.listRelatives(text_curve, shapes=True), text_node, relative=True)

# Callback function to update text dynamically during animation
def update_angle(selected):
    if len(selected) != 3:
        om.MGlobal.displayError("Please select exactly three joints.")
        return

    angle = calculate_angle(selected[0], selected[1], selected[2])

    # Get the position of the middle joint
    mid_pos = cmds.xform(selected[1], query=True, worldSpace=True, translation=True)
    update_text_annotation("angle_annotation", mid_pos, angle)

# UI to setup the process
def setup_ui():
    if cmds.window("angleVisualizerUI", exists=True):
        cmds.deleteUI("angleVisualizerUI")

    window = cmds.window("angleVisualizerUI", title="Joint Angle Visualizer")
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="Select three joints in the correct order:")
    cmds.button(label="Start Visualizing Angles", command=start_visualization)
    cmds.button(label="Stop Visualization", command=stop_visualization)

    cmds.showWindow(window)

# Start visualization by connecting a scriptJob
def start_visualization(*args):
    if len(cmds.ls(selection=True)) != 3:
        om.MGlobal.displayError("Please select exactly three joints.")
        return

    jobs = cmds.scriptJob(listJobs=True)
    for job in jobs:
        if "angleUpdateJob" in job:
            job_id = int(job.split()[0])
            cmds.scriptJob(kill=job_id, force=True)

    selected = cmds.ls(selection=True)

    # Create or update the text annotation dynamically
    cmds.scriptJob(event=["timeChanged", lambda: update_angle(selected)], killWithScene=True)
    om.MGlobal.displayInfo("Angle visualization started.")

# Stop the script and remove the dynamic updates
def stop_visualization(*args):
    jobs = cmds.scriptJob(listJobs=True)
    for job in jobs:
        if "angleUpdateJob" in job:
            job_id = int(job.split()[0])
            cmds.scriptJob(kill=job_id, force=True)
    if cmds.objExists("angle_annotation"):
        cmds.delete("angle_annotation")
    om.MGlobal.displayInfo("Angle visualization stopped.")

# Run the UI setup
setup_ui()
