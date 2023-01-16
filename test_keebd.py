from keebd import Frame, Encoder

class TestFrame:
    NULL=chr(0x00)

    def test_empty_buffer(self):
        assert self.NULL*8 == str(Frame())

    def test_press_modifier_changes_first_byte(self):
        bytes = str(Frame().press_modifier(chr(0x01)))
        assert chr(0x01) + self.NULL*7 == bytes

    def test_press_key_changes_third_byte(self):
        bytes = str(Frame().press_key(chr(0x01)))
        assert self.NULL*2+chr(0x01)+self.NULL*5 == bytes

class TestEncoder:
    def assert_encodes_to(self, bytes, char):
        actual_bytes = Encoder().encode_single_character(char)
        assert bytes == actual_bytes[0:8]
    
    def test_ignores_unmanaged_character(self):
        assert '' == Encoder().encode_single_character('@')

    def test_encode_a_letter(self):
        expected_bytes = "\x00\x00\x04\x00\x00\x00\x00\x00"
        self.assert_encodes_to(expected_bytes, 'a')

    def test_encode_a_letter_releases_that_letter(self):
        bytes = Encoder().encode_single_character('a')
        assert chr(0x00)*8 == bytes[8:]

    def test_encodes_another_letter(self):
        expected_bytes = "\x00\x00\x1d\x00\x00\x00\x00\x00"
        self.assert_encodes_to(expected_bytes, 'z')

    def test_encodes_a_capital(self):
        expected_bytes = "\x20\x00\x04\x00\x00\x00\x00\x00"
        self.assert_encodes_to(expected_bytes, 'A')

    def test_encodes_space(self):
        expected_bytes = "\x00\x00\x2c\x00\x00\x00\x00\x00"
        self.assert_encodes_to(expected_bytes, ' ')

    def test_encodes_tab(self):
        expected_bytes = "\x00\x00\x2b\x00\x00\x00\x00\x00"
        self.assert_encodes_to(expected_bytes, "\t")

    def test_encodes_string(self):
        string = "BARBARA POST"
        encoded = Encoder().to_scancodes(string)
        assert len(string)*16 ==  len(encoded)

    def test_drops_unknown_chars(self):
        string = "BARBARA@ POST"
        encoded = Encoder().to_scancodes(string)
        assert (len(string)-1)*16 == len(encoded)
