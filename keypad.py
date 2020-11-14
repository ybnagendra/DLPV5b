import copy
import omega_gpio
import time
import os,sys
from OmegaExpansion import oledExp
"""
f = open('confdata.txt', 'r') 
lines = f.readlines() 
SiteID = lines[0].rstrip('\n') 
MonitoringID= lines[1].rstrip('\n') 
AnalyzerID= lines[2].rstrip('\n') 
ParameterID= lines[3].rstrip('\n')
"""
class KEYPAD:
    def getPressKey(self):
        a = [0, 1, 2, 3, 11, 18, 8, 9]
        r = [0, 1, 2, 3]
        c = [18, 11, 8, 9]

        key = [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"],
        ]

        values = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
        ]

        lastvalues = copy.deepcopy(values)

        # close before open if used
        for pin in a:
            try:
                omega_gpio.closepin(pin)
            except:
                e = 1  # dummy command :-)

        # pin init
        for pin in r:
            omega_gpio.initpin(pin, 'out')

        for pin in c:
            omega_gpio.initpin(pin, 'in')

        while True:
            rpos = 0
            for rpin in r:
                omega_gpio.setoutput(r[0], 0)
                omega_gpio.setoutput(r[1], 0)
                omega_gpio.setoutput(r[2], 0)
                omega_gpio.setoutput(r[3], 0)
                omega_gpio.setoutput(rpin, 1)
                time.sleep(0.05)
                cpos = 0
                for cpin in c:
                    input = omega_gpio.readinput(cpin)
                    values[rpos][cpos] = input
                    cpos = cpos + 1
                rpos = rpos + 1

            for x in range(0, 4):
                for y in range(0, 4):
                    if values[x][y] != lastvalues[x][y]:
                        self.keycode = key[x][y]
                        if values[x][y] == 1:
                            return self.keycode

            lastvalues = copy.deepcopy(values)

    def checkKey(self):
        a = [0, 1, 2, 3, 11, 18, 8, 9]
        r = [0, 1, 2, 3]
        c = [18, 11, 8, 9]

        key = [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"],
        ]

        values = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
        ]

        lastvalues = copy.deepcopy(values)

        # close before open if used
        for pin in a:
            try:
                omega_gpio.closepin(pin)
            except:
                e = 1  # dummy command :-)

        # pin init
        for pin in r:
            omega_gpio.initpin(pin, 'out')

        for pin in c:
            omega_gpio.initpin(pin, 'in')

        if True:
            rpos = 0
            for rpin in r:
                omega_gpio.setoutput(r[0], 0)
                omega_gpio.setoutput(r[1], 0)
                omega_gpio.setoutput(r[2], 0)
                omega_gpio.setoutput(r[3], 0)
                omega_gpio.setoutput(rpin, 1)
                time.sleep(0.05)
                cpos = 0
                for cpin in c:
                    input = omega_gpio.readinput(cpin)
                    values[rpos][cpos] = input
                    cpos = cpos + 1
                rpos = rpos + 1

            for x in range(0, 4):
                for y in range(0, 4):
                    if values[x][y] != lastvalues[x][y]:
                        keycode = key[x][y]
                        if values[x][y] == 1:
                            if keycode == 'D':
				oledExp.clear()
                                oledExp.write("System reseting...")
                                time.sleep(5)
                                os.execl(sys.executable, sys.executable, * sys.argv)   #for resetting the program
                            elif keycode == 'A':
				f = open('confdata.txt', 'r') 
				lines = f.readlines() 
				SiteID = lines[0].rstrip('\n') 
				MonitoringID= lines[1].rstrip('\n') 
				AnalyzerID= lines[2].rstrip('\n') 
				ParameterID= lines[3].rstrip('\n')
				oledExp.clear()
                                oledExp.setCursor(0, 0)
                                oledExp.write(SiteID)
				oledExp.setCursor(1,0)
				oledExp.write(MonitoringID)
				oledExp.setCursor(2,0)                                 
				oledExp.write(AnalyzerID)
				oledExp.setCursor(3,0)                                 
				oledExp.write(ParameterID)
                                time.sleep(5)
                                oledExp.clear()
                            else:
				oledExp.clear()
                                oledExp.setCursor(0,0)
                                oledExp.write("Press 'D' for Reset")
				oledExp.setCursor(1,0)
				oledExp.write("'A' for userData")
				time.sleep(5)
				oledExp.clear()
            lastvalues = copy.deepcopy(values)

            #####################################################################################
"""
if __name__=="__main__":
	print("Hello")
	k=KEYPAD()
	while True:
		k.checkKey()

"""
