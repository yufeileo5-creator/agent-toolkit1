---
description: >-
  版本管理工作流 — 提交代码、打版本标签、推送到 GitHub，支持快速回退
---

# 版本管理工作流

用户说 `/version` 时触发此工作流。

// turbo-all

## 提交与发版流程

### 1. 检查当前状态
```bash
git status
```
- 确认有未提交的更改
- 如果没有更改，提示用户"没有需要提交的更改"

### 2. 查看具体改动
```bash
git diff --stat
```
- 向用户展示改动了哪些文件

### 3. 暂存所有更改
```bash
git add -A
```

### 4. 生成提交信息
根据改动内容，使用 **Conventional Commits** 格式生成中文提交信息：
- `feat: 新增xxx功能` — 新功能
- `fix: 修复xxx问题` — Bug修复
- `refactor: 重构xxx模块` — 重构
- `style: 调整xxx样式` — 样式调整
- `docs: 更新xxx文档` — 文档更新
- `perf: 优化xxx性能` — 性能优化
- `chore: 更新xxx配置` — 配置/工具更新

提交信息必须清晰描述改动内容，方便用户未来查阅。

### 5. 提交代码
```bash
git commit -m "<type>: <中文描述>"
```

### 6. 询问用户是否需要打版本标签
向用户确认：
- **是否需要打版本标签？**（适用于重要节点/里程碑）
- 如果需要，查看当前最新标签来建议下一个版本号：
```bash
git tag --sort=-v:refname | Select-Object -First 5
```
- 版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)：
  - `vX.Y.Z`，其中 X=重大/破坏性变更, Y=新功能, Z=Bug修复/小改进

### 7. 打标签（如果用户需要）
```bash
git tag -a vX.Y.Z -m "版本说明：xxx"
```

### 8. 推送到 GitHub
```bash
git push origin main
git push origin --tags
```

### 9. 更新 CHANGELOG.md
按照 [Keep a Changelog](https://keepachangelog.com/) 格式更新 `CHANGELOG.md`：
```markdown
## [vX.Y.Z] - YYYY-MM-DD
### Added（新增）
- 具体新增内容

### Fixed（修复）
- 具体修复内容

### Changed（变更）
- 具体变更内容
```

### 10. 提交 CHANGELOG 更新
```bash
git add CHANGELOG.md && git commit -m "docs: 更新 CHANGELOG" && git push origin main
```

---

## 选择性还原（核心功能）

> **场景**：新功能破坏了旧功能，需要恢复被破坏的部分，同时保留新功能代码。

### 方案 A：还原被破坏的特定文件（最常用）

只从旧版本恢复某几个被破坏的文件，新功能文件不受影响：

```bash
# 1. 查看版本历史，找到功能正常的版本
git log --oneline --decorate -20

# 2. 查看该版本有哪些文件
git show <版本标签或commit> --stat

# 3. 仅还原被破坏的文件（其他文件保持不变）
git checkout <版本标签或commit> -- src/path/to/broken-file1.ts src/path/to/broken-file2.ts

# 4. 提交还原
git add -A
git commit -m "fix: 从 <版本> 还原被破坏的文件，保留新功能"
git push origin main
```

### 方案 B：对比两个版本差异再决定还原

```bash
# 1. 对比当前版本与旧版本的差异
git diff <旧版本标签> HEAD -- src/path/to/file.ts

# 2. 对比两个版本之间某个目录的所有变化
git diff <旧版本标签> HEAD -- src/features/briefing/

# 3. 逐一确认哪些改动需要保留、哪些需要回退
```

### 方案 C：交互式逐块还原（精细控制）

当一个文件中同时有需要保留的新代码和需要回退的旧代码时：

```bash
# 逐块选择要保留或回退的代码段
git checkout -p <旧版本标签> -- src/path/to/file.ts
```
- 对每个代码块, Git 会问你是否应用
- 输入 `y` = 还原这段代码到旧版本
- 输入 `n` = 保持当前新代码不变
- 输入 `s` = 将代码块拆分得更细再选择

### 方案 D：创建安全分支进行实验性还原

```bash
# 1. 基于旧版本创建分支
git checkout -b restore-from-<版本> <版本标签>

# 2. 在这个分支上把新功能的文件复制过来
git checkout main -- src/path/to/new-feature.ts

# 3. 测试确认无误后合并回 main
git checkout main
git merge restore-from-<版本>
```

---

## 版本查询命令速查

| 用途 | 命令 |
|------|------|
| 查看最近提交历史 | `git log --oneline -20` |
| 查看所有版本标签 | `git tag --sort=-v:refname` |
| 查看某版本改动详情 | `git show <tag>` |
| 对比两个版本差异 | `git diff <旧tag> <新tag>` |
| 查看某文件的修改历史 | `git log --oneline -- <file>` |
| 查看某文件在旧版本的内容 | `git show <tag>:<file>` |

---

## 注意事项
- ⚠️ **严禁在已推送的 main 分支上使用 `git reset --hard`**，会丢失历史
- ✅ 使用 `git checkout <tag> -- <file>` 还原文件是最安全的方式
- ✅ **重要功能完成后必须打版本标签**，作为"存档点"
- ✅ 推送前确保代码可正常运行
- ✅ 每个版本标签的 `-m` 消息应详细说明功能状态
