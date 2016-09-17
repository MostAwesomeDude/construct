from construct.lib.binary import integer2bits, integer2bytes, onebit2integer, bits2integer, bytes2integer, bytes2bits, bits2bytes, swapbytes


class RestreamedBytesIO(object):
    __slots__ = ["substream", "encoder", "encoderunit", "decoder", "decoderunit", "rbuffer", "wbuffer"]

    def __init__(self, substream, encoder, encoderunit, decoder, decoderunit):
        self.substream = substream
        self.encoder = encoder
        self.encoderunit = encoderunit
        self.decoder = decoder
        self.decoderunit = decoderunit
        self.rbuffer = b""
        self.wbuffer = b""

    def read(self, count):
        if count < 0:
            raise ValueError("count cannot be negative")
        while len(self.rbuffer) < count:
            self.rbuffer += self.decoder(self.substream.read(self.decoderunit))
        data, self.rbuffer = self.rbuffer[:count], self.rbuffer[count:]
        return data

    def write(self, data):
        self.wbuffer += data
        while len(self.wbuffer) >= self.encoderunit:
            data, self.wbuffer = self.wbuffer[:self.encoderunit], self.wbuffer[self.encoderunit:]
            self.substream.write(self.encoder(data))

    def close(self):
        if len(self.rbuffer):
            raise ValueError("closing stream but %d unread bytes remain, %d in decoded unit" % (len(self.rbuffer), self.decoderunit))
        if len(self.wbuffer):
            raise ValueError("closing stream but %d unwritten bytes remain, %d in encoded unit" % (len(self.wbuffer), self.encoderunit))


class BitStreamReader(object):
    __slots__ = ["substream", "buffer", "total_size"]

    def __init__(self, substream):
        self.substream = substream
        self.total_size = 0
        self.buffer = b""

    def close(self):
        if self.total_size % 8 != 0:
            raise ValueError("total size of read data must be a multiple of 8", self.total_size)

    def tell(self):
        return self.substream.tell()

    def seek(self, pos, whence = 0):
        self.buffer = b""
        self.total_size = 0
        self.substream.seek(pos, whence)

    def read(self, count):
        if count < 0:
            raise ValueError("count cannot be negative")

        l = len(self.buffer)
        if count == 0:
            data = b""
        elif count <= l:
            data = self.buffer[:count]
            self.buffer = self.buffer[count:]
        else:
            data = self.buffer
            count -= l
            count_bytes = count // 8
            if count & 7:
                count_bytes += 1
            buf = bytes2bits(self.substream.read(count_bytes))
            data += buf[:count]
            self.buffer = buf[count:]
        self.total_size += len(data)
        return data


class BitStreamWriter(object):
    __slots__ = ["substream", "buffer", "pos"]

    def __init__(self, substream):
        self.substream = substream
        self.buffer = []
        self.pos = 0

    def close(self):
        self.flush()

    def flush(self):
        raw = bits2bytes(b"".join(self.buffer))
        self.substream.write(raw)
        self.buffer = []
        self.pos = 0

    def tell(self):
        return self.substream.tell() + self.pos // 8

    def seek(self, pos, whence = 0):
        self.flush()
        self.substream.seek(pos, whence)

    def write(self, data):
        if not data:
            return
        if not isinstance(data, bytes):
            raise TypeError("data must be a string, not %r" % (type(data),))
        self.buffer.append(data)

