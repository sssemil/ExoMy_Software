#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from exomy.msg import ShovelCommand
import math


def callback(data):

    global motors_enabled

    rover_cmd = ShovelCommand()

    # Reading out joystick data
    y = data.axes[1]

    rover_cmd.shovel_angle = y

    pub.publish(rover_cmd)


if __name__ == '__main__':
    global pub

    rospy.init_node('joystick_2_parser_node')
    rospy.loginfo('joystick_2_parser_node started')

    sub = rospy.Subscriber("/joy2", Joy, callback, queue_size=1)
    pub = rospy.Publisher('/shovel_command', ShovelCommand, queue_size=1)

    rospy.spin()
