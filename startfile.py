# This code Creates Folders and Files in SrcDir1(for checking the code dataLoggerMain.py)
# Note: Create SrcDir1 in the path

import time
from datetime import date, timedelta
import emmctousb
import analyserSensor
import os.path

delay=1

class WRITE_DATA_IN_FILE:
    def __init__(self,pth, fileName, response):
        completeName=os.path.join(pth,fileName+".txt")
        self.fileName = completeName
        self.response = response
        f = open(self.fileName, "w")
        f.write(self.response + '\n')
        f.close()

class MAKE_DIRECTORY:
    def __init__(self,pth,directory):
        self.parent_dir = pth
        self.directory = directory
        dst_dir_path = os.path.join(self.parent_dir, self.directory)
        os.mkdir(dst_dir_path)


if __name__ == "__main__":
    print("Welcome to Onion")
    time.sleep(delay)
    print("Data Logger Project")
    time.sleep(delay)
    res_add=''
    bkp_data=''

    b=emmctousb.ENTER_FROM_AND_TO_DATES()
    a = analyserSensor.ANALYSER_SENSOR()

    if True:
        checking_of_dates=0
        createFolders = 0
        createFiles = 0
        while (checking_of_dates==0):
            b.enterfromdate()
            b.entertodate()
            checking_of_dates = b.isdatesAcceptable()
            sdate = date(b.fr_yy, b.fr_mm, b.fr_dd)  # start date
            edate = date(b.to_yy,b.to_mm,b.to_dd)  # end date
            delta = edate - sdate  # as timedelta

            # For folders Creation
            while createFolders==0:
                for i in range(delta.days + 1):
                    d = analyserSensor.GET_DATE_TIME()
                    secs = int(d.secs)
                    mnts = int(d.mnts)

                    day = str(sdate + timedelta(days=i))
                    cdir_format = "CDIR_" + day[8:10] + day[5:7] + day[2:4]
                    pth1 = '/mnt/mmcblk0p1/BKP_DLPV3b/SrcDir1'
                    cdir = pth1 + '/CDIR_' + cdir_format[5:]
                    isDir = os.path.isdir(cdir)

                    if (isDir == 0):
                        # pth1='/home/nagendra/PycharmProjects/DLPV1b/SrcDir'
                        cdirectory = 'CDIR_' + cdir_format[5:]
                        MAKE_DIRECTORY(pth1, cdirectory)
                        pth2 = os.path.join(pth1, cdirectory)
                        idirectory = 'IDIR_' + cdir_format[5:]
                        MAKE_DIRECTORY(pth2, idirectory)
                createFolders=1

            #For File Creation
            while createFiles==0:
                for i in range(delta.days + 1):
                    day = str(sdate + timedelta(days=i))
                    cdir_format="CDIR_"+day[8:10]+day[5:7]+day[2:4]
                    pth1 ='/mnt/mmcblk0p1/BKP_DLPV3b/SrcDir1'
                    pth2 = pth1 + '/CDIR_' + cdir_format[5:]+'/IDIR_'+cdir_format[5:]

                    for j in range (0,12):
                        fln='file_hr'+str(j)
                        res1 = a.analyserRequest('rawData')
                        res2 = a.analyserRequest('userData')
                        res_add = res1 + '\n' + res2 + '\n'
                        WRITE_DATA_IN_FILE(pth2, fln, res_add)
                print("Program End")
                createFiles=1
