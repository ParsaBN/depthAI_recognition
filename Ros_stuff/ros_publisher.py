#!/usr/bin/env python
# have to make this an executable 




# import rospy
# from std_msgs.msg import String

# def talker():
#     pub = rospy.Publisher('person_det', String, queue_size=10)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     while not rospy.is_shutdown():
#         hello_str = "hello world %s" % rospy.get_time()
#         rospy.loginfo(hello_str)
#         pub.publish(hello_str)
#         rate.sleep()

# if __name__ == '__main__':
#     try:
#         talker()
#     except rospy.ROSInterruptException:
#         pass


# add to ur cmakelists.txt
# catkin_install_python(PROGRAMS scripts/talker.py scripts/listener.py
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )


import rospy
import std_msgs as msg

def talker(box):
    pub = rospy.Publisher('bbox', msg.Int32MultiArray, queue_size = 20)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        bbox_arr = box
        rospy.loginfor(bbox_arr)
        pub.publish(bbox_arr)
        rate.sleep()