#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64MultiArray

class PolynomialNode:
    def __init__(self):
        rospy.init_node('polynomial')
        
        # Подписываемся на топик с входными числами
        self.input_sub = rospy.Subscriber('input_numbers', Float64MultiArray, self.input_callback)
        
        # Публикуем обработанные числа
        self.output_pub = rospy.Publisher('polynomial_results', Float64MultiArray, queue_size=10)
        
        rospy.loginfo("Polynomial node started")
    
    def input_callback(self, msg):
        # Получаем три числа из сообщения
        numbers = msg.data
        
        if len(numbers) != 3:
            rospy.logwarn("Expected 3 numbers, got %d", len(numbers))
            return
        
        # Применяем полином: x^1, x^2, x^3
        results = []
        for i, num in enumerate(numbers):
            power = i + 1  # 1, 2, 3
            result = num ** power
            results.append(result)
            rospy.loginfo("Number %.2f to power %d = %.2f", num, power, result)
        
        # Публикуем результаты
        output_msg = Float64MultiArray()
        output_msg.data = results
        self.output_pub.publish(output_msg)
        
        rospy.loginfo("Published polynomial results: %s", results)

if __name__ == '__main__':
    try:
        node = PolynomialNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
