# Day 1｜把工程操作系统装起来

> 今天的身份不是“学 GRPO 的学生”，而是第一次把一个真实研究仓库变成自己能安全操作的工程环境的人。
>
> **执行规则：下面所有终端命令都由我亲手运行；Codex 只解释、检查输出、帮助定位问题。**

## 1. 今天和大目标的关系

我的长期主线是：

```text
Data → Eval → Agent trajectory → 实验闭环 → Post-training / Agentic RL
```

今天不直接推进算法知识，而是先补上这条主线的“工程操作系统”：我必须能确认代码来自哪里、当前改动在哪里、如何隔离实验、如何创建可复现环境、以及如何留下可审查的记录。

这不是绕路。以后做一次数据清洗、改一次 grader、跑一次 GRPO 实验，都需要同一套能力。

## 2. 今日完成定义（Definition of Done）

完成 Day 1 时，我应当拥有：

- [ ] 一个干净的个人 fork 工作流：`origin` 指向我的 fork，`upstream` 指向原作者仓库。
- [ ] 一个独立学习分支：`sprint/week1-foundation`。
- [ ] 一个由 `uv` 管理、可以导入项目关键依赖的本地环境。
- [ ] 这份包含真实执行记录的日志。
- [ ] 至少一次亲眼看过的 `git diff`、`git diff --staged` 和本地 commit。
- [ ] 能用自己的话解释：working tree、staging area、commit 分别是什么。

今天**不做**：跑完整训练、阅读 GRPO 源码、申请 API key、修改 `pyproject.toml`、`uv.lock` 或业务代码、推送远端。

建议时间：约 2.5～3 小时。若 `uv sync` 下载较久，可以暂停等待，但不要在等待时开新教程或改项目配置。

---

## 3. 开始前：先恢复到干净起点（约 15 分钟）

此前我们误操作留下过一个练习分支、一个 `upstream` remote 和一个未完成的 `.venv`。这段恢复练习本身很有价值：先观察状态，再只撤销自己确实想撤销的东西。

### 3.1 先观察，不修改

在仓库根目录 `D:\agentic-rl-lab` 运行：

```powershell
git status --short --branch
git branch --show-current
git remote -v
Test-Path -LiteralPath .venv
```

当前这次恢复的目标状态是：

```text
当前分支：main
remote：只剩 origin（walchwil/agentic-rl-lab）
.venv：False
Git 工作区：没有文件改动
```

如果已经符合目标，跳到第 4 节；不要为了“练习”重复删除。

### 3.2 仅在仍看到旧练习状态时恢复

1. 切回主分支：

   ```powershell
   git switch main
   ```

   `git checkout main` 在“切换分支”这个场景效果相同；这里用 `switch` 是为了让命令的职责更清晰。

2. 删除这次误创建、且尚未承载任何工作的分支：

   ```powershell
   git branch -d codex/sprint-week1-foundation
   ```

   如果 Git 拒绝删除，**不要立刻改成 `-D`**；先把完整输出贴给 Codex。正常工作中，分支上可能有未合并的成果，强删会丢掉这个保护。

3. 移除这次误添加的 remote：

   ```powershell
   git remote remove upstream
   ```

4. 只在下面的命令确认路径正好是本仓库的 `.venv` 后，删除这次未完成的本地环境：

   ```powershell
   Get-Item -LiteralPath .venv | Select-Object FullName,CreationTime,LastWriteTime
   Remove-Item -LiteralPath .venv -Recurse -Force
   Test-Path -LiteralPath .venv
   ```

   最后一行应输出 `False`。删除的是可由 `uv sync` 重新生成的本地环境，不是项目代码，也不会影响远端仓库。

5. 再次确认：

   ```powershell
   git status --short --branch
   git remote -v
   git branch --show-current
   ```

### 脑内模型

```text
仓库文件和提交历史      → Git 管
remote 名称和分支指针    → Git 配置 / 引用管
.venv                    → 可随时重建的本地运行环境
```

恢复时分别处理三类状态，不能因为想“回到原点”就随手运行 `git reset --hard`。

---

## 4. 建立 Fork 工作流（约 20 分钟）

### 4.1 添加并获取原作者仓库

```powershell
git remote add upstream https://github.com/KMnO4-zx/agentic-rl-lab.git
git fetch upstream
git remote -v
```

预期看到：

```text
origin    https://github.com/walchwil/agentic-rl-lab.git
upstream  https://github.com/KMnO4-zx/agentic-rl-lab.git
```powershell
git switch -c sprint/week1-foundation
git status --short --branch
```

预期状态类似：

```text
## sprint/week1-foundation
```

### 这一小步到底保护了什么？

`main` 是可随时回看的稳定起点；今天的笔记、后续的小实验都先落在 `sprint/week1-foundation`。如果今天做错了，我能精确地比较或删除这个分支，而不会把 `main` 弄乱。

---

## 6. 建立可复现 Python 环境（约 45～90 分钟）

### 6.1 先确认工具

```powershell
uv --version
```

记录版本号：`____________________________`

### 6.2 安装锁定的项目依赖

```powershell
uv sync
```

成功的核心信号是命令以退出码 0 结束，并在仓库里生成 `.venv`。不要因为它下载了 `torch`、Python 或依赖包就提前中断。

若失败：

1. 不改 `pyproject.toml`，不删 `uv.lock`，不让 AI “全部修好”。
2. 先记下错误中最早出现的失败行和最后 20 行。
3. 把完整错误与下面两条命令的输出发给 Codex：

   ```powershell
   uv --version
   uv python list
   ```

### 6.3 验证环境真的可用

只有 `uv sync` 成功后再运行：

```powershell
uv run python --version
uv run python -c "import importlib.metadata as m; import torch, pytrio; print('torch =', torch.__version__); print('pytrio =', m.version('pytrio'))"
git check-ignore -v .venv
```

预期：前两条能输出 Python、Torch、PyTRIO 的版本；最后一条能指出 `.gitignore` 中忽略 `.venv` 的规则。

### 脑内模型

```text
pyproject.toml  = 项目声明“需要什么”
uv.lock         = 本次可复现地“用哪一版”
.venv           = 本机实际安装出来、可删除重建的运行副本
```

---

## 7. 把今天变成可审查的 Git 记录（约 35 分钟）

### 7.1 填写真实记录

回到本文件，把下面的空白补成自己的真实情况。不要写任何 token、密码或 API key。

## 今日实际记录

### 环境

- `uv --version`：
- `uv sync`：成功 / 失败；耗时约：
- Python 版本：
- Torch 版本：
- PyTRIO 版本：

### Git 命令与观察

- 我确认的 `origin`：
- 我确认的 `upstream`：
- 我创建的分支：
- `git status` 显示的意思：

### 我现在理解

- `working tree`：
- `staging area`：
- `commit`：

### 我还不理解 / 今天遇到的问题

- 

### 7.2 故意观察三层 Git 状态

这份文件刚被创建时是 **untracked file**。先运行：

```powershell
git status
git diff -- notes/day1.md
```

重点观察：`git status` 会显示 `notes/` 是未跟踪内容；但第二条通常没有输出。原因不是文件不存在，而是 `git diff` 默认只比较“已被 Git 跟踪的工作区内容”和暂存区。

然后把它加入暂存区，再看完整内容：

```powershell
git add notes/day1.md
git diff --staged -- notes/day1.md
git status
```

现在请再编辑本文件至少一处真实记录，然后运行：

```powershell
git diff -- notes/day1.md
git add -p notes/day1.md
git diff --staged -- notes/day1.md
git status
```

`git add -p` 会逐块问是否暂存。今天如果只有一个小块，读完后输入 `y` 即可；若不确定，输入 `q` 退出，先把屏幕内容发给 Codex。

### 脑内模型

```text
编辑器保存的文件
        ↓
working tree（我正在修改的现场）
        ↓ git add
staging area（我挑选好、准备交卷的版本）
        ↓ git commit
commit（历史里不可变的一次快照）
```

---

## 8. 创建今天的第一条本地 commit（约 10 分钟）

仅当以下检查全部符合预期时执行：

- [ ] `git status` 只包含我能解释的 `notes/day1.md` 变动。
- [ ] `git diff --staged -- notes/day1.md` 中没有 API key、密码或无关修改。
- [ ] 我知道这次 commit 的目的只是记录 Day 1 的环境与 Git 学习，不包含模型代码改动。

执行：

```powershell
git commit -m "docs: start day 1 engineering log"
git status --short --branch
git log --oneline --graph --decorate -5
```

预期：日志里出现这一条 commit；`git status --short --branch` 不再列出文件改动。今天先不 `git push`，明天确认分支和 commit 的关系后再决定是否推送。

---

## 9. Day 1 最终验收（约 10 分钟）

最后运行并保存关键输出：

```powershell
git status --short --branch
git remote -v
git log --oneline --graph --decorate -5
uv run python --version
```

完成后，我应能不用查资料回答：

- [ ] `git checkout main` 与 `git switch main` 在当前场景为什么都能切分支？
- [ ] `origin`、`upstream`、`local` 分别是什么？
- [ ] 为什么 `.venv` 不应提交？
- [ ] 为什么未跟踪文件刚创建时，`git diff` 可能是空的？
- [ ] `git diff` 和 `git diff --staged` 分别在比较哪两个地方？

## 10. 卡住时的处理协议

1. 停在报错处，不连续尝试多个“看起来可能有用”的命令。
2. 先回答：这是 Git、Python、依赖、网络，还是项目代码层的问题？
3. 贴出命令、完整报错、我原本预期看到什么。
4. 让 Codex 只给一个下一步诊断命令；我自己执行后再回来。

---

## Day 1 收束脑内模型

```text
个人 fork / 原作者仓库
        ↓
安全分支
        ↓
可重建的 .venv
        ↓
真实记录
        ↓
审查 diff
        ↓
本地 commit
```

明天再把这套工作流接到第一条真实 GRPO 数据流上：GSM8K question → rollout → reward → advantage → update。