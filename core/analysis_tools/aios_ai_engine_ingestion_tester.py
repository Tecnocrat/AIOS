#!/usr/bin/env python3
"""
🧠 AIOS AI Engine Ingestion Tester
====================================
Test assembler capabilities for AI engine ingestion and intelligence integration.

This tool validates how well the assembler outputs can be ingested and processed
by AI engines, measuring compatibility, understanding, and actionable intelligence.
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Any, Tuple
from pathlib import Path
import subprocess
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIOSAIEngineIngestionTester:
    """Test assembler outputs for AI engine compatibility and intelligence extraction."""
    
    def __init__(self, core_dir: str = None):
        """Initialize the AI engine ingestion tester."""
        self.core_dir = core_dir or os.getcwd()
        self.assembler_paths = {
            'iter2': os.path.join(self.core_dir, 'evolutionary_assembler_iter2'),
            'iter3': os.path.join(self.core_dir, 'evolutionary_assembler_iter3')
        }
        
        # AI Engine Intelligence Metrics
        self.intelligence_metrics = {
            'code_understanding': 0.0,      # How well AI can understand generated code
            'logic_coherence': 0.0,         # Logical flow and consistency
            'pattern_recognition': 0.0,     # Recognizable patterns and conventions
            'semantic_clarity': 0.0,        # Semantic meaning and intent clarity
            'documentation_quality': 0.0,   # Documentation and comments quality
            'actionable_insights': 0.0,     # Actionable intelligence for AI systems
            'modularity_score': 0.0,        # Modular design for AI processing
            'integration_readiness': 0.0    # Ready for AI engine integration
        }
        
        self.test_results = {}
        
    def run_assembler_and_capture(self, assembler_path: str, iteration_name: str) -> Dict[str, Any]:
        """Run assembler and capture outputs for AI engine analysis."""
        logger.info(f"🧬 Running {iteration_name} assembler for AI engine ingestion test...")
        
        # Find the main assembler file (search recursively)
        main_files = []
        for root, dirs, files in os.walk(assembler_path):
            for file in files:
                if file.startswith('aios_evolutionary_assembler') and file.endswith('.py'):
                    main_files.append(os.path.join(root, file))
        
        if not main_files:
            logger.error(f"❌ No assembler file found in {assembler_path}")
            return {}
        
        # Use the most relevant assembler file (prefer coherent for iter3, enhanced for iter2)
        if iteration_name == 'iter3':
            assembler_script = next((f for f in main_files if 'coherent' in f), main_files[0])
        elif iteration_name == 'iter2':
            assembler_script = next((f for f in main_files if 'enhanced' in f), main_files[0])
        else:
            assembler_script = main_files[0]
        
        try:
            # Capture assembler output
            result = subprocess.run(
                [sys.executable, assembler_script],
                cwd=os.path.dirname(assembler_script),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Log details for debugging
            logger.info(f"   🔧 Executed: {assembler_script}")
            logger.info(f"   📁 Working dir: {os.path.dirname(assembler_script)}")
            logger.info(f"   📊 Return code: {result.returncode}")
            
            if result.stderr:
                logger.warning(f"   ⚠️ Stderr: {result.stderr[:200]}...")
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0,
                'script_path': assembler_script
            }
        except subprocess.TimeoutExpired:
            logger.warning(f"⚠️ {iteration_name} assembler timed out")
            return {'success': False, 'error': 'timeout'}
        except Exception as e:
            logger.error(f"❌ Error running {iteration_name} assembler: {e}")
            return {'success': False, 'error': str(e)}
    
    def analyze_code_understanding(self, output: str) -> float:
        """Analyze how well AI can understand the generated code structure."""
        understanding_indicators = [
            r'class\s+\w+',                    # Class definitions
            r'def\s+\w+',                      # Function definitions
            r'import\s+\w+',                   # Import statements
            r'#.*',                            # Comments
            r'""".*?"""',                      # Docstrings
            r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',  # Main execution
            r'logging\.',                      # Logging usage
            r'self\.\w+',                      # Object-oriented patterns
        ]
        
        total_score = 0
        for pattern in understanding_indicators:
            matches = len(re.findall(pattern, output, re.MULTILINE | re.DOTALL))
            total_score += min(matches * 0.1, 1.0)  # Cap each indicator at 1.0
        
        return min(total_score / len(understanding_indicators), 1.0)
    
    def analyze_logic_coherence(self, output: str) -> float:
        """Analyze logical flow and consistency in the output."""
        coherence_patterns = [
            r'initialize.*complete',           # Initialization patterns
            r'start.*end|begin.*finish',       # Start-end patterns
            r'try:.*except:',                  # Error handling
            r'if.*else',                       # Conditional logic
            r'for.*in.*:',                     # Iteration patterns
            r'return\s+\w+',                   # Return statements
            r'SUCCESS|COMPLETE|READY',         # Success indicators
            r'step\s+\d+|phase\s+\d+',        # Sequential processing
        ]
        
        coherence_score = 0
        for pattern in coherence_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                coherence_score += 0.125  # Each pattern worth 12.5%
        
        return min(coherence_score, 1.0)
    
    def analyze_pattern_recognition(self, output: str) -> float:
        """Analyze recognizable patterns and conventions."""
        pattern_indicators = [
            r'🧬|🚀|🎯|📊|🔗|⚡|🧠',          # Emoji patterns for structure
            r'=+',                             # Section dividers
            r'INFO|WARNING|ERROR',             # Log levels
            r'Version:\s*\d+\.\d+',            # Version patterns
            r'fitness.*\d+\.\d+',              # Fitness metrics
            r'coherence.*\d+\.\d+',            # Coherence metrics
            r'cycle\s+\d+|generation\s+\d+',  # Evolution cycles
            r'target.*system',                 # Target identification
        ]
        
        pattern_score = 0
        for pattern in pattern_indicators:
            matches = len(re.findall(pattern, output, re.IGNORECASE))
            pattern_score += min(matches * 0.05, 0.125)  # Cap each pattern type
        
        return min(pattern_score, 1.0)
    
    def analyze_semantic_clarity(self, output: str) -> float:
        """Analyze semantic meaning and intent clarity."""
        semantic_indicators = [
            r'assembler|evolution|consciousness',  # Core concepts
            r'optimization|improvement|enhancement',  # Development concepts
            r'coherence|compatibility|integration',   # System concepts
            r'target|goal|objective',                 # Purpose indicators
            r'analysis|assessment|evaluation',        # Process indicators
            r'success|complete|ready|operational',    # Status indicators
            r'generation|iteration|cycle',            # Progression indicators
            r'fitness|performance|metrics',           # Measurement indicators
        ]
        
        semantic_score = 0
        total_words = len(output.split())
        
        for pattern in semantic_indicators:
            matches = len(re.findall(pattern, output, re.IGNORECASE))
            semantic_score += matches
        
        # Normalize by text length
        if total_words > 0:
            semantic_density = semantic_score / total_words
            return min(semantic_density * 50, 1.0)  # Scale appropriately
        
        return 0.0
    
    def analyze_documentation_quality(self, output: str) -> float:
        """Analyze documentation and comments quality."""
        doc_patterns = [
            r'""".*?"""',                      # Docstrings
            r'#.*',                            # Comments
            r'INFO.*',                         # Info messages
            r'📊.*:|🎯.*:|🧬.*:',              # Structured info
            r'Purpose:|Description:|Note:',     # Documentation keywords
            r'Parameters:|Returns:|Args:',      # Function documentation
            r'Example:|Usage:|Demo:',           # Usage documentation
            r'Version|Author|Date',            # Metadata
        ]
        
        doc_score = 0
        for pattern in doc_patterns:
            matches = len(re.findall(pattern, output, re.MULTILINE | re.DOTALL))
            doc_score += min(matches * 0.1, 0.2)  # Cap each pattern type
        
        return min(doc_score, 1.0)
    
    def analyze_actionable_insights(self, output: str) -> float:
        """Analyze actionable intelligence for AI systems."""
        actionable_patterns = [
            r'fitness.*:\s*\d+\.\d+',          # Measurable metrics
            r'coherence.*:\s*\d+\.\d+',        # Coherence values
            r'improvement.*:\s*\d+\.\d+',      # Improvement percentages
            r'readiness.*:\s*\w+',             # Status assessments
            r'next.*iteration|next.*step',      # Next actions
            r'recommendation|suggestion|advice', # Guidance
            r'warning|error|issue',            # Problem identification
            r'optimize|enhance|improve',       # Enhancement opportunities
        ]
        
        actionable_score = 0
        for pattern in actionable_patterns:
            matches = len(re.findall(pattern, output, re.IGNORECASE))
            actionable_score += min(matches * 0.1, 0.15)  # Cap each pattern type
        
        return min(actionable_score, 1.0)
    
    def analyze_modularity_score(self, output: str) -> float:
        """Analyze modular design for AI processing."""
        modularity_indicators = [
            r'class\s+\w+:',                   # Class definitions
            r'def\s+\w+\(.*\):',               # Method definitions
            r'import.*from.*',                 # Module imports
            r'__init__.*\(.*\):',              # Constructors
            r'self\.\w+\s*=',                  # Attribute assignments
            r'return\s+\w+',                   # Return values
            r'@\w+',                           # Decorators
            r'with\s+\w+.*:',                  # Context managers
        ]
        
        modularity_score = 0
        for pattern in modularity_indicators:
            matches = len(re.findall(pattern, output))
            modularity_score += min(matches * 0.08, 0.15)  # Cap each indicator
        
        return min(modularity_score, 1.0)
    
    def analyze_integration_readiness(self, output: str) -> float:
        """Analyze readiness for AI engine integration."""
        integration_indicators = [
            r'operational|ready|complete',     # Operational status
            r'interface|api|endpoint',         # Integration points
            r'json|xml|yaml',                  # Data formats
            r'protocol|standard|convention',   # Standards compliance
            r'compatible|interoperable',       # Compatibility
            r'service|client|server',          # Service architecture
            r'async|await|threading',          # Concurrency support
            r'config|settings|parameters',     # Configurability
        ]
        
        integration_score = 0
        for pattern in integration_indicators:
            matches = len(re.findall(pattern, output, re.IGNORECASE))
            integration_score += min(matches * 0.1, 0.2)  # Cap each indicator
        
        # Bonus for structured output
        if re.search(r'=+|─+|║', output):
            integration_score += 0.1
        
        return min(integration_score, 1.0)
    
    def analyze_ai_intelligence_metrics(self, output: str) -> Dict[str, float]:
        """Analyze all AI intelligence metrics for the output."""
        return {
            'code_understanding': self.analyze_code_understanding(output),
            'logic_coherence': self.analyze_logic_coherence(output),
            'pattern_recognition': self.analyze_pattern_recognition(output),
            'semantic_clarity': self.analyze_semantic_clarity(output),
            'documentation_quality': self.analyze_documentation_quality(output),
            'actionable_insights': self.analyze_actionable_insights(output),
            'modularity_score': self.analyze_modularity_score(output),
            'integration_readiness': self.analyze_integration_readiness(output)
        }
    
    def calculate_overall_ai_compatibility(self, metrics: Dict[str, float]) -> float:
        """Calculate overall AI engine compatibility score."""
        # Weighted importance for different metrics
        weights = {
            'code_understanding': 0.15,
            'logic_coherence': 0.15,
            'pattern_recognition': 0.10,
            'semantic_clarity': 0.15,
            'documentation_quality': 0.10,
            'actionable_insights': 0.15,
            'modularity_score': 0.10,
            'integration_readiness': 0.10
        }
        
        weighted_score = sum(metrics[metric] * weights[metric] for metric in metrics)
        return weighted_score
    
    def test_assembler_ai_compatibility(self, iteration_name: str) -> Dict[str, Any]:
        """Test a specific assembler iteration for AI engine compatibility."""
        assembler_path = self.assembler_paths.get(iteration_name)
        if not assembler_path or not os.path.exists(assembler_path):
            logger.error(f"❌ Assembler path not found: {assembler_path}")
            return {}
        
        logger.info(f"🔬 Testing {iteration_name} assembler for AI engine ingestion...")
        
        # Run assembler and capture output
        execution_result = self.run_assembler_and_capture(assembler_path, iteration_name)
        if not execution_result.get('success', False):
            logger.error(f"❌ {iteration_name} assembler execution failed")
            return execution_result
        
        # Analyze AI intelligence metrics
        output_text = execution_result['stdout']
        intelligence_metrics = self.analyze_ai_intelligence_metrics(output_text)
        overall_compatibility = self.calculate_overall_ai_compatibility(intelligence_metrics)
        
        return {
            'iteration': iteration_name,
            'execution_success': True,
            'intelligence_metrics': intelligence_metrics,
            'overall_ai_compatibility': overall_compatibility,
            'output_length': len(output_text),
            'output_sample': output_text[:500] + "..." if len(output_text) > 500 else output_text
        }
    
    def run_comprehensive_ai_ingestion_test(self) -> Dict[str, Any]:
        """Run comprehensive AI engine ingestion test on all assembler iterations."""
        logger.info("🧠 STARTING COMPREHENSIVE AI ENGINE INGESTION TEST")
        logger.info("=" * 70)
        
        test_results = {}
        
        # Test each available assembler iteration
        for iteration in ['iter2', 'iter3']:
            logger.info(f"\n🔬 Testing {iteration} assembler...")
            result = self.test_assembler_ai_compatibility(iteration)
            test_results[iteration] = result
            
            if result.get('execution_success'):
                logger.info(f"✅ {iteration} AI compatibility: {result['overall_ai_compatibility']:.3f}")
                
                # Log top metrics
                metrics = result['intelligence_metrics']
                top_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)[:3]
                logger.info(f"   🎯 Top metrics: {', '.join([f'{k}: {v:.3f}' for k, v in top_metrics])}")
            else:
                logger.error(f"❌ {iteration} assembler test failed")
        
        # Generate comparative analysis
        if len(test_results) > 1:
            logger.info("\n📊 COMPARATIVE AI INTELLIGENCE ANALYSIS:")
            self._generate_comparative_analysis(test_results)
        
        # Generate recommendations
        self._generate_ai_integration_recommendations(test_results)
        
        self.test_results = test_results
        return test_results
    
    def _generate_comparative_analysis(self, test_results: Dict[str, Any]):
        """Generate comparative analysis between assembler iterations."""
        iterations = [k for k in test_results.keys() if test_results[k].get('execution_success')]
        
        if len(iterations) < 2:
            return
        
        logger.info("   🔗 Inter-iteration AI compatibility comparison:")
        
        # Compare overall compatibility
        compatibilities = {iter_name: test_results[iter_name]['overall_ai_compatibility'] 
                          for iter_name in iterations}
        best_iter = max(compatibilities.keys(), key=lambda k: compatibilities[k])
        
        logger.info(f"   🏆 Best AI compatibility: {best_iter} ({compatibilities[best_iter]:.3f})")
        
        # Compare specific metrics
        metrics_comparison = {}
        for metric in self.intelligence_metrics.keys():
            metrics_comparison[metric] = {}
            for iter_name in iterations:
                metrics_comparison[metric][iter_name] = test_results[iter_name]['intelligence_metrics'][metric]
        
        # Find best performing metrics per iteration
        for iter_name in iterations:
            best_metrics = []
            for metric, values in metrics_comparison.items():
                if values[iter_name] == max(values.values()):
                    best_metrics.append(metric)
            
            if best_metrics:
                logger.info(f"   🎯 {iter_name} excels in: {', '.join(best_metrics)}")
    
    def _generate_ai_integration_recommendations(self, test_results: Dict[str, Any]):
        """Generate recommendations for AI engine integration."""
        logger.info("\n🚀 AI ENGINE INTEGRATION RECOMMENDATIONS:")
        
        successful_tests = {k: v for k, v in test_results.items() if v.get('execution_success')}
        
        if not successful_tests:
            logger.info("   ❌ No successful assembler tests - focus on basic functionality first")
            return
        
        # Find the best performing assembler
        best_assembler = max(successful_tests.keys(), 
                           key=lambda k: successful_tests[k]['overall_ai_compatibility'])
        best_score = successful_tests[best_assembler]['overall_ai_compatibility']
        
        logger.info(f"   🏆 Recommended assembler for AI integration: {best_assembler}")
        logger.info(f"   📊 AI compatibility score: {best_score:.3f}")
        
        # Specific recommendations based on metrics
        metrics = successful_tests[best_assembler]['intelligence_metrics']
        
        if metrics['code_understanding'] < 0.7:
            logger.info("   💡 Recommendation: Improve code structure and naming conventions")
        
        if metrics['logic_coherence'] < 0.7:
            logger.info("   💡 Recommendation: Enhance logical flow and error handling")
        
        if metrics['documentation_quality'] < 0.7:
            logger.info("   💡 Recommendation: Add more comprehensive documentation")
        
        if metrics['actionable_insights'] < 0.7:
            logger.info("   💡 Recommendation: Include more measurable metrics and next-step guidance")
        
        if metrics['integration_readiness'] < 0.7:
            logger.info("   💡 Recommendation: Add API interfaces and standardized data formats")
        
        # Overall assessment
        if best_score >= 0.8:
            logger.info("   ✅ EXCELLENT AI compatibility - ready for advanced integration")
        elif best_score >= 0.6:
            logger.info("   ✅ GOOD AI compatibility - suitable for basic integration")
        elif best_score >= 0.4:
            logger.info("   ⚠️ MODERATE AI compatibility - requires optimization before integration")
        else:
            logger.info("   ❌ LOW AI compatibility - significant improvements needed")

def main():
    """Main execution function."""
    print("🧠 AIOS AI Engine Ingestion Tester")
    print("=" * 50)
    print("🔗 Testing assembler capabilities for AI engine ingestion")
    print()
    
    tester = AIOSAIEngineIngestionTester()
    results = tester.run_comprehensive_ai_ingestion_test()
    
    print("\n🎯 AI ENGINE INGESTION TEST COMPLETE!")
    print("=" * 50)
    
    # Summary statistics
    successful_tests = sum(1 for r in results.values() if r.get('execution_success', False))
    total_tests = len(results)
    
    print(f"📊 Test Summary:")
    print(f"   ✅ Successful tests: {successful_tests}/{total_tests}")
    
    if successful_tests > 0:
        avg_compatibility = sum(r['overall_ai_compatibility'] for r in results.values() 
                              if r.get('execution_success', False)) / successful_tests
        print(f"   🧠 Average AI compatibility: {avg_compatibility:.3f}")
        
        best_result = max((r for r in results.values() if r.get('execution_success', False)),
                         key=lambda x: x['overall_ai_compatibility'])
        print(f"   🏆 Best compatibility: {best_result['overall_ai_compatibility']:.3f} ({best_result['iteration']})")
    
    print("\n🚀 AI engine ingestion testing complete!")
    return results

if __name__ == "__main__":
    main()
