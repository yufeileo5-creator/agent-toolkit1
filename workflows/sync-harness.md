---
description: 自动同步并推送全局规则、工作流和技能树到中央配置仓库 (Harness Sync)
---

# Sync Harness Pipeline

当用户要求同步或推送全局配置、规则 (`.gemini`)、工作流 (`workflows/`) 或技能树 (`skills/`) 时，执行此标准工作流。

## 准备阶段 (前置确认)

1. 确认用户的**中央配置仓库 (Central Toolkit Repo)** 的绝对路径（如 `C:/AgentCode/agent-toolkit1/` 或其他专用于存放基础设置的 Git 仓库）。如果不知道，请询问用户。
2. 确认要同步的源目录。通常包括但不限于：
   - **Tier 1~3 Skills**: `C:\Users\Leo\.gemini\antigravity\skills\`
   - **Workflows**: `C:\Users\Leo\.gemini\antigravity\workflows\` 或当前项目的 `.agents/workflows/`
   - **Templates**: `C:\Users\Leo\.gemini\antigravity\templates\` （如项目中提及的 Auto-Scaffold 脚手架等母版文件）
   - **Rules**: 您个人的 `.gemini` 全局规则文件或对应的 `_versions/`

## 执行阶段 (同步与备份)

> 注意：请将下面的 `<TARGET_REPO>` 替换为真实的本地仓库路径。

// turbo
3. **清空旧备份并拷贝最新的 Skills 资源：**
```powershell
Remove-Item -Path "<TARGET_REPO>\skills" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path "C:\Users\Leo\.gemini\antigravity\skills" -Destination "<TARGET_REPO>\skills" -Recurse -Force
```

// turbo
4. **拷贝最新的 Workflows (如有需要)：**
```powershell
Remove-Item -Path "<TARGET_REPO>\workflows" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path "C:\Users\Leo\.gemini\antigravity\workflows" -Destination "<TARGET_REPO>\workflows" -Recurse -Force
```

// turbo
5. **拷贝最新的全局母版库 (Templates)：**
```powershell
Remove-Item -Path "<TARGET_REPO>\templates" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path "C:\Users\Leo\.gemini\antigravity\templates" -Destination "<TARGET_REPO>\templates" -Recurse -Force
```

// 注意：如果您的全局系统提示词 (Prompt) 保存在某特定文件，请解除注释并替换为您真实的绝对路径，然后加上 `// turbo` 注释让 AI 自动执行。
// Copy-Item -Path "填写您真实的绝对路径" -Destination "<TARGET_REPO>\" -Force -ErrorAction SilentlyContinue

## 阶段 2.5: 本地项目信息脱敏 (Data Sanitization & Path Agnosticism)

> [!CAUTION]
> **千万不能将当前项目的绝对路径或特有信息泄漏到中央仓库中！** 这是确保中央库可以被随时在新电脑上 Clone 下来直接使用的红线规则。

执行完拷贝后，**作为 AI 的你必须在提交前执行一次严格的审查：**
1. 全局检索刚才复制进 `<TARGET_REPO>` 里的 `skills`、`workflows`、`templates` 文件夹以及规则文档。
2. **剥离硬编码路径**：一旦发现里面残存了如 `C:\Users\Leo\...`、`C:\AgentCode\框架\...`，或者是当前对话的 Artifact 绝对路径（如 `brain\xxxx\`）、当前项目特有的密钥、IP等。
3. **强制泛化替换**：使用替换工具将这些本地信息强制剥离。例如将 C 盘路径转换为跨平台的 `~/.gemini/antigravity/`，将具体的项目目录转换为泛化的占位符 `<项目根目录>/`。
4. 确保所有文件处于绝对的“环境无关（Agnostic）”纯净状态后，才能进入下一阶段。

## 阶段 3: 生成导航架构与版本清册 (Smart README Generation)

> [!IMPORTANT]
> 在提交代码前，作为 AI 的你必须主动遍历刚才拷贝进 `<TARGET_REPO>` 的全部资源（如读取各个 `SKILL.md` 提取 `name` 和 `description` 等），然后在仓库根目录**生成或更新一份详尽的 `README.md`**，作为整个底层框架的使用说明书。

6. **动态编撰 `README.md` 并写入 `<TARGET_REPO>`，该文档必须包含以下结构：**
   - **标题与版本**: 记录本次同步的时间，声明这是一个由 AI Agent 维护的 Harness Config Repository。
   - **技能矩阵 (Skill Catalog)**: 用优美的 Markdown 表格分拣并列出所有存在于 Tier 1、Tier 2、Tier 3 的技能及其**精确的中文功能说明**。如果某个技能原版没有中文说明，AI 必须基于代码对其用途进行自动翻译和提炼总结。
   - **工作流指南 (Workflows)**: 列出目前都有哪些全局工作流（如 `/handoff`、`/sync-harness` 等），并写明**使用方法**和触发场景。
   - **核心设计规则 (Rules & Architecture)**: 简要概括全局 Prompt (`.gemini`) 和项目的分层防线逻辑。

7. **动态生成一键装机脚本 (Auto-Installers Deployment)**:
   大模型必须主动在 `<TARGET_REPO>` 根目录下动态生成或更新两个脚本文件：`install.ps1` (适用 Windows) 和 `install.sh` (适用 Mac/Linux)。
   - 脚本的逻辑非常简单：自动获取自身执行时所在的路径，然后使用 `cp -r` 或 `Copy-Item -Recurse -Force` 将同级的 `skills/`、`workflows/`、`templates/` 无情地覆盖写入当前电脑系统深处的 `~/.gemini/antigravity/`（Windows 为 `$HOME\.gemini\antigravity\`）同名目录下。
   - 这将使该中央仓库真正具备“只需 Clone、一键双击”即刻唤醒满血 Harness 环境的自举能力（Self-Bootstrapping）。

## 阶段 4: 提交阶段 (Version Control)

// turbo
7. **检查变更状态、打 Tag 并提交到远程仓库：**
```powershell
Set-Location -Path "<TARGET_REPO>"
git status
git add .
git commit -m "chore(harness): release new environment state [YYYY-MM-DD]

- Auto-generated README catalogs & skill matrix
- Triggered by /sync-harness workflow"
# 自动打上按日期的版本号 Tag
$dateTag = "v" + (Get-Date -Format "yyyy.MM.dd")
git tag -a $dateTag -m "Harness Snapshot for $dateTag"
git push origin main
git push origin $dateTag
```

## 收尾与通知

8. 使用 `notify_user` 告知用户同步已完成，并出具一份简短的同步简报（包含版本号 Tag、新增/删除了哪些模块，以及帮用户更新的中文技能清册目录）。
