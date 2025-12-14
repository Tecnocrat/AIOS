"""
DebugManager for runtime inspection in AIOS with Fractal Cache Integration
Enhanced for Task 1.2 - Performance Optimization and Deep Metadata Logging
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class DebugManager:
    def __init__(self, deep_log_dir: str = "runtime/logs"):
        self.requests = []
        self.handlers = []
        self.errors = []
        self.performance_data = []
        self.deep_log_dir = Path(deep_log_dir)
        self.deep_log_dir.mkdir(parents=True, exist_ok=True)
        self.session_metadata = {
            "session_start": datetime.now().isoformat(),
            "total_requests": 0,
            "total_errors": 0,
<<<<<<< HEAD
            "performance_samples": 0,
        }

    def log_request(
        self, endpoint: str, data: Any, response_time: Optional[float] = None
    ):
=======
            "performance_samples": 0
        }

    def log_request(self, endpoint: str, data: Any,
                    response_time: Optional[float] = None):
>>>>>>> origin/OS0.6.2.grok
        """Enhanced request logging with performance tracking"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "data": data,
            "response_time": response_time,
<<<<<<< HEAD
            "session_id": self.session_metadata["session_start"],
=======
            "session_id": self.session_metadata["session_start"]
>>>>>>> origin/OS0.6.2.grok
        }

        self.requests.append(log_entry)
        self.session_metadata["total_requests"] += 1

        if len(self.requests) > 50:  # Increased buffer for better analysis
            self.requests.pop(0)

        # Log to deep metadata for AINLP analysis
        self._log_deep_metadata("request", log_entry)

<<<<<<< HEAD
    def log_handler(
        self,
        handler_name: str,
        message: str,
        processing_time: Optional[float] = None,
        confidence: Optional[float] = None,
    ):
=======
    def log_handler(self, handler_name: str, message: str,
                    processing_time: Optional[float] = None,
                    confidence: Optional[float] = None):
>>>>>>> origin/OS0.6.2.grok
        """Enhanced handler logging with AINLP performance metrics"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "handler": handler_name,
            "message": message,
            "processing_time": processing_time,
            "confidence": confidence,
<<<<<<< HEAD
            "session_id": self.session_metadata["session_start"],
=======
            "session_id": self.session_metadata["session_start"]
>>>>>>> origin/OS0.6.2.grok
        }

        self.handlers.append(log_entry)
        if len(self.handlers) > 50:
            self.handlers.pop(0)

        # Log to deep metadata
        self._log_deep_metadata("handler", log_entry)

<<<<<<< HEAD
    def log_error(
        self,
        error: Any,
        context: Optional[Dict[str, Any]] = None,
        severity: str = "error",
    ):
=======
    def log_error(self, error: Any,
                  context: Optional[Dict[str, Any]] = None,
                  severity: str = "error"):
>>>>>>> origin/OS0.6.2.grok
        """Enhanced error logging with contextual metadata"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "error": str(error),
            "context": context or {},
            "severity": severity,
<<<<<<< HEAD
            "session_id": self.session_metadata["session_start"],
=======
            "session_id": self.session_metadata["session_start"]
>>>>>>> origin/OS0.6.2.grok
        }

        self.errors.append(log_entry)
        self.session_metadata["total_errors"] += 1

        if len(self.errors) > 50:
            self.errors.pop(0)

        # Log to deep metadata
        self._log_deep_metadata("error", log_entry)

    def log_performance(self, operation: str, metrics: Dict[str, Any]):
        """Log performance metrics for fractal analysis"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "metrics": metrics,
<<<<<<< HEAD
            "session_id": self.session_metadata["session_start"],
=======
            "session_id": self.session_metadata["session_start"]
>>>>>>> origin/OS0.6.2.grok
        }

        self.performance_data.append(log_entry)
        self.session_metadata["performance_samples"] += 1

        if len(self.performance_data) > 100:
            self.performance_data.pop(0)

        # Log to deep metadata
        self._log_deep_metadata("performance", log_entry)

    def get_debug_info(self) -> Dict[str, Any]:
        """Enhanced debug info with fractal analysis"""
        return {
            "requests": self.requests,
            "handlers": self.handlers,
            "errors": self.errors,
            "performance_data": self.performance_data,
            "session_metadata": self.session_metadata,
<<<<<<< HEAD
            "fractal_analysis": self._generate_fractal_analysis(),
=======
            "fractal_analysis": self._generate_fractal_analysis()
>>>>>>> origin/OS0.6.2.grok
        }

    def _generate_fractal_analysis(self) -> Dict[str, Any]:
        """Generate fractal analysis for AINLP optimization"""
        total_requests = len(self.requests)
        total_errors = len(self.errors)
        error_rate = total_errors / total_requests if total_requests > 0 else 0

        # Calculate average response times
<<<<<<< HEAD
        response_times = [
            r.get("response_time", 0) for r in self.requests if r.get("response_time")
        ]
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )
=======
        response_times = [r.get("response_time", 0) for r in self.requests
                          if r.get("response_time")]
        avg_response_time = (sum(response_times) / len(response_times)
                             if response_times else 0)
>>>>>>> origin/OS0.6.2.grok

        return {
            "error_rate": error_rate,
            "avg_response_time": avg_response_time,
            "request_pattern": self._analyze_request_patterns(),
            "handler_efficiency": self._analyze_handler_efficiency(),
<<<<<<< HEAD
            "optimization_suggestions": self._generate_optimization_suggestions(),
=======
            "optimization_suggestions":
                self._generate_optimization_suggestions()
>>>>>>> origin/OS0.6.2.grok
        }

    def _analyze_request_patterns(self) -> Dict[str, Any]:
        """Analyze request patterns for optimization insights"""
        endpoint_counts = {}
        for request in self.requests:
            endpoint = request.get("endpoint", "unknown")
            endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + 1

<<<<<<< HEAD
        most_used = (
            max(endpoint_counts.items(), key=lambda x: x[1])
            if endpoint_counts
            else None
        )
        return {"endpoint_frequency": endpoint_counts, "most_used_endpoint": most_used}
=======
        most_used = (max(endpoint_counts.items(), key=lambda x: x[1])
                     if endpoint_counts else None)
        return {
            "endpoint_frequency": endpoint_counts,
            "most_used_endpoint": most_used
        }
>>>>>>> origin/OS0.6.2.grok

    def _analyze_handler_efficiency(self) -> Dict[str, Any]:
        """Analyze handler performance for AINLP optimization"""
        handler_performance = {}
        for handler_log in self.handlers:
            handler_name = handler_log.get("handler", "unknown")
            processing_time = handler_log.get("processing_time", 0) or 0

            if handler_name not in handler_performance:
                handler_performance[handler_name] = {
                    "total_calls": 0,
                    "total_time": 0,
<<<<<<< HEAD
                    "avg_time": 0,
=======
                    "avg_time": 0
>>>>>>> origin/OS0.6.2.grok
                }

            handler_performance[handler_name]["total_calls"] += 1
            handler_performance[handler_name]["total_time"] += processing_time
            handler_performance[handler_name]["avg_time"] = (
<<<<<<< HEAD
                handler_performance[handler_name]["total_time"]
                / handler_performance[handler_name]["total_calls"]
=======
                handler_performance[handler_name]["total_time"] /
                handler_performance[handler_name]["total_calls"]
>>>>>>> origin/OS0.6.2.grok
            )

        return handler_performance

    def _generate_optimization_suggestions(self) -> List[str]:
        """Generate AINLP-driven optimization suggestions"""
        suggestions = []

        # Analyze error rate
<<<<<<< HEAD
        error_rate = len(self.errors) / len(self.requests) if self.requests else 0
        if error_rate > 0.1:
            suggestions.append("High error rate detected - implement error recovery")

        # Analyze response times
        response_times = [
            r.get("response_time", 0) for r in self.requests if r.get("response_time")
        ]
=======
        error_rate = len(self.errors) / \
            len(self.requests) if self.requests else 0
        if error_rate > 0.1:
            suggestions.append(
                "High error rate detected - implement error recovery")

        # Analyze response times
        response_times = [r.get("response_time", 0) for r in self.requests
                          if r.get("response_time")]
>>>>>>> origin/OS0.6.2.grok
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            if avg_time > 100:  # >100ms
                suggestions.append("Slow response times - implement caching")

        # Analyze handler performance
        handler_perf = self._analyze_handler_efficiency()
        for handler, perf in handler_perf.items():
            if perf["avg_time"] > 50:  # >50ms
                suggestions.append(f"Optimize {handler} handler performance")

        return suggestions

    def _log_deep_metadata(self, log_type: str, data: Dict[str, Any]):
        """Log deep metadata to runtime/logs for AINLP analysis"""
        try:
<<<<<<< HEAD
            log_file = (
                self.deep_log_dir
                / f"debug_metadata_{datetime.now().strftime('%Y%m%d')}.json"
            )
=======
            log_file = self.deep_log_dir / \
                f"debug_metadata_{datetime.now().strftime('%Y%m%d')}.json"
>>>>>>> origin/OS0.6.2.grok

            metadata_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": log_type,
                "data": data,
                "fractal_context": {
                    "session_id": self.session_metadata["session_start"],
                    "total_requests": self.session_metadata["total_requests"],
                    "total_errors": self.session_metadata["total_errors"],
<<<<<<< HEAD
                    "dendrite_level": "debug_neuron_active",
                },
=======
                    "dendrite_level": "debug_neuron_active"
                }
>>>>>>> origin/OS0.6.2.grok
            }

            # Append to daily log file
            if log_file.exists():
<<<<<<< HEAD
                with open(log_file, "r") as f:
=======
                with open(log_file, 'r') as f:
>>>>>>> origin/OS0.6.2.grok
                    existing_logs = json.load(f)
            else:
                existing_logs = []

            existing_logs.append(metadata_entry)

            # Keep only last 5000 entries per day to prevent unbounded growth
            if len(existing_logs) > 5000:
                existing_logs = existing_logs[-5000:]

<<<<<<< HEAD
            with open(log_file, "w") as f:
=======
            with open(log_file, 'w') as f:
>>>>>>> origin/OS0.6.2.grok
                json.dump(existing_logs, f, indent=2)

        except Exception as e:
            # Fallback: still capture error in memory for later analysis
            print(f"Deep metadata logging failed: {e}")


_debug_manager = DebugManager()
