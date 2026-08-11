# Day 1 · 加速版工程基础行动计划 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不把时间全扑到 Git 上的前提下，建立可控的项目环境，亲眼跑过一次最小 GRPO 训练链路，并能说清一条数据从 GSM8K 题目走到参数更新的大方向。

**Architecture:** 今天不修改训练代码，也不追求训练效果。先把 Git 当作安全护栏，再让 `uv`、PyTRIO、最小 smoke test 和顶层数据流共同组成一次真实工程闭环；所有结论都记录为可复查的证据。

**Tech Stack:** PowerShell、Git、uv、Python 3.13、PyTRIO、GSM8K、SwanLab（本日关闭）。

---

## 今天的北极星

你长期要走的是：

```text
Data Pipeline → LLM / Agent Eval → Failure Analysis
→ 数据 / Prompt / Reward 改造 → 实验验证 → Post-training / Agentic RL
```

今天只搭这条路的第一块地基：**我能安全地拿到一个陌生训练仓库，建好环境，跑一次最小实验，并追到它的数据主线。**

这不是“学会 GRPO”的一天，也不是“把 Git 背下来”的一天。

## 今日时间预算：约 7 小时

| 时段 | 时长 | 产出 |
| --- | ---: | --- |
| 0. 工作区护栏 | 25 分钟 | 当前分支、Git 状态与今天的边界清楚 |
| 1. 环境建立 | 80 分钟 | `uv sync` 成功，或一份可定位的失败记录 |
| 2. 远程训练预检 | 30 分钟 | PyTRIO 登录状态明确，不泄露任何凭据 |
| 3. 最小 GRPO 试跑 | 90 分钟 | 一次 smoke test 的终端证据，或精确故障定位 |
| 4. 追顶层数据流 | 95 分钟 | 一张属于你的 GRPO 数据流图 |
| 5. 读入口与复盘 | 50 分钟 | 说清脚本怎样启动、哪些函数负责什么 |
| 6. 检查与提交 | 30 分钟 | 只提交本笔记，能看懂 Git 树变化 |

Git 相关时间约 55 分钟；其余时间全部服务于真实训练实验和代码阅读。

## 今日禁止事项

- [ ] 不修改 `01-grpo/` 的训练代码。
- [ ] 不碰 `02-demo-async.py`；仓库快速指南已说明它仍有旧版 PyTRIO timeout 配置问题。
- [ ] 不为了“跑通”而随手改依赖版本、复制 API Key，或让 AI 整仓修复。
- [ ] 不开启 SwanLab online；今天用 `--swanlab-mode disabled`，先控制变量。
- [ ] 不用 `git add .`；今天的提交只能包含 `notes/day1.md`。

---

## Task 1：先确认自己站在哪里（0:00–0:25）

**Files:**

- Create: `notes/day1.md`（本文件）
- Do not modify: `01-grpo/` 下任何训练代码

- [ ] **Step 1：确认当前分支和工作区。**

  ```powershell
  git branch --show-current
  git status --short --branch
  git log --oneline --graph --decorate -5
  ```

  **预期：** 当前分支是 `codex/sprint-week1-foundation`；开始工作前没有与今天无关的改动。

- [ ] **Step 2：用自己的话写下三句话。**

  在本文件的“今日记录”中补全：

  ```text
  我现在在哪个分支：
  今天 commit 后哪个标签会移动：
  main 上的 test.py 为什么不会自动出现在当前分支：
  ```

**验收：** 不查资料也能说出：提交会推进当前分支，而不会自动推进 `main`、其他分支或远程仓库。

---

### 实战补充：从旧提交查看、开发与删除分支

这张卡片来自今天的真实操作：

```powershell
git checkout 977c9c1cd287d10d4988d7a6a67f997aa1ab3c63
```

这是一次已经发生的实战复盘；今天只需补完记录，不需要为了练习再创建或删除分支。

这不会切到某个分支，而是把 `HEAD` 直接指向提交 `977c9c1`，所以 Git 显示 `detached HEAD`。

```text
正常开发：HEAD → 分支名 → 提交
查看旧提交：HEAD ─────────→ 提交
```

它不是仓库损坏，也不会删除分支或提交；只是把工作区临时切成旧提交的快照。

- [ ] **只查看旧提交时，先识别 detached HEAD。**

  ```powershell
  git status --short --branch
  git branch --show-current
  ```

  若显示 `## HEAD (no branch)`，且第二条命令没有输出，你正在 detached HEAD。可以看代码、运行代码；不要在这里长期新增代码。

- [ ] **要从旧提交继续开发时，立刻创建分支。**

  若已经停在目标提交上：

  ```powershell
  git switch -c experiment/harness-rl-base
  ```

  若还在其他分支，也可以一步到位：

  ```powershell
  git switch -c experiment/harness-rl-base 977c9c1cd287d10d4988d7a6a67f997aa1ab3c63
  ```

  **脑内模型：** 切到提交 ID 是翻到旧书页；`switch -c` 是在那一页夹上一张新书签。之后的新提交才会安全推进 `experiment/harness-rl-base`。

- [ ] **只想回到刚才的分支时。**

  ```powershell
  git switch -
  ```

  这只会回到上一个位置，不会合并、删除或改写提交。

- [ ] **实验分支完成后，安全删除本地分支。**

  先离开该分支，再删：

  ```powershell
  git switch codex/sprint-week1-foundation
  git branch -d experiment/harness-rl-base
  ```

  `-d` 是安全删除：若该分支有尚未合并的独有提交，Git 会拒绝。只有明确不要那些提交时才使用 `-D`。如果分支曾被推到 GitHub，删除远程分支是另一件事：`git push origin --delete <branch-name>`。

  **停止线：** 不要为了练习执行删除命令；只有这条实验分支真实存在、你已确认不再需要它，并且已切到其他分支时才执行。

**验收：** 能区分“查看旧版本”“从旧版本开新线”“回到原分支”“删除实验分支”这四件事。

---

## Task 2：建立项目环境，不猜（0:25–1:45）

**Files:**

- Read: [pyproject.toml](/D:/agentic-rl-lab/pyproject.toml:1)
- Read: [README.md](/D:/agentic-rl-lab/README.md:63)
- Generated locally but ignored: `.venv/`、下载缓存

- [ ] **Step 1：确认工具入口。**

  ```powershell
  uv --version
  ```

  **预期：** 输出一个 `uv` 版本号。

- [ ] **Step 2：同步仓库锁定的依赖。**

  ```powershell
  uv sync
  ```

  **预期：** 命令成功结束；本地可出现被 `.gitignore` 忽略的 `.venv/`。项目要求 Python `>=3.13`，并把本地 Torch 指到 CPU 索引；这不等于训练只在本地 CPU 上进行，实际训练/采样由远程 PyTRIO 服务执行。

- [ ] **Step 3：若失败，按诊断流程而不是乱修。**

  先记录第一段真正的报错，然后只运行一次：

  ```powershell
  uv sync -v
  ```

  在“今日记录”中分类：

  ```text
  层级：操作系统 / Python 版本 / 网络或依赖源 / 包解析
  第一个有意义的错误：
  我的三个候选原因：
  下一条最小诊断命令：
  ```

  **停止线：** 没有证据时，不修改 `pyproject.toml`，不卸载 Conda，不复制网上的环境修复命令。

**验收：** `uv sync` 成功；或者你能精确说明失败在哪一层，而不是只说“环境坏了”。

---

## Task 3：准备远程训练，并做一次最小试跑（1:45–3:45）

**Files:**

- Read: [01-grpo/start.md](/D:/agentic-rl-lab/01-grpo/start.md:1)
- Read: [01-grpo/readme.md](/D:/agentic-rl-lab/01-grpo/readme.md:128)
- Run: [01-grpo/01-demo-sync.py](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:712)

- [ ] **Step 1：只完成 PyTRIO 登录。**
  裸 trio
→ PowerShell 只去系统 PATH 找
→ 找不到 .venv\Scripts\trio.exe
→ 报错

uv run trio login
→ uv 临时进入本项目 .venv
→ 找到 trio.exe
→ 执行登录

  ```powershell
  uv run trio login
  ```

  **预期：** 按 CLI 的交互式流程完成认证。不要把 token、浏览器回调 URL 或任何凭据粘贴到本笔记、终端截图或 Git 中。

  **停止线：** 如果无法认证，记录认证界面给出的错误或状态；今天仍可继续读数据流，但不要伪造环境变量或修改训练脚本。

- [ ] **Step 2：估算这次试跑的规模。**

  本次参数为：`steps=1`、`batch-size=2`、`group-size=2`、`max-tokens=64`。

  ```text
  1 个优化 step × 2 道题 × 每题 2 个 completion = 4 条 rollout
  最多生成 4 × 64 = 256 个 completion token
  ```

  这不是正式实验，只是把完整链路缩小到可观察的大小。

- [ ] **Step 3：运行 smoke test。**

  ```powershell
  uv run python 01-grpo/01-demo-sync.py --steps 1 --batch-size 2 --group-size 2 --max-tokens 64 --loss-fn importance_sampling --swanlab-mode disabled
  ```

  **成功时应依次看到：**

  ```text
  Loading GSM8K dataset...
  Creating PyTRIO clients...
  Step  0 | reward: ... | ... | loss_mean: ...
  Saving final LoRA weights for sampler...
  # all done
  ```

  第一次运行会自动下载 GSM8K train split；下载时间不属于“程序卡死”。

- [ ] **Step 4：若试跑失败，只做最小定位。**

  按下面顺序记录，而不是直接要求 AI “全修好”：

  ```text
  1. 完整命令：
  2. 第一个属于项目或依赖的 traceback 位置：
  3. 故障层级：数据下载 / PyTRIO 认证或服务 / Python 依赖 / 项目逻辑
  4. 我的一个假设：
  5. 下一步只验证什么：
  ```

  可对 AI 使用这句提示词：

  ```text
  解释这个报错发生在什么层级；列出 3 个最可能原因；不要修改任何文件；只给我下一条诊断命令和它能区分什么。
  ```

**验收：** 最好是得到一次 `Step 0` 输出；若没有，也必须留下可复现命令和精确的第一故障点。

---

## Task 4：追一条数据流，不逐行翻译（3:45–5:20）

**下面是学习示意，不是脚本原文：**

```text
GSM8K 的一行 question / answer
  ↓ load_gsm8k_train()
当前 step 的 2 道题
  ↓ pick_batch()
prompt tokens
  ↓ build_prompt()
每题 2 个模型 completion，含 token / logprob
  ↓ run_rollout_group()
reward 与组内 advantage
  ↓ grade_answer()
PyTRIO Datum
  ↓ build_grpo_datum()
forward_backward() + optim_step()
参数更新与终端指标
```

- [ ] **Step 1：按顺序只看七个锚点。**

  | 你要回答的问题 | 从哪里开始看 |
  | --- | --- |
  | 数据从哪里来？ | [`load_gsm8k_train()`](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:345) |
  | prompt 怎样构造？ | [`build_prompt()`](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:327) |
  | 一题怎样生成一组回答？ | [`run_rollout_group()`](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:359) |
  | 对错怎样变成 reward？ | [`grade_answer()`](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:311) |
  | 训练数据长什么样？ | [`build_grpo_datum()`](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:415) |
  | 主循环在哪里串起这些步骤？ | [`main()`](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:542) |
  | 程序从哪里真正开始？ | [脚本入口](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:712) |

- [ ] **Step 2：在“今日记录”中填完自己的数据流。**

  ```text
  输入样本长什么样：
  prompt 的直接产物是什么：
  group-size=2 在程序里意味着什么：
  reward 由谁产出：
  advantage 为什么不能跨题比较：
  Datum 最终交给谁：
  哪一句代码真正等待远程训练完成：
  ```

- [ ] **Step 3：只补一个阻塞理解的 Python 概念。**

  候选仅限：`@dataclass`、类型标注、`list[...]`、`.result()`、`try/finally`。选一个今天真正卡住你的，写下：它在这个脚本中解决什么问题；不要开一门脱离项目的 Python 课程。

**验收：** 你可以从“1 道 GSM8K 题”口述到“参数更新”，即使暂时说不清每个张量的精确 shape。

---

## Task 5：用一次受控的 AI Review 收束（5:20–6:30）

**Files:**

- Read: [01-demo-sync.py](/D:/agentic-rl-lab/01-grpo/01-demo-sync.py:542)
- Modify: `notes/day1.md` 的“今日记录”部分

- [ ] **Step 1：先由你写出 5 句结论。**

  ```text
  这个脚本解决的问题：
  它的外部输入：
  它产生的关键中间数据：
  它的训练更新发生在哪里：
  它结束时保存或打印了什么：
  ```

- [ ] **Step 2：再让 AI 做导航，不让 AI 代替你读。**

  ```text
  从一条 GSM8K sample 进入 01-grpo/01-demo-sync.py 开始，追踪到 parameter update 为止。
  不要泛泛解释 GRPO；给我具体函数名、文件名和调用顺序。
  先不要建议修改任何代码。
  ```

- [ ] **Step 3：比对并标记一处“我原来理解错了”的地方。**

  这一步比“全答对”更重要：它是你形成工程判断的证据。

**验收：** 你保留自己的结论，再用 AI 校正，而不是把 AI 的回答原样当作理解。

---

## Task 6：记录、检查 diff、只提交本笔记（6:30–7:00）

- [ ] **Step 1：补完本文件末尾的“今日记录”。**

- [ ] **Step 2：检查本次改动的边界。**

  ```powershell
  git status --short
  git diff --check
  git diff -- notes/day1.md
  ```

  **预期：** 只有 `notes/day1.md`；`git diff --check` 没有空白符错误。

- [ ] **Step 3：只暂存这一份笔记，再检查一次。**

  ```powershell
  git add notes/day1.md
  git diff --staged --check
  git diff --staged -- notes/day1.md
  ```

- [ ] **Step 4：提交并观察 Git 树。**

  ```powershell
  git commit -m "docs: record Day 1 GRPO foundation work"
  git log --oneline --graph --decorate -5
  ```

  **预期脑内模型：** 这是今天的第二次提交：它记录你填入的真实执行证据。新 commit 出现在最上方；`HEAD -> codex/sprint-week1-foundation` 跟着移动；`main`、`origin/main`、`upstream/main` 仍停在它们原本的位置。

---

## 今日记录（工作时由你补充）

### 1. 工作区

```text
我现在在哪个分支：
今天 commit 后哪个标签会移动：
main 上的 test.py 为什么不会自动出现在当前分支：
```

### 2. checkout / detached HEAD 实战复盘

```text
我 checkout 的提交 ID：977c9c1
当时 git status 显示什么：
为什么它不是“仓库坏了”：
若要在它上面开发，我会执行什么命令：
若只想回来，我会执行什么命令：
删除实验分支前必须先做什么：
```

### 3. 环境与试跑证据

```text
uv sync：成功 / 失败
若失败，层级与第一条有意义报错：
trio login：成功 / 阻塞在：
smoke test 完整命令：
smoke test 最终结果：
运行耗时或我观察到的下载阶段：
```

### 4. 我自己的数据流解释

```text
输入样本长什么样：
prompt 的直接产物是什么：
group-size=2 在程序里意味着什么：
reward 由谁产出：
advantage 为什么不能跨题比较：
Datum 最终交给谁：
真正等待远程训练完成的代码：
```

### 5. 今天只补的一个知识点

```text
概念：
它在这个脚本中的作用：
```

### 6. 复盘

```text
我原来理解错的一件事：
我今天得到的最重要证据：
明天最值得继续追的一处：
```

## Day 1 完成定义

- [ ] 当前分支和远程分支的关系说得清。
- [ ] 能解释 detached HEAD，并能从旧提交安全创建和删除实验分支。
- [ ] `uv sync` 成功，或有可复现、可分类的失败记录。
- [ ] 知道 PyTRIO 认证是否已就绪，且没有把凭据写入仓库。
- [ ] 最小 GRPO 试跑到达 `Step 0`，或精确定位首个阻塞层。
- [ ] 能从 GSM8K 样本口述到 `optim_step()` 的顶层链路。
- [ ] 只提交 `notes/day1.md`，并能解释 Git 树中新 commit 为什么只推进当前分支。

## 今天结束后发给 reviewer 的最小材料

```text
1. git status --short --branch
2. git log --oneline --graph --decorate -5
3. smoke test 的首段输出与末段输出，或第一段 traceback
4. 上面“我自己的数据流解释”的七个答案
5. 你最卡的一处，不超过三句话
```
