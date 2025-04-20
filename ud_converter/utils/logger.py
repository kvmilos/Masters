"""
Logging configuration for the UD Converter.

This module provides logging configuration for the entire project.
"""
import logging
import os
from datetime import datetime


class ModuleFormatter(logging.Formatter):
    """
    Custom formatter to include module name in log records.
    """
    def format(self, record):
        name = record.name
        # strip top-level package prefix
        if name.startswith('ud_converter.'):
            name = name[len('ud_converter.'):]
        # pad each level to 12 chars
        parts = name.split('.')
        padded = [part.ljust(12) for part in parts]
        name = '.'.join(padded)
        record.name = name
        return super().format(record)


def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging configuration for the project.

    :param log_level: The logging level to use for the console (default: logging.INFO)

    :return: The configured logger for the ud_converter module
    """
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
    debug_log_file = os.path.join(log_dir, f'UD_{timestamp}-DEBUG.log')
    info_log_file = os.path.join(log_dir, f'UD_{timestamp}-INFO.log')

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    debug_file_handler = logging.FileHandler(debug_log_file, encoding='utf-8')
    debug_file_handler.setLevel(logging.DEBUG)
    # use ModuleFormatter to pad each module level to 12 chars, then width 40
    debug_file_handler.setFormatter(ModuleFormatter('%(name)-40s - %(levelname)-8s - %(message)s'))

    info_file_handler = logging.FileHandler(info_log_file, encoding='utf-8')
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(ModuleFormatter('%(name)-40s - %(levelname)-8s - %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(ModuleFormatter('%(name)-40s - %(levelname)-8s - %(message)s'))

    root_logger.addHandler(debug_file_handler)
    root_logger.addHandler(info_file_handler)
    root_logger.addHandler(console_handler)

    caller_logger = logging.getLogger('ud_converter')
    caller_logger.info('Logging system initialized with INFO to console and file, DEBUG to debug file')

    return caller_logger

logging.getLogger().propagate = False


class ChangeCollector:
    """
    Collects all change events for tokens during dependency conversion.
    """
    events = []

    @classmethod
    def clear(cls):
        """
        Clears the list of events.
        """
        cls.events = []

    @classmethod
    def record(cls, sentence_id, token_id, message):
        """
        Records a change event for a token.
        """
        cls.events.append((sentence_id, token_id, message))

    @classmethod
    def get_events(cls):
        """
        Returns the list of recorded events.
        """
        return cls.events


class LoggingDict(dict):
    """
    A dict subclass that logs every set operation as a change event.
    """
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    def __setitem__(self, key, value):
        old = self.get(key)
        super().__setitem__(key, value)
        if old != value:
            sid = self.get('sent_id')
            tid = self.get('id')
            if old not in [None, '', '_']:
                ChangeCollector.record(sid, tid, f"{key} changed from {old} to {value}")
            else:
                ChangeCollector.record(sid, tid, f"{key} set to {value}")

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
