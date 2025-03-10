import datetime
import struct
import time
import unittest
#from urllib import request
import urllib
import urllib.request

import pandas as pd

#from QUANTAXIS import QUANTAXIS as QA

'''
 字节串转整数:
    转义为short型整数: struct.unpack('<hh', bytes(b'\x01\x00\x00\x00'))  ==>  (1, 0)
    转义为long型整数:  struct.unpack('<L',  bytes(b'\x01\x00\x00\x00'))  ==>  (1,)

    整数转字节串:
    转为两个字节: struct.pack('<HH', 1,2)  ==>  b'\x01\x00\x02\x00'
    转为四个字节: struct.pack('<LL', 1,2)  ==>  b'\x01\x00\x00\x00\x02\x00\x00\x00'
    
    字符串转字节串:
    字符串编码为字节码: '12abc'.encode('ascii')  ==>  b'12abc'
    数字或字符数组: bytes([1,2, ord('1'),ord('2')])  ==>  b'\x01\x0212'
    16进制字符串: bytes().fromhex('010210')  ==>  b'\x01\x02\x10'
    16进制字符串: bytes(map(ord, '\x01\x02\x31\x32'))  ==>  b'\x01\x0212'
    16进制数组: bytes([0x01,0x02,0x31,0x32])  ==>  b'\x01\x0212'

    字节串转字符串:
    字节码解码为字符串: bytes(b'\x31\x32\x61\x62').decode('ascii')  ==>  12ab
    字节串转16进制表示,夹带ascii: str(bytes(b'\x01\x0212'))[2:-1]  ==>  \x01\x0212
    字节串转16进制表示,固定两个字符表示: str(binascii.b2a_hex(b'\x01\x0212'))[2:-1]  ==>  01023132
    字节串转16进制数组: [hex(x) for x in bytes(b'\x01\x0212')]  ==>  ['0x1', '0x2', '0x31', '0x32']
'''


class QA_Test(unittest.TestCase):
    def setUp(self):
        today = datetime.date.today()

        print(today.year)
        print(today.month)
        print(today.day)
        str = "%04d-%02d-%02d" % (today.year, today.month, today.day)
        print(str)

        pass

    def setTear(self):
        pass

    def nottest_QA(self):
        fileDad = open("wss0507r.dad", 'rb')
        fileDad.seek(0, 0)

        index = 0
        first4Bytes = fileDad.read(4)

        df = pd.DataFrame(columns=["stock_name", "date", "open", "close", "low", "high", "volumn", "turn"],
                          index=["code"])

        if first4Bytes[0] == 0x8c and first4Bytes[1] == 0x19 and first4Bytes[2] == 0xfc and first4Bytes[3] == 0x33:
            fileDad.seek(0x08)
            byteNumberOfStock = fileDad.read(0x04)
            longNumberOfStock = struct.unpack('<L', byteNumberOfStock)
            # print(longNumberOfStock);

            for iStockIndex in range(0, longNumberOfStock[0]):
                fileDad.seek(0x10 + iStockIndex * 4 * 0x10)

                aStockData = fileDad.read(0x10 * 4)

                if aStockData[0] == 0xFF and aStockData[1] == 0xFF and aStockData[2] == 0xFF and aStockData[3] == 0xFF:

                    codeNameByte = aStockData[4:0x10]
                    # print(codeNameByte)
                    strCodeName = codeNameByte.decode('gbk')
                    # print(strCodeName);

                    stockNameByte = aStockData[0x14: 0x20]
                    # print(stockNameByte);
                    strStockName = stockNameByte.decode('gbk')
                    # print(strStockName);

                    stockTime = aStockData[0x20: 0x24]
                    stockTimeNumber = struct.unpack('<L', stockTime)
                    time_local = time.localtime(stockTimeNumber[0])

                    #dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    dt = time.strftime("%Y-%m-%d", time_local)

                    # print(dt);

                    i = 1
                    byte_stock_open = aStockData[0x20 +
                                                 (i * 4): 0x20+((i+1) * 4)]
                    i = 2
                    byte_stock_close = aStockData[0x20 +
                                                  (i * 4): 0x20+((i+1) * 4)]
                    i = 3
                    byte_stock_low = aStockData[0x20+(i * 4): 0x20+((i+1) * 4)]
                    i = 4
                    byte_stock_high = aStockData[0x20 +
                                                 (i * 4): 0x20+((i+1) * 4)]
                    i = 5
                    byte_stock_volume = aStockData[0x20 +
                                                   (i * 4): 0x20+((i+1) * 4)]
                    i = 6
                    byte_stock_turn = aStockData[0x20 +
                                                 (i * 4): 0x20+((i+1) * 4)]
                    i = 7

                    v1 = struct.unpack('<f', byte_stock_open)
                    stock_open = v1[0]

                    v1 = struct.unpack('<f', byte_stock_close)
                    stock_close = v1[0]

                    v1 = struct.unpack('<f', byte_stock_low)
                    stock_low = v1[0]

                    v1 = struct.unpack('<f', byte_stock_high)
                    stock_high = v1[0]

                    v1 = struct.unpack('<f', byte_stock_volume)
                    stock_volume = v1[0]

                    v1 = struct.unpack('<f', byte_stock_turn)
                    stock_turn = v1[0]

                    #print("%f %f %f %f %f %f "%(stock_open, stock_close, stock_high,stock_low, stock_volume, stock_turn))
                    # print("------")

                    df.index.astype(str)

                    df.loc[strCodeName] = [strStockName, dt, stock_open,
                                           stock_close, stock_low, stock_high, stock_volume, stock_turn]

                    pass
                pass

        fileDad.close()

        print(df)

        return df

    pass
