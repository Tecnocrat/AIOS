import json
import sys
from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def load_spec(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("pyyaml is required to load YAML specs. Install pyyaml.")
        return yaml.safe_load(text)  # type: ignore[no-any-return]
    return json.loads(text)


def gen_web(spec: Dict[str, Any]) -> str:
    title = spec.get("title", spec.get("id", "AIOS UI"))
    sections = spec.get("sections", [])
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        f'  <meta charset="utf-8"><title>{title}</title>',
        ('  <meta name="viewport" content="width=device-width, ' 'initial-scale=1">'),
        (
            "  <style>body{font-family:system-ui,Segoe UI,Arial,Helvetica,"
            "sans-serif;padding:16px}section{margin:12px 0}label{display:"
            "block;"
            "margin:6px 0 2px}button{margin-top:8px}</style>"
        ),
        "</head>",
        "<body>",
        f"<h1>{title}</h1>",
    ]

    for s in sections:
        label_txt = s.get("title", "Section")
        parts.append(f'<section role="region" aria-label="{label_txt}">')
        if s.get("title"):
            parts.append(f"  <h2>{s['title']}</h2>")
        for c in s.get("components", []):
            t = c.get("type")
            cid = c.get("id", "")
            label = c.get("label", "")
            a11y = c.get("a11y", {})
            intent = c.get("intent", "")
            role = a11y.get("role")
            aria = " ".join(
                f'{k.replace("_", "-")}="{v}"' for k, v in a11y.items() if k != "role"
            )
            data_intent = f' data-intent="{intent}"' if intent else ""
            role_attr = f' role="{role}"' if role else ""
            if t == "text":
                parts.append(
                    f'  <p id="{cid}"{role_attr} {aria}>' f"{c.get('value', '')}</p>"
                )
            elif t == "input":
                parts.append(f'  <label for="{cid}">{label}</label>')
                parts.append(f'  <input id="{cid}" aria-label="{label}" {aria} />')
            elif t == "select":
                parts.append(f'  <label for="{cid}">{label}</label>')
                parts.append(f'  <select id="{cid}" aria-label="{label}" {aria}>')
                for opt in c.get("options", []):
                    parts.append(
                        f"    <option value=\"{opt.get('value', '')}\">"
                        f"{opt.get('label', '')}</option>"
                    )
                parts.append("  </select>")
            elif t == "button":
                parts.append(
                    f'  <button id="{cid}"{role_attr}{data_intent} '
                    f'aria-label="{label}" {aria}>'
                    f"{label or 'Button'}</button>"
                )
            elif t == "list":
                parts.append(f'  <ul id="{cid}" aria-label="{label}" {aria}>')
                for item in c.get("items", []):
                    parts.append(f"    <li>{item}</li>")
                parts.append("  </ul>")
        parts.append("</section>")
    parts.append(
        (
            "<script>document.body.addEventListener('click', e => {const t = "
            "e.target; if (t.dataset.intent) { console.log('intent', "
            "t.dataset.intent); }})</script>"
        )
    )
    parts.append("</body></html>")
    return "\n".join(parts)


def gen_wpf(spec: Dict[str, Any]) -> str:
    # Minimal stub XAML; proper grid/stack not yet implemented in v0.1
    title = spec.get("title", spec.get("id", "AIOS UI"))
    parts = [
        (
            '<UserControl xmlns="http://schemas.microsoft.com/winfx/2006/'
            'xaml/presentation"'
        ),
        ('             xmlns:x="http://schemas.microsoft.com/winfx/2006/' 'xaml"'),
        (f'             x:Class="AIOS.UI.Generated.' f"{spec.get('id', 'View')}\">"),
        '  <StackPanel Margin="16">',
        (f'    <TextBlock Text="{title}" FontSize="20" ' 'Margin="0,0,0,12" />'),
        "  </StackPanel>",
        "</UserControl>",
    ]
    return "\n".join(parts)


def compile_ui(in_path: Path, out_dir: Path) -> None:
    spec = load_spec(in_path)
    out_web = out_dir / "web" / "index.html"
    out_wpf = out_dir / "wpf" / "View.xaml"
    out_web.parent.mkdir(parents=True, exist_ok=True)
    out_wpf.parent.mkdir(parents=True, exist_ok=True)

    out_web.write_text(gen_web(spec), encoding="utf-8")
    out_wpf.write_text(gen_wpf(spec), encoding="utf-8")


def main(argv: list[str]) -> int:
    import argparse

    p = argparse.ArgumentParser(description="AINLP UI Protocol compiler")
    p.add_argument("--in", dest="in_path", required=True, help="Spec file (yaml/json)")
    p.add_argument("--out", dest="out_dir", required=True, help="Output directory root")
    args = p.parse_args(argv)

    in_path = Path(args.in_path)
    out_dir = Path(args.out_dir)
    if not in_path.exists():
        print(f"Spec not found: {in_path}", file=sys.stderr)
        return 2
    try:
        compile_ui(in_path, out_dir)
    except Exception as e:  # pragma: no cover
        print(f"Compile failed: {e}", file=sys.stderr)
        return 1
    print(f"UI generated at {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
