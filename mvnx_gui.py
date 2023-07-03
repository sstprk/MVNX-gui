import matplotlib.pyplot as plt
import PySimpleGUI as sg
from load_mvnx import load_mvnx
import argparse
import os

#Segment names
segment =[
    "SEGMENT PELVIS",
    "SEGMENT L5",
    "SEGMENT L3",
    "SEGMENT T12",
    "SEGMENT T8",
    "SEGMENT NECK",
    "SEGMENT HEAD",
    "SEGMENT RIGHT SHOULDER",
    "SEGMENT RIGHT UPPER ARM",
    "SEGMENT RIGHT FOREARM",
    "SEGMENT RIGHT HAND",
    "SEGMENT LEFT SHOULDER",
    "SEGMENT LEFT UPPER ARM",
    "SEGMENT LEFT FOREARM",
    "SEGMENT LEFT HAND",
    "SEGMENT RIGHT UPPER LEG",
    "SEGMENT RIGHT LOWER LEG",
    "SEGMENT RIGHT FOOT",
    "SEGMENT RIGHT TOE",
    "SEGMENT LEFT UPPER LEG",
    "SEGMENT LEFT LOWER LEG",
    "SEGMENT LEFT FOOT",
    "SEGMENT LEFT TOE"
]

def main(file_name):
    # Check for file existence
    if not os.path.isfile(file_name):
        raise Exception("File %s could not be found" % file_name)

    tokens = file_name.lower().split('.')
    extension = tokens[-1]

    # Check for file extension
    if not extension == 'mvnx':
        raise Exception("File must be an .mvnx file")
    
#Interface design
sg.theme("DarkAmber")
layout = [
    [sg.T("MVNX File:")],
    [sg.FileBrowse(key="-PATH-", file_types=(("MVNX Files", "*.mvnx"),))],
    [sg.Ok(), sg.Cancel()],
    [sg.HorizontalSeparator()],
    [sg.T("Segment:")],
    [sg.DropDown(segment, default_value= segment[0], key="-DD-")]
]
window = sg.Window("MVNX", layout, size=(500,200))

#Persistent window
while True:
    event, values= window.read()
    if event == "Ok":
        if values["-PATH-"] != "":
            mvnx_file = load_mvnx(values["-PATH-"])

            # Read some basic data from the file
            comments = mvnx_file.comments
            frame_rate = mvnx_file.frame_rate
            configuration = mvnx_file.configuration
            original_file_name = mvnx_file.original_file_name
            recording_date = mvnx_file.recording_date
            actor_name = mvnx_file.actor_name
            frame_count = mvnx_file.frame_count
            version = mvnx_file.version
            segment_count = mvnx_file.segment_count
            joint_count = mvnx_file.joint_count

            # Read the data from the structure e.g. first segment
            idx = segment.index(values["-DD-"])
            segment_name = mvnx_file.segment_name_from_index(idx)
            segment_pos = mvnx_file.get_segment_pos(idx)

            # Alternatively, use the generic method get_data() with the data set and field. E.g.:
            # segment_pos = mvnx_file.get_data('segment_data', 'pos', idx)

            if segment_pos:
                # Plot position of a segment
                plt.figure(0)
                plt.plot(segment_pos)
                plt.xlabel('frames')
                plt.ylabel('Position in the global frame')
                plt.title('Position of ' + segment_name + ' segment')
                plt.legend(['x', 'y', 'z'])
                plt.draw()

                # Plot 3D displacement of a segment
                x, y, z = map(list, zip(*[[frame[0], frame[1], frame[2]] for frame in segment_pos]))
                plt.figure(1)
                plt.axes(projection="3d")
                plt.plot(x, y, z)
                plt.xlabel('frames')
                plt.title('Position of ' + segment_name + ' segment in 3D')
                plt.draw()
                plt.show()
        else:
            sg.popup("Please choose a file!")
    #Closing the window
    if event in ("Cancel", sg.WIN_CLOSED):
        window.close()
        break
    print(event, values)