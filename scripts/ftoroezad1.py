#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

class EvenNumberPublisher:
    def __init__(self):
        # Инициализация узла
        rospy.init_node('even_number_publisher', anonymous=True)
        
        # Публикаторы
        self.even_pub = rospy.Publisher('even_numbers', Int32, queue_size=10)
        self.overflow_pub = rospy.Publisher('number_overflow', Int32, queue_size=10)
        
        # Переменные состояния
        self.counter = 0
        self.rate = rospy.Rate(10)  # 10 Гц
        self.last_time = rospy.Time.now()
        self.message_count = 0
        
        rospy.loginfo("Even number publisher started")
        rospy.loginfo("Publishing even numbers: 0, 2, 4, 6, ... with 10 Hz frequency")

    def publish_even_numbers(self):
        """Основная функция публикации четных чисел"""
        while not rospy.is_shutdown():
            # Создание и публикация сообщения с четным числом
            even_msg = Int32()
            even_msg.data = self.counter
            self.even_pub.publish(even_msg)
            
            # Логирование публикации
            rospy.loginfo(f"Published even number: {self.counter}")
            
            # Проверка частоты публикации
            self.message_count += 1
            current_time = rospy.Time.now()
            elapsed_time = (current_time - self.last_time).to_sec()
            
            # Проверка частоты каждые 2 секунды
            if elapsed_time >= 2.0:
                actual_rate = self.message_count / elapsed_time
                self.last_time = current_time
                self.message_count = 0
            
            # Проверка достижения 100 и сброс счетчика
            self.check_overflow()
            
            # Увеличение счетчика для следующего четного числа
            self.counter += 2
            
            # Ожидание для поддержания частоты 10 Гц
            self.rate.sleep()

    def check_overflow(self):
        """Проверка достижения числа 100 и отправка сообщения о переполнении"""
        if self.counter >= 100:
            # Создание сообщения о переполнении
            overflow_msg = Int32()
            overflow_msg.data = self.counter
            self.overflow_pub.publish(overflow_msg)

            rospy.loginfo("Reset counter to 0 and sent overflow notification")
            
            # Сброс счетчика
            self.counter = 0

    def run(self):
        """Запуск публикации"""
        try:
            self.publish_even_numbers()
        except rospy.ROSInterruptException:
            rospy.loginfo("Publisher shutdown requested")

if __name__ == '__main__':
    publisher = EvenNumberPublisher()
    publisher.run()
