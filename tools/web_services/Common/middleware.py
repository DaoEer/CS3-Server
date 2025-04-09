# -*- coding: utf-8 -*-
import sys
from django import http
from django.core import exceptions
import traceback

import logging
logger = logging.getLogger("default")

class TracbackMiddleware(object):
	""" This middleware will catch exceptions and creates a ticket in an existing
	Trac environment.
	"""

	IGNORE_EXCEPTIONS = (http.Http404, SystemExit, exceptions.PermissionDenied)

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_exception(self, request, exception):
		if isinstance(exception, self.IGNORE_EXCEPTIONS) or \
				exception in self.IGNORE_EXCEPTIONS:
			return

		request_full_path = request.get_full_path().encode("utf8")
		exec_info = self._get_traceback(sys.exc_info())
		message = "{{{\n%s\n\nrequest full path: %s\n}}}" % (exec_info, request_full_path)
		logger.critical( message )
		return

	def _get_traceback(self, exc_info=None):
		"Helper function to return the traceback as a string"
		return '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))

