#############################
### Constants & Registers ###
#############################
    
### i2c addresses ###
AG_I2C_ADDR = 0x6B # accel and gyro i2c address
M_I2C_ADDR = 0x1E # magnetometer i2c address

### sensor sensitivity constans ###
SENSITIVITY_ACCEL_2 = 0.000061
SENSITIVITY_GYRO_245 = 0.00875
SENSIIVITY_MAG_4 = 0.00014
GRAVITY = 9.8

### accel/gyro (xl/g) registers ###
CTRL_REG1_G = 0x10
CTRL_REG2_G = 0x11
CTRL_REG3_G = 0x12
ORIENT_CFG_G = 0x13 

OUT_TEMP_L = 0X15
OUT_TEMP_H = 0x1

STATUS_REG_0 = 0X17

OUT_X_L_G = 0x18
OUT_X_H_G = 0x19
OUT_Y_L_G = 0x1A
OUT_Y_H_G = 0x1B
OUT_Z_L_G = 0x1C
OUT_Z_H_G = 0x1D

CTRL_REG4 = 0x1E
CTRL_REG5_XL = 0x1F
CTRL_REG6_XL = 0x20
CTRL_REG7_XL = 0X21

STATUS_REG_1 = 0x27
OUT_X_L_XL = 0x28
OUT_X_H_XL = 0x29
OUT_Y_L_XL = 0x2A
OUT_Y_H_XL = 0x2B
OUT_Z_L_XL = 0x2C
OUT_Z_H_XL = 0x2D

FIFO_CTRL = 0x2E
FIFO_SRC = 0x2F

### magneto registers ###
OFFSET_X_REG_L_M = 0x05
OFFSET_X_REG_H_M = 0x06
OFFSET_Y_REG_L_M = 0x07
OFFSET_Y_REG_H_M = 0x08
OFFSET_Z_REG_L_M = 0x09
OFFSET_Z_REG_H_M = 0x0A

CTRL_REG1_M = 0x20
CTRL_REG2_M = 0x21
CTRL_REG3_M = 0x22
CTRL_REG4_M = 0x23
CTRL_REG5_M = 0x24

STATUS_REG_M = 0x27

OUT_X_L_M = 0x28
OUT_X_H_M = 0x29
OUT_Y_L_M = 0x2A
OUT_Y_H_M = 0x2B
OUT_Z_L_M = 0x2C
OUT_Z_H_M = 0x2D

### who am i? question registers ###
WHO_AM_I_AG = 0x0F
WHO_AM_I_M = 0x0F

### who am i? response registers (for comparisson purposes) ###
WHO_AM_I_AG_RSP = 0x68
WHO_AM_I_M_RSP = 0x3D

# Verbosity constant for debug prints
VERBOSITY = False