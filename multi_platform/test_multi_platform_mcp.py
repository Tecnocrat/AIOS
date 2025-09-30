#!/usr/bin/env python3
"""
AIOS Multi-Platform MCP Integration Test Framework
Tests MCP integration across VSCode, JetBrains, Vim, and Emacs platforms
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MultiPlatformMCPTester:
    """Test framework for multi-platform MCP integration"""

    def __init__(self, interface_bridge_url: str = "http://localhost:8000"):
        self.interface_bridge_url = interface_bridge_url
        self.test_results = {}
        self.aios_root = Path(__file__).parent.parent.parent

    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive multi-platform tests"""
        logger.info("Starting multi-platform MCP integration tests...")

        self.test_results = {
            "timestamp": time.time(),
            "interface_bridge": self.test_interface_bridge(),
            "platforms": {}
        }

        # Test each platform
        platforms = {
            "vscode": self.test_vscode_integration,
            "jetbrains": self.test_jetbrains_integration,
            "vim": self.test_vim_integration,
            "emacs": self.test_emacs_integration
        }

        for platform_name, test_func in platforms.items():
            logger.info(f"Testing {platform_name} integration...")
            try:
                self.test_results["platforms"][platform_name] = test_func()
            except Exception as e:
                logger.error(f"Failed to test {platform_name}: {e}")
                self.test_results["platforms"][platform_name] = {
                    "status": "error",
                    "error": str(e)
                }

        # Add summary
        self.test_results["summary"] = self.generate_summary()
        return self.test_results

    def test_interface_bridge(self) -> Dict[str, Any]:
        """Test Interface Bridge connectivity and functionality"""
        results = {
            "connectivity": False,
            "tools_discovery": False,
            "mcp_servers": {},
            "consciousness_metrics": False
        }

        try:
            # Test health endpoint
            health_url = f"{self.interface_bridge_url}/health"
            health_response = requests.get(health_url, timeout=5)
            results["connectivity"] = health_response.status_code == 200

            if results["connectivity"]:
                # Test tools discovery
                tools_url = f"{self.interface_bridge_url}/tools"
                tools_response = requests.get(tools_url, timeout=5)
                if tools_response.status_code == 200:
                    tools_data = tools_response.json()
                    results["tools_discovery"] = len(tools_data) > 0

                    # Analyze MCP servers
                    server_tools = {}
                    for tool in tools_data:
                        server = tool.get("server", "unknown")
                        if server not in server_tools:
                            server_tools[server] = []
                        server_tools[server].append(tool)

                    for server_name, tools in server_tools.items():
                        results["mcp_servers"][server_name] = {
                            "tools_count": len(tools),
                            "status": "available"
                        }

                # Test consciousness metrics
                try:
                    metrics_url = (f"{self.interface_bridge_url}/"
                                 "consciousness/metrics")
                    metrics_response = requests.get(metrics_url, timeout=5)
                    results["consciousness_metrics"] = \
                        metrics_response.status_code == 200
                except Exception:
                    results["consciousness_metrics"] = False

        except Exception as e:
            logger.error(f"Interface Bridge test failed: {e}")

        return results

    def test_vscode_integration(self) -> Dict[str, Any]:
        """Test VSCode extension MCP integration"""
        results = {
            "extension_exists": False,
            "build_status": False,
            "mcp_client": False,
            "configuration": False
        }

        vscode_ext_path = self.aios_root / "vscode-extension"

        # Check if extension exists
        results["extension_exists"] = vscode_ext_path.exists()

        if results["extension_exists"]:
            # Check package.json
            package_json = vscode_ext_path / "package.json"
            if package_json.exists():
                with open(package_json) as f:
                    config = json.load(f)
                    contributes = config.get("contributes", {})
                    mcp_config = contributes.get("configuration", [])
                    results["configuration"] = any(
                        "aios.mcp" in str(item) for item in mcp_config)

            # Check MCP client
            mcp_client = vscode_ext_path / "src" / "mcpClient.ts"
            results["mcp_client"] = mcp_client.exists()

            # Check build status (look for dist directory)
            dist_dir = vscode_ext_path / "dist"
            results["build_status"] = dist_dir.exists() and any(dist_dir.iterdir())

        return results

    def test_jetbrains_integration(self) -> Dict[str, Any]:
        """Test JetBrains plugin MCP integration"""
        results = {
            "plugin_exists": False,
            "kotlin_sources": False,
            "gradle_build": False,
            "plugin_descriptor": False
        }

        jetbrains_path = self.aios_root / "multi_platform" / "jetbrains"

        # Check if plugin exists
        results["plugin_exists"] = jetbrains_path.exists()

        if results["plugin_exists"]:
            # Check Kotlin sources
            kotlin_src = jetbrains_path / "src" / "main" / "kotlin"
            results["kotlin_sources"] = kotlin_src.exists() and \
                                      any(kotlin_src.rglob("*.kt"))

            # Check Gradle build
            build_gradle = jetbrains_path / "build.gradle"
            results["gradle_build"] = build_gradle.exists()

            # Check plugin descriptor
            plugin_xml_path = (jetbrains_path / "src" / "main" /
                             "resources" / "META-INF" / "plugin.xml")
            results["plugin_descriptor"] = plugin_xml_path.exists()

        return results

    def test_vim_integration(self) -> Dict[str, Any]:
        """Test Vim/Neovim plugin MCP integration"""
        results = {
            "plugin_exists": False,
            "vim_script": False,
            "autoload": False,
            "documentation": False
        }

        vim_path = self.aios_root / "multi_platform" / "vim"

        # Check if plugin exists
        results["plugin_exists"] = vim_path.exists()

        if results["plugin_exists"]:
            # Check Vim script
            plugin_vim = vim_path / "plugin" / "aios_mcp.vim"
            results["vim_script"] = plugin_vim.exists()

            # Check autoload
            autoload_vim = vim_path / "autoload" / "aios_mcp.vim"
            results["autoload"] = autoload_vim.exists()

            # Check documentation
            readme = vim_path / "README.md"
            results["documentation"] = readme.exists()

        return results

    def test_emacs_integration(self) -> Dict[str, Any]:
        """Test Emacs package MCP integration"""
        results = {
            "package_exists": False,
            "emacs_lisp": False,
            "documentation": False,
            "package_headers": False
        }

        emacs_path = self.aios_root / "multi_platform" / "emacs"

        # Check if package exists
        results["package_exists"] = emacs_path.exists()

        if results["package_exists"]:
            # Check Emacs Lisp file
            el_file = emacs_path / "aios-mcp.el"
            results["emacs_lisp"] = el_file.exists()

            if results["emacs_lisp"]:
                # Check package headers
                with open(el_file) as f:
                    content = f.read()
                    header_check = ";;; aios-mcp.el ---" in content
                    requires_check = ";; Package-Requires:" in content
                    results["package_headers"] = header_check and requires_check

            # Check documentation
            readme = emacs_path / "README.md"
            results["documentation"] = readme.exists()

        return results

    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        platforms = self.test_results.get("platforms", {})
        interface_bridge = self.test_results.get("interface_bridge", {})

        summary = {
            "overall_status": "unknown",
            "interface_bridge_status": "operational" if
                interface_bridge.get("connectivity") else "failed",
            "platforms_tested": len(platforms),
            "platforms_successful": 0,
            "total_tests": 0,
            "passed_tests": 0
        }

        for platform_name, platform_results in platforms.items():
            if isinstance(platform_results, dict) and \
               platform_results.get("status") != "error":
                summary["platforms_successful"] += 1

                # Count individual tests
                for test_name, test_result in platform_results.items():
                    if isinstance(test_result, bool):
                        summary["total_tests"] += 1
                        if test_result:
                            summary["passed_tests"] += 1

        # Calculate overall status
        ib_status = summary["interface_bridge_status"]
        platforms_successful = summary["platforms_successful"]
        if ib_status == "operational" and platforms_successful > 0:
            total_tests = summary["total_tests"]
            passed_tests = summary["passed_tests"]
            success_rate = passed_tests / total_tests if total_tests > 0 else 0
            if success_rate >= 0.8:
                summary["overall_status"] = "excellent"
            elif success_rate >= 0.6:
                summary["overall_status"] = "good"
            else:
                summary["overall_status"] = "needs_improvement"
        else:
            summary["overall_status"] = "failed"

        return summary

    def save_results(self, output_file: Optional[str] = None) -> str:
        """Save test results to file"""
        if output_file is None:
            timestamp = int(time.time())
            output_file = f"multi_platform_mcp_test_results_{timestamp}.json"

        output_path = self.aios_root / "runtime_intelligence" / "logs" / output_file

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)

        logger.info(f"Test results saved to: {output_path}")
        return str(output_path)


def main():
    """Main test execution"""
    tester = MultiPlatformMCPTester()

    print("AIOS Multi-Platform MCP Integration Test Framework")
    print("=" * 55)

    results = tester.run_all_tests()
    output_file = tester.save_results()

    print("\nTest Results Summary:")
    summary = results['summary']
    print(f"Overall Status: {summary['overall_status'].upper()}")
    print(f"Interface Bridge: {summary['interface_bridge_status'].upper()}")
    print(f"Platforms Tested: {summary['platforms_tested']}")
    print(f"Platforms Successful: {summary['platforms_successful']}")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed Tests: {summary['passed_tests']}")
    print(f"Results saved to: {output_file}")

    # Print platform details
    print("\nPlatform Details:")
    for platform_name, platform_results in results.get("platforms", {}).items():
        status = "SUCCESS" if platform_results.get("status") != "error" else "ERROR"
        print(f"  {platform_name}: {status}")


if __name__ == "__main__":
    main()