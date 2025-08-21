
## AIOS_AGENT_PROTOCOL_COMPACT (AINLP-Compressed v2)
Purpose: Machine-ingestible governance + coherence + ledger rules. Audience: AI automation (NOT human narrative). Non-normative prose removed.

```
meta:
	version: 2
	format: yaml-block
	updated: 2025-08-20T00:00:00Z
	source_of_truth: true
	do_not_expand: true

policy.file_creation:
	root_new_files: forbid
	placement_order: [reuse_inject, module_subfolder, docs_or_scripts, NEVER_root]
	self_interrogation: [can_inject?, optimal_non_root_location?]
	traceability: changes_must_be_logged_existing_doc: true

coherence.score:
	base: 0.5
	adds:
		read_symbol_usages: +0.2
		opened_module_docs_or_tests: +0.2
		governance_capsule_checked: +0.1
	subs:
		single_file_focus_gt3_edits_no_search: -0.3
		api_change_no_usage_scan: -0.2
		path_convention_risk: -0.1
	thresholds:
		discover: <0.4
		cautious: 0.4-0.7
		proceed: >0.7

coherence.fast_signals:
	LFC_high_GPC_low: [many_edits_one_file, no_workspace_searches, path_divergence]
	LFC_low: [first_touch_file, unknown_symbols, no_recent_reads]

discovery.sequence: [symbols_perimeter, module_context, governance_context, observability_paths]

edit_gates:
	api_or_path_change: {require_usage_scan: true, min_impacted_call_sites: 1, require_doc_or_test_update: true}
	file_create_move: {enforce_reuse_first: true, require_changelog_entry: true}

tooling.guidance:
	search: targeted
	read_chunks_prefer: 150-300_lines
	tests_path: ai/tests
	fast_validation: encouraged

recall.recenter_triggers: [>=3_edits_without_search, touch_new_unseen_file]

ledger.ids:
	pattern: '[A-Z]{3,4}-[A-Z]+-\d{2}'
	examples: [CEL-INT-01, CEL-OBS-02]

ledger.sections_required: [Active Focus Ledger, Open Loops, Invariants]

ledger.commit_message:
	pattern: '<prefix>(<scope>)[<ID>] message'
	example: 'refactor(cells)[CEL-INT-01] Introduce training cell registry'

ledger.refactor_journal.schema_fields: [generated_at, focus_id, modified_paths, open_loops_remaining, invariants_breaches]

ledger.rules:
	must_register_before_edit: true
	single_active_loop_per_subsystem: true
	completion_marks_done_append_only: true
	abandonment_mark_deferred_no_delete: true
	stale_heartbeat_hours: 48

invariants.default:
	- no_new_code_in_migration_dirs
	- exports_require_deterministic_hash
	- demos_outside_production_modules

governance.integration:
	pre_commit: optional_id_tag_warning
	telemetry: ingest_refactor_journal_future
	context_reindex: stale_focus_failure_enabled

metrics.candidates:
	- duplication_hash_count
	- cross_layer_imports
	- migration_import_events
	- dependency_file_divergence
	- test_layer_coverage

actions.before_edit:
	- verify_ledger_focus_present
	- ensure_change_maps_to_ID
	- compute_coherence_score

actions.after_cohesive_patch:
	- emit_refactor_journal_snapshot
	- update_active_focus_heartbeat

failure_modes:
	silent_scope_creep: mitigation=hook_warning + ledger_update_required
	stale_focus: mitigation=stale_heartbeat_gate
	provenance_loss: mitigation=deterministic_hash_enforcement
	doc_fragmentation: mitigation=single_append_only_ledger

power_shell_shortcuts:
	root_clutter_enum: "Get-ChildItem -LiteralPath . -File -Filter 'test_*.py' | Select Name,Length"
	confirm_delete_absence: "(Test-Path .\\test_chatgpt_integration.py) -eq $false"
	size_json_sum: "Get-Item runtime_intelligence\\logs\\aios_context\\*.json | Measure-Object Length -Sum"

enforcement.summary:
	must_apply_before_output: true
	reject_new_root_files: true
	prefer_injection: true
	reindex_required_after_rules_version_bump: true

notes:
	- This compressed block supersedes verbose legacy instructions.
	- Do not expand prose; extend via additive keys only.
	- Removal of keys requires governance review.

testing.strategy:
	phases: [micro_test, decoherence_scan, targeted_refactor, integration_pass, ingest_and_deprecate]
	micro_test.definition: "Focused, minimal test validating a new seam or contract; candidate for later deprecation"
	decoherence_scan.inputs: [duplication_hash_count, cross_layer_imports, migration_import_events]
	refactor.trigger_thresholds:
		duplication_hash_count: ">0"
		cross_layer_imports: ">0"
	migration_test_policy: "no_new_tests under ainlp_migration; only moves or deletions"
	ephemeral_tests.marker: "pytest.mark.ephemeral"
	deprecation.rule: "Remove ephemeral tests after contract stabilized & integration tests cover behavior"
	telemetry.emit_metrics: true
	test_count_balance.max_ephemeral_ratio: 0.4

file_deletion.protocol:
	verification_steps:
		- attempt_workspace_delete
		- powershell_confirm: "(Test-Path <path>) -eq $false"
		- fallback_remove: "Remove-Item -LiteralPath <path> -Force"
	delete_guard.conditions:
		- referenced_in_recent_changes: warn_only
		- matches_temp_pattern: allow
	temp_patterns: ["_tmp_*.py", "*_scratch.py"]
	log_deletion_event: true

invariants.enforced_dynamic:
	- ephemeral_tests_ratio_within_bounds
	- deterministic_model_hash_present

learned.behaviors:
	file_deletion_verified_protocol_v1:
		context: "Temp smoke test script deletion required multi-attempt; automatic patch deletion failed, PowerShell Remove-Item succeeded."
		steps: [attempt_workspace_delete, search_confirm_absence, powershell_remove_if_present, second_confirm]
		status: adopted
		applies_to: ["_tmp_*.py", "*_scratch.py"]

file_criticality.schema:
	fields: [path, criticality_score, tier, stability_tier, ownership, last_reviewed, deprecation_stage, coupling_degree, coverage_band, security_flag, runtime_touch_freq]
	tier.mapping:
		core: 'score>=90'
		high: '75<=score<90'
		medium: '40<=score<75'
		low: 'score<40'
	precision.support: dynamic_float_precision
	precision.modes: [int, tenths, hundredths, synthetic_quantum]
	synthetic_quantum.definition: "Arbitrary precision layering to express emergent shifts; AI engines may adjust score with rationale log."

file_criticality.scoring_inputs:
	fan_in: import_reference_count
	fan_out: dependency_out_degree
	churn_90d: commits_last_90d
	blast_radius: transitive_dependents_count
	coverage_pct: test_coverage_percent
	security_flag: binary_sensitive_or_secret_risk
	runtime_touch_freq: prod_runtime_invocations
	stability_weight: stability_tier_modifier
	refactor_confidence: recent_refactor_quality_index

file_criticality.formula.v1: "score = w1*fan_in_n + w2*blast_radius_n + w3*security_flag + w4*(1-coverage_n) + w5*runtime_touch_n + w6*stability_weight - w7*refactor_confidence_n"
file_criticality.weights.v1: {w1:0.18,w2:0.15,w3:0.20,w4:0.12,w5:0.15,w6:0.12,w7:0.08}
file_criticality.dynamic_adjustments:
	- trigger: new_framework_dependency
	  delta: +2.5
	  rationale_log: true
	- trigger: superseded_by_new_architecture
	  delta: -5.0
	  require_review: true
	- trigger: security_incident_reference
	  delta: +10.0
	  escalate: true

file_criticality.index:
	storage: governance/file_criticality_index.jsonl
	authoritative: true
	update_path: runtime_intelligence/tools/generate_file_scores.py
	telemetry_emit: runtime_intelligence/logs/file_scores/latest.json

file_criticality.lifecycle_gates:
	core: [proposal_doc, dual_review, impact_simulation, staged_deprecation]
	high: [impact_scan, announce_window, single_review]
	medium: [fast_path_review]
	low: [fast_delete_protocol]

deprecation.stages: [announce, warn_runtime, soft_block, hard_block, removed]
deprecation.durations.default: {announce:14d, warn_runtime:14d, soft_block:14d, hard_block:0d}
deprecation.runtime_enforcement:
	soft_block: warning_on_import
	hard_block: ImportError_with_guidance

coherence.integration.file_scores:
	pr_comment.attach_scores: top_changed_paths
	over_threshold_alert: core_or_high_deleted_without_gate
	metrics: [avg_score_delta, high_score_changed_count]

ai_feedback_loop.file_scores:
	emergent_reassessment.enabled: true
	emergent_reassessment.triggers: [fan_in_spike, runtime_touch_spike, coverage_drop, new_security_annotation]
	emergent_reassessment.log: runtime_intelligence/logs/file_scores/reassessments.jsonl

governance.enforcement_hooks_extensions:
	pre_commit: score_lookup_warn_if_core_modified_without_ID
	pre_push: block_core_file_deletion_without_deprecation_stage

invariants.file_criticality:
	- core_files_require_dual_review
	- dynamic_adjustments_require_rationale
	- synthetic_precision_changes_logged
```

END_PROTOCOL

