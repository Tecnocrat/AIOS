-- AIOS Tachyonic Archive Database Schema
-- SQLite database for backup consolidation and archive management
-- AINLP Protocol: OS0.6.2.claude
-- Created: October 12, 2025

-- ==============================================================================
-- BACKUP FILES TABLE
-- ==============================================================================
-- Stores actual file content with deduplication via content hash
CREATE TABLE IF NOT EXISTS backup_files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_hash TEXT NOT NULL UNIQUE,  -- SHA256 hash for deduplication
    file_content BLOB NOT NULL,         -- Actual file content
    original_size INTEGER NOT NULL,     -- Size in bytes
    compressed_size INTEGER,            -- Size after compression (if applicable)
    mime_type TEXT,                     -- File MIME type
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_content_hash (content_hash)
);

-- ==============================================================================
-- BACKUP VERSIONS TABLE
-- ==============================================================================
-- Tracks all backup versions (timestamps) pointing to deduplicated content
CREATE TABLE IF NOT EXISTS backup_versions (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,           -- References backup_files.file_id
    original_path TEXT NOT NULL,        -- Original file path in repository
    backup_timestamp TIMESTAMP NOT NULL,-- When backup was created
    backup_filename TEXT NOT NULL,      -- Original backup filename
    backup_metadata TEXT,               -- JSON metadata about backup context
    created_by TEXT,                    -- System/user that created backup
    FOREIGN KEY (file_id) REFERENCES backup_files(file_id) ON DELETE CASCADE,
    INDEX idx_original_path (original_path),
    INDEX idx_backup_timestamp (backup_timestamp),
    INDEX idx_file_id (file_id)
);

-- ==============================================================================
-- SPATIAL METADATA TABLE
-- ==============================================================================
-- Stores AIOS spatial metadata for architectural awareness
CREATE TABLE IF NOT EXISTS spatial_metadata (
    metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
    folder_path TEXT NOT NULL UNIQUE,   -- Absolute folder path
    relative_path TEXT NOT NULL,        -- Relative path from AIOS root
    parent_path TEXT,                   -- Parent folder path
    depth_level INTEGER,                -- Directory depth
    primary_area TEXT,                  -- Primary architectural area
    secondary_areas TEXT,               -- JSON array of secondary areas
    consciousness_level TEXT,           -- Consciousness classification
    sibling_folders TEXT,               -- JSON array of sibling folders
    generation_timestamp TIMESTAMP,     -- When metadata was generated
    metadata_version TEXT,              -- Spatial metadata schema version
    raw_metadata TEXT,                  -- Full JSON metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_folder_path (folder_path),
    INDEX idx_primary_area (primary_area),
    INDEX idx_depth_level (depth_level)
);

-- ==============================================================================
-- DOCUMENTATION ARCHIVE TABLE
-- ==============================================================================
-- Consolidated documentation from tachyonic archive
CREATE TABLE IF NOT EXISTS documentation_archive (
    doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,            -- Original file path
    filename TEXT NOT NULL,             -- Filename
    file_extension TEXT,                -- .md, .txt, .json, etc.
    title TEXT,                         -- Document title (extracted from content)
    content TEXT NOT NULL,              -- Full document content
    content_hash TEXT NOT NULL,         -- SHA256 hash for deduplication
    category TEXT,                      -- Documentation category
    tags TEXT,                          -- JSON array of tags
    created_date TIMESTAMP,             -- Original creation date
    archived_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_filename (filename),
    INDEX idx_content_hash (content_hash),
    INDEX idx_category (category)
);

-- ==============================================================================
-- MIGRATION LOG TABLE
-- ==============================================================================
-- Tracks migration progress and rollback capability
CREATE TABLE IF NOT EXISTS migration_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    migration_phase TEXT NOT NULL,      -- Phase name (Phase 1, Phase 2, etc.)
    operation_type TEXT NOT NULL,       -- CREATE, MIGRATE, DELETE, UPDATE
    source_path TEXT,                   -- Source file/folder path
    destination_path TEXT,              -- Destination file/folder path
    status TEXT NOT NULL,               -- SUCCESS, FAILED, SKIPPED
    error_message TEXT,                 -- Error details if failed
    rollback_data TEXT,                 -- JSON data for rollback
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_migration_phase (migration_phase),
    INDEX idx_status (status),
    INDEX idx_executed_at (executed_at)
);

-- ==============================================================================
-- SYSTEM METADATA TABLE
-- ==============================================================================
-- Tracks database version and migration state
CREATE TABLE IF NOT EXISTS system_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial system metadata
INSERT OR IGNORE INTO system_metadata (key, value, description) VALUES
    ('schema_version', '1.0.0', 'Current database schema version'),
    ('migration_status', 'not_started', 'Current migration phase status'),
    ('created_at', datetime('now'), 'Database creation timestamp'),
    ('aios_version', 'OS0.6.2.claude', 'AIOS version at database creation');

-- ==============================================================================
-- VIEWS FOR COMMON QUERIES
-- ==============================================================================

-- View: Latest backup version for each file
CREATE VIEW IF NOT EXISTS latest_backups AS
SELECT 
    bv.original_path,
    bv.backup_timestamp,
    bv.backup_filename,
    bf.content_hash,
    bf.original_size,
    bv.version_id,
    bv.file_id
FROM backup_versions bv
JOIN backup_files bf ON bv.file_id = bf.file_id
WHERE bv.version_id IN (
    SELECT MAX(version_id)
    FROM backup_versions
    GROUP BY original_path
);

-- View: Backup file deduplication statistics
CREATE VIEW IF NOT EXISTS deduplication_stats AS
SELECT 
    bf.content_hash,
    bf.original_size,
    COUNT(bv.version_id) as version_count,
    MIN(bv.backup_timestamp) as first_backup,
    MAX(bv.backup_timestamp) as last_backup,
    GROUP_CONCAT(DISTINCT bv.original_path) as file_paths
FROM backup_files bf
LEFT JOIN backup_versions bv ON bf.file_id = bv.file_id
GROUP BY bf.file_id;

-- View: Space savings from deduplication
CREATE VIEW IF NOT EXISTS space_savings AS
SELECT 
    COUNT(DISTINCT bf.file_id) as unique_files,
    COUNT(bv.version_id) as total_versions,
    SUM(bf.original_size) as deduplicated_size,
    (SELECT SUM(bf2.original_size * 
        (SELECT COUNT(*) FROM backup_versions bv2 WHERE bv2.file_id = bf2.file_id)
    ) FROM backup_files bf2) as original_total_size,
    (SELECT original_total_size - deduplicated_size) as space_saved
FROM backup_files bf
LEFT JOIN backup_versions bv ON bf.file_id = bv.file_id;

-- ==============================================================================
-- TRIGGERS FOR DATA INTEGRITY
-- ==============================================================================

-- Update spatial_metadata.updated_at on changes
CREATE TRIGGER IF NOT EXISTS update_spatial_metadata_timestamp
AFTER UPDATE ON spatial_metadata
FOR EACH ROW
BEGIN
    UPDATE spatial_metadata 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE metadata_id = NEW.metadata_id;
END;

-- Update system_metadata.updated_at on changes
CREATE TRIGGER IF NOT EXISTS update_system_metadata_timestamp
AFTER UPDATE ON system_metadata
FOR EACH ROW
BEGIN
    UPDATE system_metadata 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE key = NEW.key;
END;

-- ==============================================================================
-- INDEXES FOR PERFORMANCE
-- ==============================================================================

-- Additional indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_backup_versions_path_timestamp 
    ON backup_versions(original_path, backup_timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_documentation_created_date 
    ON documentation_archive(created_date DESC);

CREATE INDEX IF NOT EXISTS idx_migration_log_phase_status 
    ON migration_log(migration_phase, status);

-- ==============================================================================
-- INITIAL DATA POPULATION QUERIES
-- ==============================================================================

-- These queries will be used by the migration script:

-- 1. Check if content already exists (deduplication):
--    SELECT file_id FROM backup_files WHERE content_hash = ?

-- 2. Insert new file content:
--    INSERT INTO backup_files (content_hash, file_content, original_size, mime_type)
--    VALUES (?, ?, ?, ?)

-- 3. Insert backup version:
--    INSERT INTO backup_versions (file_id, original_path, backup_timestamp, 
--                                   backup_filename, backup_metadata)
--    VALUES (?, ?, ?, ?, ?)

-- 4. Query all backups for a specific file:
--    SELECT * FROM backup_versions 
--    WHERE original_path = ? 
--    ORDER BY backup_timestamp DESC

-- 5. Get latest backup content:
--    SELECT bf.file_content 
--    FROM backup_files bf
--    JOIN backup_versions bv ON bf.file_id = bv.file_id
--    WHERE bv.original_path = ?
--    ORDER BY bv.backup_timestamp DESC
--    LIMIT 1

-- ==============================================================================
-- END OF SCHEMA
-- ==============================================================================
