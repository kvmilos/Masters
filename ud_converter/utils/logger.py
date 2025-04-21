"""
Logging configuration for the UD Converter.

This module provides logging configuration for the entire project.
"""
import logging
import os
from datetime import datetime
import inspect


class ModuleFormatter(logging.Formatter):
    """
    Custom formatter to include module name in log records.
    """
    def format(self, record):
        record.name = record.name.removeprefix('ud_converter.')
        return super().format(record)


class LevelFilter(logging.Filter):
    """
    Allows only records whose levelno is between low and high, inclusive.
    """
    def __init__(self, low, high=None):
        super().__init__()
        self.low = low
        self.high = high if high is not None else low

    def filter(self, record):
        return self.low <= record.levelno <= self.high


def setup_logging() -> logging.Logger:
    """
    Set up logging configuration for the project.

    :return: The configured logger for the ud_converter module
    """
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
    debug_log_file = os.path.join(log_dir, f'UD_{timestamp}-DEBUG.log')
    info_log_file = os.path.join(log_dir, f'UD_{timestamp}-WARNINGS.log')

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    debug_file_handler = logging.FileHandler(debug_log_file, encoding='utf-8')
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.addFilter(LevelFilter(logging.DEBUG, logging.WARNING))
    debug_file_handler.setFormatter(ModuleFormatter('%(name)-40s - %(levelname)-8s - %(message)s'))

    info_file_handler = logging.FileHandler(info_log_file, encoding='utf-8')
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.addFilter(LevelFilter(logging.INFO, logging.WARNING))
    info_file_handler.setFormatter(ModuleFormatter('%(name)-40s - %(levelname)-8s - %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.addFilter(LevelFilter(logging.INFO))
    console_handler.setFormatter(ModuleFormatter('%(levelname)s: %(message)s'))

    root_logger.addHandler(debug_file_handler)
    root_logger.addHandler(info_file_handler)
    root_logger.addHandler(console_handler)

    caller_logger = logging.getLogger('ud_converter')
    caller_logger.info('WARNINGs and INFO are being saved to %s', info_log_file)
    caller_logger.info('DEBUG, WARNINGs, and INFO are being saved to %s', debug_log_file)

    return caller_logger


logging.getLogger().propagate = False


class ChangeCollector:
    """
    Collects all change events for tokens during dependency conversion.
    """
    events: list[tuple[int, str, str, str, str]] = []

    @classmethod
    def clear(cls):
        """
        Clears the list of events.
        """
        cls.events = []

    @classmethod
    def record(cls, sentence_id, token_id, message, module, level='DEBUG'):
        """
        Records a change event for a token.
        :param module: dependency submodule name (e.g. 'edges.fixed') or 'conversion'
        :param level: 'DEBUG' or 'WARNING'
        """
        # Simply record the event; module should be provided by the caller
        cls.events.append((sentence_id, token_id, module, level, message))

    @classmethod
    def get_events(cls):
        """
        Returns the list of recorded events as tuples (sentence_id, token_id, module, level, message).
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
            # Only record after token has been placed in a sentence
            if not hasattr(self.token, 'sentence') or self.token.sentence is None:
                return
            sid = self.token.sentence.id
            tid = self.token.id
            msg = f"{key} changed from {old} to {value} for '{self.token.form}'" if old not in [None, '', '_'] else f"{key} set to {value} for '{self.token.form}'"

            module = 'conversion'

            for frame in inspect.stack()[1:]:
                path = frame.filename.replace('\\', '/')
                parts = path.split('ud_converter/')
                if len(parts) == 2 and parts[1].startswith('dependency/'):
                    # slice off 'dependency/' to get subpath without leading slash
                    rel = parts[1][len('dependency/'):]  # correct slicing inclusive of slash
                    rel = rel.rsplit('.', 1)[0]
                    module = rel.replace('/', '.')
                    break
            ChangeCollector.record(sid, tid, msg, module=module, level='DEBUG')

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
