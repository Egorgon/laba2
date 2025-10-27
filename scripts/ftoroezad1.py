#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


def talker():
    pub = rospy.Publisher('there_is_topic_name', String, queue_size=10)
    overflow_pub = rospy.Publisher('there_is_another_topic_name', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    msg = String()
    counter = 0

    while not rospy.is_shutdown():
        rospy.loginfo(counter)
        if counter == 100:
            msg.data = str("Value is 100! Here we go again")
            overflow_pub.publish(msg)
            pub.publish(str(counter))
            counter = 0
        else:
            msg.data = (str(counter))
            pub.publish(msg)
            counter += 2
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
