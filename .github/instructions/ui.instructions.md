applyTo: 'interface/**'
---

# AINLP UI Protocol.
- Spec: docs/AIOS/AIOS_UI_PROTOCOL.md
- Sample: docs/ui/ainlp_ui_sample.yaml
- Compiler: python -m ai.src.tools.ui_proto.compiler --in docs/ui/ainlp_ui_sample.yaml --out interface/AIOS.UI/generated

Keep code local by importing only from @/components/ui/*.
Follow accessibility guidance in all UI components.
