#include "SphereShellManager.hpp"
#include "CenterGeometryField.hpp"
#include "AIOrchestrationController.hpp"
#include "AtomicHolographyUnit.hpp"
#include "MathConstants.hpp"
#include <iostream>
#include <cmath>
#include <algorithm>
#include <random>
#include <numeric>
#include <fstream>
#include <thread>

SphereShellManager::SphereShellManager()
    : next_shell_id_(1)
    , default_radius_(1.0)
    , default_thickness_(0.1)
    , max_shell_count_(1000)
    , ai_optimization_enabled_(true)
    , shell_interactions_enabled_(true)
    , parallel_processing_enabled_(true)
    , geometric_caching_enabled_(true)
    , geometry_field_(nullptr)
    , ai_controller_(nullptr)
    , quantum_unit_(nullptr)
    , current_optimization_score_(0.5)
{
    std::cout << "[SphereShellManager] Initializing AI-Enhanced Hyperspherical Shell Manager..." << std::endl;
}

SphereShellManager::~SphereShellManager() {
    shutdown();
}

void SphereShellManager::initialize() {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    std::cout << "[SphereShellManager] Starting initialization..." << std::endl;
    
    // Clear any existing state
    shells_.clear();
    subdivisions_.clear();
    interactions_.clear();
    optimization_history_.clear();
    cached_metrics_.clear();
    cached_calculations_.clear();
    
    // Initialize with default shell configuration
    createShell(3, default_radius_, default_thickness_); // 3D sphere
    createShell(4, default_radius_ * 1.5, default_thickness_); // 4D hypersphere
    createShell(2, default_radius_ * 0.7, default_thickness_); // 2D circle
    
    // Initialize AI parameters
    ai_parameters_["complexity_weight"] = 0.3;
    ai_parameters_["stability_weight"] = 0.4;
    ai_parameters_["efficiency_weight"] = 0.3;
    ai_parameters_["mutation_rate"] = 0.1;
    
    std::cout << "[SphereShellManager] Initialization complete. Active shells: " 
              << shells_.size() << std::endl;
}

void SphereShellManager::bootstrap() {
    std::cout << "[SphereShellManager] Bootstrapping hyperspherical shell system..." << std::endl;
    
    initialize();
    
    // Create initial nested structure
    if (!shells_.empty()) {
        int base_shell = shells_.begin()->first;
        createNestedShellStructure(base_shell, 3);
    }
    
    // Start shell dynamics
    updateShellDynamics();
    
    // Initial optimization pass
    if (ai_optimization_enabled_) {
        optimizeShellConfiguration();
    }
    
    std::cout << "[SphereShellManager] Bootstrap complete." << std::endl;
}

void SphereShellManager::shutdown() {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    std::cout << "[SphereShellManager] Shutting down shell system..." << std::endl;
    
    // Save final metrics for analysis
    ShellMetrics final_metrics = calculateSystemMetrics();
    std::ofstream metrics_log("shell_metrics.log");
    if (metrics_log.is_open()) {
        metrics_log << "# SphereShellManager Final Metrics\n";
        metrics_log << "Total Surface Area: " << final_metrics.total_surface_area << "\n";
        metrics_log << "Total Volume: " << final_metrics.total_volume << "\n";
        metrics_log << "Average Curvature: " << final_metrics.average_curvature << "\n";
        metrics_log << "AI Optimization Score: " << final_metrics.ai_optimization_score << "\n";
        metrics_log << "Active Shell Count: " << final_metrics.active_shell_count << "\n";
        metrics_log.close();
    }
    
    // Clear all data structures
    shells_.clear();
    subdivisions_.clear();
    interactions_.clear();
    optimization_history_.clear();
    cached_metrics_.clear();
    cached_calculations_.clear();
}

// Core shell management
int SphereShellManager::createShell(int dimension, double radius, double thickness) {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    if (shells_.size() >= max_shell_count_) {
        std::cout << "[SphereShellManager] Warning: Maximum shell count reached" << std::endl;
        return -1;
    }
    
    int shell_id = next_shell_id_++;
    SphericalShell shell;
    
    shell.dimension = std::max(1, dimension);
    shell.radius = std::max(0.001, radius);
    shell.thickness = std::max(0.001, thickness);
    shell.curvature = std::complex<double>(1.0 / radius, 0.0); // Initial Gaussian curvature
    shell.rotation_angles.resize(shell.dimension, 0.0);
    shell.angular_velocity = 0.1; // Default rotation speed
    shell.stability_index = 1.0;
    shell.resonance_frequency = 1.0 / radius; // Natural frequency
    shell.harmonic_coefficients.resize(shell.dimension * 2, std::complex<double>(1.0, 0.0));
    shell.creation_time = std::chrono::steady_clock::now();
    shell.last_update = shell.creation_time;
    
    shells_[shell_id] = shell;
    
    std::cout << "[SphereShellManager] Created " << dimension << "D shell (ID: " 
              << shell_id << ") radius: " << radius << std::endl;
    
    return shell_id;
}

void SphereShellManager::destroyShell(int shell_id) {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    auto it = shells_.find(shell_id);
    if (it != shells_.end()) {
        std::cout << "[SphereShellManager] Destroying shell ID: " << shell_id << std::endl;
        shells_.erase(it);
        
        // Remove related subdivisions and interactions
        subdivisions_.erase(
            std::remove_if(subdivisions_.begin(), subdivisions_.end(),
                [shell_id](const ShellSubdivision& sub) {
                    return sub.parent_shell_id == shell_id ||
                           std::find(sub.child_shell_ids.begin(), sub.child_shell_ids.end(), shell_id) != 
                           sub.child_shell_ids.end();
                }),
            subdivisions_.end());
    }
}

void SphereShellManager::rotateShells() {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    auto now = std::chrono::steady_clock::now();
    
    for (auto& [shell_id, shell] : shells_) {
        updateShellRotation(shell);
        shell.last_update = now;
    }
}

void SphereShellManager::updateShellDynamics() {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    for (auto& [shell_id, shell] : shells_) {
        // Update shell geometry
        updateShellGeometry(shell);
        
        // Calculate stability
        calculateShellStability(shell);
        
        // Update resonance frequency
        updateResonanceFrequency(shell);
        
        // Calculate spherical harmonics
        calculateHarmonics(shell);
        
        shell.last_update = std::chrono::steady_clock::now();
    }
    
    // Detect and process shell interactions
    if (shell_interactions_enabled_) {
        detectShellInteractions();
        processShellResonance();
    }
}

// AI-driven shell operations
void SphereShellManager::optimizeShellConfiguration() {
    if (!ai_optimization_enabled_) return;
    
    std::cout << "[SphereShellManager] Starting AI-driven shell optimization..." << std::endl;
    
    double initial_score = current_optimization_score_;
    
    // Try different optimization strategies
    if (ai_controller_) {
        aiGuidedOptimization();
    } else {
        // Fallback to traditional optimization
        geneticAlgorithmOptimization();
    }
    
    double improvement = current_optimization_score_ - initial_score;
    optimization_history_.push_back(current_optimization_score_);
    
    std::cout << "[SphereShellManager] Optimization complete. Score improvement: " 
              << improvement << std::endl;
}

void SphereShellManager::adaptiveSubdivision() {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    std::cout << "[SphereShellManager] Performing adaptive subdivision..." << std::endl;
    
    for (const auto& [shell_id, shell] : shells_) {
        // Determine if subdivision is beneficial
        double complexity_factor = calculateShellVolume(shell) / calculateShellSurfaceArea(shell);
        
        if (complexity_factor > 2.0 && shell.stability_index > 0.8) {
            // Shell is large and stable - good candidate for subdivision
            subdivideShell(shell_id, "adaptive", 2.0);
        }
    }
}

void SphereShellManager::intelligentShellMerging() {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    std::vector<std::vector<int>> merge_candidates;
    
    // Find shells with similar properties that could benefit from merging
    for (const auto& [id_a, shell_a] : shells_) {
        for (const auto& [id_b, shell_b] : shells_) {
            if (id_a >= id_b) continue;
            
            // Check if shells are compatible for merging
            bool same_dimension = (shell_a.dimension == shell_b.dimension);
            bool similar_radius = std::abs(shell_a.radius - shell_b.radius) < 0.2;
            bool both_stable = (shell_a.stability_index > 0.7 && shell_b.stability_index > 0.7);
            
            if (same_dimension && similar_radius && both_stable) {
                merge_candidates.push_back({id_a, id_b});
            }
        }
    }
    
    // Perform merging for identified candidates
    for (const auto& candidates : merge_candidates) {
        if (candidates.size() >= 2) {
            mergeShells(candidates, "intelligent");
        }
    }
}

void SphereShellManager::aiDrivenCurvatureAdaptation() {
    if (!ai_controller_) return;
    
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    for (auto& [shell_id, shell] : shells_) {
        // AI-driven curvature optimization
        double target_complexity = ai_parameters_["complexity_weight"];
        double current_curvature = std::abs(shell.curvature);
        
        // Adapt curvature based on AI feedback
        if (current_optimization_score_ < 0.5) {
            // Increase curvature for more complex dynamics
            shell.curvature *= (1.0 + 0.1 * (1.0 - current_optimization_score_));
        } else {
            // Decrease curvature for stability
            shell.curvature *= (1.0 - 0.05 * current_optimization_score_);
        }
        
        // Ensure reasonable bounds
        double curvature_magnitude = std::abs(shell.curvature);
        if (curvature_magnitude > 10.0) {
            shell.curvature *= (10.0 / curvature_magnitude);
        } else if (curvature_magnitude < 0.1) {
            shell.curvature *= (0.1 / curvature_magnitude);
        }
    }
}

// Subdivision and merging methods
ShellSubdivision SphereShellManager::subdivideShell(int shell_id, const std::string& method, double factor) {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) {
        return ShellSubdivision{}; // Return empty subdivision if shell not found
    }
    
    const SphericalShell& parent_shell = shell_it->second;
    ShellSubdivision subdivision;
    subdivision.parent_shell_id = shell_id;
    subdivision.subdivision_type = method;
    subdivision.subdivision_factor = factor;
    subdivision.quality_metric = 0.0;
    
    std::vector<int> child_ids;
    
    if (method == "geodesic") {
        child_ids = geodesicSubdivision(shell_id, factor);
    } else if (method == "uniform") {
        child_ids = uniformSubdivision(shell_id, factor);
    } else if (method == "adaptive") {
        child_ids = adaptiveSubdivision(shell_id, factor);
    } else if (method == "ai_driven") {
        child_ids = aiDrivenSubdivision(shell_id, factor);
    }
    
    subdivision.child_shell_ids = child_ids;
    subdivision.quality_metric = static_cast<double>(child_ids.size()) / factor; // Simple quality measure
    
    subdivisions_.push_back(subdivision);
    
    std::cout << "[SphereShellManager] Subdivided shell " << shell_id 
              << " using " << method << " method. Created " << child_ids.size() << " children." << std::endl;
    
    return subdivision;
}

void SphereShellManager::mergeShells(const std::vector<int>& shell_ids, const std::string& merge_strategy) {
    if (shell_ids.size() < 2) return;
    
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    // Calculate merged shell properties
    double total_volume = 0.0;
    double weighted_radius = 0.0;
    std::complex<double> average_curvature(0.0, 0.0);
    int target_dimension = 0;
    
    for (int shell_id : shell_ids) {
        auto shell_it = shells_.find(shell_id);
        if (shell_it != shells_.end()) {
            const SphericalShell& shell = shell_it->second;
            double volume = calculateShellVolume(shell);
            total_volume += volume;
            weighted_radius += shell.radius * volume;
            average_curvature += shell.curvature * volume;
            target_dimension = std::max(target_dimension, shell.dimension);
        }
    }
    
    if (total_volume > 0) {
        weighted_radius /= total_volume;
        average_curvature /= total_volume;
        
        // Create merged shell
        int merged_id = createShell(target_dimension, weighted_radius, default_thickness_);
        if (merged_id > 0) {
            shells_[merged_id].curvature = average_curvature;
            
            // Remove original shells
            for (int shell_id : shell_ids) {
                destroyShell(shell_id);
            }
            
            std::cout << "[SphereShellManager] Merged " << shell_ids.size() 
                      << " shells into shell " << merged_id << std::endl;
        }
    }
}

void SphereShellManager::refineShellGeometry(int shell_id, double target_quality) {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return;
    
    SphericalShell& shell = shell_it->second;
    
    // Refine geometry through iterative improvement
    for (int iteration = 0; iteration < 10; iteration++) {
        updateShellGeometry(shell);
        calculateShellStability(shell);
        
        if (shell.stability_index >= target_quality) {
            break; // Quality target achieved
        }
        
        // Adjust parameters for better quality
        shell.curvature *= (1.0 + 0.01 * (target_quality - shell.stability_index));
    }
}

// Curvature and geometry methods
void SphereShellManager::updateCurvature(int shell_id, const std::complex<double>& new_curvature) {
    auto shell_it = shells_.find(shell_id);
    if (shell_it != shells_.end()) {
        shell_it->second.curvature = new_curvature;
        updateShellGeometry(shell_it->second);
    }
}

void SphereShellManager::adaptCurvatureToField(const CenterGeometryField& field) {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    const auto& field_state = field.getCurrentState();
    
    for (auto& [shell_id, shell] : shells_) {
        // Adapt curvature based on field influence
        double field_influence = field.getFieldInfluenceOnCoherence();
        std::complex<double> field_gradient = field.getFieldGradient(0.0, 0.0); // Sample at origin
        
        // Apply field-induced curvature modifications
        shell.curvature += field_gradient * 0.01 * field_influence;
        
        // Update resonance frequency based on field coupling
        shell.resonance_frequency *= (1.0 + 0.1 * field_influence);
        
        updateShellGeometry(shell);
    }
}

double SphereShellManager::calculateGaussianCurvature(int shell_id) const {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return 0.0;
    
    const SphericalShell& shell = shell_it->second;
    return shell.curvature.real(); // Real part represents Gaussian curvature
}

double SphereShellManager::calculateMeanCurvature(int shell_id) const {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return 0.0;
    
    const SphericalShell& shell = shell_it->second;
    return shell.curvature.imag(); // Imaginary part represents mean curvature
}

// Shell interaction methods
void SphereShellManager::detectShellInteractions() {
    std::lock_guard<std::mutex> lock(interactions_mutex_);
    
    interactions_.clear();
    
    for (const auto& [id_a, shell_a] : shells_) {
        for (const auto& [id_b, shell_b] : shells_) {
            if (id_a >= id_b) continue;
            
            // Check for resonance interaction
            if (detectResonance(shell_a, shell_b)) {
                ShellInteraction interaction;
                interaction.shell_a_id = id_a;
                interaction.shell_b_id = id_b;
                interaction.interaction_type = "resonance";
                interaction.interaction_strength = calculateShellCoupling(id_a, id_b);
                interaction.phase_offset = shell_a.curvature / shell_b.curvature;
                interaction.energy_transfer = interaction.interaction_strength * 0.1;
                interactions_.push_back(interaction);
            }
            
            // Check for interference
            if (detectInterference(shell_a, shell_b)) {
                ShellInteraction interaction;
                interaction.shell_a_id = id_a;
                interaction.shell_b_id = id_b;
                interaction.interaction_type = "interference";
                interaction.interaction_strength = calculateShellCoupling(id_a, id_b);
                interaction.phase_offset = shell_a.curvature - shell_b.curvature;
                interaction.energy_transfer = -interaction.interaction_strength * 0.05; // Energy loss
                interactions_.push_back(interaction);
            }
        }
    }
}

void SphereShellManager::processShellResonance() {
    for (const auto& interaction : interactions_) {
        if (interaction.interaction_type == "resonance" && interaction.interaction_strength > 0.1) {
            auto shell_a_it = shells_.find(interaction.shell_a_id);
            auto shell_b_it = shells_.find(interaction.shell_b_id);
            
            if (shell_a_it != shells_.end() && shell_b_it != shells_.end()) {
                SphericalShell& shell_a = shell_a_it->second;
                SphericalShell& shell_b = shell_b_it->second;
                
                // Apply resonance effects
                shell_a.resonance_frequency += interaction.energy_transfer * 0.01;
                shell_b.resonance_frequency += interaction.energy_transfer * 0.01;
                
                // Phase synchronization
                std::complex<double> phase_coupling = interaction.phase_offset * 0.1;
                shell_a.curvature += phase_coupling;
                shell_b.curvature += std::conj(phase_coupling);
            }
        }
    }
}

void SphereShellManager::manageShellInterference() {
    for (const auto& interaction : interactions_) {
        if (interaction.interaction_type == "interference") {
            auto shell_a_it = shells_.find(interaction.shell_a_id);
            auto shell_b_it = shells_.find(interaction.shell_b_id);
            
            if (shell_a_it != shells_.end() && shell_b_it != shells_.end()) {
                SphericalShell& shell_a = shell_a_it->second;
                SphericalShell& shell_b = shell_b_it->second;
                
                // Apply interference effects
                shell_a.stability_index *= (1.0 + interaction.energy_transfer);
                shell_b.stability_index *= (1.0 + interaction.energy_transfer);
                
                // Ensure stability bounds
                shell_a.stability_index = std::max(0.0, std::min(1.0, shell_a.stability_index));
                shell_b.stability_index = std::max(0.0, std::min(1.0, shell_b.stability_index));
            }
        }
    }
}

double SphereShellManager::calculateShellCoupling(int shell_a, int shell_b) const {
    auto shell_a_it = shells_.find(shell_a);
    auto shell_b_it = shells_.find(shell_b);
    
    if (shell_a_it == shells_.end() || shell_b_it == shells_.end()) return 0.0;
    
    const SphericalShell& sa = shell_a_it->second;
    const SphericalShell& sb = shell_b_it->second;
    
    // Calculate coupling strength based on proximity and resonance
    double radius_ratio = std::min(sa.radius, sb.radius) / std::max(sa.radius, sb.radius);
    double frequency_similarity = 1.0 / (1.0 + std::abs(sa.resonance_frequency - sb.resonance_frequency));
    double dimension_factor = (sa.dimension == sb.dimension) ? 1.0 : 0.5;
    
    return radius_ratio * frequency_similarity * dimension_factor;
}

// N-dimensional operations
void SphereShellManager::extendToNDimensions(int target_dimension) {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    for (auto& [shell_id, shell] : shells_) {
        if (shell.dimension < target_dimension) {
            // Extend shell to higher dimension
            int old_dimension = shell.dimension;
            shell.dimension = target_dimension;
            
            // Extend rotation angles vector
            shell.rotation_angles.resize(target_dimension, 0.0);
            
            // Extend harmonic coefficients
            shell.harmonic_coefficients.resize(target_dimension * 2, std::complex<double>(1.0, 0.0));
            
            // Adjust radius for higher dimension
            shell.radius *= std::pow(1.1, target_dimension - old_dimension);
            
            // Update curvature for new dimension
            shell.curvature *= std::complex<double>(0.9, 0.0);
            
            updateShellGeometry(shell);
            
            std::cout << "[SphereShellManager] Extended shell " << shell_id 
                      << " from " << old_dimension << "D to " << target_dimension << "D" << std::endl;
        }
    }
}

void SphereShellManager::projectToLowerDimension(int target_dimension) {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    for (auto& [shell_id, shell] : shells_) {
        if (shell.dimension > target_dimension && target_dimension > 0) {
            // Project shell to lower dimension
            int old_dimension = shell.dimension;
            shell.dimension = target_dimension;
            
            // Truncate rotation angles vector
            shell.rotation_angles.resize(target_dimension);
            
            // Truncate harmonic coefficients
            shell.harmonic_coefficients.resize(target_dimension * 2);
            
            // Adjust radius for lower dimension
            shell.radius *= std::pow(0.9, old_dimension - target_dimension);
            
            // Update curvature for new dimension
            shell.curvature *= std::complex<double>(1.1, 0.0);
            
            updateShellGeometry(shell);
            
            std::cout << "[SphereShellManager] Projected shell " << shell_id 
                      << " from " << old_dimension << "D to " << target_dimension << "D" << std::endl;
        }
    }
}

std::vector<double> SphereShellManager::calculateNDimensionalMetrics(int shell_id) const {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return {};
    
    const SphericalShell& shell = shell_it->second;
    std::vector<double> metrics;
    
    int n = shell.dimension;
    double r = shell.radius;
    
    // N-dimensional volume
    double volume = std::pow(M_PI, n / 2.0) * std::pow(r, n) / std::tgamma(n / 2.0 + 1);
    metrics.push_back(volume);
    
    // N-dimensional surface area
    double surface_area = 2.0 * std::pow(M_PI, n / 2.0) * std::pow(r, n - 1) / std::tgamma(n / 2.0);
    metrics.push_back(surface_area);
    
    // N-dimensional curvature
    double curvature = std::abs(shell.curvature) * std::pow(r, -2);
    metrics.push_back(curvature);
    
    // Stability in N dimensions
    double stability = shell.stability_index * std::exp(-n * 0.1); // Stability decreases with dimension
    metrics.push_back(stability);
    
    return metrics;
}

// Integration interfaces
void SphereShellManager::synchronizeWithGeometryField(const CenterGeometryField& field) {
    geometry_field_ = &field;
    adaptCurvatureToField(field);
    
    // Synchronize shell dynamics with field evolution
    const auto& field_state = field.getCurrentState();
    double field_intensity = field_state.field_intensity;
    
    std::lock_guard<std::mutex> lock(shells_mutex_);
    for (auto& [shell_id, shell] : shells_) {
        // Field affects shell angular velocity
        shell.angular_velocity *= (1.0 + 0.1 * field_intensity);
        
        // Field affects shell stability
        shell.stability_index *= (1.0 + 0.05 * field_intensity);
        shell.stability_index = std::max(0.0, std::min(1.0, shell.stability_index));
    }
}

void SphereShellManager::integrateAIFeedback(const AIOrchestrationController& ai_controller) {
    ai_controller_ = &ai_controller;
    
    // Update AI parameters based on controller feedback
    // In a real implementation, this would query the AI controller
    ai_parameters_["complexity_weight"] = 0.35;
    ai_parameters_["stability_weight"] = 0.35;
    ai_parameters_["efficiency_weight"] = 0.30;
    
    optimizeWithAI();
}

void SphereShellManager::synchronizeWithQuantumField(const AtomicHolographyUnit& quantum_unit) {
    quantum_unit_ = &quantum_unit;
    
    // Quantum field affects shell harmonic coefficients
    std::lock_guard<std::mutex> lock(shells_mutex_);
    for (auto& [shell_id, shell] : shells_) {
        // Apply quantum coherence to harmonics
        for (auto& coeff : shell.harmonic_coefficients) {
            coeff *= (1.0 + 0.01 * std::complex<double>(0.0, 1.0)); // Quantum phase evolution
        }
    }
}

// Shell nesting and hierarchy
void SphereShellManager::createNestedShellStructure(int base_shell_id, int nesting_levels) {
    auto base_shell_it = shells_.find(base_shell_id);
    if (base_shell_it == shells_.end() || nesting_levels <= 0) return;
    
    const SphericalShell& base_shell = base_shell_it->second;
    
    std::cout << "[SphereShellManager] Creating nested structure with " << nesting_levels 
              << " levels around shell " << base_shell_id << std::endl;
    
    for (int level = 1; level <= nesting_levels; level++) {
        double radius_factor = 1.0 + level * 0.3;
        double thickness_factor = 1.0 + level * 0.1;
        
        int nested_shell = createShell(
            base_shell.dimension,
            base_shell.radius * radius_factor,
            base_shell.thickness * thickness_factor
        );
        
        if (nested_shell > 0) {
            // Inherit some properties from base shell
            shells_[nested_shell].angular_velocity = base_shell.angular_velocity * 0.8;
            shells_[nested_shell].resonance_frequency = base_shell.resonance_frequency / radius_factor;
        }
    }
}

void SphereShellManager::optimizeShellHierarchy() {
    // Optimize shell arrangement for minimal energy configuration
    std::vector<int> shell_ids = getActiveShellIds();
    
    // Sort shells by radius for hierarchical optimization
    std::sort(shell_ids.begin(), shell_ids.end(), [this](int a, int b) {
        return shells_[a].radius < shells_[b].radius;
    });
    
    // Adjust spacing between shells for optimal packing
    for (size_t i = 1; i < shell_ids.size(); i++) {
        SphericalShell& inner_shell = shells_[shell_ids[i-1]];
        SphericalShell& outer_shell = shells_[shell_ids[i]];
        
        double optimal_spacing = inner_shell.radius * 1.2; // Golden ratio-inspired spacing
        if (outer_shell.radius - inner_shell.radius < optimal_spacing) {
            outer_shell.radius = inner_shell.radius + optimal_spacing;
            updateShellGeometry(outer_shell);
        }
    }
}

void SphereShellManager::balanceShellDistribution() {
    std::lock_guard<std::mutex> lock(shells_mutex_);
    
    // Balance shell distribution across dimensions
    std::unordered_map<int, int> dimension_counts;
    for (const auto& [shell_id, shell] : shells_) {
        dimension_counts[shell.dimension]++;
    }
    
    // Find under-represented dimensions
    int max_count = 0;
    for (const auto& [dim, count] : dimension_counts) {
        max_count = std::max(max_count, count);
    }
    
    // Create shells for under-represented dimensions
    for (int dim = 2; dim <= 5; dim++) { // Focus on 2D-5D
        if (dimension_counts[dim] < max_count / 2) {
            createShell(dim, default_radius_ * dim * 0.3, default_thickness_);
        }
    }
}

// Configuration and state access
void SphereShellManager::setShellParameters(double default_radius, double default_thickness) {
    default_radius_ = std::max(0.001, default_radius);
    default_thickness_ = std::max(0.001, default_thickness);
}

void SphereShellManager::enableAIOptimization(bool enable) {
    ai_optimization_enabled_ = enable;
}

void SphereShellManager::setMaxShellCount(int max_count) {
    max_shell_count_ = std::max(1, max_count);
}

void SphereShellManager::enableShellInteractions(bool enable) {
    shell_interactions_enabled_ = enable;
}

const SphericalShell& SphereShellManager::getShell(int shell_id) const {
    static SphericalShell empty_shell; // Return reference to empty shell if not found
    auto it = shells_.find(shell_id);
    return (it != shells_.end()) ? it->second : empty_shell;
}

std::vector<int> SphereShellManager::getActiveShellIds() const {
    std::vector<int> ids;
    for (const auto& [shell_id, shell] : shells_) {
        ids.push_back(shell_id);
    }
    return ids;
}

ShellMetrics SphereShellManager::calculateSystemMetrics() const {
    ShellMetrics metrics = {};
    
    for (const auto& [shell_id, shell] : shells_) {
        metrics.total_surface_area += calculateShellSurfaceArea(shell);
        metrics.total_volume += calculateShellVolume(shell);
        metrics.average_curvature += std::abs(shell.curvature);
        metrics.geometric_complexity += shell.dimension * std::abs(shell.curvature);
    }
    
    metrics.active_shell_count = static_cast<int>(shells_.size());
    if (metrics.active_shell_count > 0) {
        metrics.average_curvature /= metrics.active_shell_count;
    }
    
    metrics.ai_optimization_score = current_optimization_score_;
    metrics.field_coupling_strength = geometry_field_ ? 0.8 : 0.0;
    
    return metrics;
}

const std::vector<ShellInteraction>& SphereShellManager::getShellInteractions() const {
    return interactions_;
}

// Internal calculation methods
void SphereShellManager::updateShellRotation(SphericalShell& shell) {
    auto now = std::chrono::steady_clock::now();
    auto time_diff = std::chrono::duration_cast<std::chrono::microseconds>(
        now - shell.last_update).count() / 1e6;
    
    // Update rotation angles
    for (size_t i = 0; i < shell.rotation_angles.size(); i++) {
        shell.rotation_angles[i] += shell.angular_velocity * time_diff * (i + 1) * 0.1;
        
        // Keep angles in [0, 2π) range
        while (shell.rotation_angles[i] >= 2.0 * M_PI) {
            shell.rotation_angles[i] -= 2.0 * M_PI;
        }
        while (shell.rotation_angles[i] < 0.0) {
            shell.rotation_angles[i] += 2.0 * M_PI;
        }
    }
}

void SphereShellManager::calculateShellStability(SphericalShell& shell) {
    // Calculate stability based on multiple factors
    double curvature_factor = 1.0 / (1.0 + std::abs(shell.curvature));
    double resonance_factor = 1.0 / (1.0 + std::abs(shell.resonance_frequency - 1.0));
    double dimension_factor = 1.0 / (1.0 + shell.dimension * 0.1);
    double rotation_factor = 1.0 / (1.0 + shell.angular_velocity);
    
    shell.stability_index = curvature_factor * resonance_factor * dimension_factor * rotation_factor;
    shell.stability_index = std::max(0.0, std::min(1.0, shell.stability_index));
}

void SphereShellManager::updateResonanceFrequency(SphericalShell& shell) {
    // Natural frequency depends on radius and dimension
    double base_frequency = 1.0 / shell.radius;
    double dimension_correction = std::sqrt(static_cast<double>(shell.dimension));
    
    shell.resonance_frequency = base_frequency * dimension_correction;
    
    // Apply field coupling if available
    if (geometry_field_) {
        double field_influence = geometry_field_->getFieldInfluenceOnCoherence();
        shell.resonance_frequency *= (1.0 + 0.1 * field_influence);
    }
}

void SphereShellManager::calculateHarmonics(SphericalShell& shell) {
    // Calculate spherical harmonic coefficients
    for (size_t i = 0; i < shell.harmonic_coefficients.size(); i++) {
        int l = static_cast<int>(i / 2); // Degree
        int m = static_cast<int>(i % 2); // Order (simplified)
        
        double theta = shell.rotation_angles[0];
        double phi = (shell.rotation_angles.size() > 1) ? shell.rotation_angles[1] : 0.0;
        
        // Simplified spherical harmonic calculation
        double real_part = std::cos(l * theta + m * phi) * std::exp(-l * 0.1);
        double imag_part = std::sin(l * theta + m * phi) * std::exp(-l * 0.1);
        
        shell.harmonic_coefficients[i] = std::complex<double>(real_part, imag_part);
    }
}

// Subdivision algorithms
std::vector<int> SphereShellManager::geodesicSubdivision(int shell_id, double factor) {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return {};
    
    const SphericalShell& parent = shell_it->second;
    std::vector<int> child_ids;
    
    int num_children = static_cast<int>(factor);
    
    for (int i = 0; i < num_children; i++) {
        // Create child shells at geodesic positions
        double angle = 2.0 * M_PI * i / num_children;
        double child_radius = parent.radius * 0.8;
        
        int child_id = createShell(parent.dimension, child_radius, parent.thickness * 0.8);
        if (child_id > 0) {
            SphericalShell& child = shells_[child_id];
            
            // Position child at geodesic location
            child.rotation_angles[0] = angle;
            if (child.rotation_angles.size() > 1) {
                child.rotation_angles[1] = angle * 0.5;
            }
            
            // Inherit curvature with variation
            child.curvature = parent.curvature * std::exp(std::complex<double>(0.0, angle * 0.1));
            
            child_ids.push_back(child_id);
        }
    }
    
    return child_ids;
}

std::vector<int> SphereShellManager::uniformSubdivision(int shell_id, double factor) {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return {};
    
    const SphericalShell& parent = shell_it->second;
    std::vector<int> child_ids;
    
    int num_children = static_cast<int>(factor);
    double radius_step = parent.radius / (num_children + 1);
    
    for (int i = 1; i <= num_children; i++) {
        double child_radius = radius_step * i;
        
        int child_id = createShell(parent.dimension, child_radius, parent.thickness);
        if (child_id > 0) {
            SphericalShell& child = shells_[child_id];
            
            // Uniform scaling of properties
            child.curvature = parent.curvature * (child_radius / parent.radius);
            child.angular_velocity = parent.angular_velocity * std::sqrt(parent.radius / child_radius);
            
            child_ids.push_back(child_id);
        }
    }
    
    return child_ids;
}

std::vector<int> SphereShellManager::adaptiveSubdivision(int shell_id, double factor) {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return {};
    
    const SphericalShell& parent = shell_it->second;
    std::vector<int> child_ids;
    
    // Adaptive subdivision based on shell properties
    int num_children = static_cast<int>(factor * parent.stability_index);
    num_children = std::max(1, std::min(num_children, 10)); // Reasonable bounds
    
    for (int i = 0; i < num_children; i++) {
        // Adaptive radius based on curvature
        double curvature_magnitude = std::abs(parent.curvature);
        double adaptive_factor = 0.5 + 0.3 * (1.0 / (1.0 + curvature_magnitude));
        double child_radius = parent.radius * adaptive_factor;
        
        int child_id = createShell(parent.dimension, child_radius, parent.thickness);
        if (child_id > 0) {
            SphericalShell& child = shells_[child_id];
            
            // Adaptive property inheritance
            child.curvature = parent.curvature * (1.0 + 0.1 * i);
            child.stability_index = parent.stability_index * 0.9;
            
            child_ids.push_back(child_id);
        }
    }
    
    return child_ids;
}

std::vector<int> SphereShellManager::aiDrivenSubdivision(int shell_id, double factor) {
    if (!ai_controller_) {
        return adaptiveSubdivision(shell_id, factor); // Fallback
    }
    
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) return {};
    
    const SphericalShell& parent = shell_it->second;
    std::vector<int> child_ids;
    
    // AI-driven subdivision parameters
    double complexity_weight = ai_parameters_.at("complexity_weight");
    double stability_weight = ai_parameters_.at("stability_weight");
    double mutation_rate = ai_parameters_.at("mutation_rate");
    
    int num_children = static_cast<int>(factor * (complexity_weight + stability_weight));
    num_children = std::max(1, std::min(num_children, 8));
    
    for (int i = 0; i < num_children; i++) {
        // AI-optimized child properties
        double ai_radius_factor = 0.6 + 0.4 * complexity_weight;
        double child_radius = parent.radius * ai_radius_factor;
        
        int child_id = createShell(parent.dimension, child_radius, parent.thickness);
        if (child_id > 0) {
            SphericalShell& child = shells_[child_id];
            
            // AI-driven mutations
            std::random_device rd;
            std::mt19937 gen(rd());
            std::normal_distribution<double> mutation(1.0, mutation_rate);
            
            child.curvature = parent.curvature * mutation(gen);
            child.angular_velocity = parent.angular_velocity * mutation(gen);
            child.stability_index = parent.stability_index * (stability_weight + 0.5);
            
            child_ids.push_back(child_id);
        }
    }
    
    return child_ids;
}

// Geometric calculations
void SphereShellManager::updateShellGeometry(SphericalShell& shell) {
    // Update complex curvature based on current state
    shell.curvature = calculateComplexCurvature(shell);
    
    // Update harmonic coefficients
    calculateHarmonics(shell);
    
    // Cache geometric properties if enabled
    if (geometric_caching_enabled_) {
        // Find shell ID for this shell reference
        int shell_id = -1;
        for (const auto& [id, shell_ref] : shells_) {
            if (&shell_ref == &shell) {
                shell_id = id;
                break;
            }
        }
        
        if (shell_id != -1) {
            std::vector<double> metrics = calculateNDimensionalMetrics(shell_id);
            cached_metrics_[shell_id] = metrics;
        }
    }
}

double SphereShellManager::calculateShellVolume(const SphericalShell& shell) const {
    int n = shell.dimension;
    double r = shell.radius;
    double t = shell.thickness;
    
    // Volume of n-dimensional spherical shell
    double outer_volume = std::pow(M_PI, n / 2.0) * std::pow(r + t/2, n) / std::tgamma(n / 2.0 + 1);
    double inner_volume = std::pow(M_PI, n / 2.0) * std::pow(r - t/2, n) / std::tgamma(n / 2.0 + 1);
    
    return outer_volume - inner_volume;
}

double SphereShellManager::calculateShellSurfaceArea(const SphericalShell& shell) const {
    int n = shell.dimension;
    double r = shell.radius;
    
    // Surface area of n-dimensional sphere
    return 2.0 * std::pow(M_PI, n / 2.0) * std::pow(r, n - 1) / std::tgamma(n / 2.0);
}

std::complex<double> SphereShellManager::calculateComplexCurvature(const SphericalShell& shell) const {
    // Gaussian curvature (real part)
    double gaussian_curvature = 1.0 / (shell.radius * shell.radius);
    
    // Mean curvature (imaginary part) - affected by shell dynamics
    double mean_curvature = (shell.dimension - 1.0) / shell.radius;
    mean_curvature *= (1.0 + 0.1 * shell.angular_velocity);
    
    return std::complex<double>(gaussian_curvature, mean_curvature);
}

// Interaction detection methods
bool SphereShellManager::detectResonance(const SphericalShell& a, const SphericalShell& b) const {
    double frequency_diff = std::abs(a.resonance_frequency - b.resonance_frequency);
    double tolerance = 0.1 * std::min(a.resonance_frequency, b.resonance_frequency);
    
    return frequency_diff < tolerance;
}

bool SphereShellManager::detectInterference(const SphericalShell& a, const SphericalShell& b) const {
    // Check for spatial overlap or proximity
    double distance = std::abs(a.radius - b.radius);
    double combined_thickness = (a.thickness + b.thickness) / 2.0;
    
    return distance < combined_thickness * 2.0;
}

void SphereShellManager::processShellCoupling(const SphericalShell& a, const SphericalShell& b) {
    // Process coupling effects between shells
    // This is a placeholder for more complex coupling dynamics
}

// AI integration and optimization methods
void SphereShellManager::extractShellPatterns() {
    // Extract patterns from shell evolution for AI learning
    if (optimization_history_.size() < 5) return;
    
    // Calculate pattern metrics
    double avg_improvement = 0.0;
    for (size_t i = 1; i < optimization_history_.size(); i++) {
        avg_improvement += optimization_history_[i] - optimization_history_[i-1];
    }
    avg_improvement /= (optimization_history_.size() - 1);
    
    // Store pattern for AI system
    ai_parameters_["avg_improvement"] = avg_improvement;
}

void SphereShellManager::optimizeWithAI() {
    if (!ai_optimization_enabled_) return;
    
    extractShellPatterns();
    aiGuidedOptimization();
    adaptToAIFeedback();
}

void SphereShellManager::adaptToAIFeedback() {
    // Adapt system parameters based on AI feedback
    if (current_optimization_score_ > 0.8) {
        // High performance - maintain current strategy
        ai_parameters_["mutation_rate"] *= 0.95;
    } else if (current_optimization_score_ < 0.3) {
        // Poor performance - increase exploration
        ai_parameters_["mutation_rate"] *= 1.1;
        ai_parameters_["complexity_weight"] *= 1.05;
    }
    
    // Ensure reasonable bounds
    ai_parameters_["mutation_rate"] = std::max(0.01, std::min(0.5, ai_parameters_["mutation_rate"]));
}

// Optimization algorithms
void SphereShellManager::geneticAlgorithmOptimization() {
    std::cout << "[SphereShellManager] Running genetic algorithm optimization..." << std::endl;
    
    std::vector<int> shell_ids = getActiveShellIds();
    if (shell_ids.size() < 2) return;
    
    // Genetic algorithm parameters
    int population_size = std::min(10, static_cast<int>(shell_ids.size()));
    int generations = 20;
    double mutation_rate = ai_parameters_["mutation_rate"];
    
    for (int gen = 0; gen < generations; gen++) {
        // Evaluate fitness of current population
        std::vector<std::pair<int, double>> fitness_scores;
        for (int shell_id : shell_ids) {
            const SphericalShell& shell = shells_[shell_id];
            double fitness = shell.stability_index * (1.0 / (1.0 + std::abs(shell.curvature)));
            fitness_scores.push_back({shell_id, fitness});
        }
        
        // Sort by fitness
        std::sort(fitness_scores.begin(), fitness_scores.end(),
                 [](const auto& a, const auto& b) { return a.second > b.second; });
        
        // Select top performers for reproduction
        int elite_count = population_size / 2;
        for (int i = elite_count; i < population_size && i < fitness_scores.size(); i++) {
            int shell_id = fitness_scores[i].first;
            SphericalShell& shell = shells_[shell_id];
            
            // Mutate shell properties
            std::random_device rd;
            std::mt19937 gen(rd());
            std::normal_distribution<double> mutation(1.0, mutation_rate);
            
            shell.radius *= mutation(gen);
            shell.curvature *= mutation(gen);
            shell.angular_velocity *= mutation(gen);
            
            // Ensure reasonable bounds
            shell.radius = std::max(0.1, std::min(10.0, shell.radius));
            
            updateShellGeometry(shell);
        }
    }
    
    // Update optimization score
    ShellMetrics metrics = calculateSystemMetrics();
    current_optimization_score_ = metrics.ai_optimization_score;
}

void SphereShellManager::gradientDescentOptimization() {
    std::cout << "[SphereShellManager] Running gradient descent optimization..." << std::endl;
    
    double learning_rate = 0.01;
    int iterations = 50;
    
    for (int iter = 0; iter < iterations; iter++) {
        double current_score = calculateSystemMetrics().ai_optimization_score;
        
        for (auto& [shell_id, shell] : shells_) {
            // Calculate gradients for shell parameters
            double radius_gradient = 0.0;
            double curvature_gradient = 0.0;
            
            // Finite difference approximation
            double epsilon = 0.001;
            
            // Radius gradient
            shell.radius += epsilon;
            updateShellGeometry(shell);
            double score_plus = calculateSystemMetrics().ai_optimization_score;
            
            shell.radius -= 2.0 * epsilon;
            updateShellGeometry(shell);
            double score_minus = calculateSystemMetrics().ai_optimization_score;
            
            shell.radius += epsilon; // Restore original
            radius_gradient = (score_plus - score_minus) / (2.0 * epsilon);
            
            // Apply gradient update
            shell.radius += learning_rate * radius_gradient;
            shell.radius = std::max(0.1, std::min(10.0, shell.radius));
            
            updateShellGeometry(shell);
        }
    }
    
    current_optimization_score_ = calculateSystemMetrics().ai_optimization_score;
}

void SphereShellManager::simulatedAnnealingOptimization() {
    std::cout << "[SphereShellManager] Running simulated annealing optimization..." << std::endl;
    
    double initial_temperature = 1.0;
    double cooling_rate = 0.95;
    int iterations = 100;
    
    double temperature = initial_temperature;
    double current_score = calculateSystemMetrics().ai_optimization_score;
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> random(0.0, 1.0);
    
    for (int iter = 0; iter < iterations; iter++) {
        // Select random shell for modification
        std::vector<int> shell_ids = getActiveShellIds();
        if (shell_ids.empty()) break;
        
        int random_shell = shell_ids[gen() % shell_ids.size()];
        SphericalShell& shell = shells_[random_shell];
        
        // Save current state
        double old_radius = shell.radius;
        std::complex<double> old_curvature = shell.curvature;
        
        // Apply random perturbation
        std::normal_distribution<double> perturbation(1.0, temperature * 0.1);
        shell.radius *= perturbation(gen);
        shell.curvature *= perturbation(gen);
        
        // Ensure bounds
        shell.radius = std::max(0.1, std::min(10.0, shell.radius));
        updateShellGeometry(shell);
        
        // Calculate new score
        double new_score = calculateSystemMetrics().ai_optimization_score;
        double delta = new_score - current_score;
        
        // Accept or reject change
        if (delta > 0 || random(gen) < std::exp(delta / temperature)) {
            current_score = new_score;
        } else {
            // Reject change - restore old state
            shell.radius = old_radius;
            shell.curvature = old_curvature;
            updateShellGeometry(shell);
        }
        
        // Cool down
        temperature *= cooling_rate;
    }
    
    current_optimization_score_ = current_score;
}

void SphereShellManager::aiGuidedOptimization() {
    if (!ai_controller_) {
        simulatedAnnealingOptimization(); // Fallback
        return;
    }
    
    std::cout << "[SphereShellManager] Running AI-guided optimization..." << std::endl;
    
    // AI-guided multi-objective optimization
    double complexity_weight = ai_parameters_["complexity_weight"];
    double stability_weight = ai_parameters_["stability_weight"];
    double efficiency_weight = ai_parameters_["efficiency_weight"];
    
    // Optimization targets
    for (auto& [shell_id, shell] : shells_) {
        // AI-driven parameter adjustment
        double target_stability = 0.8;
        double target_complexity = complexity_weight;
        
        // Adjust radius for stability
        if (shell.stability_index < target_stability) {
            shell.radius *= (1.0 + 0.1 * (target_stability - shell.stability_index));
        }
        
        // Adjust curvature for complexity
        double current_complexity = std::abs(shell.curvature) * shell.dimension;
        if (current_complexity < target_complexity) {
            shell.curvature *= (1.0 + 0.1 * (target_complexity - current_complexity));
        }
        
        // Efficiency optimization
        shell.angular_velocity *= (1.0 + 0.05 * efficiency_weight);
        
        updateShellGeometry(shell);
    }
    
    current_optimization_score_ = calculateSystemMetrics().ai_optimization_score;
}

// Advanced features
void SphereShellManager::simulateShellEvolution() {
    std::cout << "[SphereShellManager] Simulating shell evolution..." << std::endl;
    
    for (auto& [shell_id, shell] : shells_) {
        // Evolutionary pressure based on stability and efficiency
        double evolution_pressure = (1.0 - shell.stability_index) * 0.1;
        
        // Evolve shell properties
        shell.radius *= (1.0 + evolution_pressure * 0.1);
        shell.curvature *= std::exp(std::complex<double>(evolution_pressure * 0.01, 0.0));
        shell.resonance_frequency *= (1.0 + evolution_pressure * 0.05);
        
        // Update derived properties
        updateShellGeometry(shell);
        calculateShellStability(shell);
    }
}

void SphereShellManager::modelTopologicalTransitions() {
    std::cout << "[SphereShellManager] Modeling topological transitions..." << std::endl;
    
    for (auto& [shell_id, shell] : shells_) {
        // Check for topology change conditions
        double curvature_magnitude = std::abs(shell.curvature);
        
        if (curvature_magnitude > 5.0) {
            // High curvature - potential dimension increase
            if (shell.dimension < 6) {
                std::cout << "[SphereShellManager] Topological transition: " << shell.dimension 
                          << "D -> " << (shell.dimension + 1) << "D for shell " << shell_id << std::endl;
                shell.dimension++;
                shell.rotation_angles.resize(shell.dimension, 0.0);
                shell.harmonic_coefficients.resize(shell.dimension * 2, std::complex<double>(1.0, 0.0));
                updateShellGeometry(shell);
            }
        } else if (curvature_magnitude < 0.2 && shell.dimension > 2) {
            // Low curvature - potential dimension decrease
            std::cout << "[SphereShellManager] Topological transition: " << shell.dimension 
                      << "D -> " << (shell.dimension - 1) << "D for shell " << shell_id << std::endl;
            shell.dimension--;
            shell.rotation_angles.resize(shell.dimension);
            shell.harmonic_coefficients.resize(shell.dimension * 2);
            updateShellGeometry(shell);
        }
    }
}

void SphereShellManager::calculateShellEntanglement() {
    std::cout << "[SphereShellManager] Calculating shell entanglement..." << std::endl;
    
    // Calculate quantum-inspired entanglement between shells
    for (const auto& interaction : interactions_) {
        if (interaction.interaction_type == "resonance") {
            auto shell_a_it = shells_.find(interaction.shell_a_id);
            auto shell_b_it = shells_.find(interaction.shell_b_id);
            
            if (shell_a_it != shells_.end() && shell_b_it != shells_.end()) {
                SphericalShell& shell_a = shell_a_it->second;
                SphericalShell& shell_b = shell_b_it->second;
                
                // Calculate entanglement measure
                double entanglement = interaction.interaction_strength * 
                    std::abs(interaction.phase_offset) / (1.0 + std::abs(shell_a.radius - shell_b.radius));
                
                if (entanglement > 0.5) {
                    // Strong entanglement - synchronize properties
                    shell_a.resonance_frequency = (shell_a.resonance_frequency + shell_b.resonance_frequency) / 2.0;
                    shell_b.resonance_frequency = shell_a.resonance_frequency;
                    
                    std::cout << "[SphereShellManager] Strong entanglement detected between shells " 
                              << interaction.shell_a_id << " and " << interaction.shell_b_id 
                              << " (strength: " << entanglement << ")" << std::endl;
                }
            }
        }
    }
}

void SphereShellManager::optimizeForMinimalSurface() {
    std::cout << "[SphereShellManager] Optimizing for minimal surface..." << std::endl;
    
    // Minimize total surface area while maintaining functionality
    double total_surface_area = calculateSystemMetrics().total_surface_area;
    double target_reduction = 0.1; // 10% reduction target
    
    for (auto& [shell_id, shell] : shells_) {
        // Reduce shell thickness while maintaining stability
        if (shell.stability_index > 0.7) {
            shell.thickness *= 0.95;
            shell.thickness = std::max(0.01, shell.thickness); // Minimum thickness
        }
        
        // Optimize radius for minimal surface
        double optimal_radius = std::pow(calculateShellVolume(shell) * 3.0 / (4.0 * M_PI), 1.0/3.0);
        shell.radius = 0.9 * shell.radius + 0.1 * optimal_radius; // Gradual adjustment
        
        updateShellGeometry(shell);
    }
}

// Performance and utility methods
void SphereShellManager::enableParallelProcessing(bool enable) {
    parallel_processing_enabled_ = enable;
}

void SphereShellManager::optimizeMemoryUsage() {
    cleanupInactiveShells();
    optimizeDataStructures();
}

void SphereShellManager::cacheGeometricCalculations(bool enable) {
    geometric_caching_enabled_ = enable;
    if (!enable) {
        cached_metrics_.clear();
        cached_calculations_.clear();
    }
}

void SphereShellManager::cleanupInactiveShells() {
    std::vector<int> shells_to_remove;
    
    for (const auto& [shell_id, shell] : shells_) {
        // Remove shells with very low stability or extreme properties
        if (shell.stability_index < 0.1 || shell.radius < 0.01 || shell.radius > 100.0) {
            shells_to_remove.push_back(shell_id);
        }
    }
    
    for (int shell_id : shells_to_remove) {
        std::cout << "[SphereShellManager] Cleaning up inactive shell " << shell_id << std::endl;
        destroyShell(shell_id);
    }
}

void SphereShellManager::optimizeDataStructures() {
    // Optimize data structures for better cache performance
    if (shells_.size() > shells_.bucket_count() * 0.75) {
        shells_.rehash(shells_.size() * 2);
    }
}

void SphereShellManager::updatePerformanceMetrics() {
    // Update performance metrics for monitoring
    ShellMetrics metrics = calculateSystemMetrics();
    
    // Log performance if significant changes
    static double last_optimization_score = 0.0;
    if (std::abs(metrics.ai_optimization_score - last_optimization_score) > 0.1) {
        std::cout << "[SphereShellManager] Performance update - Optimization score: " 
                  << metrics.ai_optimization_score << ", Active shells: " 
                  << metrics.active_shell_count << std::endl;
        last_optimization_score = metrics.ai_optimization_score;
    }
}

// Validation and debugging
bool SphereShellManager::validateShellConsistency() const {
    for (const auto& [shell_id, shell] : shells_) {
        if (shell.radius <= 0 || shell.thickness <= 0 || shell.dimension < 1) {
            std::cout << "[SphereShellManager] ERROR: Invalid shell " << shell_id 
                      << " - radius: " << shell.radius << ", thickness: " << shell.thickness 
                      << ", dimension: " << shell.dimension << std::endl;
            return false;
        }
        
        if (shell.stability_index < 0.0 || shell.stability_index > 1.0) {
            std::cout << "[SphereShellManager] WARNING: Shell " << shell_id 
                      << " has invalid stability index: " << shell.stability_index << std::endl;
        }
    }
    return true;
}

void SphereShellManager::debugShellState(int shell_id) const {
    auto shell_it = shells_.find(shell_id);
    if (shell_it == shells_.end()) {
        std::cout << "[SphereShellManager] DEBUG: Shell " << shell_id << " not found" << std::endl;
        return;
    }
    
    const SphericalShell& shell = shell_it->second;
    std::cout << "[SphereShellManager] DEBUG Shell " << shell_id << ":" << std::endl;
    std::cout << "  Dimension: " << shell.dimension << std::endl;
    std::cout << "  Radius: " << shell.radius << std::endl;
    std::cout << "  Thickness: " << shell.thickness << std::endl;
    std::cout << "  Curvature: " << shell.curvature << std::endl;
    std::cout << "  Stability: " << shell.stability_index << std::endl;
    std::cout << "  Resonance: " << shell.resonance_frequency << std::endl;
    std::cout << "  Angular Velocity: " << shell.angular_velocity << std::endl;
}

void SphereShellManager::logShellMetrics() const {
    ShellMetrics metrics = calculateSystemMetrics();
    
    std::cout << "[SphereShellManager] System Metrics:" << std::endl;
    std::cout << "  Total Surface Area: " << metrics.total_surface_area << std::endl;
    std::cout << "  Total Volume: " << metrics.total_volume << std::endl;
    std::cout << "  Average Curvature: " << metrics.average_curvature << std::endl;
    std::cout << "  Geometric Complexity: " << metrics.geometric_complexity << std::endl;
    std::cout << "  AI Optimization Score: " << metrics.ai_optimization_score << std::endl;
    std::cout << "  Active Shell Count: " << metrics.active_shell_count << std::endl;
    std::cout << "  Field Coupling Strength: " << metrics.field_coupling_strength << std::endl;
}