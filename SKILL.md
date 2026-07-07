---
name: obsidian-manage
description: Build, design, organize, import, rename, move, link, date-stamp, index, audit, and maintain personal Obsidian knowledge vaults. Use when the user asks an agent to create a local Obsidian knowledge base, design an AGENTS.md/vault rule system, route notes into folders, manage Markdown notes, maintain navigation pages, rebuild JSONL indexes, or organize an existing Obsidian vault.
---

# Obsidian Manage

Use this skill to build and maintain a personal Obsidian knowledge vault without damaging user-authored notes. It works for a new vault design as well as ongoing maintenance of an existing vault.

## Operating Principles

1. Treat the user's current explicit instruction as highest priority.
2. At the very start of first-time setup, run setup detection in this order: check the Obsidian app, prepare installation guidance if missing, then detect candidate vaults. App detection never decides whether a vault exists; vault detection decides whether to create a new vault or adapt an existing one. On macOS, if Obsidian is missing and Homebrew is available, the agent may offer a Homebrew install command. If both Obsidian and Homebrew are missing, give the user the official download URL instead of trying to download the app directly. Installing software must still use the current environment's approval mechanism; do not perform a silent install.
3. Ask for or infer the vault root before acting. If multiple possible vaults exist, ask the user which one to use.
4. If the vault already has `AGENTS.md`, read it before writing anything.
5. If the vault has system/routing/index documents, read them before doing routing or index work.
6. Inspect the real filesystem before relying on JSONL indexes. The filesystem is the source of truth.
7. If writing outside the current workspace or protected paths, ask for permission or use the available approval mechanism with a clear user-facing justification.

## Safety Rules

- Do not create, move, rename, delete, merge, split, or bulk-edit files unless the user clearly asked for that action or approved the plan.
- Before modifying an existing Markdown file, reread its current content.
- Preserve user-authored body content. Prefer adding metadata/link blocks and changing paths over rewriting prose.
- Never delete user material automatically. Only remove obvious system metadata such as `.DS_Store` when it is part of a user-approved import/cleanup.
- Ask before changing `AGENTS.md`, system-rule folders, index structure, or top-level vault directories unless the user explicitly requested it.

## Detect Obsidian App And Existing Vaults

When the user is unsure whether they already have Obsidian or a vault:

1. Check the Obsidian app first so the user can install it if needed, but use vault detection to decide whether to create a new vault or adapt an existing one. A vault can exist without the app, and the app can exist without a vault.
2. First ask for the intended vault path. If the user does not know it, scan common user folders for candidate vaults.
3. Treat a folder as a candidate vault if it contains `.obsidian/`, `AGENTS.md`, or a meaningful collection of Markdown files.
4. Detecting the Obsidian app is only auxiliary: use it to help the user understand local setup, not to decide whether a vault exists.
5. If existing vaults are found, summarize them and ask the user which one to adapt before changing anything.

Use the bundled script for setup checks and installation guidance:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --detect-app
python3 /path/to/obsidian-manage/scripts/vault_index.py --install-app
python3 /path/to/obsidian-manage/scripts/vault_index.py --install-app --yes-install
python3 /path/to/obsidian-manage/scripts/vault_index.py --find-vaults
python3 /path/to/obsidian-manage/scripts/vault_index.py --find-vaults --search-root /path/to/search
```

`--install-app` is a dry run by default. On macOS, if Obsidian is not installed and `brew` is available, it prints `brew install --cask obsidian`. Add `--yes-install` to actually run that command, after explicit user approval. If Obsidian and Homebrew are both missing, it prints the official download URL: `https://obsidian.md/download` and exits successfully because manual installation guidance is the expected fallback. Do not auto-download DMG files from the website.

## New Vault vs Existing Vault

Before creating a knowledge base, check whether the target path already exists and whether it contains an Obsidian vault (`.obsidian/`, `AGENTS.md`, or existing Markdown folders).

- If no vault exists, propose a new-vault structure and wait for user confirmation before creating folders or rule files.
- If a vault already exists, do not overwrite or recreate it. Treat the task as an existing-vault improvement: audit the current structure, propose incremental changes, and wait for explicit user confirmation before moving, renaming, deleting, or creating rule/navigation/index files.
- When the user says “build a new knowledge base” but the target already has content, state that an existing vault was found and ask whether to adapt it, create a separate new vault, or stop.
- Existing user content always wins over templates. Apply templates only as suggestions or incremental additions after confirmation.

## User-Customizable Template

Use the recommended structure as a default proposal, not a fixed requirement. Before creating or significantly modifying a vault:

1. Present the proposed first-level directory map and key rules.
2. Tell the user they can modify any single item, rename folders, add new areas, remove areas, or change naming/link/index rules.
3. Apply only the confirmed version. If the user changes one part, keep the rest of the default template unless they say otherwise.
4. For existing vaults, present changes as a diff-style proposal: keep, rename, add, remove, move. Do not apply the proposal until the user confirms.
5. If a user asks for an addition/removal later, update the directory map, navigation pages, rules, and indexes consistently after confirmation.

## Design A New Personal Vault

When the user asks to build a personal Obsidian knowledge base, design the system before moving content.

1. Clarify the vault's job: personal knowledge archive, AI working memory, project archive, study notes, writing system, research system, or mixed vault.
2. Propose 6-10 stable first-level areas using the default template when appropriate. Explicitly invite the user to rename, add, remove, or adjust any area.
3. Define each area's purpose, default note types, and what does not belong there; apply only the user-confirmed version.
4. Draft `AGENTS.md` as the vault constitution:
   - highest principles and write safety
   - directory map
   - naming rules
   - date header rules
   - link rules
   - task routing
   - index maintenance
   - actions requiring confirmation
5. Create only first-level navigation pages by default, such as `00-目录名说明.md`. Each page must be written from the confirmed directory name, purpose, allowed note types, exclusion rules, and actual or planned child topics. Do not create identical boilerplate directory descriptions.
6. Add a lightweight index plan only after the folder system is stable.
7. Import existing content in small batches, preserving original meaning and avoiding broad rewrites.

For a reusable vault template and detailed rules, read `references/vault-rules.md`.

## Common Maintenance Workflows

### Import Or Move Materials

1. Inspect the source tree with `find` or `rg --files`.
2. Decide the destination by reading the vault rules and existing nearby folders.
3. Explain the intended destination and any renames before bulk moves.
4. Move/import files only after user approval when the operation is broad or ambiguous.
5. Normalize directory and file names to the vault naming style unless the user explicitly wants original names preserved.
6. Add/update date blocks, `相关入口`, and sibling `相关文档` links.
7. Update the relevant first-level navigation page.
8. Rebuild JSONL indexes or append an index record as appropriate.
9. Verify old paths are gone and new Obsidian links/index entries resolve.

### Add Or Normalize Markdown

1. Preserve the original body.
2. Add or update the date header.
3. Add `相关入口` after the date block.
4. Add `相关文档` for sibling/topic links when useful.
5. Clean obvious converter artifacts such as `\.`, `\-`, `\+`, `\_`, escaped brackets, and HTML conversion comments, but avoid altering code blocks unless necessary.

### Maintain Navigation And Links

- First-level navigation pages are the main table of contents for each area.
- First-level navigation pages must reflect the user's confirmed area design. When an area is renamed, added, removed, or repurposed, update its description, allowed content, excluded content, links, and related rules instead of copying a generic template.
- Do not create second-level README/index notes unless the user asks or the folder is large enough to need one.
- Use Obsidian double links, for example `[[05-实习材料/00-实习材料说明|实习材料]]`.
- `相关入口` links upward to the first-level navigation page.
- `相关文档` links sideways to sibling or topic-group notes.

### Rebuild Or Check JSONL Indexes

Use the bundled script from this skill folder:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --vault /path/to/vault --check-dates
python3 /path/to/obsidian-manage/scripts/vault_index.py --vault /path/to/vault --rebuild-index
```

`--check-dates` is read-only. `--rebuild-index` rewrites JSONL index files under `00-系统规则/03-索引文件/`; explain before running it.

## Required Formatting

Every Markdown file starts with a blank line, then:

```text
最后修改日期：YYYY-MM-DD
```

followed by one blank line before the rest of the document. Update the date whenever you modify a Markdown file.

## Verification Checklist

After edits, verify:

- No unintended wrapper folders or stale paths remain.
- All touched Markdown files have the correct date header for the current date.
- Navigation pages link to newly added notes.
- Sibling/topic documents link to each other when required.
- JSONL indexes include the final paths.
- `AGENTS.md` and system-rule files were updated only when necessary and allowed.
