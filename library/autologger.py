import logging
import os
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler

class AutoLogger:
    def __init__(self, log_dir="C:\\dev\\logs", max_log_size=5 * 1024 * 1024, backup_count=5):
        """
        Initializes the centralized autologging system.
        :param log_dir: Directory where logs will be stored.
        :param max_log_size: Maximum size of a log file in bytes before rotation.
        :param backup_count: Number of backup log files to keep.
        """
        self.log_dir = log_dir
        self.max_log_size = max_log_size
        self.backup_count = backup_count

        # Ensure the log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Dictionary to store loggers by namespace
        self.loggers = {}

    def get_logger(self, namespace="default"):
        """
        Returns a logger for the given namespace.
        :param namespace: The namespace for the logger (e.g., 'main', 'utils').
        :return: A logger instance.
        """
        if namespace not in self.loggers:
            # Create a new logger for the namespace
            logger = logging.getLogger(namespace)
            logger.setLevel(logging.INFO)

            # Create a rotating file handler
            log_file = os.path.join(self.log_dir, f"{namespace}.log")
            handler = RotatingFileHandler(log_file, maxBytes=self.max_log_size, backupCount=self.backup_count)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)

            # Add the handler to the logger
            logger.addHandler(handler)

            # Store the logger
            self.loggers[namespace] = logger

        return self.loggers[namespace]

class AutoLogDebugger:
    def __init__(self, log_dir="C:\\dev\\logs", log_file="system.log", max_log_size=5 * 1024 * 1024):
        """
        Initializes the autolog and debugger system.
        :param log_dir: Directory where logs will be stored.
        :param log_file: Name of the log file.
        :param max_log_size: Maximum size of the log file in bytes before rotation.
        """
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        self.max_log_size = max_log_size

        # Ensure the log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Configure logging
        self.logger = logging.getLogger("AutoLogDebugger")
        self.logger.setLevel(logging.INFO)
        log_handler = logging.FileHandler(self.log_file, mode="a")
        log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        log_handler.setFormatter(log_formatter)
        self.logger.addHandler(log_handler)

    def log_info(self, message):
        """Logs an informational message."""
        self._rotate_logs_if_needed()
        self.logger.info(message)

    def log_warning(self, message):
        """Logs a warning message."""
        self._rotate_logs_if_needed()
        self.logger.warning(message)

    def log_error(self, message):
        """Logs an error message."""
        self._rotate_logs_if_needed()
        self.logger.error(message)

    def log_exception(self, exception):
        """Logs an exception with a stack trace."""
        self._rotate_logs_if_needed()
        self.logger.error("Exception occurred: %s", traceback.format_exc())

    def debug_variable(self, var_name, var_value):
        """Logs the value of a variable for debugging purposes."""
        self._rotate_logs_if_needed()
        self.logger.debug(f"DEBUG: {var_name} = {var_value}")

    def _rotate_logs_if_needed(self):
        """Rotates the log file if it exceeds the maximum size."""
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_log_size:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            rotated_file = f"{self.log_file}.{timestamp}.bak"
            os.rename(self.log_file, rotated_file)
            self.logger.info(f"Log file rotated: {rotated_file}")

    def health_check(self, cpu_usage, memory_usage, disk_usage, cpu_threshold=90, memory_threshold=90, disk_threshold=90):
        """
        Logs health check information and alerts if thresholds are exceeded.
        """
        self.log_info(f"Health Check - CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%")
        if cpu_usage > cpu_threshold:
            self.log_warning(f"High CPU Usage Alert: {cpu_usage}% (Threshold: {cpu_threshold}%)")
        if memory_usage > memory_threshold:
            self.log_warning(f"High Memory Usage Alert: {memory_usage}% (Threshold: {memory_threshold}%)")
        if disk_usage > disk_threshold:
            self.log_warning(f"High Disk Usage Alert: {disk_usage}% (Threshold: {disk_threshold}%)")