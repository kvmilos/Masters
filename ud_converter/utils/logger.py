"""
Logging configuration for the UD Converter.

This module provides logging configuration for the entire project.
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration for the project.
    
    :param log_level: The logging level to use for the console (default: logging.INFO)
        
    :return: The configured logger for the ud_converter module
    """
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    debug_log_file = os.path.join(log_dir, f'ud_converter_debug_{timestamp}.log')
    info_log_file = os.path.join(log_dir, f'ud_converter_info_{timestamp}.log')

    root_logger = logging.getLogger('ud_converter')
    root_logger.setLevel(logging.DEBUG)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    debug_file_handler = logging.FileHandler(debug_log_file, encoding='utf-8')
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)-60s - %(levelname)-8s - %(message)s'))

    info_file_handler = logging.FileHandler(info_log_file, encoding='utf-8')
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)-40s - %(levelname)-8s - %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)-40s - %(levelname)-8s - %(message)s'))

    root_logger.addHandler(debug_file_handler)
    root_logger.addHandler(info_file_handler)
    root_logger.addHandler(console_handler)

    caller_logger = logging.getLogger('ud_converter')
    caller_logger.info('Logging system initialized with INFO to console and file, DEBUG to debug file')

    return caller_logger

logging.getLogger('ud_converter').propagate = True
