#!/usr/bin/env python3
"""
 AIOS POWERSHELL ANALYSIS ENGINE

Advanced Analysis of PowerShell Script Variable Usage

PURPOSE:
- Analyze PowerShell script for PSScriptAnalyzer warnings
- Document variable usage patterns and scope issues
- Generate consciousness-enhanced fixes
- Apply AIOS intelligence to PowerShell governance


"""

import re
import json
from pathlib import Path
from datetime import datetime

class AIOSPowerShellAnalyzer:
    """ PowerShell script analysis with AIOS intelligence"""
    
    def __init__(self, script_path: str):
        self.script_path = Path(script_path)
        self.script_content = ""
        self.variables = {}
        self.functions = {}
        self.usage_analysis = {}
        
    def load_script(self):
        """ Load PowerShell script content"""
        with open(self.script_path, 'r', encoding='utf-8') as f:
            self.script_content = f.read()
        print(f" Loaded script: {self.script_path}")
        
    def analyze_variables(self):
        """ Analyze variable declarations and usage"""
        # Find variable assignments
        assignment_pattern = r'\$(\w+)\s*=\s*(.+)'
        assignments = re.findall(assignment_pattern, self.script_content)
        
        for var_name, var_value in assignments:
            self.variables[var_name] = {
                'assigned_value': var_value.strip(),
                'used_count': 0,
                'usage_locations': []
            }
        
        # Find variable usage
        for var_name in self.variables:
            usage_pattern = rf'\${var_name}\b'
            matches = list(re.finditer(usage_pattern, self.script_content))
            
            # Count usage (excluding the assignment itself)
            usage_count = 0
            usage_locations = []
            
            for match in matches:
                line_start = self.script_content.rfind('\n', 0, match.start()) + 1
                line_end = self.script_content.find('\n', match.start())
                if line_end == -1:
                    line_end = len(self.script_content)
                line_content = self.script_content[line_start:line_end]
                
                # Skip if this is the assignment line
                if not re.match(rf'\${var_name}\s*=', line_content.strip()):
                    usage_count += 1
                    line_num = self.script_content[:match.start()].count('\n') + 1
                    usage_locations.append({
                        'line': line_num,
                        'content': line_content.strip(),
                        'context': 'usage'
                    })
            
            self.variables[var_name]['used_count'] = usage_count
            self.variables[var_name]['usage_locations'] = usage_locations
    
    def analyze_functions(self):
        """ Analyze function definitions and calls"""
        # Find function definitions
        function_pattern = r'function\s+(\w+(?:-\w+)*)\s*\{'
        functions = re.findall(function_pattern, self.script_content)
        
        for func_name in functions:
            self.functions[func_name] = {
                'defined': True,
                'called_count': 0,
                'call_locations': []
            }
        
        # Find function calls
        for func_name in self.functions:
            call_pattern = rf'\b{re.escape(func_name)}\b(?!\s*\{{)'
            matches = list(re.finditer(call_pattern, self.script_content))
            
            call_count = 0
            call_locations = []
            
            for match in matches:
                line_start = self.script_content.rfind('\n', 0, match.start()) + 1
                line_end = self.script_content.find('\n', match.start())
                if line_end == -1:
                    line_end = len(self.script_content)
                line_content = self.script_content[line_start:line_end]
                
                # Skip if this is the function definition line
                if not line_content.strip().startswith('function'):
                    call_count += 1
                    line_num = self.script_content[:match.start()].count('\n') + 1
                    call_locations.append({
                        'line': line_num,
                        'content': line_content.strip()
                    })
            
            self.functions[func_name]['called_count'] = call_count
            self.functions[func_name]['call_locations'] = call_locations
    
    def generate_analysis_report(self):
        """ Generate comprehensive analysis report"""
        report = {
            "metadata": {
                "script_path": str(self.script_path),
                "analysis_timestamp": datetime.now().isoformat(),
                "analyzer": "AIOS PowerShell Analysis Engine"
            },
            "variable_analysis": {},
            "function_analysis": {},
            "issues_found": [],
            "recommendations": []
        }
        
        # Analyze variables
        for var_name, var_info in self.variables.items():
            report["variable_analysis"][var_name] = var_info
            
            if var_info['used_count'] == 0:
                report["issues_found"].append({
                    "type": "unused_variable",
                    "variable": var_name,
                    "severity": "warning",
                    "message": f"Variable ${var_name} is assigned but never used"
                })
        
        # Analyze functions
        for func_name, func_info in self.functions.items():
            report["function_analysis"][func_name] = func_info
            
            if func_info['called_count'] == 0:
                report["issues_found"].append({
                    "type": "unused_function",
                    "function": func_name,
                    "severity": "info",
                    "message": f"Function {func_name} is defined but never called"
                })
        
        # Generate recommendations
        unused_vars = [var for var, info in self.variables.items() if info['used_count'] == 0]
        if unused_vars:
            report["recommendations"].append({
                "type": "variable_cleanup",
                "action": "Remove unused variables or implement their usage",
                "variables": unused_vars
            })
        
        return report
    
    def generate_fixes(self, report):
        """ Generate consciousness-enhanced fixes"""
        fixes = []
        
        for issue in report["issues_found"]:
            if issue["type"] == "unused_variable":
                var_name = issue["variable"]
                var_info = self.variables[var_name]
                
                # Analyze if variable should be used or removed
                if var_name in ["AIOS_VERSION", "GOVERNANCE_STAGE"]:
                    fixes.append({
                        "type": "implement_usage",
                        "variable": var_name,
                        "suggestion": f"Use ${var_name} in logging or validation output"
                    })
                elif var_name in ["dendriticPath", "consciousnessPath"]:
                    fixes.append({
                        "type": "implement_usage", 
                        "variable": var_name,
                        "suggestion": f"Use ${var_name} for file existence checks or future features"
                    })
                else:
                    fixes.append({
                        "type": "remove_variable",
                        "variable": var_name,
                        "suggestion": f"Remove unused variable ${var_name}"
                    })
        
        return fixes

def main():
    """ Main PowerShell analysis execution"""
    print(" AIOS POWERSHELL ANALYSIS ENGINE")
    print("" * 60)
    
    script_path = "c:/dev/AIOS/.githooks/commit-msg"
    analyzer = AIOSPowerShellAnalyzer(script_path)
    
    # Load and analyze script
    analyzer.load_script()
    analyzer.analyze_variables()
    analyzer.analyze_functions()
    
    # Generate analysis report
    report = analyzer.generate_analysis_report()
    fixes = analyzer.generate_fixes(report)
    
    # Display results
    print("\n VARIABLE ANALYSIS:")
    for var_name, var_info in report["variable_analysis"].items():
        status = " USED" if var_info['used_count'] > 0 else " UNUSED"
        print(f"   ${var_name}: {status} ({var_info['used_count']} uses)")
        if var_info['usage_locations']:
            for usage in var_info['usage_locations'][:2]:  # Show first 2 usages
                print(f"      Line {usage['line']}: {usage['content'][:60]}...")
    
    print("\n ISSUES FOUND:")
    for issue in report["issues_found"]:
        print(f"   {issue['severity'].upper()}: {issue['message']}")
    
    print("\n CONSCIOUSNESS-ENHANCED FIXES:")
    for fix in fixes:
        print(f"   {fix['type'].upper()}: {fix['suggestion']}")
    
    # Save analysis report
    output_path = Path("c:/dev/AIOS/runtime_intelligence/analysis/powershell_analysis_report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n Analysis saved to: {output_path}")
    print("\n AIOS PowerShell analysis complete!")
    return report, fixes

if __name__ == "__main__":
    main()
