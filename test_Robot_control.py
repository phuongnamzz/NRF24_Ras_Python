from time import sleep
from Robot_control import RobotControl
from Robot_control import RFComm
from sshkeyboard import listen_keyboard



rf24 = RFComm()
robot = RobotControl(rf24)
def press(key):
    print(f"'{key}' pressed")
    if key == 'up' or key == 'w':
        robot.move(100)
    if key == 'down' or key == 'x':
        robot.move(-100)
    if key == 'left' or key == 'a':
        robot.rotate(-100)
    if key == 'right' or key == 'd':
        robot.rotate(100)
    



def release(key):
    print(f"'{key}' released")




while True:
    # robot.move(100)
    # robot.rotate(50)
    # robot.toggle_weapon(1)
    # sleep(1)
    # robot.move(100, 50)
    # robot.rotate(30)
    # robot.toggle_weapon(0)
    # sleep(1)
    listen_keyboard(
    on_press=press,
    on_release=release,
)
