// AIOS Emoticon Destroyer - C++ High-Performance Engine
// STRICT NO EMOTICON POLICY ENFORCED

#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <filesystem>
#include <vector>
#include <chrono>

class EmoticonDestroyer {
private:
    int emoticons_destroyed = 0;
    int files_processed = 0;
    std::vector<std::string> backup_files;
    
    // Define emoticon patterns (ranges of Unicode emoticon blocks)
    std::vector<std::string> emoticon_patterns = {
        "[\u{1F600}-\u{1F64F}]",  // Emoticons
        "[\u{1F300}-\u{1F5FF}]",  // Misc Symbols
        "[\u{1F680}-\u{1F6FF}]",  // Transport
        "[\u{1F1E0}-\u{1F1FF}]",  // Flags
        "[\u{2600}-\u{26FF}]",    // Misc symbols
        "[\u{2700}-\u{27BF}]",    // Dingbats
        "[\u{E000}-\u{F8FF}]",    // Private use
        "[\u{FE00}-\u{FE0F}]",    // Variation selectors
        "[\u{1F900}-\u{1F9FF}]",  // Supplemental Symbols
        "[\u{1FA70}-\u{1FAFF}]"   // Extended emoticons
    };
    
public:
    bool create_backup(const std::string& filepath) {
        std::string backup_path = filepath + ".backup";
        try {
            std::filesystem::copy_file(filepath, backup_path);
            backup_files.push_back(backup_path);
            return true;
        } catch (const std::exception& e) {
            std::cerr << "[ERROR] Failed to create backup: " << e.what() << std::endl;
            return false;
        }
    }
    
    int count_emoticons(const std::string& content) {
        int count = 0;
        for (const auto& pattern : emoticon_patterns) {
            std::regex regex_pattern(pattern);
            std::sregex_iterator iter(content.begin(), content.end(), regex_pattern);
            std::sregex_iterator end;
            count += std::distance(iter, end);
        }
        return count;
    }
    
    std::string remove_emoticons(const std::string& content) {
        std::string result = content;
        for (const auto& pattern : emoticon_patterns) {
            std::regex regex_pattern(pattern);
            result = std::regex_replace(result, regex_pattern, "");
        }
        return result;
    }
    
    bool process_file(const std::string& filepath) {
        std::cout << "[C++] Processing: " << filepath << std::endl;
        
        // Read file content
        std::ifstream file(filepath, std::ios::in | std::ios::binary);
        if (!file) {
            std::cerr << "[ERROR] Cannot open file: " << filepath << std::endl;
            return false;
        }
        
        std::string content((std::istreambuf_iterator<char>(file)),
                           std::istreambuf_iterator<char>());
        file.close();
        
        // Count emoticons before removal
        int initial_count = count_emoticons(content);
        if (initial_count == 0) {
            std::cout << "[INFO] No emoticons found in: " << filepath << std::endl;
            return true;
        }
        
        // Create backup before modification
        if (!create_backup(filepath)) {
            return false;
        }
        
        // Remove emoticons
        std::string cleaned_content = remove_emoticons(content);
        
        // Write cleaned content back
        std::ofstream output_file(filepath, std::ios::out | std::ios::binary);
        if (!output_file) {
            std::cerr << "[ERROR] Cannot write to file: " << filepath << std::endl;
            return false;
        }
        
        output_file << cleaned_content;
        output_file.close();
        
        // Update statistics
        emoticons_destroyed += initial_count;
        files_processed++;
        
        std::cout << "[SUCCESS] Removed " << initial_count 
                  << " emoticons from: " << filepath << std::endl;
        
        return true;
    }
    
    bool process_directory(const std::string& dir_path) {
        std::cout << "[C++] Scanning directory: " << dir_path << std::endl;
        
        // File extensions to process
        std::vector<std::string> target_extensions = {
            ".md", ".txt", ".py", ".cpp", ".c", ".h", ".hpp", 
            ".cs", ".js", ".ts", ".json", ".yaml", ".yml"
        };
        
        // Directories to skip
        std::vector<std::string> skip_dirs = {
            "node_modules", ".git", "venv", "env", "__pycache__",
            "aios_env", ".vscode", "bin", "obj", "build", ".vs"
        };
        
        try {
            for (const auto& entry : std::filesystem::recursive_directory_iterator(dir_path)) {
                if (entry.is_regular_file()) {
                    std::string filepath = entry.path().string();
                    std::string extension = entry.path().extension().string();
                    
                    // Check if we should skip this directory
                    bool skip = false;
                    for (const auto& skip_dir : skip_dirs) {
                        if (filepath.find(skip_dir) != std::string::npos) {
                            skip = true;
                            break;
                        }
                    }
                    
                    if (skip) continue;
                    
                    // Check if this is a target file type
                    if (std::find(target_extensions.begin(), target_extensions.end(), extension) 
                        != target_extensions.end()) {
                        process_file(filepath);
                    }
                }
            }
        } catch (const std::exception& e) {
            std::cerr << "[ERROR] Directory processing failed: " << e.what() << std::endl;
            return false;
        }
        
        return true;
    }
    
    void print_statistics() {
        std::cout << "\n[STATISTICS]" << std::endl;
        std::cout << "Files processed: " << files_processed << std::endl;
        std::cout << "Emoticons destroyed: " << emoticons_destroyed << std::endl;
        std::cout << "Backup files created: " << backup_files.size() << std::endl;
    }
};

int main(int argc, char* argv[]) {
    std::cout << "[AIOS] Emoticon Destroyer C++ Engine" << std::endl;
    std::cout << "[POLICY] No emoticons allowed in codebase" << std::endl;
    
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <file_or_directory_path>" << std::endl;
        return 1;
    }
    
    std::string target_path = argv[1];
    EmoticonDestroyer destroyer;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    bool success = false;
    if (std::filesystem::is_directory(target_path)) {
        success = destroyer.process_directory(target_path);
    } else if (std::filesystem::is_regular_file(target_path)) {
        success = destroyer.process_file(target_path);
    } else {
        std::cerr << "[ERROR] Invalid path: " << target_path << std::endl;
        return 1;
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    destroyer.print_statistics();
    std::cout << "Execution time: " << duration.count() << " ms" << std::endl;
    
    return success ? 0 : 1;
}