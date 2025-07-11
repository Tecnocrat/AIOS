import argparse
import logging
import os
import sys

# Add current directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import AIOS OpenCV Vision Module
from opencv_vision_module import OpenCVVisionService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

# Global service registry
_service_registry = {}

def initialize_services():
    """Initialize all AIOS services."""
    global _service_registry
    
    logging.info("Initializing AIOS services...")
    
    # Initialize OpenCV Vision Service
    try:
        opencv_service = OpenCVVisionService()
        if opencv_service.initialize():
            _service_registry['opencv_vision'] = opencv_service
            logging.info("✅ OpenCV Vision Service initialized")
        else:
            logging.error("❌ Failed to initialize OpenCV Vision Service")
    except Exception as e:
        logging.error(f"❌ Error initializing OpenCV Vision Service: {e}")
    
    logging.info(f"Services initialized: {list(_service_registry.keys())}")

def list_services():
    """List available services."""
    if not _service_registry:
        initialize_services()
    
    services = list(_service_registry.keys())
    logging.info("Available services: %s", services)
    return services

def get_service(service_name):
    """Get a service by name."""
    if not _service_registry:
        initialize_services()
    
    return _service_registry.get(service_name)

def invoke_service(service_name, action, params):
    """Invoke a service with the given action and parameters."""
    logging.info("Invoking service: %s", service_name)
    logging.info("Action: %s", action)
    logging.info("Parameters: %s", params)
    
    # Get the service
    service = get_service(service_name)
    if not service:
        error_msg = f"Service '{service_name}' not found. Available services: {list(_service_registry.keys())}"
        logging.error(error_msg)
        return {"error": error_msg}
    
    # Prepare request for service
    request = {
        'action': action,
        **params  # Merge parameters into request
    }
    
    try:
        # Process request through service
        result = service.process_request(request)
        logging.info("Service result: %s", result.get('success', False))
        return result
    except Exception as e:
        error_msg = f"Error invoking service {service_name}: {e}"
        logging.error(error_msg)
        return {"error": error_msg}

def shutdown_services():
    """Shutdown all services."""
    global _service_registry
    
    logging.info("Shutting down AIOS services...")
    for service_name, service in _service_registry.items():
        try:
            service.shutdown()
            logging.info(f"✅ {service_name} service shut down")
        except Exception as e:
            logging.error(f"❌ Error shutting down {service_name}: {e}")
    
    _service_registry.clear()
    logging.info("All services shut down")

def main():
    """Main entry point for glue logic."""
    parser = argparse.ArgumentParser(description="AI OS Glue Logic with OpenCV Vision")
    parser.add_argument("--list-services", action="store_true", help="List available services")
    parser.add_argument("--invoke-service", type=str, help="Service name to invoke")
    parser.add_argument("--action", type=str, help="Action to perform")
    parser.add_argument("--params", type=str, help="Parameters for the action (key=value pairs)")
    parser.add_argument("--image-path", type=str, help="Path to image for vision processing")
    parser.add_argument("--analysis-type", type=str, default="comprehensive", 
                       choices=["basic", "comprehensive", "consciousness_emergence"],
                       help="Type of vision analysis")

    args = parser.parse_args()

    try:
        if args.list_services:
            services = list_services()
            print(f"Available services: {services}")
        elif args.invoke_service:
            params = {}
            if args.params:
                # Parse key=value pairs into a dictionary
                params = dict(pair.split("=") for pair in args.params.split(","))
            
            # Add image processing parameters if provided
            if args.image_path:
                params['image_path'] = args.image_path
            if args.analysis_type:
                params['analysis_type'] = args.analysis_type
            
            result = invoke_service(args.invoke_service, args.action or "process_image", params)
            print(f"Service result: {result}")
        else:
            logging.info("No valid arguments provided. Use --help for usage information.")
            
            # Show example usage
            print("\n🎯 AIOS OpenCV Vision Integration Examples:")
            print("  List services:")
            print("    python main.py --list-services")
            print("  Process image:")
            print("    python main.py --invoke-service opencv_vision --action process_image --image-path /path/to/image.png")
            print("  Get consciousness state:")
            print("    python main.py --invoke-service opencv_vision --action get_consciousness_state")
    
    finally:
        # Always shutdown services on exit
        shutdown_services()

if __name__ == "__main__":
    main()