# AIOS AINLP UI Protocol (v0.1)

Purpose: Define a minimal, source-agnostic UI specification so AIOS can generate platform-specific UIs (WebView2 HTML/CSS/JS and WPF XAML) without depending on external component libraries.

## Design goals
- Deterministic: a small schema with explicit roles and accessibility.
- Portable: map to WPF XAML and basic web components (vanilla HTML/CSS/JS).
- Minimal: keep primitives small (Button, Text, Input, Select, List, Section, Grid).
- Accessible: reflect WAI-ARIA roles and labels in the spec.

## Schema (YAML or JSON)
root:
- id: string (slug)
- title: string
- layout: stack | grid
- sections: [Section]

Section:
- id: string
- title: string
- layout: stack | grid
- components: [Component]

Component (discriminated by type):
- type: text | button | input | select | list
- id: string
- label: string
- value: string (for text/input), options: [{label, value}] (for select)
- a11y: { role?: string, ariaLabel?: string, describedBy?: string }
- intent: string (AINLP action name for events like click/submit)
- tokens: { variant?: primary|secondary|ghost, size?: sm|md|lg }

Example: see docs/ui/ainlp_ui_sample.yaml

## Platform mappings
- Web (HTML):
  - layout stack → <section> with flex column; grid → CSS grid with tokenized gaps.
  - a11y: role/aria-* emitted as given.
  - events: data-intent attributes for bridge handlers.
- WPF (XAML):
  - layout stack → StackPanel; grid → Grid with Columns/Rows inferred.
  - a11y: AutomationProperties.Name from label/ariaLabel.
  - events: x:Name + TODO hooks; current v0.1 emits static UI (no code-behind binding yet).

## CLI (v0.1)
python -m ai.src.tools.ui_proto.compiler --in docs/ui/ainlp_ui_sample.yaml --out interface/AIOS.UI/web/generated

Outputs:
- out/web/index.html  (web)
- out/wpf/View.xaml   (wpf)

## Roadmap
- Add data-binding for WPF.
- Add theming tokens file and build-time CSS vars.
- Add event bridge stubs for WebView2 and C#.

— End of AINLP UI Protocol v0.1 —
