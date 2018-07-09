import time
import sys
sys.path.insert(0, '/home/pi/ZeroBorg')

import ZeroBorg



ZB = ZeroBorg.ZeroBorg()
ZB.Init()

ZB.SetMotor1(1)
ZB.SetMotor2(1)
ZB.SetMotor3(1)
ZB.SetMotor4(1)

time.sleep(1)

ZB.SetMotor1(0.8)
ZB.SetMotor2(0.8)
ZB.SetMotor3(0.8)
ZB.SetMotor4(0.8)

time.sleep(1)

ZB.MotorsOff()

exit()
