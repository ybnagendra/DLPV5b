import datetime, pytz
import random
import jsonpickle

class GET_DATE_TIME:
    def __init__(self):
        now_utc = datetime.datetime.utcnow()
        local_tz = pytz.timezone('Asia/Kolkata')
        now_utc = pytz.utc.localize(now_utc)
        x = now_utc.astimezone(local_tz)
	self.mnts=x.strftime("%M")
	self.secs=x.strftime("%S")
        self.date_time = x.strftime("%d/%m/%y,%H:%M:%S")


class ANALYSER_SENSOR:
    def analyserRequest(self, command):
        if command == 'rawData':
            d = GET_DATE_TIME()
            # Collect data
            time1 = d.date_time
            barometricPressure = random.randint(500, 1200)
            temperature = random.randint(20, 60)
            humidity = random.randint(20, 60)
            packetNo = random.random()  # Return a float value between 0 and 1

            dataObj1 = {
                'Time': time1,
                'BarometricPressure': barometricPressure,
                'Temperature': temperature,
                'Humidity': humidity,
                'PacketNo': packetNo
            }

            self.ds1 = jsonpickle.encode(dataObj1)
            return self.ds1

        elif command == 'userData':
            f = open('confdata.txt', 'r')
            lines = f.readlines()
            dataObj2 = {
                'SiteId': lines[0].rstrip('\n'),
                'MonitoringID': lines[1].rstrip('\n'),
                'AnalyzerID': lines[2].rstrip('\n'),
                'ParameterID': lines[3].rstrip('\n')
            }
            self.ds2 = jsonpickle.encode(dataObj2)
            return self.ds2