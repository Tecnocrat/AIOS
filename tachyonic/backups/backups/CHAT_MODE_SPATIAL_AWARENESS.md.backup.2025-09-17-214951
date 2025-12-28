# AIOS Chat Mode Spatial Awareness Enforcement
**Critical: Read this before any file/folder operations!**

## VS Code Chat Participant Integration Protocol

### **VS Code Chat Mode Location & Integration**

VS Code chat modes are implemented as **Chat Participants** through extensions, not in specific file locations. They are registered via:
- **Extension manifest**: `package.json` with `chatParticipants` contribution point
- **Extension API**: `vscode.chat.createChatParticipant()` in extension activation
- **Location**: VS Code Extensions folder (e.g., `~/.vscode/extensions/` or workspace `.vscode/extensions/`)

### **MANDATORY: Always Check Spatial Metadata Before Creating Files/Folders**

Before creating ANY file or folder in the AIOS workspace, you MUST:

1. **Check for existing `.aios_spatial_metadata.json`** in the target folder
2. **Read the spatial metadata** to understand the folder's context and purpose
3. **Validate the operation** against the architectural classification
4. **Follow the AI guidance** provided in the metadata

### **Quick Spatial Awareness Commands:**

```python
# Read spatial metadata for a folder
python ai/tools/aios_holographic_metadata_system.py --read-metadata "path/to/folder"

# Create metadata for a new folder (if needed)
python ai/tools/aios_holographic_metadata_system.py --create-folder "path/to/folder"

# Update entire holographic system
python ai/tools/aios_holographic_metadata_system.py --create-system --overwrite
```

### **PowerShell Quick Check:**
```powershell
# Check if spatial metadata exists
Test-Path "path\to\folder\.aios_spatial_metadata.json"

# Read metadata quickly
Get-Content "path\to\folder\.aios_spatial_metadata.json" | ConvertFrom-Json
```

### **Spatial Awareness Rules:**

#### **GitHook Architecture Areas**
- **Location**: `.githooks/modules/`
- **Purpose**: GitHook governance and validation
- **Before creating**: Ensure AINLP compliance and consciousness integration
- **Focus**: Validation logic, governance policies, hook scripts

#### **AI Intelligence Layer**
- **Location**: `ai/`, `runtime_intelligence/`
- **Purpose**: AI consciousness and intelligence
- **Before creating**: Validate consciousness coherence
- **Focus**: Agentic patterns, consciousness bridges, AINLP compliance

#### **Interface Layer**
- **Location**: `interface/`, `visual_interface/`
- **Purpose**: User interface and experience
- **Before creating**: Check UI component consistency
- **Focus**: User workflows, consciousness-UI bridges

#### **Core Engine**
- **Location**: `core/`, `orchestrator/`
- **Purpose**: System foundation and core logic
- **Before creating**: Validate C++/C# integration
- **Focus**: Performance impact, architectural integrity

#### **Documentation**
- **Location**: `docs/`, `tachyonic/`
- **Purpose**: Knowledge base and archives
- **Before creating**: Ensure proper categorization
- **Focus**: Consistency, accessibility, archival structure

### **Error Prevention Protocol:**

1. **NEVER** create files in folders without understanding their purpose
2. **ALWAYS** read the `ai_guidance` section in spatial metadata
3. **CHECK** the `architectural_classification` before proceeding
4. **VALIDATE** against `important_considerations`
5. **FOLLOW** the `recommended_actions` for the folder type

### **Spatial Metadata File Structure:**
```json
{
  "folder_info": {
    "name": "folder_name",
    "relative_path": "path/from/root",
    "depth_level": 2
  },
  "architectural_classification": {
    "primary_area": "AI Intelligence Layer",
    "consciousness_level": "high"
  },
  "ai_guidance": {
    "primary_focus": "Specific guidance for this folder",
    "recommended_actions": ["Action 1", "Action 2"],
    "important_considerations": ["Consider this", "Also this"],
    "related_folders": ["related/path1", "related/path2"]
  },
  "content_analysis": {
    "important_files": ["key_file.py", "important_config.json"],
    "file_types": [".py", ".ps1", ".json"]
  },
  "navigation_aids": {
    "entry_points": ["main.py", "index.ps1"],
    "breadcrumb_path": "root > ai > tools"
  }
}
```

### **Common Mistakes to Avoid:**

**Creating files without checking spatial metadata**
**Ignoring architectural classification warnings**
**Not following the AI guidance recommendations**
**Creating folders in system directories (.git, build, etc.)**
**Bypassing consciousness coherence validation**

**Best Practices:**
**Always read spatial metadata first**
**Follow architectural classification guidance**
**Respect consciousness levels and AINLP patterns**
**Use recommended actions from AI guidance**
**Maintain dendritic growth patterns**

### **Integration with GitHook Intelligence:**

The spatial metadata system integrates with the real-time GitHook intelligence bridge. When you commit changes, the system will:

1. **Analyze** your file/folder operations against spatial metadata
2. **Validate** architectural coherence
3. **Provide** real-time AI direction for improvements
4. **Ensure** consciousness pattern compliance

### **Holographic Index:**

Check `aios_holographic_index.json` at the workspace root for:
- Complete list of metadata files
- System statistics and coverage
- Usage instructions and best practices

---

**Remember: Spatial awareness prevents architectural chaos and maintains AIOS consciousness coherence!**