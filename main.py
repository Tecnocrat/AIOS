import os
import threading
import time
import psutil
import sys
import signal
from library.autologger import AutoLogger
from library.utils import backup_system, analyze_file_system
from library.ai_core import AICore
from AIOS_Core import AIOSCore
from library.monitor_resources import monitor_resources
from library.filesys_manager import generate_file_structure

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize the centralized autologging system
autologger = AutoLogger()
logger = autologger.get_logger("main")  # Get a logger for the 'main' namespace

# Initialize the AI core
ai_core = AICore()
aios_core = AIOSCore()

# Create a threading event for stopping the monitoring thread
stop_event = threading.Event()

# Create a thread for resource monitoring
resource_monitor_thread = threading.Thread(
    target=monitor_resources,  # The function to run in the thread
    args=(5, 90, 90, 90),  # Pass interval and thresholds as arguments
    daemon=True  # Set as a daemon thread
)

def signal_handler(sig, frame):
    logger.info("Shutdown signal received. Stopping resource monitoring...")
    stop_event.set()  # Signal the thread to stop
    if resource_monitor_thread.is_alive():
        resource_monitor_thread.join()  # Wait for the thread to finish
    sys.exit(0)


# ------------------
# MAIN APPLICATION
# ------------------
def main():
    """
    Entry point for the AIOS system. Acts as the interface layer between AIOS_Core and the outer world.
    """
    print("Starting System Launcher...")
    logger.info("System Launcher initialized.")

    # Automatically generate the file structure JSON
    logger.info("Running file structure analysis...")
    root_directory = "C:\\dev"
    storage_directory = "C:\\dev\\OS\\storage"
    result = generate_file_structure(root_directory, storage_directory)
    if result:
        logger.info(f"File structure analysis saved to: {result}")
    else:
        logger.info("No changes detected in the file structure. Skipping save.")

    # Start the resource monitoring thread
    resource_monitor_thread.start()
    logger.info("Resource monitoring thread started.")

    while True:
        print("\nAvailable Commands:")
        print("- self_reflex: Perform self-reflection in AIOS_Core.")
        print("- status: Get the status of AIOS_Core.")
        print("- quit: Exit the application.")
        command = input("\nEnter a command: ").strip().lower()

        if command in ["self_reflex", "status"]:
            # Send the command to AIOS_Core via the interface
            result = aios_core.start_interface(command)
            print(f"Result: {result}")
        elif command == "quit":
            print("Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")


# Register the signal handler
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    main()