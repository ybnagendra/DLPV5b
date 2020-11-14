import os.path
import datetime, time, pytz
import analyserSensor
import emmctousb
import zipfile
import keypad
import serial
import RTC_Driver
from OmegaExpansion import oledExp

ser = serial.Serial(port="/dev/ttyS1", baudrate=115200, timeout=100)

a = analyserSensor.ANALYSER_SENSOR()
k = keypad.KEYPAD()

delay = 1
usb_dir_path = '/mnt/sda1'
pth1 = '/mnt/mmcblk0p1/DLPV5b/SrcDir'

def oledBkpDisp1():
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

def copyfiles_to_usb():
    isUSB = os.path.isdir(usb_dir_path)
    time.sleep(3)
    oledBkpDisp1()
    emmctousb.EMMC_TO_USB_COPY()
    oledExp.clear()
    print("Copy Done")
    oledExp.setCursor(1, 0)
    oledExp.write("Copy Done")
    oledExp.setCursor(2, 0)
    oledExp.write("Remove Pendrive")
    oledExp.setCursor(3, 0)
    oledExp.write("to enter Run Mode")
    oledExp.setCursor(6, 0)
    oledExp.write("*********************")
    oledExp.setCursor(7, 8)
    oledExp.write("BKP MODE")
    print("Remove Pendrive")
    count3=0
    while (isUSB):
        isUSB = os.path.isdir(usb_dir_path)
        time.sleep(1)
        count3=count3+1
        if count3==60:
            RUN_MODE()
        else:
            pass
    else:
        oledExp.clear()
        print("Enters Run mode after Files Copied")


class MAKE_DIRECTORY:
    def __init__(self, pth, directory):
        self.parent_dir = pth
        self.directory = directory
        dst_dir_path = os.path.join(self.parent_dir, self.directory)
        os.mkdir(dst_dir_path)


class WRITE_DATA_IN_FILE:
    def __init__(self, pth, fileName, response):
        completeName = os.path.join(pth, fileName + ".txt")
        self.fileName = completeName
        self.response = response
        f = open(self.fileName, "w")
        f.write(self.response + '\n')
        f.close()

class RTC_DATE_TIME:     
    def __init__(self):         
	ds3231 = RTC_Driver.SDL_DS3231(0, 0x68)         
	DS3231 = ds3231.read_datetime()         	
	ds = str(DS3231)     
	self.seconds=ds[17:]
	self.minutes=ds[14:16]
	self.hours=ds[11:13]    
	self.dir_format=ds[8:10] + ds[5:7]  + ds[2:4]         
	self.rtc_date = ds[8:10] + "/" + ds[5:7] + "/" + ds[2:4]         
	self.rtc_time = ds[11:13] + ":" + ds[14:16] + ":" + ds[17:]         
	self.rtc_dateTime = "Dt: " + self.rtc_date + " " + self.rtc_time


class RUN_MODE:
    def __init__(self):
        print("Enters Run mode")
        res_add = ''
        bkp_data = ''

        voltage = ''
        current = ''
        power = ''
        resistance = ''
        capacitance = ''
        conductance = ''
        inductance = ''
        impedance = ''
        frequency = ''

        realPower = ''
        reactivePower = ''
        apparentPower = ''
        ampereHour = ''
        joule = ''
        electricField = ''
        magneticField = ''
        magneticFlux = ''
        try:
	        oledExp.clear()
        except:
            pass

        while True:
            #k.checkKey()
	    r=RTC_DATE_TIME()             
	    _seconds=int(r.seconds)
	    _minutes=int(r.minutes)
	    secs =_seconds             
	    mnts =_minutes
            '''
            isUSB = os.path.isdir(usb_dir_path)
            if isUSB:
                print("USB Inserted")
                oledExp.setCursor(3, 0)
                oledExp.write("USB Connected")
                time.sleep(1)
                oledExp.clear()
                copyfiles_to_usb()
            
            '''
            cdir = pth1 + '/CDIR_' + r.dir_format
            isDir = os.path.isdir(cdir)
            while (isDir == 0):
                cdirectory = 'CDIR_' + r.dir_format
                MAKE_DIRECTORY(pth1, cdirectory)
                pth2 = os.path.join(pth1, cdirectory)
                idirectory = 'IDIR_' + r.dir_format
                MAKE_DIRECTORY(pth2, idirectory)
                # date time synchronize
		# ds3231.write_now()  # through Wifi
                break

            if secs % 10 == 0:
                res1 = a.analyserRequest('rawData')
                res2 = a.analyserRequest('userData')

                resp1 = "V=448 A=21 KW=875 R=138.8226 C=70.082 G=92.0 L=63 Z=51.26 F=43.977 "
                resp2 = "KW=295.04 VAR=400.81 KVA=497.692 Ah=641.17 J=255.5 E=670.6 M=571.19 Wb=198.3392"

                resA = resp1 + '\n' + resp2 + '\n'
                resB = res1 + '\n' + res2 + '\n'
                res = resA + resB

                x1 = resp1.index('V')
                x2 = resp1.index('A')
                x3 = resp1.index('KW')
                x4 = resp1.index('R')
                x5 = resp1.index('C')
                x6 = resp1.index('G')
                x7 = resp1.index('L')
                x8 = resp1.index('Z')
                x9 = resp1.index('F')

                voltage = resp1[x1 + 2:x2 - 1]
                current = resp1[x2 + 2:x3 - 1]
                power = resp1[x3 + 3:x4 - 1]
                resistance = resp1[x4 + 2:x5 - 1]
                capacitance = resp1[x5 + 2:x6 - 1]
                conductance = resp1[x6 + 2:x7 - 1]
                inductance = resp1[x7 + 2:x8 - 1]
                impedance = resp1[x8 + 2:x9 - 1]
                frequency = resp1[x9 + 2:]

                y1 = resp2.index('KW')
                y2 = resp2.index('VAR')
                y3 = resp2.index('KVA')
                y4 = resp2.index('Ah')
                y5 = resp2.index('J')
                y6 = resp2.index('E')
                y7 = resp2.index('M')
                y8 = resp2.index('Wb')

                realPower = resp2[y1 + 3:y2 - 1]
                reactivePower = resp2[y2 + 4:y3 - 1]
                apparentPower = resp2[y3 + 4:y4 - 1]
                ampereHour = resp2[y4 + 3:y5 - 1]
                joule = resp2[y5 + 2:y6 - 1]
                electricField = resp2[y6 + 2:y7 - 1]
                magneticField = resp2[y7 + 2:y8 - 1]
                magneticFlux = resp2[y8 + 3:]

                res_add = res_add + res
                time.sleep(1)
                #oledExp.clear()

                if secs == 0:
                    fln = 'File_hr' + r.hours + '_mnts' + str(mnts - 1)
                    pth = '/mnt/mmcblk0p1/DLPV5b'
                    WRITE_DATA_IN_FILE(pth, fln, res_add)
                    bkp_data = bkp_data + res_add
                    print(res_add)
                    res_add = ''

                    # create ZIp file
                    with zipfile.ZipFile('Files.zip', 'a', compression=zipfile.ZIP_DEFLATED) as my_zip:
                        my_zip.write(fln + ".txt")
                        # Send Zip file to server
                    os.remove(fln + ".txt")
                    # time.sleep(1)

                    if mnts % 2 == 0 and secs == 0:  # for 1hr data
                        pth2 = pth1 + '/CDIR_' + r.dir_format + '/IDIR_' + r.dir_format
                        bkp_fln = 'File_hr' + r.hours + '_mnts' + str(mnts - 2)
                        # Saves file in EMMC
                        WRITE_DATA_IN_FILE(pth2, bkp_fln, bkp_data)
                        bkp_data = ''
                        # time.sleep(1)
            try:
                if 0 <= secs <= 9:
                    oledExp.setCursor(0, 0)
                    oledExp.write(r.rtc_dateTime)
                    oledExp.setCursor(1, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(2, 0)
                    oledExp.write("VOLTAGE = " + str(voltage) + " V")
                    oledExp.setCursor(3, 0)
                    oledExp.write("CURRENT = " + str(current) + " A")
                    oledExp.setCursor(4, 0)
                    oledExp.write("POWER = " + str(power) + " KW")
                    oledExp.setCursor(6, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(7, 7)
                    oledExp.write("RUN MODE")

                elif 10 <= secs <= 19:
                    oledExp.setCursor(0, 0)
                    oledExp.write(r.rtc_dateTime)
                    oledExp.setCursor(1, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(2, 0)
                    oledExp.write("RES = " + str(resistance) + " Ohm")
                    oledExp.setCursor(3, 0)
                    oledExp.write("CAP = " + str(capacitance) + " uf")
                    oledExp.setCursor(4, 0)
                    oledExp.write("CON = " + str(conductance) + " mho")
                    oledExp.setCursor(6, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(7, 7)
                    oledExp.write("RUN MODE")

                elif 20 <= secs <= 29:
                    oledExp.setCursor(0, 0)
                    oledExp.write(r.rtc_dateTime)
                    oledExp.setCursor(1, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(2, 0)
                    oledExp.write("L = " + str(inductance) + " H")
                    oledExp.setCursor(3, 0)
                    oledExp.write("Z = " + str(impedance) + " Ohm")
                    oledExp.setCursor(4, 0)
                    oledExp.write("FREQ = " + str(frequency) + " Hz")
                    oledExp.setCursor(6, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(7, 7)
                    oledExp.write("RUN MODE")


                elif 30 <= secs <= 39:
                    oledExp.setCursor(0, 0)
                    oledExp.write(r.rtc_dateTime)
                    oledExp.setCursor(1, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(2, 0)
                    oledExp.write("P = " + str(realPower) + " KW")
                    oledExp.setCursor(3, 0)
                    oledExp.write("Q = " + str(reactivePower) + " KVAR")
                    oledExp.setCursor(4, 0)
                    oledExp.write("S = " + str(apparentPower) + " KVA")
                    oledExp.setCursor(6, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(7, 7)
                    oledExp.write("RUN MODE")

                elif 40 <= secs <= 49:
                    oledExp.setCursor(0, 0)
                    oledExp.write(r.rtc_dateTime)
                    oledExp.setCursor(1, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(2, 0)
                    oledExp.write("Bat.Level= " + str(ampereHour) + " Ah")
                    oledExp.setCursor(3, 0)
                    oledExp.write("ENERGY= " + str(joule) + " J")
                    oledExp.setCursor(4, 0)
                    oledExp.write("Elec. Fld= " + str(electricField) + " v/m")
                    oledExp.setCursor(6, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(7, 7)
                    oledExp.write("RUN MODE")

                elif 50 <= secs <= 59:
                    oledExp.setCursor(0, 0)
                    oledExp.write(r.rtc_dateTime)
                    oledExp.setCursor(1, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(2, 0)
                    oledExp.write("Mag. Fld= " + str(magneticField) + " T")
                    oledExp.setCursor(3, 0)
                    oledExp.write("Mag. Flux= " + str(magneticFlux) + " Wb")
                    oledExp.setCursor(6, 0)
                    oledExp.write("*********************")
                    oledExp.setCursor(7, 7)
                    oledExp.write("RUN MODE")
                del r
            except:
                pass
	    time.sleep(0.5)


class DIRECT_RUN_MODE:
    def __init__(self):
        isUSB = os.path.isdir(usb_dir_path)
        count=0
        while isUSB:
            r=RTC_DATE_TIME()
            try:
                print("Remove Pendrive to enter run mode")
                oledExp.setCursor(0, 0)
                oledExp.write(r.rtc_dateTime)
                oledExp.setCursor(1, 0)
                oledExp.write("*********************")
                oledExp.setCursor(2, 3)
                oledExp.write("Remove USB to ")
                oledExp.setCursor(3, 3)
                oledExp.write("enter run mode ")
                oledExp.setCursor(6, 0)
                oledExp.write("*********************")
                oledExp.setCursor(7, 3)
                oledExp.write("WAITING MODE")
                #time.sleep(1)
            except:
                pass
            time.sleep(1)
            count = count+1
            # oledExp.clear()
            isUSB = os.path.isdir(usb_dir_path)
            del r
            if count==60:
                RUN_MODE()
            else:
                pass
        else:
            try:
                oledExp.clear()
            except:
                pass
            RUN_MODE()


class DIRECT_BACKUP_MODE:
    def __init__(self):
        isUSB = os.path.isdir(usb_dir_path)
        if isUSB:
            copyfiles_to_usb()
        else:
            oledExp.setCursor(2, 0)
            oledExp.write("Connect USB to enter BACKUP Mode")
            # print("USB not Connected")
            oledExp.setCursor(6, 0)
            oledExp.write("*********************")
            oledExp.setCursor(7, 3)
            oledExp.write("WAITING MODE")
            count2=0
            while (isUSB == 0):
                isUSB = os.path.isdir(usb_dir_path)
                time.sleep(1)
                count2 =count2+1
                if count2==60:
                    RUN_MODE()
                else:
                    pass
            else:
                oledExp.clear()
                copyfiles_to_usb()

            ###################################################################


