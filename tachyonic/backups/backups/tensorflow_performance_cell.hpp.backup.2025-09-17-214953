#ifndef TENSORFLOW_PERFORMANCE_CELL_HPP
#define TENSORFLOW_PERFORMANCE_CELL_HPP

#include <memory>
#include <string>
#include <vector>
#include <map>
#include <chrono>

namespace aios {
namespace tensorflow {

    /**
     * @brief Tensor data structure for high-performance inference
     */
    struct Tensor {
        std::vector<float> data;
        std::vector<int64_t> shape;
        std::string dtype;
        
        Tensor() = default;
        Tensor(const std::vector<float>& d, const std::vector<int64_t>& s, const std::string& dt = "float32")
            : data(d), shape(s), dtype(dt) {}
    };

    /**
     * @brief Inference result with performance metrics
     */
    struct InferenceResult {
        std::vector<Tensor> outputs;
        std::chrono::microseconds inferenceTime;
        bool success;
        std::string error;
        
        InferenceResult() : inferenceTime(0), success(false) {}
    };

    /**
     * @brief Performance metrics for monitoring
     */
    struct PerformanceMetrics {
        std::chrono::microseconds averageInferenceTime;
        std::chrono::microseconds minInferenceTime;
        std::chrono::microseconds maxInferenceTime;
        uint64_t totalInferences;
        uint64_t successfulInferences;
        double successRate;
        
        PerformanceMetrics() : averageInferenceTime(0), minInferenceTime(0), 
                              maxInferenceTime(0), totalInferences(0), 
                              successfulInferences(0), successRate(0.0) {}
    };

    /**
     * @brief TensorFlow C++ Performance Cell for sub-millisecond inference
     * 
     * This class provides high-performance TensorFlow model inference
     * optimized for production deployment with minimal latency.
     */
    class TensorFlowPerformanceCell {
    public:
        /**
         * @brief Construct a new TensorFlow Performance Cell
         */
        TensorFlowPerformanceCell();

        /**
         * @brief Destroy the TensorFlow Performance Cell
         */
        ~TensorFlowPerformanceCell();

        /**
         * @brief Initialize the performance cell
         * @param configPath Path to configuration file
         * @return true if initialization successful
         */
        bool initialize(const std::string& configPath = "");

        /**
         * @brief Load a TensorFlow SavedModel
         * @param modelPath Path to the SavedModel directory
         * @param tags Model tags (e.g., "serve")
         * @return true if model loaded successfully
         */
        bool loadModel(const std::string& modelPath, const std::vector<std::string>& tags = {"serve"});

        /**
         * @brief Perform high-performance inference
         * @param inputs Input tensors
         * @return Inference result with outputs and metrics
         */
        InferenceResult inference(const std::vector<Tensor>& inputs);

        /**
         * @brief Get performance metrics
         * @return Current performance metrics
         */
        PerformanceMetrics getMetrics() const;

        /**
         * @brief Reset performance metrics
         */
        void resetMetrics();

        /**
         * @brief Check if a model is loaded
         * @return true if model is ready for inference
         */
        bool isModelLoaded() const;

        /**
         * @brief Get loaded model information
         * @return Model metadata
         */
        std::map<std::string, std::string> getModelInfo() const;

        /**
         * @brief Warmup the inference engine
         * @param iterations Number of warmup iterations
         */
        void warmup(int iterations = 10);

    private:
        // Implementation class (PIMPL pattern)
        class Impl;
        std::unique_ptr<Impl> impl_;
    };

} // namespace tensorflow
} // namespace aios

#endif // TENSORFLOW_PERFORMANCE_CELL_HPP