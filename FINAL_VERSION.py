from pyparrot.Bebop import Bebop
from pyparrot.DroneVisionGUI import DroneVisionGUI
import threading
import cv2
import time
from PyQt5.QtGui import QImage
from pynput import keyboard
from moods import main

isAlive = False

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        #print("saving picture")
        img = self.vision.get_latest_valid_picture()

        # limiting the pictures to the first 10 just to limit the demo from writing out a ton of files
        if (img is not None and self.index <= 10):
            filename = "test_image_%06d.png" % self.index
            cv2.imwrite(filename, img)
            self.index +=1

def is_int(to_check):
    try:
        int(to_check)
        return True
    except ValueError:
        return False

# LIVE KEYBOARD INPUT FUNCTION
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def draw_current_photo():
    """
    Quick demo of returning an image to show in the user window. Clearly one would want to make this a dynamic image
    """
    image = cv2.imread('test_image_000001.png')
    if (image is not None):
        if len(image.shape) < 3 or image.shape[2] == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, byteValue = image.shape
            byteValue = byteValue * width

            qimage = QImage(image, width, height, byteValue, QImage.Format_RGB888)

            return qimage
    else:
        return None

def demo_user_code_after_vision_opened(bebopVision, args):
    bebop = args[0]

    print("Vision successfully started!")

    if (bebopVision.vision_running):

        # takeoff
        print("Taking Off...")
        bebop.smart_sleep(1)
        bebop.safe_takeoff(10)

        print("Adjusting Height...")
        bebop.fly_direct(roll = 0, pitch = 0, yaw = 0, vertical_movement = 20, duration = 3)

        print("D R O N E   R E A D Y")
        print("")
        input("Press any key to start taking pictures >")

        for i in range(10):
            time.sleep(1)
            cv2.imwrite(f"images/outfile{i}.jpg", bebopVision.get_latest_valid_picture())
            print(f"Saved Image {i}")

        print("Landing...")
        bebop.smart_sleep(1)
        bebop.safe_land(10)

        main()

        # counter = 0
        #
        # def on_press(key):
        #     global counter
        #     key = str(key).replace("'", "").lower()
        #
        #     if key == "q":
        #         keyboard.Listener.stop()
        #     elif key == "l":
        #         bebop.safe_land(10)
        #     elif key == "p":
        #         cv2.imwrite(f"images\outfile{counter}.jpg", bebopVision.get_latest_valid_picture())
        #         print(f"Saved Image {counter}")
        #         counter += 1
        #         if counter >= 10:
        #             counter = 0
        #
        # with keyboard.Listener(on_press=on_press) as listener:
            # listener.join()

        # for i in range(10):
        #     time.sleep(1)

            # option = input("-> ").lower()
            #
            # if option == "l":
            #     bebop.safe_land(10)
            # elif is_int(option):
            #     bebop.fly_direct(roll = 0, pitch = 0, yaw = int(option), vertical_movement = 0, duration = 3)
            # elif option == "h":
            #     bebop.fly_direct(roll = 0, pitch = 0, yaw = 0, vertical_movement = 5, duration = 3)
            # else:
            #     cv2.imwrite(f"images\outfile{i}.jpg", bebopVision.get_latest_valid_picture())
            #     print(f"Saved Image {i}")

        # land
        # print("Landing...")
        # bebop.smart_sleep(1)
        # bebop.safe_land(10)

        # print("Finishing demo and stopping vision")
        # bebopVision.close_video()

    # disconnect nicely so we don't need a reboot
    # print("disconnecting")
    # bebop.disconnect()

# make my bebop object
bebop = Bebop()

# connect to the bebop
success = bebop.connect(5)

if (success):
    # start up the video
    bebopVision = DroneVisionGUI(bebop, is_bebop=True, user_code_to_run=demo_user_code_after_vision_opened, user_args=(bebop, ), user_draw_window_fn=draw_current_photo)

    userVision = UserVision(bebopVision)
    bebopVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
    bebopVision.open_video()

else:
    print("Error connecting to bebop. Retry")
