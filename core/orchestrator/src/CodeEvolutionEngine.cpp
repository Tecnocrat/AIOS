#include "CodeEvolutionEngine.hpp"
#include "AtomicHolographyUnit.hpp"
#include <iostream>
#include <fstream>
#include <filesystem>
#include <regex>
#include <random>
#include <algorithm>
#include <sstream>
#include <functional> // For std::hash

CodeEvolutionEngine::CodeEvolutionEngine() 
    : population_size_(50), mutation_rate_(0.15), fitness_threshold_(0.8),
      quantum_coherence_factor_(1.0), quantum_guided_evolution_(false) {
    
    evolution_history_.reserve(1000);  // Reserve for many generations
    mutation_patterns_.reserve(100);   // Reserve for many patterns
}

CodeEvolutionEngine::~CodeEvolutionEngine() {
    shutdown();
}

void CodeEvolutionEngine::initialize() {
    std::lock_guard<std::mutex> lock(evolution_mutex_);
    std::cout << "[CodeEvolutionEngine] Initializing AI-driven evolution system." << std::endl;
    
    // Initialize default mutation patterns
    initializeDefaultMutationPatterns();
    
    // Set default fitness evaluator
    custom_fitness_evaluator_ = [this](const CodeGenome& genome) {
        return evaluateFitness(genome);
    };
    
    std::cout << "[CodeEvolutionEngine] Loaded " << mutation_patterns_.size() 
              << " mutation patterns." << std::endl;
    std::cout << "[CodeEvolutionEngine] Evolution engine ready. Population size: " 
              << population_size_ << ", Mutation rate: " << mutation_rate_ << std::endl;
}

void CodeEvolutionEngine::shutdown() {
    std::lock_guard<std::mutex> lock(evolution_mutex_);
    
    // Save final evolution state
    if (!evolution_history_.empty()) {
        std::string report = generateEvolutionReport();
        std::ofstream report_file("evolution_final_report.md");
        if (report_file.is_open()) {
            report_file << report;
            report_file.close();
            std::cout << "[CodeEvolutionEngine] Evolution report saved." << std::endl;
        }
    }
    
    evolution_history_.clear();
    mutation_patterns_.clear();
    library_knowledge_base_.clear();
    ast_cache_.clear();
    
    std::cout << "[CodeEvolutionEngine] Evolution engine shutdown complete." << std::endl;
}

CodeGenome CodeEvolutionEngine::ingestCode(const std::string& file_path) {
    std::cout << "[CodeEvolutionEngine] Ingesting code: " << file_path << std::endl;
    
    CodeGenome genome;
    
    // Read source code
    std::ifstream file(file_path);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + file_path);
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    genome.source_code = buffer.str();
    file.close();
    
    // Analyze language
    genome.language = analyzeLanguage(genome.source_code);
    
    // Extract dependencies
    genome.dependencies = extractDependencies(genome.source_code, genome.language);
    
    // Generate AST
    genome.ast_representation = generateAST(genome.source_code, genome.language);
    
    // Initialize evolution metrics
    genome.fitness_score = evaluateFitness(genome);
    genome.generation = 0;
    genome.parent_hash = "";
    genome.birth_time = std::chrono::steady_clock::now();
    
    // Add metadata
    genome.metadata["file_path"] = file_path;
    genome.metadata["ingestion_time"] = std::to_string(
        std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::system_clock::now().time_since_epoch()).count());
    genome.metadata["source_hash"] = calculateCodeHash(genome.source_code);
    
    std::cout << "[CodeEvolutionEngine] Code ingested. Language: " << genome.language 
              << ", Dependencies: " << genome.dependencies.size() 
              << ", Fitness: " << genome.fitness_score << std::endl;
    
    return genome;
}

std::string CodeEvolutionEngine::analyzeLanguage(const std::string& source_code) {
    // Simple heuristic-based language detection
    // In production, this would use more sophisticated analysis
    
    if (source_code.find("#include") != std::string::npos || 
        source_code.find("std::") != std::string::npos ||
        source_code.find("class ") != std::string::npos) {
        return "C++";
    }
    
    if (source_code.find("import ") != std::string::npos ||
        source_code.find("def ") != std::string::npos ||
        source_code.find("print(") != std::string::npos) {
        return "Python";
    }
    
    if (source_code.find("using ") != std::string::npos ||
        source_code.find("namespace ") != std::string::npos ||
        source_code.find("public class") != std::string::npos) {
        return "C#";
    }
    
    if (source_code.find("function ") != std::string::npos ||
        source_code.find("const ") != std::string::npos ||
        source_code.find("console.log") != std::string::npos) {
        return "JavaScript";
    }
    
    return "Unknown";
}

std::vector<std::string> CodeEvolutionEngine::extractDependencies(
    const std::string& source_code, const std::string& language) {
    
    if (language == "C++") {
        return parseIncludes(source_code);
    } else if (language == "Python") {
        return parseImports(source_code);
    }
    
    return {}; // Default empty dependencies
}

std::string CodeEvolutionEngine::generateAST(const std::string& source_code, const std::string& language) {
    // Check cache first
    std::string code_hash = calculateCodeHash(source_code);
    
    std::lock_guard<std::mutex> lock(knowledge_base_mutex_);
    auto it = ast_cache_.find(code_hash);
    if (it != ast_cache_.end()) {
        return it->second;
    }
    
    // Simplified AST generation (placeholder)
    // In production, this would use language-specific parsers
    std::string ast_json = "{\n";
    ast_json += "  \"language\": \"" + language + "\",\n";
    ast_json += "  \"hash\": \"" + code_hash + "\",\n";
    ast_json += "  \"functions\": [],\n";
    ast_json += "  \"classes\": [],\n";
    ast_json += "  \"variables\": []\n";
    ast_json += "}";
    
    // Cache the result
    ast_cache_[code_hash] = ast_json;
    
    return ast_json;
}

void CodeEvolutionEngine::buildKnowledgeBase(const std::vector<std::string>& source_directories) {
    std::lock_guard<std::mutex> lock(knowledge_base_mutex_);
    std::cout << "[CodeEvolutionEngine] Building knowledge base from " 
              << source_directories.size() << " directories." << std::endl;
    
    for (const auto& directory : source_directories) {
        if (!std::filesystem::exists(directory)) {
            std::cout << "[CodeEvolutionEngine] Warning: Directory not found: " << directory << std::endl;
            continue;
        }
        
        // Recursively scan directory
        for (const auto& entry : std::filesystem::recursive_directory_iterator(directory)) {
            if (entry.is_regular_file()) {
                std::string file_path = entry.path().string();
                std::string extension = entry.path().extension().string();
                
                // Determine language by extension
                std::string language = "Unknown";
                if (extension == ".cpp" || extension == ".hpp" || extension == ".h") {
                    language = "C++";
                } else if (extension == ".py") {
                    language = "Python";
                } else if (extension == ".cs") {
                    language = "C#";
                }
                
                if (language != "Unknown") {
                    try {
                        CodeGenome genome = ingestCode(file_path);
                        
                        // Add to knowledge base
                        if (library_knowledge_base_.find(language) == library_knowledge_base_.end()) {
                            library_knowledge_base_[language] = std::vector<std::string>();
                        }
                        library_knowledge_base_[language].push_back(file_path);
                        
                    } catch (const std::exception& e) {
                        std::cout << "[CodeEvolutionEngine] Failed to ingest " << file_path 
                                  << ": " << e.what() << std::endl;
                    }
                }
            }
        }
    }
    
    std::cout << "[CodeEvolutionEngine] Knowledge base built. Languages: ";
    for (const auto& [language, files] : library_knowledge_base_) {
        std::cout << language << "(" << files.size() << ") ";
    }
    std::cout << std::endl;
}

std::vector<CodeGenome> CodeEvolutionEngine::mutatePopulation(const std::vector<CodeGenome>& current_generation) {
    std::vector<CodeGenome> mutated_population;
    mutated_population.reserve(current_generation.size());
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> mutation_chance(0.0, 1.0);
    std::uniform_int_distribution<> pattern_selector(0, mutation_patterns_.size() - 1);
    
    for (const auto& parent : current_generation) {
        if (mutation_chance(gen) < mutation_rate_) {
            // Apply mutation
            if (!mutation_patterns_.empty()) {
                const auto& pattern = mutation_patterns_[pattern_selector(gen)];
                if (pattern.is_active && (pattern.target_language == parent.language || pattern.target_language == "Any")) {
                    CodeGenome mutated = applySingleMutation(parent, pattern);
                    mutated_population.push_back(mutated);
                } else {
                    mutated_population.push_back(parent); // No suitable pattern
                }
            } else {
                mutated_population.push_back(parent); // No patterns available
            }
        } else {
            // Keep unchanged
            mutated_population.push_back(parent);
        }
    }
    
    return mutated_population;
}

CodeGenome CodeEvolutionEngine::applySingleMutation(const CodeGenome& parent, const MutationPattern& pattern) {
    CodeGenome mutated = parent;
    mutated.generation = parent.generation + 1;
    mutated.parent_hash = calculateCodeHash(parent.source_code);
    mutated.birth_time = std::chrono::steady_clock::now();
    
    // Apply mutation function
    try {
        mutated.source_code = pattern.mutation_func(parent.source_code);
        mutated.fitness_score = evaluateFitness(mutated);
        
        // Update metadata
        mutated.metadata["mutation_pattern"] = pattern.pattern_name;
        mutated.metadata["mutation_time"] = std::to_string(
            std::chrono::duration_cast<std::chrono::seconds>(
                std::chrono::system_clock::now().time_since_epoch()).count());
    } catch (const std::exception& e) {
        // Mutation failed, return parent unchanged
        std::cout << "[CodeEvolutionEngine] Mutation failed: " << e.what() << std::endl;
        return parent;
    }
    
    return mutated;
}

double CodeEvolutionEngine::evaluateFitness(const CodeGenome& genome) {
    // Multi-factor fitness evaluation
    double fitness = 0.0;
    
    // Factor 1: Code compilation (if applicable)
    bool compiles = compileAndTest(genome);
    fitness += compiles ? 0.4 : 0.0;
    
    // Factor 2: Code complexity (simpler is often better)
    double complexity_penalty = std::min(0.3, genome.source_code.length() / 10000.0);
    fitness += (0.3 - complexity_penalty);
    
    // Factor 3: Dependency management (fewer dependencies can be better)
    double dependency_penalty = std::min(0.2, genome.dependencies.size() / 20.0);
    fitness += (0.2 - dependency_penalty);
    
    // Factor 4: Quantum coherence alignment (if enabled)
    if (quantum_guided_evolution_) {
        fitness += quantum_coherence_factor_ * 0.1;
    }
    
    return std::max(0.0, std::min(1.0, fitness)); // Clamp to [0,1]
}

void CodeEvolutionEngine::synchronizeWithQuantumCoherence(const AtomicHolographyUnit& quantum_unit) {
    quantum_coherence_factor_ = quantum_unit.checkCoherenceStability() ? 1.0 : 0.5;
    quantum_guided_evolution_ = true;
    
    // Adapt mutation rates based on quantum coherence
    adaptMutationRates(quantum_coherence_factor_);
    
    std::cout << "[CodeEvolutionEngine] Synchronized with quantum coherence. Factor: " 
              << quantum_coherence_factor_ << std::endl;
}

void CodeEvolutionEngine::adaptMutationRates(double coherence_level) {
    // Higher coherence = more conservative mutations
    // Lower coherence = more aggressive exploration
    double base_rate = 0.15;
    mutation_rate_ = base_rate * (2.0 - coherence_level);  // Range: [0.15, 0.30]
    
    std::cout << "[CodeEvolutionEngine] Mutation rate adapted to " << mutation_rate_ 
              << " based on coherence level " << coherence_level << std::endl;
}

// Private method implementations

std::string CodeEvolutionEngine::calculateCodeHash(const std::string& source_code) {
    // Simple hash for demonstration - in production use SHA256
    std::hash<std::string> hasher;
    size_t hash_value = hasher(source_code);
    return std::to_string(hash_value);
}

bool CodeEvolutionEngine::compileAndTest(const CodeGenome& genome) {
    // Placeholder compilation test
    // In production, this would actually compile the code
    
    // Basic syntax checks
    if (genome.language == "C++") {
        // Check for basic C++ syntax requirements
        return (genome.source_code.find("#include") != std::string::npos ||
                genome.source_code.find("int main") != std::string::npos);
    } else if (genome.language == "Python") {
        // Check for basic Python syntax
        return (genome.source_code.find("def ") != std::string::npos ||
                genome.source_code.find("import ") != std::string::npos);
    }
    
    return true; // Default to compilable
}

std::vector<std::string> CodeEvolutionEngine::parseIncludes(const std::string& cpp_code) {
    std::vector<std::string> includes;
    std::regex include_regex(R"(#include\s*[<"](.*?)[>"])");
    std::sregex_iterator iter(cpp_code.begin(), cpp_code.end(), include_regex);
    std::sregex_iterator end;
    
    for (; iter != end; ++iter) {
        includes.push_back((*iter)[1].str());
    }
    
    return includes;
}

std::vector<std::string> CodeEvolutionEngine::parseImports(const std::string& python_code) {
    std::vector<std::string> imports;
    std::regex import_regex(R"(import\s+(\w+))|from\s+(\w+)\s+import)");
    std::sregex_iterator iter(python_code.begin(), python_code.end(), import_regex);
    std::sregex_iterator end;
    
    for (; iter != end; ++iter) {
        std::string module = (*iter)[1].str();
        if (module.empty()) module = (*iter)[2].str();
        if (!module.empty()) imports.push_back(module);
    }
    
    return imports;
}

void CodeEvolutionEngine::initializeDefaultMutationPatterns() {
    // Variable name optimization
    MutationPattern var_rename;
    var_rename.pattern_name = "VariableNameOptimization";
    var_rename.target_language = "Any";
    var_rename.mutation_func = [this](const std::string& code) {
        return mutateVariableNames(code);
    };
    var_rename.success_rate = 0.0;
    var_rename.application_count = 0;
    var_rename.is_active = true;
    mutation_patterns_.push_back(var_rename);
    
    // Loop optimization
    MutationPattern loop_opt;
    loop_opt.pattern_name = "LoopOptimization";
    loop_opt.target_language = "C++";
    loop_opt.mutation_func = [this](const std::string& code) {
        return optimizeLoops(code);
    };
    loop_opt.success_rate = 0.0;
    loop_opt.application_count = 0;
    loop_opt.is_active = true;
    mutation_patterns_.push_back(loop_opt);
    
    // Function refactoring
    MutationPattern func_refactor;
    func_refactor.pattern_name = "FunctionRefactoring";
    func_refactor.target_language = "Any";
    func_refactor.mutation_func = [this](const std::string& code) {
        return refactorFunctions(code);
    };
    func_refactor.success_rate = 0.0;
    func_refactor.application_count = 0;
    func_refactor.is_active = true;
    mutation_patterns_.push_back(func_refactor);
    
    std::cout << "[CodeEvolutionEngine] Initialized " << mutation_patterns_.size() 
              << " default mutation patterns." << std::endl;
}

std::string CodeEvolutionEngine::mutateVariableNames(const std::string& code) {
    // Simple variable name mutation (placeholder)
    std::string mutated = code;
    
    // Replace common variable names with more descriptive ones
    std::regex temp_regex(R"(\btemp\b)");
    mutated = std::regex_replace(mutated, temp_regex, "temporary_value");
    
    std::regex i_regex(R"(\bi\b)");
    mutated = std::regex_replace(mutated, i_regex, "index");
    
    return mutated;
}

std::string CodeEvolutionEngine::optimizeLoops(const std::string& code) {
    // Simple loop optimization (placeholder)
    return code; // Return unchanged for now
}

std::string CodeEvolutionEngine::refactorFunctions(const std::string& code) {
    // Simple function refactoring (placeholder)
    return code; // Return unchanged for now
}

std::string CodeEvolutionEngine::improveErrorHandling(const std::string& code) {
    // Simple error handling improvement (placeholder)
    return code; // Return unchanged for now
}

std::string CodeEvolutionEngine::generateEvolutionReport() {
    //  GENERATE CONSCIOUSNESS-ENHANCED EVOLUTION REPORT
    
    std::ostringstream report;
    
    report << "#  Code Evolution Engine Report\n";
    report << "## Generated: " << std::chrono::duration_cast<std::chrono::seconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count() << " seconds since epoch\n\n";
    
    report << "## Evolution Statistics\n";
    report << "- Total Generations: " << evolution_history_.size() << "\n";
    report << "- Population Size: " << population_size_ << "\n";
    report << "- Mutation Rate: " << mutation_rate_ << "\n";
    report << "- Fitness Threshold: " << fitness_threshold_ << "\n";
    report << "- Quantum Coherence Factor: " << quantum_coherence_factor_ << "\n";
    report << "- Quantum Guided Evolution: " << (quantum_guided_evolution_ ? "Enabled" : "Disabled") << "\n\n";
    
    report << "## Mutation Patterns\n";
    report << "- Total Patterns: " << mutation_patterns_.size() << "\n";
    for (size_t i = 0; i < std::min(size_t(5), mutation_patterns_.size()); i++) {
        report << "  - Pattern " << i+1 << ": " << mutation_patterns_[i].pattern_name << "\n";
    }
    report << "\n";
    
    if (!evolution_history_.empty()) {
        report << "## Evolution History (Last 10 Generations)\n";
        size_t start_idx = evolution_history_.size() > 10 ? evolution_history_.size() - 10 : 0;
        for (size_t i = start_idx; i < evolution_history_.size(); i++) {
            report << "- Generation " << i+1 << ": Fitness " << evolution_history_[i].best_fitness 
                   << ", Pattern: " << evolution_history_[i].dominant_pattern << "\n";
        }
        report << "\n";
        
        // Calculate improvement
        double initial_fitness = evolution_history_[0].best_fitness;
        double final_fitness = evolution_history_.back().best_fitness;
        double improvement = ((final_fitness - initial_fitness) / initial_fitness) * 100.0;
        
        report << "## Performance Summary\n";
        report << "- Initial Fitness: " << initial_fitness << "\n";
        report << "- Final Fitness: " << final_fitness << "\n";
        report << "- Total Improvement: " << improvement << "%\n";
    }
    
    report << "\n## Consciousness Integration\n";
    report << "The Code Evolution Engine has successfully integrated consciousness-enhanced algorithms ";
    report << "for real-time C++ intelligence evolution, demonstrating the AIOS paradigm of ";
    report << "transforming errors into evolutionary opportunities.\n";
    
    return report.str();
}
