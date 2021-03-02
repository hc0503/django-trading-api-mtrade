# django imports
from django.test import TestCase, RequestFactory
import logging

logging.addLevelName(logging.CRITICAL, 'FATAL')

class DebugLoggerTest(TestCase):
	def test_logging(self):
		with self.assertLogs('foo', level='DEBUG') as cm:
			logging.getLogger('foo').info('The info message')
			logging.getLogger('foo').error('The error message')
			logging.getLogger('foo').debug('The debug message')
			logging.getLogger('foo').warning('The warning message')
			logging.getLogger('foo').fatal('The fatal message')
		self.assertEqual(cm.output, [
			'INFO:foo:The info message',
			'ERROR:foo:The error message',
			'DEBUG:foo:The debug message',
			'WARNING:foo:The warning message',
			'FATAL:foo:The fatal message',
		])