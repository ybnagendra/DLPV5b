import shutil
from datetime import date, timedelta
import datetime, time, pytz
import keypad
import os.path
from OmegaExpansion import oledExp
import RTC_Driver

delay = 1

k = keypad.KEYPAD()


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def check_date(year, month, day):
    correctDate = None
    try:
        newDate = datetime.datetime(year, month, day)
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate


def oledBkpDisplay1():
    oledExp.clear()
    oledExp.setCursor(0, 0)
    oledExp.write("Enter FROM and TO")
    oledExp.setCursor(1, 0)
    oledExp.write("dates in the format:")
    oledExp.setCursor(2, 0)
    oledExp.write("dd*mm*yy ")
    oledExp.setCursor(3, 0)
    oledExp.write("Ex: 23/01/20")
    time.sleep(2)


class MAKE_DIRECTORY:
    def __init__(self, pth, directory):
        self.parent_dir = pth
        self.directory = directory
        dst_dir_path = os.path.join(self.parent_dir, self.directory)
        os.mkdir(dst_dir_path)


class GET_DATE_TIME:
    def __init__(self):
        now_utc = datetime.datetime.utcnow()
        local_tz = pytz.timezone('Asia/Kolkata')
        now_utc = pytz.utc.localize(now_utc)
        x = now_utc.astimezone(local_tz)
        self.bkpdt = x.strftime("%d%m%y_%H%M%S")

class RTC_BKP_TIME:     
    def __init__(self):                  
	ds3231 = RTC_Driver.SDL_DS3231(0, 0x68)                  
	DS3231 = ds3231.read_datetime()         
	ds = str(DS3231)              
	self.bkpdt= ds[8:10] + ds[5:7] + ds[2:4]  +"_"+ds[11:13] + ds[14:16] + ds[17:] 


class ENTER_FROM_AND_TO_DATES:
    def enterfromdate(self):
        while True:
            print("Enter 'FROM DATE' to copy files in the format dd*mm*yy: ")
            oledExp.clear()
            oledExp.setCursor(1, 0)
            oledExp.write("FROM DATE: ")
            fromDate = ''

            while (True):
                key = k.getPressKey()
                if (key == 'C'):
                    fromDate = fromDate[:-1]
                    print(fromDate)
                    oledExp.clear()
                    oledExp.setCursor(1, 0)
                    oledExp.write("FROM DATE: ")
                    oledExp.setCursor(2, 0)
                    oledExp.write(fromDate)
                elif (key == '#'):
                    oledExp.clear()
                    break

                else:
                    fromDate = fromDate + key
                    print(fromDate)
                    oledExp.setCursor(1, 0)
                    oledExp.write("FROM DATE: ")
                    oledExp.setCursor(2, 0)
                    oledExp.write(fromDate)

                time.sleep(0.05)

            try:
                self.fr_dd = int(fromDate[0:2])
                self.fr_mm = int(fromDate[3:5])
                self.fr_yy = int(fromDate[6:8]) + 2000
                isvalid_fromdate = check_date(self.fr_yy, self.fr_mm, self.fr_dd)
                lfd = len(fromDate)

                if isvalid_fromdate == True and fromDate[2] == '*' and fromDate[5] == '*' and lfd == 8:
                    break
                elif isvalid_fromdate == True and fromDate[2] == '*' and fromDate[5] == '*' and lfd != 8:
                    oledExp.write("Format should be dd*mm*yy")
                    time.sleep(2)
                    oledExp.clear()
                    print("Format should be dd*mm*yy")
                elif isvalid_fromdate == True and (fromDate[2] != '*' or fromDate[5] != '*'):
                    oledExp.write("Format should be dd*mm*yy")
                    time.sleep(2)
                    oledExp.clear()
                elif isvalid_fromdate == False and (fromDate[2] == '*' and fromDate[5] == '*' and lfd == 8):
                    oledExp.write("Invalid Date. ")
                    time.sleep(2)
                    oledExp.clear()

            except:
                oledExp.write("Format should be dd*mm*yy")
                time.sleep(2)
                oledExp.clear()
        self.fd = datetime.datetime(self.fr_yy, self.fr_mm, self.fr_dd)

    def entertodate(self):
        while True:
            print("Enter 'TO DATE' to copy files in the format dd*mm*yy: ")
            oledExp.clear()
            oledExp.setCursor(1, 0)
            oledExp.write("TO DATE: ")
            toDate = ''
            while (True):
                key = k.getPressKey()
                if (key == 'C'):
                    toDate = toDate[:-1]
                    print(toDate)
                    oledExp.clear()
                    oledExp.setCursor(1, 0)
                    oledExp.write("TO DATE: ")
                    oledExp.setCursor(2, 0)
                    oledExp.write(toDate)
                elif (key == '#'):
                    oledExp.clear()
                    break
                else:
                    toDate = toDate + key
                    print(toDate)
                    oledExp.setCursor(1, 0)
                    oledExp.write("TO DATE: ")
                    oledExp.setCursor(2, 0)
                    oledExp.write(toDate)
                time.sleep(0.05)

            try:
                self.to_dd = int(toDate[0:2])
                self.to_mm = int(toDate[3:5])
                self.to_yy = int(toDate[6:8]) + 2000
                isvalid_todate = check_date(self.to_yy, self.to_mm, self.to_dd)
                tfd = len(toDate)
                if isvalid_todate == True and toDate[2] == '*' and toDate[5] == '*' and tfd == 8:
                    break
                elif isvalid_todate == True and toDate[2] == '*' and toDate[5] == '*' and tfd != 8:
                    oledExp.write("Format should be dd*mm*yy")
                    time.sleep(2)
                    oledExp.clear()
                    print("Format should be dd*mm*yy")
                elif isvalid_todate == True and (toDate[2] != '*' or toDate[5] != '*'):
                    oledExp.write("Format should be dd*mm*yy")
                    time.sleep(2)
                    oledExp.clear()
                    print("Format should be dd*mm*yy")
                elif isvalid_todate == False and (toDate[2] == '*' and toDate[5] == '*' and tfd == 8):
                    oledExp.write("Invalid Date")
                    time.sleep(2)
                    oledExp.clear()

            except:
                oledExp.write("Format should be dd*mm*yy")
                time.sleep(2)
                oledExp.clear()
        self.td = datetime.datetime(self.to_yy, self.to_mm, self.to_dd)

    def isdatesAcceptable(self):
        if self.td < self.fd:
            print("TO DATE should be greater than FROM DATE ")
            oledExp.write("TO DATE should be greater than FROM DATE")
            oledExp.setCursor(3, 0)
            oledExp.write("TRY AGAIN")
            time.sleep(2)
            oledExp.clear()
            return False
        else:
            return True


class EMMC_TO_USB_COPY:
    def __init__(self):
        e = ENTER_FROM_AND_TO_DATES()
        r=RTC_BKP_TIME()
        if True:
            checking_of_dates = 0
            while (checking_of_dates == 0):
                e.enterfromdate()
                e.entertodate()
                checking_of_dates = e.isdatesAcceptable()
		  
		if checking_of_dates==1:
                	sdate = date(e.fr_yy, e.fr_mm, e.fr_dd)  # start date
                	edate = date(e.to_yy, e.to_mm, e.to_dd)  # end date

	                delta = edate - sdate  # as timedelta
        	        pth1 = '/mnt/mtdblock6/BKP_DLPV3b/SrcDir1/'
                	usb_pth = '/mnt/sda1'
                	bkp_dir = 'BKP_' + r.bkpdt
                	MAKE_DIRECTORY(usb_pth, bkp_dir)
                	bkp_dir_pth = usb_pth + "/" + bkp_dir

                	for i in range(delta.days + 1):
        	            	day = str(sdate + timedelta(days=i))
	                    	cdir_path = pth1 + "CDIR_" + day[8:10] + day[5:7] + day[2:4]
                	    	isdir = os.path.isdir(cdir_path)

                    		if (isdir):
                        		copytree(cdir_path, bkp_dir_pth)
                    		else:
                        		pass

######################################################################################################




