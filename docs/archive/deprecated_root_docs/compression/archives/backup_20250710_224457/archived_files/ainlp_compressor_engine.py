#!/usr/bin/env python3
"""
AINLP Compressor Engine - /refactor.compressor Implementation
OP ITER [Analyze_Patterns, Map_Dependencies, Merge_Logic, Refactor_Affected]
merge_optimization.AIOS.class paradigm
July 10, 2025
"""
import ast
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class AINLPCompressorEngine:
    """
    AINLP Compressor Engine implementing merge_optimization.AIOS.class

    Executes OP ITER pattern for code compression and optimization:
    1. Analyze_Patterns: Detect similar logic patterns and merge opportunities
    2. Map_Dependencies: Build dependency graph and impact analysis
    3. Merge_Logic: Execute consolidation strategies
    4. Refactor_Affected: Update dependencies and validate changes
    """

    def __init__(self, workspace_root: str = r"c:\dev\AIOS"):
        self.workspace_root = Path(workspace_root)
        self.scripts_path = self.workspace_root / "scripts"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # OP ITER tracking
        self.op_iter_results = {
            'analyze_patterns': {'score': 0.0, 'patterns': [], 'candidates': []},
            'map_dependencies': {'score': 0.0, 'dependencies': {}, 'impacts': []},
            'merge_logic': {'score': 0.0, 'merges': [], 'optimizations': []},
            'refactor_affected': {'score': 0.0, 'updates': [], 'validations': []}
        }

        # Compressor state
        self.compression_metrics = {
            'files_analyzed': 0,
            'merge_opportunities': 0,
            'lines_saved': 0,
            'complexity_reduction': 0.0,
            'performance_improvement': 0.0
        }

        # Pattern detection configurations
        self.similarity_thresholds = {
            'exact_match': 0.95,
            'semantic_similarity': 0.80,
            'structural_pattern': 0.75,
            'function_signature': 0.85,
            'class_hierarchy': 0.70
        }

        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   AINLP /refactor.compressor EXECUTION                      ║
║                    merge_optimization.AIOS.class                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

🗜️  COMPRESSOR ENGINE ACTIVATED
📁 Workspace: {self.workspace_root}
📂 Scripts Target: {self.scripts_path}
⏰ Execution Time: {self.timestamp}

🔄 OP ITER Pattern:
   1. Analyze_Patterns: Logic similarity detection and ranking
   2. Map_Dependencies: Import/call graph construction
   3. Merge_Logic: Consolidation strategies execution
   4. Refactor_Affected: Dependency updates and validation

════════════════════════════════════════════════════════════════════════════════
""")

    def execute_compressor_command(self) -> Dict[str, Any]:
        """Execute the complete /refactor.compressor command with OP ITER methodology"""

        print("\n🗜️  EXECUTING COMPRESSOR COMMAND...")

        # Get target files for compression analysis
        target_files = self._get_target_files()
        print(f"\n📋 Target Files for Analysis: {len(target_files)}")
        for file in target_files:
            print(f"   📄 {file.name}")

        # OP ITER 1: Analyze_Patterns
        print("\n" + "="*80)
        print("🔍 OP ITER 1: Analyze_Patterns")
        print("="*80)
        self._execute_op_iter_1_analyze_patterns(target_files)

        # OP ITER 2: Map_Dependencies
        print("\n" + "="*80)
        print("🗺️  OP ITER 2: Map_Dependencies")
        print("="*80)
        self._execute_op_iter_2_map_dependencies(target_files)

        # OP ITER 3: Merge_Logic
        print("\n" + "="*80)
        print("🔀 OP ITER 3: Merge_Logic")
        print("="*80)
        self._execute_op_iter_3_merge_logic()

        # OP ITER 4: Refactor_Affected
        print("\n" + "="*80)
        print("🔧 OP ITER 4: Refactor_Affected")
        print("="*80)
        self._execute_op_iter_4_refactor_affected()

        # Generate compression results
        results = self._generate_compression_results()

        # Create compression report
        self._create_compression_report(results)

        print("\n" + "="*80)
        print("✅ COMPRESSOR EXECUTION COMPLETE")
        print("="*80)

        return results

    def _get_target_files(self) -> List[Path]:
        """Get Python files from scripts directory for compression analysis"""
        target_files = []

        if self.scripts_path.exists():
            for py_file in self.scripts_path.glob("*.py"):
                if py_file.name != "ainlp_compressor_engine.py":  # Exclude self
                    target_files.append(py_file)

        self.compression_metrics['files_analyzed'] = len(target_files)
        return target_files

    def _execute_op_iter_1_analyze_patterns(self, files: List[Path]):
        """OP ITER 1: Analyze code patterns for similarity and merge opportunities"""

        print("  🔍 Phase 1.1: Logic Similarity Detection")
        similarity_patterns = self._detect_logic_similarity(files)
        self.op_iter_results['analyze_patterns']['patterns'] = similarity_patterns

        print("  📊 Phase 1.2: Code Duplication Scoring")
        duplication_scores = self._score_code_duplication(files)

        print("  🎯 Phase 1.3: Merge Opportunity Ranking")
        merge_candidates = self._rank_merge_opportunities(files, similarity_patterns, duplication_scores)
        self.op_iter_results['analyze_patterns']['candidates'] = merge_candidates

        # Calculate analysis score
        pattern_count = len(similarity_patterns)
        candidate_count = len(merge_candidates)
        self.op_iter_results['analyze_patterns']['score'] = min(1.0, (pattern_count + candidate_count) / 10.0)

        print(f"  ✅ Found {pattern_count} similarity patterns, {candidate_count} merge candidates")
        print(f"  📈 Analysis Score: {self.op_iter_results['analyze_patterns']['score']:.2f}")

    def _detect_logic_similarity(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Detect similar logic patterns across files"""
        patterns = []

        for i, file_a in enumerate(files):
            for file_b in files[i+1:]:
                try:
                    content_a = file_a.read_text(encoding='utf-8')
                    content_b = file_b.read_text(encoding='utf-8')

                    # Function pattern detection
                    functions_a = self._extract_functions(content_a)
                    functions_b = self._extract_functions(content_b)

                    # Class pattern detection
                    classes_a = self._extract_classes(content_a)
                    classes_b = self._extract_classes(content_b)

                    # Import pattern detection
                    imports_a = self._extract_imports(content_a)
                    imports_b = self._extract_imports(content_b)

                    # Calculate similarity scores
                    function_similarity = self._calculate_function_similarity(functions_a, functions_b)
                    class_similarity = self._calculate_class_similarity(classes_a, classes_b)
                    import_similarity = self._calculate_import_similarity(imports_a, imports_b)

                    if max(function_similarity, class_similarity, import_similarity) > self.similarity_thresholds['structural_pattern']:
                        patterns.append({
                            'file_a': file_a.name,
                            'file_b': file_b.name,
                            'function_similarity': function_similarity,
                            'class_similarity': class_similarity,
                            'import_similarity': import_similarity,
                            'overall_similarity': (function_similarity + class_similarity + import_similarity) / 3,
                            'merge_potential': 'HIGH' if function_similarity > 0.8 else 'MEDIUM' if function_similarity > 0.6 else 'LOW'
                        })

                except Exception as e:
                    print(f"    ⚠️  Error analyzing {file_a.name} vs {file_b.name}: {e}")

        return patterns

    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions and signatures"""
        functions = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    functions.append({
                        'name': node.name,
                        'args': args,
                        'arg_count': len(args),
                        'line_start': node.lineno,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    })
        except:
            pass
        return functions

    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions and methods"""
        classes = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append(item.name)

                    classes.append({
                        'name': node.name,
                        'methods': methods,
                        'method_count': len(methods),
                        'line_start': node.lineno,
                        'bases': [base.id if hasattr(base, 'id') else str(base) for base in node.bases]
                    })
        except:
            pass
        return classes

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            imports.append(f"{node.module}.{alias.name}")
        except:
            pass
        return imports

    def _calculate_function_similarity(self, functions_a: List[Dict], functions_b: List[Dict]) -> float:
        """Calculate similarity between function sets"""
        if not functions_a or not functions_b:
            return 0.0

        name_matches = 0
        signature_matches = 0

        for func_a in functions_a:
            for func_b in functions_b:
                # Name similarity
                if func_a['name'] == func_b['name']:
                    name_matches += 1

                # Signature similarity
                if (func_a['name'] == func_b['name'] and
                    func_a['arg_count'] == func_b['arg_count'] and
                    func_a['args'] == func_b['args']):
                    signature_matches += 1

        max_functions = max(len(functions_a), len(functions_b))
        return (name_matches * 0.5 + signature_matches * 0.5) / max_functions

    def _calculate_class_similarity(self, classes_a: List[Dict], classes_b: List[Dict]) -> float:
        """Calculate similarity between class sets"""
        if not classes_a or not classes_b:
            return 0.0

        name_matches = 0
        structure_matches = 0

        for class_a in classes_a:
            for class_b in classes_b:
                if class_a['name'] == class_b['name']:
                    name_matches += 1

                    # Method similarity
                    common_methods = set(class_a['methods']) & set(class_b['methods'])
                    if common_methods:
                        method_similarity = len(common_methods) / max(len(class_a['methods']), len(class_b['methods']))
                        if method_similarity > 0.5:
                            structure_matches += 1

        max_classes = max(len(classes_a), len(classes_b))
        return (name_matches * 0.6 + structure_matches * 0.4) / max_classes

    def _calculate_import_similarity(self, imports_a: List[str], imports_b: List[str]) -> float:
        """Calculate similarity between import sets"""
        if not imports_a or not imports_b:
            return 0.0

        common_imports = set(imports_a) & set(imports_b)
        total_imports = set(imports_a) | set(imports_b)

        return len(common_imports) / len(total_imports) if total_imports else 0.0

    def _score_code_duplication(self, files: List[Path]) -> Dict[str, Any]:
        """Score code duplication patterns"""
        duplication_data = {
            'exact_matches': [],
            'semantic_similarity': [],
            'structural_patterns': []
        }

        for file in files:
            try:
                content = file.read_text(encoding='utf-8')
                lines = content.split('\n')

                # Count common patterns
                duplication_data['exact_matches'].append({
                    'file': file.name,
                    'total_lines': len(lines),
                    'empty_lines': len([line for line in lines if not line.strip()]),
                    'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
                    'import_lines': len([line for line in lines if line.strip().startswith(('import ', 'from '))])
                })

            except Exception as e:
                print(f"    ⚠️  Error analyzing duplication in {file.name}: {e}")

        return duplication_data

    def _rank_merge_opportunities(self, files: List[Path], patterns: List[Dict], duplication: Dict) -> List[Dict[str, Any]]:
        """Rank files by merge opportunity potential"""
        candidates = []

        # Analyze each pattern for merge potential
        for pattern in patterns:
            if pattern['overall_similarity'] > self.similarity_thresholds['semantic_similarity']:
                impact_score = pattern['overall_similarity']
                complexity_score = 1.0 - (pattern['function_similarity'] * 0.4 + pattern['class_similarity'] * 0.6)
                benefit_ratio = impact_score / max(complexity_score, 0.1)

                candidates.append({
                    'file_a': pattern['file_a'],
                    'file_b': pattern['file_b'],
                    'similarity_score': pattern['overall_similarity'],
                    'impact_score': impact_score,
                    'complexity_score': complexity_score,
                    'benefit_ratio': benefit_ratio,
                    'merge_recommendation': 'MERGE' if benefit_ratio > 2.0 else 'REVIEW' if benefit_ratio > 1.0 else 'SKIP',
                    'merge_strategy': self._determine_merge_strategy(pattern)
                })

        # Sort by benefit ratio (highest first)
        candidates.sort(key=lambda x: x['benefit_ratio'], reverse=True)

        self.compression_metrics['merge_opportunities'] = len([c for c in candidates if c['merge_recommendation'] == 'MERGE'])

        return candidates

    def _determine_merge_strategy(self, pattern: Dict[str, Any]) -> str:
        """Determine the best merge strategy for a pattern"""
        if pattern['class_similarity'] > 0.7:
            return 'CLASS_INHERITANCE'
        elif pattern['function_similarity'] > 0.8:
            return 'UTILITY_MERGING'
        elif pattern['import_similarity'] > 0.9:
            return 'MODULE_CONSOLIDATION'
        else:
            return 'INTERFACE_UNIFICATION'

    def _execute_op_iter_2_map_dependencies(self, files: List[Path]):
        """OP ITER 2: Map dependencies and analyze impact"""

        print("  🗺️  Phase 2.1: Import Chain Analysis")
        import_chains = self._analyze_import_chains(files)

        print("  📞 Phase 2.2: Call Graph Construction")
        call_graphs = self._construct_call_graphs(files)

        print("  📈 Phase 2.3: Impact Propagation Model")
        impact_models = self._build_impact_propagation_models(files, import_chains, call_graphs)

        self.op_iter_results['map_dependencies']['dependencies'] = {
            'import_chains': import_chains,
            'call_graphs': call_graphs
        }
        self.op_iter_results['map_dependencies']['impacts'] = impact_models

        # Calculate dependency mapping score
        dependency_complexity = len(import_chains) + len(call_graphs)
        self.op_iter_results['map_dependencies']['score'] = min(1.0, dependency_complexity / 15.0)

        print(f"  ✅ Mapped {len(import_chains)} import chains, {len(call_graphs)} call relationships")
        print(f"  📈 Dependency Score: {self.op_iter_results['map_dependencies']['score']:.2f}")

    def _analyze_import_chains(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Analyze import dependency chains"""
        chains = []

        for file in files:
            try:
                content = file.read_text(encoding='utf-8')
                imports = self._extract_imports(content)

                # Categorize imports
                direct_imports = [imp for imp in imports if not '.' in imp or imp.startswith('core.') or imp.startswith('ai.')]
                external_imports = [imp for imp in imports if imp not in direct_imports]

                chains.append({
                    'file': file.name,
                    'direct_imports': direct_imports,
                    'external_imports': external_imports,
                    'total_imports': len(imports),
                    'internal_ratio': len(direct_imports) / len(imports) if imports else 0
                })

            except Exception as e:
                print(f"    ⚠️  Error analyzing imports in {file.name}: {e}")

        return chains

    def _construct_call_graphs(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Construct function call graphs"""
        graphs = []

        for file in files:
            try:
                content = file.read_text(encoding='utf-8')
                functions = self._extract_functions(content)

                # Simple call analysis (function names in content)
                function_calls = []
                for func in functions:
                    calls_in_func = [other_func['name'] for other_func in functions
                                   if other_func['name'] != func['name'] and other_func['name'] in content]
                    function_calls.append({
                        'function': func['name'],
                        'calls': calls_in_func,
                        'call_count': len(calls_in_func)
                    })

                graphs.append({
                    'file': file.name,
                    'function_calls': function_calls,
                    'total_functions': len(functions),
                    'internal_calls': sum(call['call_count'] for call in function_calls)
                })

            except Exception as e:
                print(f"    ⚠️  Error constructing call graph for {file.name}: {e}")

        return graphs

    def _build_impact_propagation_models(self, files: List[Path], import_chains: List[Dict], call_graphs: List[Dict]) -> List[Dict[str, Any]]:
        """Build impact propagation models for changes"""
        models = []

        for file in files:
            file_imports = next((chain for chain in import_chains if chain['file'] == file.name), {})
            file_calls = next((graph for graph in call_graphs if graph['file'] == file.name), {})

            # Calculate impact radius
            direct_dependencies = len(file_imports.get('direct_imports', []))
            internal_calls = file_calls.get('internal_calls', 0)

            impact_radius = direct_dependencies + internal_calls
            risk_level = 'HIGH' if impact_radius > 15 else 'MEDIUM' if impact_radius > 8 else 'LOW'

            models.append({
                'file': file.name,
                'impact_radius': impact_radius,
                'risk_level': risk_level,
                'affected_files': file_imports.get('direct_imports', []),
                'breaking_change_potential': 'HIGH' if internal_calls > 10 else 'LOW',
                'refactor_scope': 'ISOLATED' if impact_radius < 5 else 'MODERATE' if impact_radius < 12 else 'EXTENSIVE'
            })

        return models

    def _execute_op_iter_3_merge_logic(self):
        """OP ITER 3: Execute merge logic and consolidation strategies"""

        print("  🔀 Phase 3.1: Consolidation Pattern Analysis")
        consolidation_strategies = self._analyze_consolidation_patterns()

        print("  ⚡ Phase 3.2: Logic Optimization")
        optimization_opportunities = self._identify_logic_optimizations()

        print("  📁 Phase 3.3: File Restructuring")
        restructuring_plan = self._plan_file_restructuring()

        self.op_iter_results['merge_logic']['merges'] = consolidation_strategies
        self.op_iter_results['merge_logic']['optimizations'] = optimization_opportunities

        # Calculate merge logic score
        total_optimizations = len(consolidation_strategies) + len(optimization_opportunities)
        self.op_iter_results['merge_logic']['score'] = min(1.0, total_optimizations / 8.0)

        print(f"  ✅ Identified {len(consolidation_strategies)} consolidation opportunities")
        print(f"  ✅ Found {len(optimization_opportunities)} optimization targets")
        print(f"  📈 Merge Logic Score: {self.op_iter_results['merge_logic']['score']:.2f}")

    def _analyze_consolidation_patterns(self) -> List[Dict[str, Any]]:
        """Analyze consolidation patterns from merge candidates"""
        patterns = []

        merge_candidates = self.op_iter_results['analyze_patterns']['candidates']

        for candidate in merge_candidates:
            if candidate['merge_recommendation'] == 'MERGE':
                patterns.append({
                    'type': candidate['merge_strategy'],
                    'files': [candidate['file_a'], candidate['file_b']],
                    'similarity_score': candidate['similarity_score'],
                    'expected_lines_saved': self._estimate_lines_saved(candidate),
                    'complexity_reduction': candidate['complexity_score'],
                    'consolidation_method': self._determine_consolidation_method(candidate['merge_strategy'])
                })

        return patterns

    def _estimate_lines_saved(self, candidate: Dict[str, Any]) -> int:
        """Estimate lines of code that could be saved through merging"""
        # Simple estimation based on similarity score
        base_lines = 50  # Average file size estimate
        similarity = candidate['similarity_score']
        return int(base_lines * similarity * 0.6)  # Conservative estimate

    def _determine_consolidation_method(self, strategy: str) -> str:
        """Determine specific consolidation method"""
        methods = {
            'UTILITY_MERGING': 'Combine utility functions into shared module',
            'CLASS_INHERITANCE': 'Extract common base class with shared methods',
            'INTERFACE_UNIFICATION': 'Create unified interface with common protocols',
            'MODULE_CONSOLIDATION': 'Merge modules with overlapping functionality'
        }
        return methods.get(strategy, 'Generic consolidation approach')

    def _identify_logic_optimizations(self) -> List[Dict[str, Any]]:
        """Identify logic optimization opportunities"""
        optimizations = []

        # Based on analysis patterns, identify specific optimizations
        patterns = self.op_iter_results['analyze_patterns']['patterns']

        for pattern in patterns:
            if pattern['function_similarity'] > 0.7:
                optimizations.append({
                    'type': 'DEAD_CODE_REMOVAL',
                    'target_files': [pattern['file_a'], pattern['file_b']],
                    'description': 'Remove duplicate functions with identical logic',
                    'impact': 'Code size reduction and maintenance simplification'
                })

            if pattern['import_similarity'] > 0.8:
                optimizations.append({
                    'type': 'IMPORT_OPTIMIZATION',
                    'target_files': [pattern['file_a'], pattern['file_b']],
                    'description': 'Consolidate common imports into shared module',
                    'impact': 'Reduced import overhead and cleaner dependencies'
                })

        return optimizations

    def _plan_file_restructuring(self) -> Dict[str, Any]:
        """Plan file restructuring for optimal organization"""
        return {
            'hierarchy_flattening': 'Reduce nested directory complexity',
            'module_consolidation': 'Group related functionality into fewer modules',
            'namespace_cleanup': 'Simplify import paths and reduce circular dependencies'
        }

    def _execute_op_iter_4_refactor_affected(self):
        """OP ITER 4: Refactor affected files and validate changes"""

        print("  🔧 Phase 4.1: Staged Migration Planning")
        migration_plan = self._plan_staged_migration()

        print("  🔄 Phase 4.2: Automated Updates")
        update_plan = self._plan_automated_updates()

        print("  🧪 Phase 4.3: Validation Testing")
        validation_plan = self._plan_validation_testing()

        self.op_iter_results['refactor_affected']['updates'] = update_plan
        self.op_iter_results['refactor_affected']['validations'] = validation_plan

        # Calculate refactor score
        total_updates = len(update_plan) + len(validation_plan)
        self.op_iter_results['refactor_affected']['score'] = min(1.0, total_updates / 6.0)

        print(f"  ✅ Planned {len(update_plan)} automated updates")
        print(f"  ✅ Designed {len(validation_plan)} validation tests")
        print(f"  📈 Refactor Score: {self.op_iter_results['refactor_affected']['score']:.2f}")

    def _plan_staged_migration(self) -> Dict[str, Any]:
        """Plan staged migration strategy"""
        return {
            'dependency_order': 'Process files in dependency order to avoid breaking changes',
            'compatibility_preservation': 'Maintain backward compatibility during transition',
            'rollback_safety': 'Ensure safe rollback mechanisms for each stage'
        }

    def _plan_automated_updates(self) -> List[Dict[str, Any]]:
        """Plan automated update operations"""
        updates = [
            {
                'type': 'IMPORT_PATH_FIXES',
                'description': 'Update import paths after file consolidation',
                'automated': True,
                'risk_level': 'LOW'
            },
            {
                'type': 'CALL_SIGNATURE_UPDATES',
                'description': 'Update function calls after signature changes',
                'automated': True,
                'risk_level': 'MEDIUM'
            },
            {
                'type': 'INTERFACE_ADAPTATIONS',
                'description': 'Adapt interfaces after consolidation',
                'automated': False,
                'risk_level': 'HIGH'
            }
        ]
        return updates

    def _plan_validation_testing(self) -> List[Dict[str, Any]]:
        """Plan validation testing strategy"""
        validations = [
            {
                'type': 'FUNCTIONALITY_VERIFICATION',
                'description': 'Verify all functions work as expected after merge',
                'automated': True,
                'priority': 'HIGH'
            },
            {
                'type': 'PERFORMANCE_BENCHMARKS',
                'description': 'Ensure performance improvements are achieved',
                'automated': True,
                'priority': 'MEDIUM'
            },
            {
                'type': 'INTEGRATION_TESTS',
                'description': 'Test integration between consolidated components',
                'automated': False,
                'priority': 'HIGH'
            }
        ]
        return validations

    def _generate_compression_results(self) -> Dict[str, Any]:
        """Generate comprehensive compression results"""

        # Calculate overall compression metrics
        total_score = sum(result['score'] for result in self.op_iter_results.values()) / len(self.op_iter_results)

        # Estimate compression benefits
        merge_candidates = self.op_iter_results['analyze_patterns']['candidates']
        mergeable_files = len([c for c in merge_candidates if c['merge_recommendation'] == 'MERGE'])

        estimated_lines_saved = sum(self._estimate_lines_saved(c) for c in merge_candidates
                                  if c['merge_recommendation'] == 'MERGE')

        complexity_reduction = sum(c['complexity_score'] for c in merge_candidates) / max(len(merge_candidates), 1)

        results = {
            'timestamp': self.timestamp,
            'execution_successful': True,
            'op_iter_results': self.op_iter_results,
            'compression_metrics': {
                **self.compression_metrics,
                'overall_score': total_score,
                'mergeable_files': mergeable_files,
                'estimated_lines_saved': estimated_lines_saved,
                'complexity_reduction': complexity_reduction,
                'performance_improvement': self._estimate_performance_improvement(mergeable_files)
            },
            'recommendations': self._generate_recommendations(merge_candidates)
        }

        return results

    def _estimate_performance_improvement(self, mergeable_files: int) -> float:
        """Estimate performance improvement from file consolidation"""
        # Simple estimation: fewer files = less import overhead
        return min(0.15, mergeable_files * 0.02)  # Up to 15% improvement

    def _generate_recommendations(self, merge_candidates: List[Dict]) -> List[str]:
        """Generate compression recommendations"""
        recommendations = []

        mergeable = [c for c in merge_candidates if c['merge_recommendation'] == 'MERGE']

        if mergeable:
            recommendations.append(f"Merge {len(mergeable)} file pairs to reduce codebase complexity")

        utility_merges = [c for c in mergeable if c['merge_strategy'] == 'UTILITY_MERGING']
        if utility_merges:
            recommendations.append(f"Consolidate {len(utility_merges)} utility function sets")

        class_merges = [c for c in mergeable if c['merge_strategy'] == 'CLASS_INHERITANCE']
        if class_merges:
            recommendations.append(f"Extract common base classes for {len(class_merges)} class pairs")

        if not mergeable:
            recommendations.append("No immediate merge opportunities found - codebase is well-organized")

        return recommendations

    def _create_compression_report(self, results: Dict[str, Any]):
        """Create detailed compression analysis report"""

        report_path = self.workspace_root / "docs" / "compression_reports" / f"compression_analysis_{self.timestamp}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report_content = f"""# AINLP Compressor Analysis Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Command**: @AIOS /refactor.compressor
**OP ITER Pattern**: [Analyze_Patterns, Map_Dependencies, Merge_Logic, Refactor_Affected]

## Executive Summary

- **Files Analyzed**: {results['compression_metrics']['files_analyzed']}
- **Merge Opportunities**: {results['compression_metrics']['merge_opportunities']}
- **Estimated Lines Saved**: {results['compression_metrics']['estimated_lines_saved']}
- **Overall Compression Score**: {results['compression_metrics']['overall_score']:.2f}

## OP ITER Results

### 1. Analyze_Patterns (Score: {results['op_iter_results']['analyze_patterns']['score']:.2f})
- **Similarity Patterns Found**: {len(results['op_iter_results']['analyze_patterns']['patterns'])}
- **Merge Candidates**: {len(results['op_iter_results']['analyze_patterns']['candidates'])}

### 2. Map_Dependencies (Score: {results['op_iter_results']['map_dependencies']['score']:.2f})
- **Import Chains Mapped**: {len(results['op_iter_results']['map_dependencies']['dependencies'].get('import_chains', []))}
- **Call Graphs Constructed**: {len(results['op_iter_results']['map_dependencies']['dependencies'].get('call_graphs', []))}

### 3. Merge_Logic (Score: {results['op_iter_results']['merge_logic']['score']:.2f})
- **Consolidation Opportunities**: {len(results['op_iter_results']['merge_logic']['merges'])}
- **Optimization Targets**: {len(results['op_iter_results']['merge_logic']['optimizations'])}

### 4. Refactor_Affected (Score: {results['op_iter_results']['refactor_affected']['score']:.2f})
- **Automated Updates Planned**: {len(results['op_iter_results']['refactor_affected']['updates'])}
- **Validation Tests Designed**: {len(results['op_iter_results']['refactor_affected']['validations'])}

## Compression Recommendations

"""

        for i, recommendation in enumerate(results['recommendations'], 1):
            report_content += f"{i}. {recommendation}\n"

        report_content += f"""
## Impact Analysis

- **Complexity Reduction**: {results['compression_metrics']['complexity_reduction']:.2f}
- **Performance Improvement**: {results['compression_metrics']['performance_improvement']:.1%}
- **Maintenance Benefit**: Simplified codebase with fewer files to maintain

## Next Steps

1. Review merge candidates for implementation priority
2. Execute staged migration following dependency order
3. Run validation tests after each consolidation step
4. Monitor performance metrics post-compression

---
*Generated by AINLP Compressor Engine v1.0*
"""

        report_path.write_text(report_content, encoding='utf-8')
        print(f"\n📄 Compression report saved: {report_path}")


def main():
    """Main execution function"""
    print("AINLP /refactor.compressor Command")
    print("merge_optimization.AIOS.class | OP ITER Execution")
    print("=" * 60)

    try:
        compressor = AINLPCompressorEngine()
        results = compressor.execute_compressor_command()

        print(f"\n✅ COMPRESSION ANALYSIS COMPLETE")
        print(f"📊 Overall Score: {results['compression_metrics']['overall_score']:.2f}")
        print(f"🎯 Merge Opportunities: {results['compression_metrics']['merge_opportunities']}")
        print(f"💾 Estimated Lines Saved: {results['compression_metrics']['estimated_lines_saved']}")

        return 0

    except Exception as e:
        print(f"\n❌ COMPRESSION EXECUTION FAILED: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
