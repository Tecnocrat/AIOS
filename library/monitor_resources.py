import time
import psutil
import sqlite3
import threading
from datetime import datetime
from typing import List
from library.autologger import AutoLogger

# Initialize logger
autologger = AutoLogger()
logger = autologger.get_logger("monitor_resources")

# Define the stop_event globally
stop_event = threading.Event()

def initialize_database(db_path: str = "C:\\dev\\OS\\storage\\resource_monitor.db") -> sqlite3.Connection:
    """
    Initializes the SQLite database and creates the resource monitoring table if it doesn't exist.
    :param db_path: Path to the SQLite database file.
    :return: Connection to the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the resource monitoring table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resource_monitor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu_global REAL NOT NULL,
            cpu_per_core TEXT NOT NULL,
            memory_usage REAL NOT NULL,
            disk_usage REAL NOT NULL,
            process_uptime REAL NOT NULL
        )
    """)
    conn.commit()
    return conn

def monitor_resources(interval=5, cpu_threshold=90, memory_threshold=90, disk_threshold=90):
    """
    Monitors system resources (CPU, memory, and disk usage) and logs high-priority alerts.
    """
    logger.info("Starting resource monitoring...")
    try:
        while not stop_event.is_set():
            # Get overall CPU usage percentage
            cpu_global: float = psutil.cpu_percent(interval=1)  # Returns a float
            if cpu_global > cpu_threshold:
                logger.warning(f"High CPU Usage Alert: {cpu_global}% (Threshold: {cpu_threshold}%)")

            # Get per-CPU usage percentages
            cpu_usages: list[float] = psutil.cpu_percent(interval=1, percpu=True)  # Returns a list of floats
            for i, usage in enumerate(cpu_usages):
                if usage > cpu_threshold:
                    logger.warning(f"High CPU Usage Alert on CPU {i}: {usage}% (Threshold: {cpu_threshold}%)")

            memory: float = psutil.virtual_memory().percent
            disk: float = psutil.disk_usage('/').percent

            # Log health check
            logger.info(f"Health Check - CPU: {cpu_global}%, Memory: {memory}%, Disk: {disk}%")
            if memory > memory_threshold:
                logger.warning(f"High Memory Usage Alert: {memory}% (Threshold: {memory_threshold}%)")
            if disk > disk_threshold:
                logger.warning(f"High Disk Usage Alert: {disk}% (Threshold: {disk_threshold}%)")

            time.sleep(interval)
    except Exception as e:
        logger.error(f"Error during resource monitoring: {e}")