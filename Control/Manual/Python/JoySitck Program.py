import pygame
import time
import sys

class JoystickHandler:
    def __init__(self):
        pygame.joystick.init()
        self.joystick = None
        self._initialize_joystick()

    def _initialize_joystick(self):
        if pygame.joystick.get_count() == 0:
            print("No joysticks found.")
            quit()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"Joystick Name: {self.joystick.get_name()}")
        print(f"Number of Axes: {self.joystick.get_numaxes()}")
        print(f"Number of Buttons: {self.joystick.get_numbuttons()}")

    def get_axes(self):
        axes = [float(self.joystick.get_axis(i) * 1) for i in range(self.joystick.get_numaxes())]
        for i in range(len(axes)):
            if axes[i] > 0.97: axes[i] = 1.00
            elif axes[i] < -0.97: axes[i] = -1.00
            elif axes[i] < 0.03 and axes[i] > -0.03: axes[i] = 0
            if i == 1 or i == 3:
                axes[i] = axes[i] * -1
        return axes

    def get_buttons(self):
        return [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]

    def get_dpad(self):
        return [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]

def main():
    pygame.init()

    joystick_handler = JoystickHandler()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            axes = joystick_handler.get_axes()
            buttons_state = joystick_handler.get_buttons()
            dpad = joystick_handler.get_dpad()

            bfunc = 0

            for i in range(len(buttons_state)):
                if int(buttons_state[i]) == 1:
                    bfunc = i+1

            output_string = f"Axes: {axes}, Buttons: {buttons_state}, Dpad: {dpad}                                  "
            # print(output_string, end='\r', flush=True)
            print(str(axes[0])+":"+str(axes[1])+":"+str(axes[2])+":"+str(bfunc), end='\r', flush=True)
            sys.stdout.write("\033[K")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
