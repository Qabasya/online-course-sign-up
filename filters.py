import logging

class ErrorOnlyFilter(logging.Filter):
    """Пропускает только ERROR"""
    def filter(self, record):
        return record.levelname == 'ERROR'

class WarningOnlyFilter(logging.Filter):
    """Пропускает только WARNING"""
    def filter(self, record):
        return record.levelname == 'WARNING'

class CriticalOnlyFilter(logging.Filter):
    """Пропускает только CRITICAL"""
    def filter(self, record):
        return record.levelname == 'CRITICAL'

class InfoOnlyFilter(logging.Filter):
    """Пропускает только INFO"""
    def filter(self, record):
        return record.levelname == 'INFO'