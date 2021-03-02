# django imports
from django.test import TestCase, RequestFactory

class DebugLoggerTest(TestCase):
	def test_call_view_load(self):
		response = self.client.get('/api/v0/loggers/debug')
		self.assertEqual(response.status_code, 200)

class InfoLoggerTest(TestCase):
	def test_call_view_load(self):
		response = self.client.get('/api/v0/loggers/info')
		self.assertEqual(response.status_code, 200)

class WarningLoggerTest(TestCase):
	def test_call_view_load(self):
		response = self.client.get('/api/v0/loggers/warning')
		self.assertEqual(response.status_code, 200)

class ErrorLoggerTest(TestCase):
	def test_call_view_load(self):
		response = self.client.get('/api/v0/loggers/error')
		self.assertEqual(response.status_code, 200)

class FatalLoggerTest(TestCase):
	def test_call_view_load(self):
		response = self.client.get('/api/v0/loggers/fatal')
		self.assertEqual(response.status_code, 200)