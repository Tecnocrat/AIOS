#include "tensorflow_performance_cell.hpp"
#include <iostream>
#include <cassert>

int main() {
    std::cout << "Running TensorFlow Performance Cell tests..." << std::endl;
    
    try {
        // Test cell creation
        aios::tensorflow::TensorFlowPerformanceCell cell;
        std::cout << " TensorFlow Performance Cell creation test passed" << std::endl;
        
        // Test initialization
        bool initialized = cell.initialize();
        assert(initialized);
        (void)initialized; // Suppress unused warning
        std::cout << " TensorFlow Performance Cell initialization test passed" << std::endl;
        
        // Test model loading (simulate with empty path for now)
        bool modelLoaded = cell.loadModel("models/mock_model", {"serve"});
        assert(modelLoaded);
        assert(cell.isModelLoaded());
        (void)modelLoaded; // Suppress unused warning
        std::cout << " Model loading test passed" << std::endl;
        
        // Test model info
        auto modelInfo = cell.getModelInfo();
        assert(modelInfo["status"] == "loaded");
        assert(modelInfo["framework"] == "TensorFlow");
        std::cout << " Model info test passed" << std::endl;
        
        // Test inference
        std::vector<aios::tensorflow::Tensor> inputs;
        aios::tensorflow::Tensor input;
        input.data = {1.0f, 2.0f, 3.0f, 4.0f};
        input.shape = {1, 4};
        input.dtype = "float32";
        inputs.push_back(input);
        
        auto result = cell.inference(inputs);
        assert(result.success);
        assert(!result.outputs.empty());
        assert(result.outputs[0].data.size() == 4);
        std::cout << " Inference test passed" << std::endl;
        
        // Test multiple inferences for performance metrics
        for (int i = 0; i < 5; ++i) {
            cell.inference(inputs);
        }
        
        auto metrics = cell.getMetrics();
        assert(metrics.totalInferences >= 6); // At least 6 inferences (1 + 5)
        assert(metrics.successfulInferences == metrics.totalInferences);
        assert(metrics.successRate == 1.0);
        (void)metrics; // Suppress unused warning
        std::cout << " Performance metrics test passed" << std::endl;
        
        // Test warmup
        cell.warmup(3);
        auto metricsAfterWarmup = cell.getMetrics();
        assert(metricsAfterWarmup.totalInferences == metrics.totalInferences); // Warmup shouldn't count
        (void)metricsAfterWarmup; // Suppress unused warning
        std::cout << " Warmup test passed" << std::endl;
        
        // Test metrics reset
        cell.resetMetrics();
        auto resetMetrics = cell.getMetrics();
        assert(resetMetrics.totalInferences == 0);
        assert(resetMetrics.successfulInferences == 0);
        (void)resetMetrics; // Suppress unused warning
        std::cout << " Metrics reset test passed" << std::endl;
        
        std::cout << "\n All TensorFlow Performance Cell tests passed!" << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << " Test failed: " << e.what() << std::endl;
        return 1;
    }
}