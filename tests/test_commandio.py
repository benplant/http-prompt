from mock import patch, Mock
import unittest

from http_prompt.commandio import CommandIO


class TestCommandIO(unittest.TestCase):

    def setUp(self):
        super(TestCommandIO, self).setUp()
        self.patchers = [
            ('commandio_click', patch('http_prompt.printer.click')),
        ]
        for attr_name, patcher in self.patchers:
            setattr(self, attr_name, patcher.start())

        self.test_data = 'whatever'

        attrs = {
            'write.return_value': 3,
            'close.return_value': None,
            'read.return_value': self.test_data
        }
        self.dummyStream = Mock(mode=None, out=None, **attrs)

    def tearDown(self):
        super(TestCommandIO, self).tearDown()
        for _, patcher in self.patchers:
            patcher.stop()

    def test_close(self):
        output = CommandIO(self.dummyStream)
        output.close()
        self.assertTrue(self.dummyStream.close.called)

    def test_write(self):
        output = CommandIO(self.dummyStream)
        output.write(self.test_data)

        self.assertTrue(self.dummyStream.write.called)
        args = self.dummyStream.write.call_args[0][0]
        self.assertEqual(self.test_data, args)

    def test_write_append(self):
        self.dummyStream.mode = 'a'
        output = CommandIO(self.dummyStream)
        output.write(self.test_data)

        self.assertTrue(self.dummyStream.write.called)
        args = self.dummyStream.write.call_args[0][0]
        self.assertEqual('\n' + self.test_data, args)

    def test_read(self):
        output = CommandIO(self.dummyStream)
        output.read()

        self.assertTrue(self.dummyStream.read.called)

    def test_set_output_stream(self):
        stream = Mock()
        output = CommandIO(self.dummyStream)
        output.setOutputStream(stream)

        self.assertEqual(stream, output.out)
