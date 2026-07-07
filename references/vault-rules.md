# Obsidian Manage Reference

This reference captures a reusable process for personal Obsidian knowledge bases. Treat the folder map below as the default editable template, not a fixed requirement.

## Modular Execution Model

Use this reference through a modular flow:

1. **Preflight And Routing**: identify the user's current goal, vault root, read/write risk, and applicable vault rules.
2. **Install Or Resume Obsidian**: check the app, guide Homebrew or manual official installation, then continue after the user returns.
3. **Select Or Create Vault**: scan candidate vaults or confirm the target path.
4. **New Vault Design**: use only for an empty or absent target path.
5. **Existing Vault Improvement**: use for any target with `.obsidian/`, `AGENTS.md`, numbered folders, navigation pages, or meaningful Markdown content.
6. **Import And Normalize Materials**: route, move, rename, date-stamp, link, and index imported materials.
7. **Navigation And Link Maintenance**: keep first-level navigation pages and Obsidian links accurate.
8. **Index And Audit Maintenance**: check date headers and rebuild JSONL indexes.

Every task starts with preflight, but later tasks should jump directly to the needed module instead of rerunning the full setup flow.

## App And Vault Detection

Detecting Obsidian app installation and detecting existing vaults are separate tasks.

- App detection answers: “Is Obsidian installed on this machine?”
- Vault detection answers: “Where is the user's existing knowledge base?”

At the start of first-time setup, check app installation first. If Obsidian is not installed, prepare installation guidance before vault creation or migration. On macOS, if Homebrew is installed, automatic installation may use `brew install --cask obsidian`. If both Obsidian and Homebrew are missing, give the user the official download URL, ask them to install manually, and explicitly tell them to return to the conversation after installation and say "Obsidian is installed" so the agent can continue: `https://obsidian.md/download`. Installation is dry-run by default in the bundled script; actual Homebrew installation requires `--yes-install` and the active agent environment's approval mechanism.

After app detection or installation planning, use vault detection to decide whether to create a new vault or adapt an existing one. Common vault signals include `.obsidian/`, `AGENTS.md`, first-level numbered note folders, navigation notes, or many Markdown files. If candidate vaults are found, ask the user which to use before modifying anything.

Obsidian app detection is platform-dependent and best-effort. This skill intentionally supports macOS and Linux only:

- macOS: `/Applications/Obsidian.app`, `~/Applications/Obsidian.app`, or Spotlight/mdfind results.
- Linux: `command -v obsidian`, Flatpak/Snap package checks, AppImage locations, or desktop entries.

Suggested install behavior:

- macOS with Obsidian already installed: report the detected app path.
- macOS with Homebrew but no Obsidian: print `brew install --cask obsidian`; run it only with `--yes-install` and user approval.
- macOS without Obsidian and without Homebrew: print `https://obsidian.md/download`, tell the user to install manually, explicitly ask them to return and say "Obsidian is installed", and treat this as a normal guidance result rather than a script failure.
- Linux: detect existing installs best-effort, but default to the official download URL for installation guidance.

## Existing Vault Handling

Always check the target path before building. If the target already contains an Obsidian vault or meaningful Markdown content, do not treat it as a blank slate. Work from the existing structure and request confirmation for any structural changes.

Recommended decision flow:

1. Inspect the target path.
2. If empty or absent: propose a new vault structure.
3. If existing content is present: summarize the current structure, identify gaps, and propose incremental changes.
4. Ask the user to confirm before creating top-level folders, moving files, renaming files, deleting anything, or replacing rule/navigation/index files.
5. Never overwrite existing `AGENTS.md` or navigation pages with a template. Merge carefully only after confirmation.

## Customization Workflow

The example directory map is the default proposal. Users may change any part of it before or after vault creation.

When proposing a vault structure, show it in an editable form and explicitly support these operations:

- Rename an area.
- Add an area.
- Remove an area.
- Move a topic from one area to another.
- Change note naming, date header, link, or index rules.
- Keep the default for everything else.

For existing vaults, do not force the default template onto the current structure. Present an incremental proposal with labels such as `keep`, `rename`, `add`, `remove`, and `move`, then wait for confirmation.

## Build Process For A Personal Vault

1. **Define the vault role**: decide whether it is mainly for work memory, study notes, projects, writing, research, personal planning, or an AI-readable operating system.
2. **Design stable first-level areas**: 6-10 folders is usually enough. Prefer areas that will survive for years.
3. **Create a vault constitution**: write `AGENTS.md` with safety rules, directory map, routing, naming, linking, and index policy.
4. **Create first-level navigation pages**: one `00-...说明.md` per first-level area. Write each page from the user's confirmed area purpose, allowed note types, exclusion rules, and actual or planned child topics. Avoid repeated generic descriptions.
5. **Set naming rules early**: choose folder and note naming before importing lots of files.
6. **Import in batches**: move one source folder/topic at a time, then normalize names, dates, links, navigation, and index.
7. **Add indexes after structure stabilizes**: JSONL indexes are useful for agents but should not replace the filesystem.
8. **Audit regularly**: check date headers, broken/stale paths, orphan notes, and navigation gaps.

## Recommended AGENTS.md Sections

- Vault purpose
- Highest safety principles
- Directory map
- Naming rules
- Date header rules
- Link rules
- Task routing rules
- Index and record rules
- Actions requiring confirmation
- External rules/project rule priority

## Default Editable Directory Map

Users can rename, add, remove, or reorder any area before the agent creates or changes files.

- `00-系统规则/`: Vault rules, task routing, index rules, JSONL index files.
- `01-小草稿箱/`: Unclassified ideas, temporary excerpts, half-finished notes.
- `02-产品工作/`: PRDs, product decisions, competitive analysis, product research.
- `03-学习经验/`: Tool learning, computer learning, CLI/Agent workflows.
- `04-项目沉淀/`: Project memories, decisions, technical lessons, retrospectives.
- `05-职业材料/`: Internship, job, interview, resume, company research, career materials.
- `06-学术研究/`: Papers, research design, literature review, academic writing.
- `07-计划复盘/`: Weekly/monthly plans, retrospectives, action reviews.
- `08-关于我的/`: Personal profile, style, preferences, long-term context.
- `09-小废纸篓/`: Low-priority old material kept out of the main knowledge system.

## Naming

- Directories should be numbered: `两位数-名称/`.
- Formal notes usually use `两位数-中文.md`, allowing product/tool names such as `AI`, `CLI`, `SQL`, `Dify`, etc. when they are part of the real topic.
- Drafts: `YYYY-MM-DD-主题.md`.
- Plans/retrospectives: `YYYY-MM-DD-周复盘.md` or `YYYY-MM-月计划.md`.
- Do not add unnumbered directories unless the user explicitly asks.

## Date Header

Every Markdown file must start exactly like this, with a blank line before and after the code block:

````markdown

```text
最后修改日期：YYYY-MM-DD
```

# 正文标题
````

When modifying a Markdown file, update this date to the current local date.

## Link Blocks

After the date block, formal notes should usually have:

```markdown
相关入口：[[05-职业材料/00-职业材料说明|职业材料]]

相关文档：
- [[同组路径/01-文档|文档]]
```

Use `相关入口` for the first-level navigation page and `相关文档` for sibling/topic links.

## JSONL Index Files

Index directory: `00-系统规则/03-索引文件/`.

The bundled script now generates per-area index files from the vault's actual first-level directories. The following names are examples, not a fixed schema:

- `01-全库索引.jsonl`
- `02-产品工作索引.jsonl`
- `03-学习经验索引.jsonl`
- `04-项目沉淀索引.jsonl`
- `05-职业材料索引.jsonl`
- `06-学术研究索引.jsonl`
- `07-计划复盘索引.jsonl`
- `08-关于我的索引.jsonl`
- `09-系统规则索引.jsonl`

Record shape:

```json
{"date":"2026-07-07","path":"05-职业材料/01-面试准备/01-岗位分析.md","title":"01-岗位分析","area":"05-职业材料","type":"note","status":"active"}
```

The filesystem is the source of truth. Rebuild indexes when paths have changed a lot.

## Routing Reminders

- Product/PRD work: read relevant product rules and `02-产品工作/` notes.
- Project work: read the specific project rules before writing project memories.
- Academic work: never invent references; mark unverified claims clearly.
- Career/interview/resume work: stay grounded in the user's real experience.
- Writing/personal preference work: read the personal-context area first.
