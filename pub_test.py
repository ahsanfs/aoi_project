import rospy
from std_msgs.msg import String

def command():
    pub = rospy.Publisher('/sub/aoi/spain/status', String, queue_size=10)
    rospy.init_node('spain_side', anonymous=True)
    rate = rospy.Rate(10)
    # while not rospy.is_shutdown():
    com = "110000000001"
    rospy.loginfo(com)
    pub.publish(com)
    rate.sleep()

if __name__ == '__main__':
    try:
        command()
    except rospy.ROSInterruptException:
        pass
