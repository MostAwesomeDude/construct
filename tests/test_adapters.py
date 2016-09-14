# import unittest

# from construct import *
# from construct.protocols.layer3.ipv4 import IpAddress


# class TestFlagsAdapter(unittest.TestCase):

#     def setUp(self):
#         self.fa = FlagsAdapter(Byte('HID_type'), {'feature': 4, 'output': 2, 'input': 1})

#     def test_trivial(self):
#         pass

#     def test_parse(self):
#         self.assertEqual(self.fa.parse(b'\x04'), FlagsContainer(output=False,feature=True,input=False))

#     def test_build(self):
#         self.assertEqual(self.fa.build(dict(feature=True, output=True, input=False)), b'\x06')
#         self.assertEqual(self.fa.build(dict(feature=True)), b'\x04')
#         self.assertEqual(self.fa.build(dict()), b'\x00')

#     def test_build_unknown_flag_given(self):
#         self.assertRaises(MappingError, self.fa.build, dict(unknown=True, feature=True))

