# import django
import logging
import ujson
import json_log_formatter
import datetime

class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    json_lib = ujson

    def json_record(self, message, extra, record):
        extra['msg'] = message
        extra['level'] = record.__dict__['levelname']
        extra['module'] = record.__dict__['pathname']
        extra['time'] = datetime.datetime.now()
        
        request = extra.pop('request', None)
        if request:
            extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        
        return extra