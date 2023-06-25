import machine
import imuRegisters as reg

##############################
### 9DoF Stick - IMU Class ###
##############################

class IMU:

    ###################
    ### Constructor ###
    ###################

    def __init__(self, i2c_id, I2C_SDA_PIN, I2C_SCL_PIN):
        # i2c_id is shown in the pin diagram
        # define the SDA and SCL pins with respect to the machine.Pin class
        # default frequency is 400000 Hz (40kHz)
        self.i2c = machine.I2C(id = i2c_id, 
                    scl = machine.Pin(I2C_SCL_PIN), 
                    sda = machine.Pin(I2C_SDA_PIN),
                    freq = 400000)

    ###########################
    ### I2C Bus & Functions ###
    ###########################

    # writes data into the i2c line to the specified slave address
    def dev_write(self, data):
        pass

    # reads n bytes of data from the i2c line from the specified
    # slave address 
    def dev_read(self, i2c, addr, nbytes = 1):
        pass

    # writes data into the i2c line to the specified slave address and
    # specific register address
    def reg_write(self, addr, reg, data):
        # create bytearray to send the data in proper format
        buffer = bytearray()
        buffer.append(data)

        # send data using i2c interface
        self.i2c.writeto_mem(addr, reg, buffer)

    # reads n bytes of data from the i2c line from the specified
    # slave address and a specific register address
    def reg_read(self, addr, reg, nbytes = 1):

        # use i2c interface to receive data
        data = self.i2c.readfrom_mem(addr, reg, nbytes)
        # return the data
        return data
    
    # returns a list of available i2c devices :)
    def i2c_scan(self):
        return self.i2c.scan()

    #####################
    ### IMU Functions ###
    #####################

    # verifies that i2c communication is working
    # returns the value of the combined WHO AM I register responses
    def verify(self):
        # verify communication by reading from the WHO_AM_I registers
        agTest = int.from_bytes(self.reg_read(reg.AG_I2C_ADDR, reg.WHO_AM_I_AG, 1), 'big')
        mTest = int.from_bytes(self.reg_read(reg.M_I2C_ADDR, reg.WHO_AM_I_M, 1), 'big')
        
        # combine the two responses and compare
        result = (agTest << 8) | mTest
        expected = (reg.WHO_AM_I_AG_RSP << 8) | reg.WHO_AM_I_M_RSP
        
        if (result != expected):
            return 0

        return 1
    
    # initializes gyro ctrl registers with default values
    def initGyro(self):
        # Init CTRL_REG1_G with the value 0xA0 (011 000 00)
        # ODR value of 119 Hz (ODR_G[2:0] = 011)
        self.reg_write(reg.AG_I2C_ADDR, reg.CTRL_REG1_G, 0xA0)

        # init CTRL_REG2_G with the default value 0x00
        self.reg_write(reg.AG_I2C_ADDR, reg.CTRL_REG2_G, 0x00)

        # init CTRL_REG3_G with the default value of 0x00
        self.reg_write(reg.AG_I2C_ADDR, reg.CTRL_REG3_G, 0x00)

        # init CTRL_REG4 with the default value 0x38
        self.reg_write(reg.AG_I2C_ADDR, reg.CTRL_REG4, 0x38)

        # init ORIENT_CFG_G with the default value 0x00
        self.reg_write(reg.AG_I2C_ADDR, reg.ORIENT_CFG_G, 0x00)
    
    # initializes accel ctrl registers with default values
    def initAccel(self):
        # init CTRL_REG5_XL with the default value 0x38
        self.reg_write(reg.AG_I2C_ADDR, reg.CTRL_REG5_XL, 0x38)

        # init CTRL_REG6_XL with the value 0xA0 (011 000 00)
        # ODR value of 119 Hz (ODR_XL[2:0] = 011)
        self.reg_write(reg.AG_I2C_ADDR, reg.CTRL_REG6_XL, 0xA0)

        # init CTRl_REG7_XL with default value 0x00
        self.reg_write(reg.AG_I2C_ADDR, reg.CTRL_REG7_XL, 0x00)

    
    # initializes mag ctrl reisters with default values
    def initMag(self):
        # init CTRL_REG1_M with the default value 0x90
        # OM[6:5] = 10 (high-performance mode)
        # ODR[4:2] = 100 (10 Hz output data rate)
        self.reg_write(reg.M_I2C_ADDR, reg.CTRL_REG1_G, 0x50)

        # init CTRL_REG2_M with default value 0x00
        self.reg_write(reg.M_I2C_ADDR, reg.CTRL_REG2_M, 0x00)

        # init CTRL_REG3_M with default value 0x00
        # MD[1:0] = 00 (continuos conversion operating mode) 
        self.reg_write(reg.M_I2C_ADDR, reg.CTRL_REG3_M, 0x00)

        # init CTRL_REG4_M with default value 0x08
        # OMZ[3:2] = 10 (high-performance mode)
        self.reg_write(reg.M_I2C_ADDR, reg.CTRL_REG4_M, 0x08)

        # init CTRL_REG5_M with default value 0x00
        self.reg_write(reg.M_I2C_ADDR, reg.CTRL_REG5_M, 0x00)

    # 
    def accelAvailable(self):
        # read one byte from STATUS_REG_1
        status = self.reg_read(reg.AG_I2C_ADDR, reg.STATUS_REG_1)

        # return bit corresponding to new accel info\
        if ((status[0] & 0x1) == 0x1):
            return True
        
        return False 
    
    # 
    def gyroAvailable(self):
        # read one byte from STATUS_REG_1
        status = self.reg_read(reg.AG_I2C_ADDR, reg.STATUS_REG_1)

        # return bit corresponding to new gyro info
        if ((status[0] & 0x2) == 0x2):
            return True
        
        return False
    
    #
    def tempAvailable(self):
        # read one byte from STATUS_REG_1
        status = self.reg_read(reg.AG_I2C_ADDR, reg.STATUS_REG_1)

        # return bit corresponding to new temp info
        if ((status[0] & 0x4) == 0x4):
            return True
        
        return False

    #
    def magAvailable(self):
        # read one byte from STATUS_REG_1
        status = self.reg_read(reg.M_I2C_ADDR, reg.STATUS_REG_M)

        # extract new status bit for each axis
        xAvailable = (status[0] & 0x1) >> 0
        yAvailable = (status[0] & 0x2) >> 1
        zAvailable = (status[0] & 0x4) >> 2

        # return true if any axis contains new data
        if (xAvailable == 1 or yAvailable == 1 or zAvailable == 1):
            return True
        
        return False

    #
    def magAvailableAxis(self, axis):
        pass

    # reads the accel data, scales it, and returns it as a 3-tuple of data
    # (X_AXIS, Y_AXIS, Z_AXIS)
    def readAccel(self):
        # read 6 bytes from consecutive register addresses
        # data is of type bytearray
        raw_data = self.reg_read(reg.AG_I2C_ADDR, reg.OUT_X_L_XL, 6)
        
        ### convert raw 2's complement into signed int ###
        # check if MSB is 1 (negative)
        raw_ax = (raw_data[1] << 8) | raw_data[0]
        if (raw_ax >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            ax = -1 * ((raw_ax ^ 0xFFFF) + 0x1)
        else:
            # just return value as is
            ax = raw_ax

        raw_ay = (raw_data[3] << 8) | raw_data[2]
        if (raw_ay >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            ay = -1 * ((raw_ay ^ 0xFFFF) + 0x1)
        else:
            ay = raw_ay
        
        raw_az = (raw_data[5] << 8) | raw_data[4]
        if (raw_az >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            az = -1 * ((raw_az ^ 0xFFFF) + 0x1)
        else:
            az = raw_az

        # use conversion values based on default scale of 2g
        ax = ax * reg.SENSITIVITY_ACCEL_2 * reg.GRAVITY
        ay = ay * reg.SENSITIVITY_ACCEL_2 * reg.GRAVITY
        az = az * reg.SENSITIVITY_ACCEL_2 * reg.GRAVITY

        # create output 3-tuple
        output = (ax, ay, az)

        # return the output array containing data of the format [ax, ay, az]
        return output
    
    # reads the gyro data, scales it, and returns it as a 3-tuple of data
    # (X_AXIS, Y_AXIS, Z_AXIS
    def readGyro(self):
        # read 6 bytes from consecutive register addresses
        # data is of type bytearray
        raw_data = self.reg_read(reg.AG_I2C_ADDR, reg.OUT_X_L_G, 6)

        ### convert raw 2's complement into signed int ###
        # check if MSB is 1 (negative)
        raw_x = (raw_data[1] << 8) | raw_data[0]
        if (raw_x >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            x = -1 * ((raw_x ^ 0xFFFF) + 0x1)
        else:
            # just return value as is
            x = raw_x

        raw_y = (raw_data[3] << 8) | raw_data[2]
        if (raw_y >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            y = -1 * ((raw_y ^ 0xFFFF) + 0x1)
        else:
            y = raw_y
        
        raw_z = (raw_data[5] << 8) | raw_data[4]
        if (raw_z >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            z = -1 * ((raw_z ^ 0xFFFF) + 0x1)
        else:
            z = raw_z

        # use conversion values based on default scale of 245 DPS
        gx = x * reg.SENSITIVITY_GYRO_245
        gy = y * reg.SENSITIVITY_GYRO_245
        gz = z * reg.SENSITIVITY_GYRO_245

        # create output 3-tuple
        output = (gx, gy, gz)

        # return the output array containing data of the format [ax, ay, az]
        return output
    
    # reads the magneto data, scales it, and returns it as a 3-tuple of data
    # (X_AXIS, Y_AXIS, Z_AXIS)
    def readMag(self, mode = 0):
        # read 6 bytes from consecutive register addresses
        # data is of type bytearray
        raw_data = self.reg_read(reg.M_I2C_ADDR, reg.OUT_X_L_M, 6)

        ### convert raw 2's complement into signed int ###
        # check if MSB is 1 (negative)
        raw_x = (raw_data[1] << 8) | raw_data[0]
        if (raw_x >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            x = -1 * ((raw_x ^ 0xFFFF) + 0x1)
        else:
            # just return value as is
            x = raw_x

        raw_y = (raw_data[3] << 8) | raw_data[2]
        if (raw_y >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            y = -1 * ((raw_y ^ 0xFFFF) + 0x1)
        else:
            y = raw_y
        
        raw_z = (raw_data[5] << 8) | raw_data[4]
        if (raw_z >> 15 == 1):
            # 2's complement conversion using the bitwise XOR and adding one
            z = -1 * ((raw_z ^ 0xFFFF) + 0x1)
        else:
            z = raw_z

        # use conversion values based on the default scale
        mx = x * reg.SENSIIVITY_MAG_4
        my = y * reg.SENSIIVITY_MAG_4
        mz = z * reg.SENSIIVITY_MAG_4

        # create output 3-tuple
        if (mode == 1):
            # raw values (without scaling)
            # used for magneto calibration
            output = (x, y, z)
        else:
            output = (mx, my, mz)

        # return the output array containing data of the format [mx, my, mz]
        return output
    
    # reads the temp data and stores it
    def readTemp():
        pass

    ### Calibration ###
    def calibrateAG(self):
        # calibrate accel and gyro
        pass

    def calibrateMag(self):
        # array to hold min for each axis
        magMin = [0, 0, 0]
        # array to hold max for each axis
        magMax = [0, 0, 0]

        i = 0
        # use 128 samples to calibrate
        while (i < 128):
            if (self.magAvailable()):
                # increment i
                i += 1
                # read and store raw magneto values
                magTemp = self.readMag(mode=1)

                # 1, 2, and 3
                for j in range(3):
                    if (magTemp[j] > magMax[j]):
                        magMax[j] = magTemp[j]
                    if (magTemp[j] < magMin[j]):
                        magMin[j] = magTemp[j]

        for j in range(3):
            offset = int( (magMax[j] + magMin[j]) / 2 )
            offset_h = (offset & 0xFF00) >> 8
            offset_l = offset & 0x00FF

            self.reg_write(reg.M_I2C_ADDR, (reg.OFFSET_X_REG_L_M + (2 * j)), offset_l)
            self.reg_write(reg.M_I2C_ADDR, (reg.OFFSET_X_REG_H_M + (2 * j)), offset_h)

    ### Init & Start ###
    def initIMU(self):
        # verify i2c connection was succesful
        if not(self.verify()):
            # if verify returns a value of 0 it means that connection was not succesful
            # exit upon error in connection and report to terminal
            if (reg.VERBOSITY):
                print('ERROR: i2c verification failed')
            return 0

        # initialize every sensor
        self.initAccel()
        self.initGyro()
        self.initMag()

        # initialized succesfully
        return 1




##################################
### Main: Debugging & Testing ####
##################################

if __name__ == '__main__':
    pass
    

    

