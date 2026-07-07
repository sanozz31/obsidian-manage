---
name: obsidian-manage
description: Build, design, organize, import, rename, move, link, date-stamp, index, audit, and maintain personal Obsidian knowledge vaults. Use when the user asks an agent to create a local Obsidian knowledge base, design an AGENTS.md/vault rule system, route notes into folders, manage Markdown notes, maintain navigation pages, rebuild JSONL indexes, or organize an existing Obsidian vault.
---

# Obsidian Manage

Use this skill to build and maintain a personal Obsidian knowledge vault without damaging user-authored notes. The skill is modular: always run the preflight module first, then route to only the module needed for the user's current request.

## Module Router

1. **Preflight And Routing**: run at the start of every task.
2. **Install Or Resume Obsidian**: use when Obsidian is missing or the user says they installed it.
3. **Select Or Create Vault**: use when the vault root is unknown, new, or ambiguous.
4. **New Vault Design**: use for first-time vault creation after the vault target is confirmed empty or absent.
5. **Existing Vault Improvement**: use when a vault or meaningful Markdown content already exists.
6. **Import And Normalize Materials**: use for moving, renaming, converting, linking, and date-stamping notes.
7. **Navigation And Link Maintenance**: use for directory descriptions, entry links, sibling links, and broken/stale links.
8. **Index And Audit Maintenance**: use for date checks, JSONL rebuilds, and consistency audits.

Do not run a full setup flow when a later module is enough. Example: if the user asks to rebuild indexes for a known vault, run preflight, read the vault rules if present, then use Index And Audit Maintenance.

## Module 1: Preflight And Routing

Run this module before every action.

1. Restate the user's current goal in one sentence.
2. Determine whether the task is read-only or will modify files.
3. Identify the vault root from the user's message, prior context, or candidate scan.
4. If the vault root is known, inspect the real filesystem before relying on JSONL indexes.
5. If the vault has `AGENTS.md`, read it before writing anything.
6. If the vault has system/routing/index documents, read them before routing notes or rebuilding indexes.
7. Choose exactly one next module unless the task clearly needs a sequence.
8. If writing outside the current workspace or protected paths, ask for permission or use the available approval mechanism with a clear user-facing justification.

Filesystem state is the source of truth. JSONL indexes are auxiliary.

## Module 2: Install Or Resume Obsidian

Use this module when the user is setting up for the first time, is unsure whether Obsidian is installed, or says they have just installed it.

1. Check the Obsidian app first:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --detect-app
```

2. If Obsidian is installed, report the detected path and continue to Select Or Create Vault.
3. If Obsidian is not installed, prepare installation guidance:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --install-app
```

4. On macOS, if `brew` is available, offer:

```bash
brew install --cask obsidian
```

Run the install only after explicit user approval:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --install-app --yes-install
```

5. If Obsidian and Homebrew are both missing, give the official download URL: `https://obsidian.md/download`. Tell the user clearly: after manual installation, return to the conversation and say "Obsidian is installed" so the agent can rerun detection and continue.
6. Do not auto-download DMG files from the website.

Detecting the app never decides whether a vault exists. Vault detection decides whether to create a new vault or adapt an existing one.

## Module 3: Select Or Create Vault

Use this module when the vault root is unknown, new, or ambiguous.

1. Ask for the intended vault path if it is not known.
2. If the user does not know the path, scan common user folders:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --find-vaults
python3 /path/to/obsidian-manage/scripts/vault_index.py --find-vaults --search-root /path/to/search
python3 /path/to/obsidian-manage/scripts/vault_index.py --find-vaults --search-root /path/to/search --nested-max-dirs 80
```

3. Treat a folder as a candidate vault if it contains `.obsidian/`, `AGENTS.md`, first-level numbered note folders, navigation notes, or a meaningful collection of Markdown files.
4. If multiple candidate vaults exist, summarize them and ask the user which one to use.
5. If the target path already contains a vault or meaningful Markdown content, route to Existing Vault Improvement.
6. If the target path is absent or empty, route to New Vault Design.
7. When the user says "build a new knowledge base" but the target already has content, ask whether to adapt the existing vault, create a separate new vault, or stop.

## Module 4: New Vault Design

Use this module only after the target path is confirmed empty or absent.

1. Clarify the vault's job: personal knowledge archive, AI working memory, project archive, study notes, writing system, research system, or mixed vault.
2. Present the default first-level directory map as an editable proposal, not a fixed requirement.
3. Tell the user they can rename any area, add areas, remove areas, reorder areas, or change naming/link/index rules.
4. Apply only the confirmed version. If the user changes one part, keep the rest of the default template unless they say otherwise.
5. Draft `AGENTS.md` as the vault constitution:
   - vault purpose
   - highest safety principles
   - directory map
   - naming rules
   - date header rules
   - link rules
   - task routing
   - index maintenance
   - actions requiring confirmation
6. Create only first-level navigation pages by default, such as `00-目录名说明.md`. Each page must be written from the confirmed directory name, purpose, allowed note types, exclusion rules, and actual or planned child topics. Do not create identical boilerplate directory descriptions.
7. Add a lightweight index plan only after the folder system is stable.

For the default template and detailed rules, read `references/vault-rules.md`.

## Module 5: Existing Vault Improvement

Use this module when the target already contains `.obsidian/`, `AGENTS.md`, first-level folders, navigation pages, or meaningful Markdown content.

1. Audit the current structure before proposing changes.
2. Never overwrite existing `AGENTS.md`, navigation pages, or user-authored notes with a template.
3. Present an incremental proposal with labels such as `keep`, `rename`, `add`, `remove`, and `move`.
4. Wait for explicit user confirmation before creating top-level folders, moving files, renaming files, deleting anything, or replacing rule/navigation/index files.
5. Existing user content wins over the default template.
6. When a directory is renamed, added, removed, or repurposed, update the directory map, navigation pages, links, task routing, and indexes consistently.

## Module 6: Import And Normalize Materials

Use this module when the user asks to import, move, rename, convert, or organize materials.

1. Inspect the source tree with `find` or `rg --files`.
2. Decide the destination by reading the vault rules and existing nearby folders.
3. Explain the intended destination and any renames before broad or ambiguous moves.
4. Move/import files only after user approval when the operation is broad or ambiguous.
5. Normalize directory and file names to the vault naming style unless the user explicitly wants original names preserved.
6. When two files share the same topic/title but have different formats, keep the same two-digit sequence number, for example `03-项目简历.md` and `03-项目简历.docx`.
7. Preserve user-authored body content. Prefer adding metadata/link blocks and changing paths over rewriting prose.
8. Add or update the date block, `相关入口`, and useful sibling/topic `相关文档` links. For same-topic files in different formats, add explicit links between the Markdown note and the source/companion file.
9. Clean obvious converter artifacts such as `\.`, `\-`, `\+`, `\_`, escaped brackets, and HTML conversion comments, but avoid altering code blocks unless necessary.
10. Update the relevant first-level navigation page.
11. Rebuild JSONL indexes or append an index record as appropriate.
12. Verify old paths are gone and new Obsidian links/index entries resolve.

## Module 7: Navigation And Link Maintenance

Use this module when maintaining directory descriptions, entry links, sibling links, or broken/stale links.

- First-level navigation pages are the main table of contents for each area.
- First-level navigation pages must reflect the user's confirmed area design. Each page should explain the area's purpose, what belongs there, what does not belong there, and the important child topics or notes.
- Do not create second-level README/index notes unless the user asks or the folder is large enough to need one.
- Use Obsidian double links, for example `[[05-职业材料/00-职业材料说明|职业材料]]`.
- `相关入口` links upward to the first-level navigation page.
- `相关文档` links sideways to sibling or topic-group notes.
- Same-topic files with different formats must share the same two-digit sequence number and link to each other.
- When moving or renaming notes, update affected Obsidian links and navigation entries.

## Module 8: Index And Audit Maintenance

Use this module for JSONL indexes, date checks, and consistency audits.

Read-only date check:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --vault /path/to/vault --check-dates
```

Index rebuild:

```bash
python3 /path/to/obsidian-manage/scripts/vault_index.py --vault /path/to/vault --rebuild-index
python3 /path/to/obsidian-manage/scripts/vault_index.py --vault /path/to/vault --index-dir path/inside/vault --rebuild-index
```

`--check-dates` is read-only. `--rebuild-index` rewrites the JSONL index files generated for the current vault under the configured index directory, defaults to `00-系统规则/03-索引文件/`, and automatically removes stale script-generated index files. It must not clear unrelated user-created JSONL files. Use `--index-dir` when the user customized the system/index folder path; by default it must resolve inside the vault. Only use `--allow-external-index-dir` after explicit user confirmation that indexes should live outside the vault.

## Required Formatting

Every Markdown file starts with a blank line, then:

```text
最后修改日期：YYYY-MM-DD
```

followed by one blank line before the rest of the document. Update the date whenever you modify a Markdown file.

## Safety Rules

- Treat the user's current explicit instruction as highest priority.
- Do not create, move, rename, delete, merge, split, or bulk-edit files unless the user clearly asked for that action or approved the plan.
- Before modifying an existing Markdown file, reread its current content.
- Preserve user-authored body content.
- Never delete user material automatically. Only remove obvious system metadata such as `.DS_Store` when it is part of a user-approved import/cleanup.
- Ask before changing `AGENTS.md`, system-rule folders, index structure, or top-level vault directories unless the user explicitly requested it.

## Verification Checklist

After edits, verify:

- The selected module matched the user's current goal.
- No unintended wrapper folders or stale paths remain.
- All touched Markdown files have the correct date header for the current date.
- Navigation pages are specific to their directories, not duplicated boilerplate.
- Navigation pages link to newly added notes.
- Sibling/topic documents link to each other when required.
- JSONL indexes include the final paths.
- `AGENTS.md` and system-rule files were updated only when necessary and allowed.
