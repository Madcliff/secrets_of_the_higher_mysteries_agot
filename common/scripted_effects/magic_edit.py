import re

SUCCESS_WEIGHT = 75
FAILURE_WEIGHT = 25

def wrap_shadow_effects(text):
    pattern = re.compile(
        r'(zz_valyria_magic_water_magic_(\d+)_effect\s*=\s*\{)',
        re.MULTILINE
    )

    output = []
    idx = 0

    for match in pattern.finditer(text):
        start = match.start()
        output.append(text[idx:start])

        header = match.group(1)
        spell_id = match.group(2)

        # Find matching closing brace for this block
        brace_count = 0
        i = match.end()

        while i < len(text):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                if brace_count == 0:
                    break
                brace_count -= 1
            i += 1

        block_body = text[match.end():i].strip()

        # Detect indentation
        indent_match = re.search(r'(\n[ \t]*)\S', text[start:])
        indent = indent_match.group(1) if indent_match else "\n\t"

        # Build wrapped block
        wrapped = f"""{header}
\trandom_list = {{
\t\t{SUCCESS_WEIGHT} = {{
{indent}\t\tmodifier = {{ add = zz_valyria_magic_$SPELLSCHOOL$_$SPELL$_value }}

{indent}{block_body}

\t\t}}
\t\t{FAILURE_WEIGHT} = {{
\t\t\tzz_valyria_magic_spell_failure_interface = {{ SPELLSCHOOL = $SPELLSCHOOL$ SPELL = $SPELL$}}
\t\t}}
\t}}
}}"""

        output.append(wrapped)
        idx = i + 1

    output.append(text[idx:])
    return "".join(output)


if __name__ == "__main__":
    input_file = "magic_effects.txt"
    output_file = "magic_effects_wrapped.txt"

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = wrap_shadow_effects(content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Done. Wrapped effects written to:", output_file)
