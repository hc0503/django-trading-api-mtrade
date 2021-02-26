# import django
import logging
import ujson
import json_log_formatter

class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    json_lib = ujson

    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra['msg'] = message

        # Include builtins
        extra['level'] = record.levelname
        extra['time'] = record.time

        return extra