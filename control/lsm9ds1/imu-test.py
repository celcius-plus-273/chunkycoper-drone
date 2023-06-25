import imu
import machine
import time

newImu = imu.IMU(1, 14, 15)

scanned = newImu.i2c_scan()
for scan in scanned:
    print(f'{scan:x} is an available i2c address')

# init IMU
result = newImu.initIMU()
if (result):
    print('imu has been init')
else:
    print('error during init')

newImu.calibrateMag()
print('mag has been calibrated')
time.sleep_ms(500)

while True:
    # check if there's new accel data
    if (newImu.accelAvailable()):
        accelData = newImu.readAccel()
    else:
        accelData = (0, 0, 0)
        print('no new accel data available')

    if (newImu.gyroAvailable()):
        gyroData = newImu.readGyro()
    else:
        gyroData = (0, 0, 0)
        print('no new gyro data available')

    if (newImu.magAvailable()):
        magData = newImu.readMag()
    else:
        magData = (0, 0, 0)
        print("no new mag data available")

    # print accel data for each axis    
    print(f'|| ax = {accelData[0]:6.3f} | ay = {accelData[1]:6.3f} | az = {accelData[2]:6.3f} ||')
    print(f'|| gx = {gyroData[0]:6.2f} | gy = {gyroData[1]:6.2f} | gz = {gyroData[2]:6.2f} ||')
    print(f'|| mx = {magData[0]:6.3f} | my = {magData[1]:6.3f} | mz = {magData[2]:6.3f} ||')
    print("==========================================")
    time.sleep_ms(200)
