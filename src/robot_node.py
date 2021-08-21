#!/usr/bin/env python
import time
from exomy.msg import RoverCommand, MotorCommands, Screen, ShovelCommands, ShovelMotorCommands
import rospy
from rover import Rover
import message_filters


global exomy
exomy = Rover()


def joy_callback(message):
    cmds = MotorCommands()

    if message.motors_enabled is True:
        exomy.setLocomotionMode(message.locomotion_mode)

        cmds.motor_angles = exomy.joystickToSteeringAngle(
            message.vel, message.steering)
        cmds.motor_speeds = exomy.joystickToVelocity(
            message.vel, message.steering)
    else:
        cmds.motor_angles = exomy.joystickToSteeringAngle(0, 0)
        cmds.motor_speeds = exomy.joystickToVelocity(0, 0)

    robot_pub.publish(cmds)


def joy_2_callback(message):
    print("got commands for shovel 2")
    print(str(message))

    cmds = ShovelMotorCommands()

    cmds.shovel_angles = exomy.joystickToShovelAngle(message.shovel_angle)

    shovel_pub.publish(cmds)


if __name__ == '__main__':
    rospy.init_node('robot_node')
    rospy.loginfo("Starting the robot node")
    global robot_pub
    joy_sub = rospy.Subscriber(
        "/rover_command", RoverCommand, joy_callback, queue_size=1)
    joy2_sub = rospy.Subscriber(
        "/shovel_command", ShovelCommands, joy_2_callback, queue_size=1)

    rate = rospy.Rate(10)

    robot_pub = rospy.Publisher("/motor_commands", MotorCommands, queue_size=1)
    shovel_pub = rospy.Publisher(
        "/shovel_motor_commands", ShovelMotorCommands, queue_size=1)

    rospy.spin()
