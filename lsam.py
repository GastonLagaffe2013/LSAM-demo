import configparser
import socket
import tqdm
import os
import argparse
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

canvas_width = 400
canvas_height = 290


c_DeltaHost = "192.168.178.80"
c_DeltaDevice = "/dev/ttyUSB0"
c_DeltaPort = 6001
c_RobotHost = "192.168.178.81"
c_RobotDevice = "/dev/ttyUSB0"
c_RobotPort = 6002
c_GripperHost = "192.168.178.82"
c_GripperDevice = "/dev/ttyUSB0"
c_GripperPort = 6003
config = configparser.ConfigParser()
try:
    config.read('AtosLSAM.ini')
    print("Reading configuration")
    c_DeltaHost = (config['DeltaPrinter']['host'])
    c_DeltaDevice = (config['DeltaPrinter']['device'])
    c_DeltaPort = int(config['DeltaPrinter']['port'])
    c_RobotHost = (config['RobotArm']['host'])
    c_RobotDevice = (config['RobotArm']['device'])
    c_RobotPort = int(config['RobotArm']['port'])
    c_GripperHost = (config['Gripper']['host'])
    c_GripperDevice = (config['Gripper']['device'])
    c_GripperPort = int(config['Gripper']['port'])
except:
    print("Using default configuration")
    conf_camera = 0 

parser = argparse.ArgumentParser(description="LSAM worker")
parser.add_argument("-t", "--type", help="Gui Type (GUI/CLI)", default="CLI")
parser.add_argument("-m", "--mode", help="LSAM mode (arm, gripper, printer, master)", default="master")
args = parser.parse_args()
c_type = args.type
c_mode = args.mode

print(f"[+] Delta Printer on {c_DeltaHost}:{c_DeltaPort} {c_DeltaDevice}")
print(f"[+] RobotArm on {c_RobotHost}:{c_RobotPort} {c_RobotDevice}")
print(f"[+] Delta Printer on {c_GripperHost}:{c_GripperPort} {c_GripperDevice}")
print(f"[+] interface mode:{c_type}")
print(f"[+] LSAM mode:{c_mode}")

#GUI
# NOTE: Frame will make a top-level window if one doesn't already exist which
# can then be accessed via the frame's master attribute

# make a Frame whose parent is root, named "LSAM"
master = Frame(name='dashboard')
root = master.master  # short-cut to top-level window
master.pack()  # pack the Frame into root, defaults to side=TOP
root.title('LSAM Dashboard')  # name the window
root.option_add("*Font", "helvetica 8")

# create notebook
dashPanel = Frame(master, name='dash')  # create a new frame slaved to master
dashPanel.pack()  # pack the Frame into root

# create (notebook) demo panel
nb = ttk.Notebook(dashPanel, name='notebook')  # create the ttk.Notebook widget

# extend bindings to top level window allowing
#   CTRL+TAB - cycles thru tabs
#   SHIFT+CTRL+TAB - previous tab
#   ALT+K - select tab using mnemonic (K = underlined letter)
nb.enable_traversal()

nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)  # add margin

##################################################################################
# create notebook tab for robot arm
# populate the third frame with a text widget
arm_frame = Frame(nb)
arm_input = Frame(arm_frame)
arm_output = Frame(arm_frame)

arm_in = Text(arm_input, wrap=WORD, width=60, height=30)
arm_out = Text(arm_output, wrap=WORD, width=60, height=30)
arm_scrollin = Scrollbar(arm_input, orient=VERTICAL, command=arm_in.yview)
arm_scrollout = Scrollbar(arm_output, orient=VERTICAL, command=arm_out.yview)
arm_in['yscroll'] = arm_scrollin.set
arm_out['yscroll'] = arm_scrollout.set
arm_scrollin.pack(side=RIGHT, fill=Y)
arm_scrollout.pack(side=RIGHT, fill=Y)
arm_in.pack(fill=BOTH, expand=Y)
arm_out.pack(fill=BOTH, expand=Y)

def ClearArmSerial():
    arm_out.delete(0.0, END)
    arm_in.delete(0.0, END)

ClrArmBtn = Button(arm_frame, text='Clear', underline=0, command=ClearArmSerial)
ClrArmBtn.grid(row=1, column=0, sticky=W)
arm_input.grid(row=0, column=0, sticky=W)
arm_output.grid(row=0, column=1, sticky=W)

# add to notebook (underline = index for short-cut character)
nb.add(arm_frame, text='Robot Arm Monitor', underline=0)
##################################################################################

##################################################################################
# create notebook tab for gripper
# populate the third frame with a text widget
grp_frame = Frame(nb)
grp_input = Frame(grp_frame)
grp_output = Frame(grp_frame)

grp_in = Text(grp_input, wrap=WORD, width=60, height=30)
grp_out = Text(grp_output, wrap=WORD, width=60, height=30)
grp_scrollin = Scrollbar(grp_input, orient=VERTICAL, command=grp_in.yview)
grp_scrollout = Scrollbar(grp_output, orient=VERTICAL, command=grp_out.yview)
grp_in['yscroll'] = grp_scrollin.set
grp_out['yscroll'] = grp_scrollout.set
grp_scrollin.pack(side=RIGHT, fill=Y)
grp_scrollout.pack(side=RIGHT, fill=Y)
grp_in.pack(fill=BOTH, expand=Y)
grp_out.pack(fill=BOTH, expand=Y)

def ClearGrpSerial():
    grp_out.delete(0.0, END)
    grp_in.delete(0.0, END)

ClrArmBtn = Button(grp_frame, text='Clear', underline=0, command=ClearGrpSerial)
ClrArmBtn.grid(row=1, column=0, sticky=W)
grp_input.grid(row=0, column=0, sticky=W)
grp_output.grid(row=0, column=1, sticky=W)

# add to notebook (underline = index for short-cut character)
nb.add(grp_frame, text='Gripper Monitor', underline=0)
##################################################################################


def myLoop():
    global arm_out
    global arm_in
    global grp_out
    global grp_in
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = 'ARM>' + current_time + '<\n\r'
#    mySerial.write(msg.encode())
    arm_in.insert(END, msg)
    arm_out.insert(END, msg)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = 'GRP>' + current_time + '<\n\r'
#    mySerial.write(msg.encode())
    grp_in.insert(END, msg)
    grp_out.insert(END, msg)

    master.after(100, myLoop)
    
master.after(100, myLoop)
master.mainloop()