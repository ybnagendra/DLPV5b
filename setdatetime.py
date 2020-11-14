import keypad
from OmegaExpansion import oledExp
import datetime,time

k = keypad.KEYPAD()

def check_date(year, month, day):
    correctDate = None
    try:
        newDate = datetime.datetime(year, month, day)
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate

class SET_DATE_AND_TIME:
    def setDate(self):
        while True:
            print("Set date in the format hr*min*sec: ")
            oledExp.clear()
            oledExp.setCursor(1, 0)
            oledExp.write("Enter date in the")
            oledExp.setCursor(2, 0)
            oledExp.write("format dd*mm*yy")
            date_string = ''

            while (True):
                key = k.getPressKey()
                if (key == 'C'):
                    date_string = date_string[:-1]
                    print(date_string)
                    oledExp.clear()
                    oledExp.setCursor(1, 0)
                    oledExp.write("Enter date in the")
                    oledExp.setCursor(2, 0)
                    oledExp.write("format dd*mm*yy")
                    oledExp.setCursor(3, 0)
                    oledExp.write(date_string)

                elif (key == '#'):
                    oledExp.clear()
                    break

                else:
                    date_string = date_string + key
                    print(date_string)
                    oledExp.setCursor(1, 0)
                    oledExp.write("Enter date in the")
                    oledExp.setCursor(2, 0)
                    oledExp.write("format dd*mm*yy")
                    oledExp.setCursor(3, 0)
                    oledExp.write(date_string)

                time.sleep(0.05)

            try:
                self._dd = int(date_string[0:2])
                self._mm = int(date_string[3:5])
                self._yy = int(date_string[6:8]) + 2000
                isvalid_date_string = check_date(self._yy, self._mm, self._dd)
                lfd = len(date_string)

                if isvalid_date_string == True and date_string[2] == '*' and date_string[5] == '*' and lfd == 8:
                    break
                elif isvalid_date_string == True and date_string[2] == '*' and date_string[5] == '*' and lfd != 8:
                    oledExp.write("Format should be dd*mm*yy")
                    time.sleep(2)
                    oledExp.clear()
                    print("Format should be dd*mm*yy")
                elif isvalid_date_string == True and (date_string[2] != '*' or date_string[5] != '*'):
                    oledExp.write("Format should be dd*mm*yy")
                    time.sleep(2)
                    oledExp.clear()
                elif isvalid_date_string == False and (date_string[2] == '*' and date_string[5] == '*' and lfd == 8):
                    oledExp.write("Invalid Date. ")
                    time.sleep(2)
                    oledExp.clear()

            except:
                oledExp.write("Format should be dd*mm*yy")
                time.sleep(2)
                oledExp.clear()
        self.dateString = str(self._dd) + "-" + str(self._mm) + "-" + str(self._yy)

    def setTime(self):
        while True:
            print("Set time in the format hr*min*sec: ")
            oledExp.clear()
            oledExp.setCursor(1, 0)
            oledExp.write("Enter time in the")
            oledExp.setCursor(2, 0)
            oledExp.write("format hr*min*sec")
            time_string = ''

            while True:
                key = k.getPressKey()
                if (key == 'C'):
                    time_string = time_string[:-1]
                    print(time_string)
                    oledExp.clear()
                    oledExp.setCursor(1, 0)
                    oledExp.write("Enter time in the")
                    oledExp.setCursor(2, 0)
                    oledExp.write("format hr*min*sec")
                    oledExp.setCursor(3, 0)
                    oledExp.write(time_string)
                elif (key == '#'):
                    oledExp.clear()
                    break

                else:
                    time_string = time_string + key
                    print(time_string)
                    oledExp.setCursor(1, 0)
                    oledExp.write("Enter time in the")
                    oledExp.setCursor(2, 0)
                    oledExp.write("format hr*min*sec")
                    oledExp.setCursor(3, 0)
                    oledExp.write(time_string)

                time.sleep(0.05)

            try:
                self.hr = int(time_string[0:2])
                self.min = int(time_string[3:5])
                self.sec = int(time_string[6:8])

                if 0 <= self.hr <= 24 and 0 <= self.min <= 59 and 0 <= self.sec <= 59:
                    self.isvalid_ts = True
                else:
                    self.isvalid_ts = False

                isvalid_time_string = self.isvalid_ts
                len_of_time = len(time_string)

                if isvalid_time_string == True and time_string[2] == '*' and time_string[5] == '*' and len_of_time == 8:
                    break
                elif isvalid_time_string == True and time_string[2] == '*' and time_string[
                    5] == '*' and len_of_time != 8:
                    oledExp.write("Format should be hr*min*sec Ex- 13*01*02")
                    time.sleep(2)
                    oledExp.clear()
                    print("Format should be hr*min*sec")
                elif isvalid_time_string == True and (time_string[2] != '*' or time_string[5] != '*'):
                    oledExp.write("Format should be hr*min*sec Ex- 13*01*02")
                    time.sleep(2)
                    oledExp.clear()
                elif isvalid_time_string == False and (
                        time_string[2] == '*' and time_string[5] == '*' and len_of_time == 8):
                    oledExp.write("Invalid Time. ")
                    time.sleep(2)
                    oledExp.clear()

            except:
                oledExp.write("Format should be hr*min*sec Ex- 13*01*02")
                time.sleep(2)
                oledExp.clear()
        self.timeString = str(self.hr) + ":" + str(self.min) + ":" + str(self.sec)

