import sys
import configparser
from socket import *
import tqdm
import os
import argparse
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

canvas_width = 400
canvas_height = 290
LSAM_ON = False

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

def exitPrg():
    print("Closing Program")
    root.destroy()
    sys.exit()


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
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = 'Clear - ' + current_time + '\n\r'
    arm_in.insert(END, msg)
    arm_out.insert(END, msg)

def dummy(cmd):
    global c_RobotHost
    global c_RobotPort
    global LSAM_ON
    print(f"[+] SendArm called {cmd}")
    arm_out.insert(END, "calling...")

def SendArm(cmd):
    global c_RobotHost
    global c_RobotPort
    global LSAM_ON
#    print(f"[+] SendArm called")
    serverName = c_RobotHost
    serverPort = c_RobotPort
    print(f"[+] SendArm try connect {serverName} on {serverPort}")
#    arm_out.insert(END, "try to connect ...\n\r")
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        print(f"[+] SendArm try open socket")
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(bytes(cmd, 'utf-8'))
        replyfromserver = str(clientSocket.recv(1024),'utf-8')
        print(f"[+] Reply Message from Server: {replyfromserver}")
        arm_in.insert(END, cmd+'\n\r')
        arm_out.insert(END, replyfromserver+'\n\r')
        clientSocket.close()
    except:
        print(f"[+] SendArm connect failed")
        arm_out.insert(END, "FAIL connection timeout\n\r")

            

ArmBtnExit = Button(arm_frame, text='Exit', underline=0, command = exitPrg)
ArmBtnClear = Button(arm_frame, text='Clear', underline=0, command=ClearArmSerial)
ArmBtnVersion = Button(arm_frame, text='Connect', underline=0, command = lambda: SendArm("Version"))
ArmBtnHome = Button(arm_frame, text='Home', underline=0, command = lambda: SendArm("Home"))
ArmBtnPos1 = Button(arm_frame, text='Pos1', underline=0, command = lambda: SendArm("Pos1"))
ArmBtnPos2 = Button(arm_frame, text='Pos2', underline=0, command = lambda: SendArm("Pos2"))
ArmBtnPark = Button(arm_frame, text='Park', underline=0, command = lambda: SendArm("Park"))
ArmBtnExit.place(x=0, y=424, width=48)
ArmBtnClear.place(x=50, y=424, width=48)
ArmBtnVersion.place(x=100, y=424, width=48)
ArmBtnHome.place(x=150, y=424, width=48)
ArmBtnPos1.place(x=200, y=424, width=48)
ArmBtnPos2.place(x=250, y=424, width=48)
ArmBtnPark.place(x=300, y=424, width=48)
arm_ttlvar1 = StringVar()
arm_ttlvar1.set('Robot Arm Control Version 0.1.1')
arm_title1 = Label(arm_frame, textvariable=arm_ttlvar1, anchor=CENTER, background="#000000", foreground="#FFC000")
arm_title1.grid(row=1, column=1, sticky=E)
arm_input.grid(row=0, column=0, sticky=W)
arm_output.grid(row=0, column=1, sticky=W)

# add to notebook (underline = index for short-cut character)
nb.add(arm_frame, text='Robot Arm Control', underline=0)
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
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = 'Clear - ' + current_time + '\n\r'
    grp_in.insert(END, msg)
    grp_out.insert(END, msg)

def SendGrp(cmd):
    global c_GripperHost
    global c_GripperPort
    global LSAM_ON
#    print(f"[+] SendGrp called")
    serverName = c_GripperHost
    serverPort = c_GripperPort
    print(f"[+] SendGrp try connect {serverName} on {serverPort}")
#    grp_out.insert(END, "try to connect ...\n\r")
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        print(f"[+] SendGrp try open socket")
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(bytes(cmd, 'utf-8'))
        replyfromserver = str(clientSocket.recv(1024),'utf-8')
        print(f"[+] Reply Message from Server: {replyfromserver}")
        grp_in.insert(END, cmd+'\n\r')
        grp_out.insert(END, replyfromserver+'\n\r')
        clientSocket.close()
    except:
        print(f"[+] SendGrp connect failed")
        grp_out.insert(END, "FAIL connection timeout\n\r")

GrpBtnExit = Button(grp_frame, text='Exit', underline=0, command = exitPrg)
GrpBtnClear = Button(grp_frame, text='Clear', underline=0, command=ClearGrpSerial)
GrpBtnVersion = Button(grp_frame, text='Connect', underline=0, command = lambda: SendGrp("Version"))
GrpBtnHome = Button(grp_frame, text='Pump ON', underline=0, command = lambda: SendGrp("Pump ON"))
GrpBtnPos1 = Button(grp_frame, text='Pump OFF', underline=0, command = lambda: SendGrp("Pump OFF"))
GrpBtnPos2 = Button(grp_frame, text='Attach', underline=0, command = lambda: SendGrp("Attach"))
GrpBtnPark = Button(grp_frame, text='Release', underline=0, command = lambda: SendGrp("Release"))

GrpBtnExit.place(x=0, y=424, width=48)
GrpBtnClear.place(x=50, y=424, width=48)
GrpBtnVersion.place(x=100, y=424, width=48)
GrpBtnHome.place(x=150, y=424, width=48)
GrpBtnPos1.place(x=200, y=424, width=48)
GrpBtnPos2.place(x=250, y=424, width=48)
GrpBtnPark.place(x=300, y=424, width=48)

grp_ttlvar1 = StringVar()
grp_ttlvar1.set('Gripper Control Version 0.1.1')
grp_title1 = Label(grp_frame, textvariable=grp_ttlvar1, anchor=CENTER, background="#000000", foreground="#FFC000")
grp_title1.grid(row=1, column=1, sticky=E)
grp_input.grid(row=0, column=0, sticky=W)
grp_output.grid(row=0, column=1, sticky=W)

# add to notebook (underline = index for short-cut character)
nb.add(grp_frame, text='Gripper Control', underline=0)
##################################################################################


def myLoop():
    global arm_out
    global arm_in
    global grp_out
    global grp_in
    global LSAM_ON
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = 'GRP>' + current_time + '<\n\r'
#    mySerial.write(msg.encode())
#    grp_in.insert(END, msg)
#    grp_out.insert(END, msg)
    LSAM_ON = True
    master.after(100, myLoop)
    
master.after(100, myLoop)
master.mainloop()