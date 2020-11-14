import time
from OmegaExpansion import oledExp
import configure,keypad
import dlmode

k = keypad.KEYPAD()

def welcomeMessage():
    oledExp.setVerbosity(0)
    oledExp.driverInit()
    oledExp.clear()
    oledExp.setCursor(3, 0)
    oledExp.write("Welcome to OnionOmega")
    oledExp.setCursor(4, 0)
    oledExp.write("Data Logger Project")
    time.sleep(5)


def displayModes():
    oledExp.clear()
    oledExp.setCursor(2, 0)
    oledExp.write("Select mode(1,2,3):")
    oledExp.setCursor(3, 0)
    oledExp.write("1. CONFIGURE MODE")
    oledExp.setCursor(4, 0)
    oledExp.write("2. RUN MODE")
    oledExp.setCursor(5, 0)
    oledExp.write("3. BACKUP MODE")
    oledExp.setCursor(6, 0)
    oledExp.write("Mode of Operation:")


if __name__ == "__main__":
    try:
        welcomeMessage()
    except:
        pass
    while True:
        try:
            displayModes()
        except:
            pass
        # Wait for user keypad input
        # key = k.getPressKey()
	    key='3'
        try:
            oledExp.setCursor(7, 0)
            oledExp.write(key)
            time.sleep(2)
            oledExp.clear()
        except:
            pass

        if (key == '1'):
            print("----------------------CONF MODE----------------------")
            configure.DL_SETTINGS()
            dlmode.RUN_MODE()
        elif (key == '2'):
            print("----------------------RUN MODE----------------------")
            dlmode.DIRECT_RUN_MODE()
        elif (key == '3'):
            print("----------------------BKP MODE----------------------")
            dlmode.DIRECT_BACKUP_MODE()
            dlmode.RUN_MODE()
        else:
            try:
                oledExp.write("Invalid Selection")
                oledExp.write("Select 1 or 2 or 3")
                time.sleep(2)
            except:
                pass