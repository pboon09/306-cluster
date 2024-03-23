import rclpy
from rclpy.node import Node

# from joy_stick_lib import JoystickHandler

from std_msgs.msg import Float32MultiArray

import pygame
import sys

class JoystickHandler:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = self._initialize_joystick()

    def _initialize_joystick(self):
        if pygame.joystick.get_count() == 0:
            print("No joysticks found.")
            sys.exit()

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Joystick Name: {joystick.get_name()}")
        print(f"Number of Axes: {joystick.get_numaxes()}")
        print(f"Number of Buttons: {joystick.get_numbuttons()}")
        return joystick

    def get_axes(self):
        axes = [float(self.joystick.get_axis(i)) for i in range(self.joystick.get_numaxes())]
        for i in range(len(axes)):
            if axes[i] > 0.97: axes[i] = 1.00
            elif axes[i] < -0.97: axes[i] = -1.00
            elif axes[i] < 0.08 and axes[i] > -0.08: axes[i] = 0
            if i == 1 or i == 3:
                axes[i] = axes[i] * -1
        return axes

    def get_buttons(self):
        return [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]

    def get_dpad(self):
        return [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]

    def get_all(self):
        pygame.event.pump()  # Process event queue
        axes = self.get_axes()
        buttons_state = self.get_buttons()
        dpad = self.get_dpad()

        output_string = f"Axes: {axes}, Buttons: {buttons_state}, Dpad: {dpad}"
        # print(output_string)
        return output_string
    
    def process_input(self):
        pygame.event.pump()  # Process event queue
        axes = self.get_axes()
        buttons_state = self.get_buttons()
        dpad = self.get_dpad()

        bfunc = 0
        for i in range(len(buttons_state)):
            if int(buttons_state[i]) == 1:
                bfunc = i+1

        process_output = [float(axes[1]),float(axes[0]),float(axes[3]),float(bfunc)]
        # print(process_output)
        return process_output
    
class JoyStickNode(Node):

    def __init__(self):
        super().__init__('JoyStickNode')
        self.publisher_joy_data_ = self.create_publisher(Float32MultiArray, '/joy_data', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.joystick_handler = JoystickHandler()

    def timer_callback(self):

        joy_data = self.joystick_handler.process_input()
        msg = Float32MultiArray()
        msg.data = joy_data;
        self.publisher_joy_data_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    JoyStick_Node = JoyStickNode()

    rclpy.spin(JoyStick_Node)

    JoyStick_Node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

# def main():
#     joystick_handler = JoystickHandler()

#     try:
#         while True:
#             joystick_handler.process_input()
#             pygame.time.wait(100)

#     except KeyboardInterrupt:
#         print("\nExiting...")
#     finally:
#         pygame.quit()

# if __name__ == "__main__":
#     main()
