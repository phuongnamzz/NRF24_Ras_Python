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
    

    if key == '1':
        robot.start()
    if key == '2':
        robot.stop()
    if key == '3':
        robot.weapon1(20)
    if key == '4':
        robot.weapon2(100)
    if key == '5':
        robot.weapon3(-10)
    if key == '6':
        robot.weapon4(30)
    if key == '7':
        robot.weapon5(40)
    if key == '8':
        robot.weapon6(-100)
    if key == '9':
        robot.weapon7(-10)
    if key == '0':
        robot.weapon8(-30)
    if key == 'p':
        robot.weapon9(-50)
    if key == 'o':
        robot.weapon10(50)
    if key == 't':
        robot.weapon10(200)

    



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
