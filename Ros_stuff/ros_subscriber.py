#!/usr/bin/env python
import rospy
import std_msg as msg

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + f"I heard {data.data}")
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("person_det", msg.Int32MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()


# edit catking_install_python() call in cmakelists.txt to look below
# catkin_install_python(PROGRAMS scripts/talker.py scripts/listener.py
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )