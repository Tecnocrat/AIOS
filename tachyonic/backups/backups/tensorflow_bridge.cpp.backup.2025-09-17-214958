"""
TensorFlow Cellular Bridge - pybind11 C++ ↔ Python Bridge

Provides seamless communication between Python AI Training Cells
and C++ TensorFlow Performance Cells in the AIOS cellular ecosystem.
"""

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>
#include <map>
#include <string>
#include <memory>
#include <chrono>

// Include TensorFlow Performance Cell
#include "../languages/cpp/core/include/tensorflow_performance_cell.hpp"

namespace py = pybind11;
using namespace aios::tensorflow;

/**
 * @brief Bridge class for intercellular communication
 * 
 * Provides Python interface to C++ TensorFlow Performance Cell
 * with efficient tensor data transfer and performance monitoring.
 */
class TensorFlowCellularBridge {
public:
    TensorFlowCellularBridge() : performance_cell_(std::make_unique<TensorFlowPerformanceCell>()) {
        // Initialize the C++ performance cell
        performance_cell_->initialize();
    }

    ~TensorFlowCellularBridge() = default;

    /**
     * @brief Load model from Python training cell export
     */
    bool loadModelFromPythonExport(const std::string& export_path, 
                                   const std::vector<std::string>& tags = {"serve"}) {
        return performance_cell_->loadModel(export_path, tags);
    }

    /**
     * @brief Perform high-performance inference with numpy arrays
     */
    py::dict performInference(py::array_t<float> input_array) {
        auto result = py::dict();
        
        try {
            // Convert numpy array to C++ tensor
            auto buf = input_array.request();
            
            Tensor input_tensor;
            input_tensor.data.assign(
                static_cast<float*>(buf.ptr),
                static_cast<float*>(buf.ptr) + buf.size
            );
            
            // Convert numpy shape to C++ shape
            for (auto dim : buf.shape) {
                input_tensor.shape.push_back(static_cast<int64_t>(dim));
            }
            input_tensor.dtype = "float32";

            // Perform inference
            auto inference_result = performance_cell_->inference({input_tensor});
            
            // Convert results back to Python
            result["success"] = inference_result.success;
            result["inference_time_microseconds"] = inference_result.inferenceTime.count();
            
            if (inference_result.success && !inference_result.outputs.empty()) {
                auto& output_tensor = inference_result.outputs[0];
                
                // Convert C++ tensor back to numpy array
                std::vector<ssize_t> output_shape;
                for (auto dim : output_tensor.shape) {
                    output_shape.push_back(static_cast<ssize_t>(dim));
                }
                
                result["output"] = py::array_t<float>(
                    output_shape,
                    output_tensor.data.data()
                );
            } else {
                result["error"] = inference_result.error;
            }
            
        } catch (const std::exception& e) {
            result["success"] = false;
            result["error"] = e.what();
        }
        
        return result;
    }

    /**
     * @brief Get performance metrics from C++ cell
     */
    py::dict getPerformanceMetrics() {
        auto metrics = performance_cell_->getMetrics();
        auto result = py::dict();
        
        result["total_inferences"] = metrics.totalInferences;
        result["successful_inferences"] = metrics.successfulInferences;
        result["success_rate"] = metrics.successRate;
        result["average_inference_time_microseconds"] = metrics.averageInferenceTime.count();
        result["min_inference_time_microseconds"] = metrics.minInferenceTime.count();
        result["max_inference_time_microseconds"] = metrics.maxInferenceTime.count();
        
        return result;
    }

    /**
     * @brief Warmup the C++ inference engine
     */
    void warmupInferenceEngine(int iterations = 10) {
        performance_cell_->warmup(iterations);
    }

    /**
     * @brief Check if model is loaded
     */
    bool isModelLoaded() const {
        return performance_cell_->isModelLoaded();
    }

    /**
     * @brief Get model information
     */
    py::dict getModelInfo() {
        auto info = performance_cell_->getModelInfo();
        auto result = py::dict();
        
        for (const auto& [key, value] : info) {
            result[key.c_str()] = value;
        }
        
        return result;
    }

    /**
     * @brief Reset performance metrics
     */
    void resetMetrics() {
        performance_cell_->resetMetrics();
    }

    /**
     * @brief Benchmark inference performance
     */
    py::dict benchmarkPerformance(py::array_t<float> input_array, int iterations = 100) {
        auto result = py::dict();
        
        try {
            std::vector<std::chrono::microseconds> times;
            times.reserve(iterations);
            
            // Reset metrics before benchmark
            resetMetrics();
            
            // Run benchmark
            for (int i = 0; i < iterations; ++i) {
                auto start = std::chrono::high_resolution_clock::now();
                auto inference_result = performInference(input_array);
                auto end = std::chrono::high_resolution_clock::now();
                
                auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
                times.push_back(duration);
                
                if (!inference_result["success"].cast<bool>()) {
                    result["error"] = "Inference failed during benchmark";
                    return result;
                }
            }
            
            // Calculate statistics
            auto total_time = std::accumulate(times.begin(), times.end(), std::chrono::microseconds(0));
            auto avg_time = total_time / iterations;
            auto min_time = *std::min_element(times.begin(), times.end());
            auto max_time = *std::max_element(times.begin(), times.end());
            
            // Calculate throughput (inferences per second)
            double throughput = 1000000.0 / avg_time.count(); // Convert microseconds to seconds
            
            result["iterations"] = iterations;
            result["average_time_microseconds"] = avg_time.count();
            result["min_time_microseconds"] = min_time.count();
            result["max_time_microseconds"] = max_time.count();
            result["throughput_inferences_per_second"] = throughput;
            result["sub_millisecond_achievement"] = (avg_time.count() < 1000); // < 1ms
            result["target_achieved"] = (avg_time.count() < 1000); // Target: < 1ms
            
        } catch (const std::exception& e) {
            result["error"] = e.what();
        }
        
        return result;
    }

private:
    std::unique_ptr<TensorFlowPerformanceCell> performance_cell_;
};


// pybind11 module definition
PYBIND11_MODULE(tensorflow_cellular_bridge, m) {
    m.doc() = "TensorFlow Cellular Bridge for AIOS - C++ ↔ Python intercellular communication";

    // Bind the main bridge class
    py::class_<TensorFlowCellularBridge>(m, "TensorFlowCellularBridge")
        .def(py::init<>())
        .def("load_model_from_python_export", &TensorFlowCellularBridge::loadModelFromPythonExport,
             "Load model exported from Python training cell",
             py::arg("export_path"), py::arg("tags") = std::vector<std::string>{"serve"})
        .def("perform_inference", &TensorFlowCellularBridge::performInference,
             "Perform high-performance inference with numpy array input")
        .def("get_performance_metrics", &TensorFlowCellularBridge::getPerformanceMetrics,
             "Get performance metrics from C++ inference cell")
        .def("warmup_inference_engine", &TensorFlowCellularBridge::warmupInferenceEngine,
             "Warmup the C++ inference engine", py::arg("iterations") = 10)
        .def("is_model_loaded", &TensorFlowCellularBridge::isModelLoaded,
             "Check if model is loaded and ready")
        .def("get_model_info", &TensorFlowCellularBridge::getModelInfo,
             "Get loaded model information")
        .def("reset_metrics", &TensorFlowCellularBridge::resetMetrics,
             "Reset performance metrics")
        .def("benchmark_performance", &TensorFlowCellularBridge::benchmarkPerformance,
             "Benchmark inference performance", 
             py::arg("input_array"), py::arg("iterations") = 100);

    // Module-level functions
    m.def("create_bridge", []() {
        return std::make_unique<TensorFlowCellularBridge>();
    }, "Create a new TensorFlow Cellular Bridge instance");

    m.def("get_version", []() {
        return "0.4.0";
    }, "Get TensorFlow Cellular Bridge version");

    m.def("check_cpp_performance_cell", []() {
        try {
            auto cell = std::make_unique<TensorFlowPerformanceCell>();
            return cell->initialize();
        } catch (...) {
            return false;
        }
    }, "Check if C++ TensorFlow Performance Cell is available");
}