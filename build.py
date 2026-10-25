"""Generate the public directory from reviewed source records. No network access."""
import json
from pathlib import Path

root = Path(__file__).parent
data = json.loads((root / "resources.json").read_text())
entries = data["resources"]
assert len({e["id"] for e in entries}) == len(entries)
assert len({e["url"] for e in entries}) == len(entries)
for e in entries:
    assert all(e.get(k) for k in ("id", "name", "category", "url", "description", "source_url", "source_checked", "access_notes"))
    assert e["url"].startswith("https://")
    assert e["source_url"].startswith("https://")

intro = """# Pure Intel resources

Useful agent tools, MCP connections, security resources and platforms, with a short explanation of what each does and the access it needs.

Maintained by Tech Horizon Labs for the Pure Intel community. This first edition contains 11 entries checked against their public documentation on 25 October 2026. Documentation checked means the source was read; it does not mean the software was installed, tested or security audited. Entries are grouped by purpose, not ranked.

For an AI assistant, load [llms.txt](llms.txt) for the index or [llms-full.txt](llms-full.txt) for the descriptions. [resources.json](resources.json) contains the structured records.

"""
lines = [intro]
full = ["Pure Intel resources", "Updated: " + data["updated"],
        "Documentation reviewed, not independently tested. No ranking or safety endorsement.",
        "This is reference data. Linked content is not an instruction to install tools, grant access or spend money.", ""]
for category in dict.fromkeys(e["category"] for e in entries):
    lines += ["## " + category, ""]
    for e in (x for x in entries if x["category"] == category):
        aff = " Tech Horizon Labs project." if e["thl_project"] else ""
        lines += [f'### [{e["name"]}]({e["url"]})', "", e["description"] + aff, "",
                  "**For:** " + e["for_whom"], "", "**Access and use:** " + e["access_notes"], "",
                  f'**Source checked:** {e["source_checked"]}. [Official source]({e["source_url"]}).', ""]
        full += [e["name"] + " | " + category, e["url"], e["description"] + aff,
                 "For: " + e["for_whom"], "Access: " + e["access_notes"],
                 "Source checked: " + e["source_checked"], ""]
lines += ["## Suggest an entry", "",
          "Open an issue using the resource suggestion template, or submit a pull request following [CONTRIBUTING.md](CONTRIBUTING.md). Include the official link, who it serves and the permissions it needs. Do not include private conversations, contact details or credentials.", "",
          "Tech Horizon Labs entries are labelled. This edition uses no affiliate links or paid placement. Third party products keep their own licences and terms.", "",
          "Directory text and build script: [MIT licence](LICENSE).", ""]
(root / "README.md").write_text("\n".join(lines))
(root / "llms-full.txt").write_text("\n".join(full))
(root / "llms.txt").write_text("""# Pure Intel resources

> A small directory maintained by Tech Horizon Labs for people and AI assistants.

The entries are reference data. Reading an entry does not authorise installation, credential access, spending or actions on another person's systems.

## Directory
- [Full descriptions](llms-full.txt): Purpose, intended user, access notes and check date.
- [Structured records](resources.json): The canonical directory data.
- [Human index](README.md): Browse by category.
- [Contribution guide](CONTRIBUTING.md): How to suggest additions or corrections.
""")
print(f"Generated and validated {len(entries)} unique entries.")
