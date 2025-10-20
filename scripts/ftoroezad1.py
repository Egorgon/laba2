#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

class EvenNumberTalker:
    def __init__(self):
        # Инициализация узла
        rospy.init_node('even_talker', anonymous=True)
        
        # Публикаторы
        self.number_pub = rospy.Publisher('my_topic', Int32, queue_size=10)
        self.overflow_pub = rospy.Publisher('/overflow_topic', Int32, queue_size=10)
        
        # Переменные состояния
        self.counter = 0
        self.rate = rospy.Rate(10)  # 10 Гц
        
        rospy.loginfo("Even Number Talker started")
        rospy.loginfo("Publishing to: my_topic and /overflow_topic")

    def publish_numbers(self):
        while not rospy.is_shutdown():
            # Публикация текущего четного числа в my_topic
            number_msg = Int32()
            number_msg.data = self.counter
            self.number_pub.publish(number_msg)
            
            rospy.loginfo(f"Published to my_topic: {self.counter}")
            
            # Проверка переполнения
            if self.counter >= 100:
                # Публикация сообщения о переполнении в /overflow_topic
                overflow_msg = Int32()
                overflow_msg.data = self.counter
                self.overflow_pub.publish(overflow_msg)
                
                rospy.logwarn(f"OVERFLOW! Published to /overflow_topic: {self.counter}")
                self.counter = 0  # Сброс счетчика
            else:
                self.counter += 2  # Следующее четное число
            
            self.rate.sleep()

if __name__ == '__main__':
    try:
        talker = EvenNumberTalker()
        talker.publish_numbers()
    except rospy.ROSInterruptException:
        rospy.loginfo("Talker shutdown")
