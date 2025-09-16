/* AIOS Emoticon Destroyer - Pure C Implementation
 * STRICT NO EMOTICON POLICY ENFORCED
 * Optimized for maximum performance and minimal dependencies
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>

#define MAX_PATH_LENGTH 4096
#define MAX_BUFFER_SIZE 1048576
#define MAX_EXTENSIONS 20
#define MAX_SKIP_DIRS 20

typedef struct {
    int emoticons_destroyed;
    int files_processed;
    int backup_files_created;
    clock_t start_time;
} EmoticonStats;

typedef struct {
    char extensions[MAX_EXTENSIONS][10];
    int extension_count;
    char skip_dirs[MAX_SKIP_DIRS][50];
    int skip_dir_count;
} ProcessingConfig;

/* Initialize processing configuration */
void init_config(ProcessingConfig* config) {
    /* Target file extensions */
    strcpy(config->extensions[0], ".md");
    strcpy(config->extensions[1], ".txt");
    strcpy(config->extensions[2], ".py");
    strcpy(config->extensions[3], ".cpp");
    strcpy(config->extensions[4], ".c");
    strcpy(config->extensions[5], ".h");
    strcpy(config->extensions[6], ".hpp");
    strcpy(config->extensions[7], ".cs");
    strcpy(config->extensions[8], ".js");
    strcpy(config->extensions[9], ".ts");
    strcpy(config->extensions[10], ".json");
    strcpy(config->extensions[11], ".yaml");
    strcpy(config->extensions[12], ".yml");
    config->extension_count = 13;
    
    /* Directories to skip */
    strcpy(config->skip_dirs[0], "node_modules");
    strcpy(config->skip_dirs[1], ".git");
    strcpy(config->skip_dirs[2], "venv");
    strcpy(config->skip_dirs[3], "env");
    strcpy(config->skip_dirs[4], "__pycache__");
    strcpy(config->skip_dirs[5], "aios_env");
    strcpy(config->skip_dirs[6], ".vscode");
    strcpy(config->skip_dirs[7], "bin");
    strcpy(config->skip_dirs[8], "obj");
    strcpy(config->skip_dirs[9], "build");
    strcpy(config->skip_dirs[10], ".vs");
    config->skip_dir_count = 11;
}

/* Check if path should be skipped */
int should_skip_path(const char* path, ProcessingConfig* config) {
    for (int i = 0; i < config->skip_dir_count; i++) {
        if (strstr(path, config->skip_dirs[i]) != NULL) {
            return 1;
        }
    }
    return 0;
}

/* Check if file has target extension */
int has_target_extension(const char* filename, ProcessingConfig* config) {
    const char* ext = strrchr(filename, '.');
    if (ext == NULL) return 0;
    
    for (int i = 0; i < config->extension_count; i++) {
        if (strcmp(ext, config->extensions[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

/* Create backup file */
int create_backup(const char* filepath) {
    char backup_path[MAX_PATH_LENGTH];
    snprintf(backup_path, sizeof(backup_path), "%s.backup", filepath);
    
    FILE* source = fopen(filepath, "rb");
    if (!source) {
        printf("[ERROR] Cannot open source file: %s\n", filepath);
        return 0;
    }
    
    FILE* backup = fopen(backup_path, "wb");
    if (!backup) {
        printf("[ERROR] Cannot create backup file: %s\n", backup_path);
        fclose(source);
        return 0;
    }
    
    char buffer[8192];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), source)) > 0) {
        if (fwrite(buffer, 1, bytes, backup) != bytes) {
            printf("[ERROR] Backup write failed for: %s\n", backup_path);
            fclose(source);
            fclose(backup);
            return 0;
        }
    }
    
    fclose(source);
    fclose(backup);
    printf("[BACKUP] Created: %s\n", backup_path);
    return 1;
}

/* Simple emoticon detection (UTF-8 aware) */
int count_emoticons(const char* content, size_t length) {
    int count = 0;
    for (size_t i = 0; i < length; i++) {
        unsigned char c = (unsigned char)content[i];
        
        /* Detect UTF-8 emoticon patterns */
        if (c == 0xF0 && i + 3 < length) {
            unsigned char c1 = (unsigned char)content[i + 1];
            unsigned char c2 = (unsigned char)content[i + 2];
            unsigned char c3 = (unsigned char)content[i + 3];
            
            /* Common emoticon ranges in UTF-8 */
            if ((c1 == 0x9F && c2 >= 0x98 && c2 <= 0x9B) ||  /* Main emoticon blocks */
                (c1 == 0x9F && c2 >= 0x8C && c2 <= 0x8F) ||  /* Misc symbols */
                (c1 == 0x9F && c2 >= 0x9A && c2 <= 0x9B)) {  /* Transport & flags */
                count++;
                i += 3; /* Skip the next 3 bytes */
            }
        }
        /* Also check for common ASCII emoticons */
        else if (i + 1 < length) {
            if ((c == ':' && (content[i+1] == ')' || content[i+1] == '(' || content[i+1] == 'D')) ||
                (c == ';' && content[i+1] == ')') ||
                (c == ':' && content[i+1] == 'P')) {
                count++;
                i++; /* Skip next character */
            }
        }
    }
    return count;
}

/* Remove emoticons from content */
size_t remove_emoticons(char* content, size_t length) {
    size_t write_pos = 0;
    size_t read_pos = 0;
    
    while (read_pos < length) {
        unsigned char c = (unsigned char)content[read_pos];
        int skip = 0;
        
        /* Check for UTF-8 emoticons */
        if (c == 0xF0 && read_pos + 3 < length) {
            unsigned char c1 = (unsigned char)content[read_pos + 1];
            unsigned char c2 = (unsigned char)content[read_pos + 2];
            unsigned char c3 = (unsigned char)content[read_pos + 3];
            
            if ((c1 == 0x9F && c2 >= 0x98 && c2 <= 0x9B) ||
                (c1 == 0x9F && c2 >= 0x8C && c2 <= 0x8F) ||
                (c1 == 0x9F && c2 >= 0x9A && c2 <= 0x9B)) {
                read_pos += 4; /* Skip emoticon */
                skip = 1;
            }
        }
        /* Check for ASCII emoticons */
        else if (read_pos + 1 < length) {
            if ((c == ':' && (content[read_pos+1] == ')' || content[read_pos+1] == '(' || content[read_pos+1] == 'D')) ||
                (c == ';' && content[read_pos+1] == ')') ||
                (c == ':' && content[read_pos+1] == 'P')) {
                read_pos += 2; /* Skip emoticon */
                skip = 1;
            }
        }
        
        if (!skip) {
            content[write_pos++] = content[read_pos++];
        }
    }
    
    return write_pos; /* New length */
}

/* Process single file */
int process_file(const char* filepath, EmoticonStats* stats) {
    printf("[C] Processing: %s\n", filepath);
    
    FILE* file = fopen(filepath, "rb");
    if (!file) {
        printf("[ERROR] Cannot open file: %s\n", filepath);
        return 0;
    }
    
    /* Get file size */
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    if (file_size <= 0 || file_size > MAX_BUFFER_SIZE) {
        printf("[SKIP] File too large or empty: %s\n", filepath);
        fclose(file);
        return 1;
    }
    
    /* Read file content */
    char* content = malloc(file_size + 1);
    if (!content) {
        printf("[ERROR] Memory allocation failed for: %s\n", filepath);
        fclose(file);
        return 0;
    }
    
    size_t bytes_read = fread(content, 1, file_size, file);
    fclose(file);
    
    if (bytes_read != (size_t)file_size) {
        printf("[ERROR] Read failed for: %s\n", filepath);
        free(content);
        return 0;
    }
    
    content[file_size] = '\0';
    
    /* Count emoticons */
    int initial_count = count_emoticons(content, file_size);
    if (initial_count == 0) {
        printf("[INFO] No emoticons found in: %s\n", filepath);
        free(content);
        return 1;
    }
    
    /* Create backup */
    if (!create_backup(filepath)) {
        free(content);
        return 0;
    }
    stats->backup_files_created++;
    
    /* Remove emoticons */
    size_t new_length = remove_emoticons(content, file_size);
    
    /* Write cleaned content */
    FILE* output = fopen(filepath, "wb");
    if (!output) {
        printf("[ERROR] Cannot write to file: %s\n", filepath);
        free(content);
        return 0;
    }
    
    if (fwrite(content, 1, new_length, output) != new_length) {
        printf("[ERROR] Write failed for: %s\n", filepath);
        fclose(output);
        free(content);
        return 0;
    }
    
    fclose(output);
    free(content);
    
    /* Update statistics */
    stats->emoticons_destroyed += initial_count;
    stats->files_processed++;
    
    printf("[SUCCESS] Removed %d emoticons from: %s\n", initial_count, filepath);
    return 1;
}

/* Process directory recursively */
int process_directory(const char* dir_path, EmoticonStats* stats, ProcessingConfig* config) {
    printf("[C] Scanning directory: %s\n", dir_path);
    
    DIR* dir = opendir(dir_path);
    if (!dir) {
        printf("[ERROR] Cannot open directory: %s\n", dir_path);
        return 0;
    }
    
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        
        char full_path[MAX_PATH_LENGTH];
        snprintf(full_path, sizeof(full_path), "%s/%s", dir_path, entry->d_name);
        
        if (should_skip_path(full_path, config)) {
            continue;
        }
        
        struct stat file_stat;
        if (stat(full_path, &file_stat) != 0) {
            continue;
        }
        
        if (S_ISDIR(file_stat.st_mode)) {
            process_directory(full_path, stats, config);
        } else if (S_ISREG(file_stat.st_mode) && has_target_extension(entry->d_name, config)) {
            process_file(full_path, stats);
        }
    }
    
    closedir(dir);
    return 1;
}

/* Print statistics */
void print_statistics(EmoticonStats* stats) {
    clock_t end_time = clock();
    double execution_time = ((double)(end_time - stats->start_time)) / CLOCKS_PER_SEC;
    
    printf("\n[STATISTICS]\n");
    printf("Files processed: %d\n", stats->files_processed);
    printf("Emoticons destroyed: %d\n", stats->emoticons_destroyed);
    printf("Backup files created: %d\n", stats->backup_files_created);
    printf("Execution time: %.2f seconds\n", execution_time);
}

int main(int argc, char* argv[]) {
    printf("[AIOS] Emoticon Destroyer C Engine\n");
    printf("[POLICY] No emoticons allowed in codebase\n");
    
    if (argc < 2) {
        printf("Usage: %s <file_or_directory_path>\n", argv[0]);
        return 1;
    }
    
    EmoticonStats stats = {0, 0, 0, clock()};
    ProcessingConfig config;
    init_config(&config);
    
    const char* target_path = argv[1];
    
    struct stat path_stat;
    if (stat(target_path, &path_stat) != 0) {
        printf("[ERROR] Invalid path: %s\n", target_path);
        return 1;
    }
    
    int success = 0;
    if (S_ISDIR(path_stat.st_mode)) {
        success = process_directory(target_path, &stats, &config);
    } else if (S_ISREG(path_stat.st_mode)) {
        success = process_file(target_path, &stats);
    } else {
        printf("[ERROR] Invalid path type: %s\n", target_path);
        return 1;
    }
    
    print_statistics(&stats);
    
    return success ? 0 : 1;
}