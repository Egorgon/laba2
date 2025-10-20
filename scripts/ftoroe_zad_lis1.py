#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

class NumberListener:
    def __init__(self):
        # Инициализация узла
        rospy.init_node('number_listener', anonymous=True)
        
        # Подписка на топик с четными числами
        rospy.Subscriber('my_topic', Int32, self.number_callback)
        
        # Счетчик полученных сообщений
        self.message_count = 0
        self.last_time = rospy.Time.now()
        
        rospy.loginfo("Number Listener started - listening to my_topic")

    def number_callback(self, msg):
        # Обработка полученного четного числа
        self.message_count += 1
        current_time = rospy.Time.now()
        
        # Вывод информации о полученном числе
        rospy.loginfo(f"📊 Received even number: {msg.data}")
        
        # Проверка частоты получения сообщений каждые 5 секунд
        elapsed_time = (current_time - self.last_time).to_sec()
        if elapsed_time >= 5.0:
            actual_rate = self.message_count / elapsed_time
            rospy.loginfo(f"📈 Receiving rate: {actual_rate:.2f} Hz")
            self.last_time = current_time
            self.message_count = 0

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        listener = NumberListener()
        listener.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Listener shutdown")
