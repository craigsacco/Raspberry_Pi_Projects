import types

def add_i2c_device_overrides(device):

    def _read_raw_s16(self, little_endian=True):
        result = self.readRawU16(little_endian)
        if result > 32767:
            result -= 65536
        return result

    def _read_raw_s16be(self):
        return self.readRawS16(False)

    def _read_raw_u16(self, little_endian=True):
        bytes = self._bus.read_bytes(self._address, 2)
        result = bytes[0] + (bytes[1] << 8)
        self._logger.debug("Read 0x%04X", result)
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    def _read_raw_u16be(self):
        return self.readRawU16(False)

    device.readRawS16 = types.MethodType(_read_raw_s16, device)
    device.readRawS16BE = types.MethodType(_read_raw_s16be, device)
    device.readRawU16 = types.MethodType(_read_raw_u16, device)
    device.readRawU16BE = types.MethodType(_read_raw_u16be, device)
    return device

def add_smbus_overrides(smbus):

    def _read_bytes(self, addr, len=1):
        self._select_device(addr)
        return [ord(x) for x in self._device.read(len)]

    smbus.read_bytes = types.MethodType(_read_bytes, smbus)
    return smbus
