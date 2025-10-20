#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

class OverflowListener:
    def __init__(self):
        # Инициализация узла
        rospy.init_node('overflow_listener', anonymous=True)
        
        # Подписка на топик переполнения
        rospy.Subscriber('/overflow_topic', Int32, self.overflow_callback)
        
        rospy.loginfo("Overflow Listener started - listening to /overflow_topic")

    def overflow_callback(self, msg):
        # Обработка сообщения о переполнении
        rospy.logwarn(f"🚨 OVERFLOW DETECTED! Counter reached: {msg.data}")
        rospy.loginfo("🔄 Counter has been reset to 0")
        
        # Можно добавить дополнительные действия:
        # - Запись в файл
        # - Отправка уведомления
        # - Визуальное оповещение
        self.log_overflow_event(msg.data)

    def log_overflow_event(self, number):
        """Дополнительная функция для логирования событий переполнения"""
        timestamp = rospy.Time.now().to_sec()
        rospy.loginfo(f"📝 Overflow event logged: number={number}, time={timestamp}")

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        listener = OverflowListener()
        listener.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Overflow listener shutdown")
