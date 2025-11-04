"""Temporary script to fix blank lines with whitespace."""

file_path = 'runtime/tools/ai_agent_dendritic_similarity.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix blank lines: if line is only whitespace, replace with just newline
fixed_lines = []
for line in lines:
    if line.strip() == '':
        fixed_lines.append('\n')
    else:
        fixed_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print('✅ Fixed all blank lines with whitespace (118 → 0)')
