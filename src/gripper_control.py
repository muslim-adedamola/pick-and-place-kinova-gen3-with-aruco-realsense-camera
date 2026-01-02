#adapted and modified from
#https://github.com/Kinovarobotics/Kinova-kortex2_Gen3_G3L/blob/master/api_python/examples/106-Gripper_command/01-gripper_command.py

from kortex_api.autogen.messages import Base_pb2

def close_gripper(base, position=1.0):
    cmd = Base_pb2.GripperCommand()
    cmd.mode = Base_pb2.GRIPPER_POSITION

    finger = cmd.gripper.finger.add()
    finger.finger_identifier = 1
    finger.value = position  # 1.0 = closed, 0.0 = open

    base.SendGripperCommand(cmd)

def open_gripper(base):
    close_gripper(base, position=0.0)
