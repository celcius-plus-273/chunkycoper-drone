
### hex to int conversion test ###
value = '01FF'

print(f'The string literal is: {value}')
print(f'Its type is: {type(value)}')

converted = bytes.fromhex(value)

print(f'The converted string literal is: {converted}')
print(f'Its type is: {type(converted)}')

number = int.from_bytes(converted, 'big')
print(f'The integer value is: {number}')
print(f'Its type is: {type(number)}')

### testing bytearray() ###
buffer1 = bytearray()


buffer1.append(0x01)

buffer1.append(0xFF)

print(buffer1[0:1])
hex1 = int.from_bytes(buffer1, 'big', signed=True) >> 8
hex2 = int.from_bytes(buffer1[1:2], 'big', signed=True)

a = converted[0:1]
print(f'a: {a}')
b = converted[1:2]
print(f'b: {b}')

print(f'len(a): {len(a)}')
hex3 = int.from_bytes(converted[0:1], 'big', signed=True)
hex4 = int.from_bytes(converted[1:2], 'big', signed=True)

print(f'Hex1: {hex1}, Hex2: {hex2}, Hex3: {hex3}, Hex4: {hex4}')

print(f'a[0]: {a[0]}')

seven_bits = b[0] >> 1
myByteArray = bytearray()
myByteArray.append(seven_bits)

if (b[0] >> 7 == 1):
    print(-1* int.from_bytes(myByteArray, 'big'))
else:
    print(int.from_bytes(myByteArray, 'big'))

### inverting bits test ###
hex_num = 0xa
print(f'hex_num: {hex_num:4b}')

inverted_hex_num = (hex_num ^ 0xf) + 1
print(f'inverted_hex_num: {inverted_hex_num:4b}')

