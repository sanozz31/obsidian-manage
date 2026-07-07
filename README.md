# obsidian-manage

`obsidian-manage` 是一个面向 Agent 的 Obsidian 知识库管理 Skill，用来帮助用户从零搭建、改造和持续维护本地 Obsidian Vault。

它适合这些场景：

- 新建个人 Obsidian 知识库
- 检测本地是否已经安装 Obsidian
- 扫描已有 Obsidian Vault
- 设计 `AGENTS.md` / Vault 规则系统
- 规划可修改的默认目录模板
- 导入、移动、重命名 Markdown 资料
- 补充最后修改日期、入口链接和同组互链
- 维护一级目录导航页
- 检查 Markdown 日期头
- 重建 JSONL 索引

## 支持范围

本 Skill 面向 macOS 优先使用；Linux 仅做已有安装检测、Vault 扫描和官网安装引导。不提供 Windows 自动流程。

## 默认目录模板

默认模板只是提案，不是强制规则。创建或改造知识库前，Agent 应该先展示目录方案，让用户确认。用户可以重命名、新增、删除或调整任意目录。

```text
00-系统规则/
01-小草稿箱/
02-产品工作/
03-学习经验/
04-项目沉淀/
05-职业材料/
06-学术研究/
07-计划复盘/
08-关于我的/
09-小废纸篓/
```

## 核心原则

- 已有 Vault 不能当空白库重建。
- 如果目标路径已有 `.obsidian/`、`AGENTS.md` 或 Markdown 内容，必须先审计现有结构。
- 创建、移动、重命名、删除、合并、拆分、改规则前，必须让用户确认。
- 用户已有内容优先于模板。
- 文件系统是真实来源，JSONL 索引只是辅助。
- Obsidian App 检测和 Vault 检测是两件事：App 是否安装不能决定 Vault 是否存在。

## 模块化流程

每次调用 Skill 时，Agent 应先做前置检测，然后只进入当前任务需要的模块，不必每次重跑完整建库流程。

```text
01 前置检测与路由
02 安装或继续 Obsidian
03 选择或创建 Vault
04 新建知识库设计
05 现有知识库改造
06 导入与规范化资料
07 导航与链接维护
08 索引与审计维护
```

例如：用户只要求重建索引时，Agent 应先确认 vault 和规则，再直接进入“索引与审计维护”；用户说“Obsidian 已经安装好了”时，Agent 应重新检测安装状态，然后继续选择或创建 Vault。

## Markdown 日期头

正式 Markdown 文件建议以如下格式开头：

````markdown

```text
最后修改日期：YYYY-MM-DD
```

# 正文标题
````

## 脚本工具

脚本位于：

```text
scripts/vault_index.py
```

### 检测 Obsidian App

```bash
python3 scripts/vault_index.py --detect-app
```

### 准备安装 Obsidian

默认是 dry-run，不会真正安装。macOS 下如果已经安装 Homebrew 且没有检测到 Obsidian，会打印：

```bash
brew install --cask obsidian
```

如果本机既没有 Obsidian，也没有 Homebrew，则直接提示用户去官网下载：

```text
https://obsidian.md/download
```

不会自动从官网下载、挂载或安装 DMG。
这个分支是正常的人工安装引导，不代表脚本执行失败。用户人工安装完成后，需要回到对话里告诉 Agent：“Obsidian 已经安装好了”，Agent 再继续下一步检测和建库流程。

```bash
python3 scripts/vault_index.py --install-app
```

确认要执行安装时：

```bash
python3 scripts/vault_index.py --install-app --yes-install
```

### 扫描候选 Vault

```bash
python3 scripts/vault_index.py --find-vaults
python3 scripts/vault_index.py --find-vaults --search-root /path/to/search --max-depth 3
```

### 检查日期头

```bash
python3 scripts/vault_index.py --vault /path/to/vault --check-dates
```

### 重建 JSONL 索引

```bash
python3 scripts/vault_index.py --vault /path/to/vault --rebuild-index
```

重建索引只覆盖脚本为当前 Vault 生成的索引文件，不会清空同目录下用户自建的其他 JSONL 文件。

## Skill 文件结构

```text
obsidian-manage/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   └── vault-rules.md
└── scripts/
    └── vault_index.py
```

## 使用方式

在支持 Skill 的 Agent 环境中，将本目录放入对应的 skills 目录后，可以这样调用：

```text
Use $obsidian-manage to build or organize my local Obsidian vault.
```

Agent 应先读取 `SKILL.md`，需要详细规则时再读取 `references/vault-rules.md`。

## 发布前检查

建议发布前运行：

```bash
python3 scripts/vault_index.py --detect-app
python3 scripts/vault_index.py --find-vaults --search-root /path/to/search
python3 scripts/vault_index.py --vault /path/to/vault --check-dates
```

如果要公开分享本 Skill，还应确认仓库中没有个人姓名、绝对用户路径、密钥或私有项目资料。
