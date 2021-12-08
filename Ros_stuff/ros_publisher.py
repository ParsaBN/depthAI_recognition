# !/usr/bin/env python
# have to make this an executable 


# add to ur cmakelists.txt
# catkin_install_python(PROGRAMS scripts/talker.py scripts/listener.py
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )


import rospy
import std_msgs as msg

def talker(coords):
    pub = rospy.Publisher('bbox', msg.Int32MultiArray, queue_size = 20)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # this should be less than queue for multiple things in a msg ideally
    while not rospy.is_shutdown():
        coords_arr = coords
        rospy.loginfor(coords_arr)
        pub.publish(coords_arr)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass