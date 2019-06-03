SET_COLUMN_ADDRESS_LSB = 0x00;
SET_COLUMN_ADDRESS_LSB_datamask = 0x0F;
SET_COLUMN_ADDRESS_MSB = 0x10;
SET_COLUMN_ADDRESS_MSB_datamask = 0x0F;
SET_PAGE_ADDRESS = 0xB0;
SET_PAGE_ADDRESS_datamask = 0x0F;

SYSTEM_RESET = 0xE2

SET_POWER_CONTROL = 0x28;
SET_POWER_CONTROL_datamask = 0x07;
POWER_CONTROL_BOOST = 0x04;
POWER_CONTROL_VOLTAGE_REGULATOR = 0x02;
POWER_CONTROL_VOLTAGE_FOLLOWER = 0x01;

SET_Vlcd_RESISTOR_RATIO = 0x20;
SET_Vlcd_RESISTOR_RATIO_mask = 0x07;

SET_ELECTRONIC_VOLUME_b1 = 0x81
SET_ELECTRONIC_VOLUME_b2 = 0x00
SET_ELECTRONIC_VOLUME_b2_mask = 0x3F

SET_LCD_BIAS_RATIO = 0xA2
SET_LCD_BIAS_RATIO_mask = 0x01

SET_COM_DIRECTION = 0xC0
SET_COM_DIRECTION_mask = 0x08

SET_SEG_DIRECTION = 0xA0
SET_SEG_DIRECTION_mask = 0x01

SET_SCROLL_LINE = 0x40
SET_SCROLL_LINE_mask = 0x3F

SET_DISPLAY_ENABLE = 0xAE
SET_DISPLAY_ENABLE_mask = 0x01

SET_INVERSE_DISPLAY = 0xA6
SET_INVERSE_DISPLAY_mask = 0x01

class UC1701SPI():
    def __init__(self, spi, reset, rs, cs=None):
        self.spi = spi
        self.reset = reset
        self.rs = rs
        self.cs = cs

        self.reset.setOutputDirection()
        self.reset.setValue(1)

        self.rs.setOutputDirection()
        self.rs.setValue(0)
        if self.cs:
            self.cs.setOutputDirection()
            self.cs.setValue(1)

    def __spi_send(self,data):
        if self.cs:
            self.cs.setValue(0)

        self.spi.writebytes(data)

        if self.cs:
            self.cs.setValue(1)


    def __send_commands(self, commands):
        tmp = self.rs.getValue()
        self.rs.setValue(0)
        self.__spi_send(commands)
        self.rs.setValue(tmp)

    def __send_data(self, data):
        tmp = self.rs.getValue()
        self.rs.setValue(1)
        self.__spi_send(data)
        self.rs.setValue(tmp)

    def __lcd_address(self, page, column):

        column = column - 1
        page = page - 1
        

        self.__send_commands([
            SET_PAGE_ADDRESS | page & SET_PAGE_ADDRESS_datamask,
            SET_COLUMN_ADDRESS_MSB | (column>>4) & SET_COLUMN_ADDRESS_MSB_datamask,
            SET_COLUMN_ADDRESS_LSB | column & SET_COLUMN_ADDRESS_LSB_datamask
        ])

    def __lcd_reset(self):
        self.reset.setValue(0)
        time.sleep(0.100)
        self.reset.setValue(1)


    def inverse_display(self, inv=True):
        self.__send_commands([
            SET_INVERSE_DISPLAY | (inv & SET_INVERSE_DISPLAY_mask)
        ])


    def begin(self):
        self.__lcd_reset()
        time.sleep(0.020)

        self.__send_commands([SYSTEM_RESET])
        time.sleep(0.005)

        self.__send_commands([
            SET_POWER_CONTROL | (POWER_CONTROL_BOOST & SET_POWER_CONTROL_datamask)
        ])
        time.sleep(0.005)

        self.__send_commands([
            SET_POWER_CONTROL | ((POWER_CONTROL_BOOST | POWER_CONTROL_VOLTAGE_REGULATOR) & SET_POWER_CONTROL_datamask)
        ])
        time.sleep(0.005)

        self.__send_commands([
            SET_POWER_CONTROL | ((POWER_CONTROL_BOOST | POWER_CONTROL_VOLTAGE_REGULATOR | POWER_CONTROL_VOLTAGE_FOLLOWER) & SET_POWER_CONTROL_datamask)
        ])
        time.sleep(0.005)

        self.__send_commands([
            SET_Vlcd_RESISTOR_RATIO | (0x03 & SET_Vlcd_RESISTOR_RATIO_mask),
            SET_ELECTRONIC_VOLUME_b1, SET_ELECTRONIC_VOLUME_b2 | (0x28 & SET_ELECTRONIC_VOLUME_b2_mask),
            SET_LCD_BIAS_RATIO | (0x00 & SET_LCD_BIAS_RATIO_mask),
            SET_COM_DIRECTION | (1<<3 & SET_COM_DIRECTION_mask),
            SET_SEG_DIRECTION | (0 & SET_SEG_DIRECTION_mask),
            SET_SCROLL_LINE | (0 & SET_SCROLL_LINE_mask),
            SET_DISPLAY_ENABLE | (1 & SET_DISPLAY_ENABLE_mask)
        ])

    def cls(self):
        self.fill(0x00)

    def fill(self, pattern):
        data = [pattern] * 132
        for i in range(0,9):
            self.__lcd_address(1+i,1)
            self.__send_data(data)

    def end(self):
        self.__lcd_reset()
