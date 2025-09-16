# AIOS VS Code Auto-Launch Configuration
**STRICT NO EMOTICON POLICY ENFORCED**

This configuration optimizes VS Code to automatically load the AIOS workspace and set the correct PowerShell working directory, eliminating the need to manually select folders on each startup.

## Problem Solved

VS Code was prompting to select a folder on each launch and asking to set the PowerShell working directory to "🧠 AIOS Core". This configuration eliminates those prompts and automatically loads the optimal development environment.

## Configuration Components

### 1. Workspace Settings (`AIOS.code-workspace`)
- **PowerShell CWD**: Automatically set to `${workspaceFolder}` (C:\dev\AIOS)
- **Terminal Integration**: PowerShell starts in the correct directory
- **Window Behavior**: Optimized for AIOS development workflow
- **Auto-Launch**: Minimizes startup prompts and delays

### 2. VS Code Auto-Launch Script (`configure-vscode-autolaunch.ps1`)
- **User Settings**: Configures VS Code to remember and prioritize AIOS workspace
- **PowerShell Profile**: Sets up automatic directory navigation
- **Desktop Shortcut**: Creates quick access to AIOS workspace
- **Batch Launcher**: Simple double-click workspace access

### 3. Quick Launch Batch File (`launch-aios-workspace.bat`)
- **Direct Access**: Immediately opens AIOS workspace in VS Code
- **Error Handling**: Validates VS Code installation and workspace path
- **Status Reporting**: Professional feedback during launch process

## Installation Instructions

### Option 1: Automatic Configuration (Recommended)
```powershell
# Run the auto-configuration script
.\configure-vscode-autolaunch.ps1 -Install -CreateShortcut
```

### Option 2: Manual Setup
1. **Copy workspace settings**: The workspace file is already configured
2. **Create desktop shortcut**: Use the script or create manually
3. **Update PowerShell profile**: Add AIOS auto-navigation

### Option 3: Quick Launch Only
```batch
# Double-click the batch file
launch-aios-workspace.bat
```

## Features Implemented

### Auto-Directory Selection
- **Default Location**: VS Code automatically opens to C:\dev\AIOS
- **Workspace Priority**: AIOS.code-workspace is the preferred workspace
- **No Folder Prompts**: Eliminates manual folder selection on startup

### PowerShell Integration
- **Working Directory**: Automatically set to AIOS root
- **Terminal Integration**: PowerShell starts in correct location
- **Profile Configuration**: Auto-navigation when PowerShell starts in wrong location
- **Environment Variables**: AIOS_HOME and development paths pre-configured

### Window Management
- **Startup Behavior**: No welcome screen, direct workspace access
- **Window Restoration**: Consistent window state and layout
- **Maximized Launch**: Full-screen development environment

### Development Workflow
- **Multi-Root Workspace**: All AIOS components accessible
- **Integrated Terminal**: PowerShell ready in correct directory
- **Project Detection**: Automatic recognition of AIOS project structure

## Usage Examples

### Daily Development Workflow
1. **Open VS Code**: Automatically loads AIOS workspace
2. **Open Terminal**: PowerShell starts in C:\dev\AIOS
3. **Navigate Projects**: All folders available in workspace explorer
4. **Run Commands**: All AIOS tools accessible from correct directory

### Command Line Launch
```batch
# Quick workspace launch
launch-aios-workspace.bat

# Direct VS Code command
code "C:\dev\AIOS\AIOS.code-workspace"

# PowerShell launch
powershell -Command "code 'C:\dev\AIOS\AIOS.code-workspace'"
```

### Shortcut Usage
- **Desktop Shortcut**: Double-click "AIOS Workspace" icon
- **Start Menu**: Pin batch file to start menu for quick access
- **Taskbar**: Pin VS Code with AIOS workspace as default

## Configuration Details

### Workspace Settings Applied
```json
{
    "powershell.cwd": "${workspaceFolder}",
    "terminal.integrated.cwd": "${workspaceFolder}",
    "window.restoreWindows": "one",
    "workbench.startupEditor": "none",
    "window.openFoldersInNewWindow": "on"
}
```

### PowerShell Profile Addition
```powershell
# Auto-navigate to AIOS if starting in default locations
if (Test-Path 'C:\dev\AIOS') {
    if ((Get-Location).Path -eq $env:USERPROFILE -or 
        (Get-Location).Path -eq 'C:\Windows\System32') {
        Set-Location 'C:\dev\AIOS'
        Write-Host '[AIOS] Workspace ready: C:\dev\AIOS' -ForegroundColor Green
    }
}
```

### VS Code User Settings
```json
{
    "window.restoreWindows": "one",
    "workbench.startupEditor": "none",
    "window.reopenFolders": "all",
    "workbench.welcome.enabled": false
}
```

## Troubleshooting

### VS Code Still Prompts for Folder
- **Solution**: Run the configuration script with `-Install` flag
- **Manual Fix**: Update VS Code user settings to include workspace preferences
- **Alternative**: Use the batch launcher for direct workspace access

### PowerShell Starts in Wrong Directory
- **Solution**: The workspace settings override this behavior
- **Backup**: PowerShell profile includes auto-navigation
- **Manual Fix**: Use `Set-Location 'C:\dev\AIOS'` command

### Desktop Shortcut Not Working
- **Solution**: Re-run script with `-CreateShortcut` flag
- **Manual Creation**: Right-click desktop, create shortcut to VS Code with workspace argument
- **Alternative**: Use the batch file launcher

### VS Code Not Found
- **Solution**: Install VS Code and ensure it's in PATH
- **Verification**: Run `code --version` in command prompt
- **Installation**: Download from official VS Code website

## Benefits

### Professional Development Environment
- **Consistent Setup**: Same workspace configuration every time
- **Reduced Friction**: No manual setup steps required
- **Professional Standards**: Clean, efficient workflow without distractions

### Time Savings
- **Instant Access**: Direct workspace loading eliminates navigation time
- **Automated Setup**: All development tools ready immediately
- **Consistent State**: Predictable environment every session

### Error Reduction
- **Correct Directories**: No more running commands in wrong locations
- **Path Consistency**: All relative paths work correctly
- **Environment Validation**: Scripts verify setup before proceeding

## Maintenance

### Updating Configuration
- **Workspace Changes**: Edit `AIOS.code-workspace` for permanent changes
- **User Preferences**: Run configuration script to update user settings
- **Profile Updates**: Modify PowerShell profile for startup behavior changes

### Backup and Recovery
- **Workspace Backup**: AIOS.code-workspace is version controlled
- **Settings Export**: VS Code settings can be exported/imported
- **Script Recreation**: Configuration script can regenerate all settings

### Monitoring and Validation
- **Test Function**: Configuration script includes validation tests
- **Manual Verification**: Check VS Code behavior after configuration
- **Troubleshooting**: Use provided solutions for common issues

## Integration with AIOS

### Supercell Architecture
- **Professional Standards**: No manual prompts or user friction
- **Automated Workflow**: Consistent with AIOS automation principles
- **Development Efficiency**: Optimized for AIOS multi-language development

### Runtime Intelligence
- **Environment Monitoring**: PowerShell profile can report workspace status
- **Usage Analytics**: Track workspace usage patterns
- **Performance Metrics**: Monitor startup and configuration times

---

**NOTICE**: This configuration maintains strict professional standards without any informal language or interface elements. All prompts and interactions follow AIOS professional coding practices.