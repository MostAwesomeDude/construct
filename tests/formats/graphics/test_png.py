import unittest, os
ontravis = 'TRAVIS' in os.environ

from construct.lib.container import Container
from construct.formats.graphics.png import png_file


# @unittest.skip("removing OnDemand")
# class TestPngFormat(unittest.TestCase):

#     def test_parse(self):
#         filename = 'sample.png' if ontravis else 'tests/sample.png'
#         with open(filename,'rb') as f:
#             data = f.read()
#         sample = png_file.parse(data)
