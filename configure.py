import time
import serial
import RTC_Driver
import keypad
from OmegaExpansion import oledExp
import datetime

k = keypad.KEYPAD()

# Open port with baud rate
ser = serial.Serial(port="/dev/ttyS1", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    timeout=100)


def check_date(year, month, day):
    correctDate = None
    try:
        newDate = datetime.datetime(year, month, day)
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate


class DL_SETTINGS:
    def __init__(self):
        oledExp.setCursor(7, 0)
        oledExp.write("CONFIGURATION MODE")
        oledExp.setCursor(6, 0)
        oledExp.write("*********************")
        oledExp.setCursor(1, 0)
        oledExp.write("1. SET DATE AND TIME ")
        oledExp.setCursor(2, 0)
        oledExp.write("2. To Edit Other Parameters")
        oledExp.setCursor(3,0)
        oledExp.write("3. To Read Configuration")
        oledExp.setCursor(4, 0)
        oledExp.write("Your Selection: ")
        selection = k.getPressKey()
        oledExp.setCursor(5, 0)
        oledExp.write(selection)
        time.sleep(2)
        oledExp.clear()

        if (selection == '1'):
            print("----------------------SET DATE AND TIME----------------------")
            self.set_date_time()
        elif (selection == '2'):
            print("----------------To Edit Other Parameters---------------")
            self.site_details()
        elif (selection == '3'):
            print("---------------To Read Configuration--------------------")
            self.read_confdata()
        else:             
	    oledExp.clear()             
	    oledExp.setCursor(4, 0)             
	    oledExp.write("Invalid Selection")             
            time.sleep(3)             
            oledExp.clear()
	    self.__init__()

    def set_date_time(self):
        # DS3231 Address
        ds3231 = RTC_Driver.SDL_DS3231(0, 0x68)
        # comment out the next line after the clock has been initialized
        # ds3231.write_now()  # through Wifi
        # ds3231.set_datetime()     #through user input
        ds3231.set_datetime_through_keypad()

    def site_details(self):
        oledExp.setCursor(6, 0)
        oledExp.write("CONFIGURATION MODE")
        oledExp.setCursor(7, 0)
        oledExp.write("*********************")
        oledExp.setCursor(3, 0)
        oledExp.write("Connect to PC/Laptop ")
        oledExp.setCursor(4, 0)
        oledExp.write("through USB Cable ")

        siteId = ''
        monitoringId = ''
        analyzerId = ''
        parameterId = ''
        while len(siteId) == 0:
            # Serial input
            ser.write('Enter site ID: ')
            siteId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            siteId += ser.read(data_left)
            ser.write(siteId + '\r\n')
            oledExp.clear()
            oledExp.setCursor(1, 0)
            oledExp.write(siteId)
            time.sleep(1)
        while len(monitoringId) == 0:
            ser.write('Enter monitoring ID: ')
            monitoringId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            monitoringId += ser.read(data_left)
            ser.write(monitoringId + '\r\n')
            oledExp.setCursor(2, 0)
            oledExp.write(monitoringId)
            time.sleep(1)
        while len(analyzerId) == 0:
            ser.write('Enter analyserID: ')
            analyzerId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            analyzerId += ser.read(data_left)
            ser.write(analyzerId + '\r\n')
            oledExp.setCursor(3, 0)
            oledExp.write(analyzerId)
            time.sleep(1)
        while len(parameterId) == 0:
            ser.write('Enter ParameterID: ')
            parameterId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            parameterId += ser.read(data_left)
            ser.write(parameterId + '\r\n')
            oledExp.setCursor(4, 0)
            oledExp.write(parameterId)

        f = open('confdata.txt', 'w')
        f.write(siteId + '\n')
        f.write(monitoringId + '\n')
        f.write(analyzerId + '\n')
        f.write(parameterId + '\n')
        time.sleep(5)
        oledExp.clear()
        oledExp.setCursor(0, 0)
        oledExp.write("CONFIGURATION MODE")
        oledExp.setCursor(1, 0)
        oledExp.write("*********************")
        oledExp.setCursor(2, 0)
        oledExp.write("Configuartion done")
        oledExp.setCursor(4, 3)
        oledExp.write("System is going ")
        oledExp.setCursor(5, 3)
        oledExp.write("through RUN Mode")

        oledExp.setCursor(6, 9)
        oledExp.write("WAIT")
        time.sleep(2)
        oledExp.clear()

    def read_confdata(self):
        f = open('confdata.txt', 'r')
        lines = f.readlines()
        SiteID = lines[0].rstrip('\n')
        MonitoringID = lines[1].rstrip('\n')
        AnalyzerID = lines[2].rstrip('\n')
        ParameterID = lines[3].rstrip('\n')
        oledExp.clear()
        oledExp.setCursor(0, 0)
        oledExp.write(SiteID)
        oledExp.setCursor(1, 0)
        oledExp.write(MonitoringID)
        oledExp.setCursor(2, 0)
        oledExp.write(AnalyzerID)
        oledExp.setCursor(3, 0)
        oledExp.write(ParameterID)
        self.goto_menu()

    def goto_menu(self):
        oledExp.setCursor(5,0)
        oledExp.write("Press '#' to return")
        oledExp.setCursor(6, 0)
        oledExp.write("Main Menu")
        key2=k.getPressKey()
        if key2=='#':
            oledExp.setCursor(7, 0)
            oledExp.write(key2)
            time.sleep(2)
            oledExp.clear()
            self.__init__()


