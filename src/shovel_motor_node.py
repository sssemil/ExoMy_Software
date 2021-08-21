#!/usr/bin/env python
import time
import rospy

from exomy.msg import ShovelCommands
from motors import Motors

motors = Motors()
global watchdog_timer


def callback(cmds):
    motors.setShovel(cmds.motor_shovel)

    global watchdog_timer
    watchdog_timer.shutdown()
    # If this timer runs longer than the duration specified,
    # then watchdog() is called stopping the driving motors.
    watchdog_timer = rospy.Timer(rospy.Duration(5.0), watchdog, oneshot=True)


def shutdown():
    motors.stopMotors()


def watchdog(event):
    rospy.loginfo("Watchdog fired. NOT Stopping shovel motors.")
    pass


if __name__ == "__main__":
    # This node waits for commands from the robot and sets the motors accordingly
    rospy.init_node("motors")
    rospy.loginfo("Starting the motors node")
    rospy.on_shutdown(shutdown)

    global watchdog_timer
    watchdog_timer = rospy.Timer(rospy.Duration(1.0), watchdog, oneshot=True)

    sub = rospy.Subscriber(
        "/shovel_motor_commands", ShovelCommands, callback, queue_size=1)

    rate = rospy.Rate(10)

    rospy.spin()
