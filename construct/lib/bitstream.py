

class RestreamedBytesIO(object):
    """Used internally."""
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
        datalen = len(data)
        while len(self.wbuffer) >= self.encoderunit:
            data, self.wbuffer = self.wbuffer[:self.encoderunit], self.wbuffer[self.encoderunit:]
            self.substream.write(self.encoder(data))
        return datalen

    def close(self):
        if len(self.rbuffer):
            raise ValueError("closing stream but %d unread bytes remain, %d in decoded unit" % (len(self.rbuffer), self.decoderunit))
        if len(self.wbuffer):
            raise ValueError("closing stream but %d unwritten bytes remain, %d in encoded unit" % (len(self.wbuffer), self.encoderunit))

