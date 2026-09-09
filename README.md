# AI Video Production Director

面向 Codex 的 AI 视频制作导演 Skill。它可以从模糊想法开始协助发展故事，继续完成 Scene/Cut 设计、视觉故事板、素材职责、Seedance 提示词、连续性管理、审片返修和交付。本 Skill 已内置并重新组织 `seedance-2.0 v6.7.0` 的模型专项能力，用户无需另外安装 Seedance Skill。

English summary: a Codex skill for story development, shot design, visual storyboards, Seedance prompt compilation, continuity, review, revision, and delivery.

## 适合什么工作

- 从大致想法讨论到可执行故事，而不是过早生成提示词。
- 在故事成熟时主动建议视觉故事板，并按叙事、动作、空间和参考污染风险选择方案。
- 将已经确认的设计交给内置 Seedance 编译层，生成模型可执行的提示词。
- 根据实际生成结果维护连续性，处理续写、返修、剪辑和交付。
- 在制作阶段或路由改变时显示当前步骤和实际调用的模块。

提示词正文默认使用中文；用户明确指定时可切换为英文。成片对白语言独立处理，因此中文提示词可以保留日语或其他语言对白。

## 安装

直接安装到 Codex Skills 目录：

```powershell
git clone https://github.com/cocoa316/ai-video-production-director-skill.git "$HOME\.codex\skills\ai-video-production-director"
```

也可以先克隆到任意工作目录，再运行安装器：

```powershell
git clone https://github.com/cocoa316/ai-video-production-director-skill.git
cd ai-video-production-director-skill
python scripts/install_codex_skill.py
```

macOS 或 Linux 将安装目标写为 `~/.codex/skills/ai-video-production-director` 即可。更新直接安装的副本时，在该目录运行 `git pull`；通过安装器部署时，先更新源码，再重新运行安装器。

## 使用

可以显式调用：

```text
$ai-video-production-director 帮我把这个想法发展成 15 秒短片，并在合适的时候建议是否使用故事板。
```

也可以直接描述 AI 视频创意、故事板、镜头、提示词、续写或审片需求。Skill 默认允许 Codex 根据任务自动调用。

## 校验

```powershell
python scripts/validate_skill.py .
python scripts/behavior_contract_check.py .
```

`scripts/schema_check.py` 是可选的开发检查，需要 `jsonschema`。`evals/` 与 `references/migrated/` 保留上游评测及迁移依据，不会在普通任务中自动全部载入。

## 结构与兼容性

根目录只有一个可发现入口 `SKILL.md`。各专项能力放在 `skills/*/MODULE.md` 中，由主 Skill 按需路由，避免成为互相竞争的独立 Skill。更多说明见 [安装与兼容性](references/installation-and-compatibility.md)。

## 来源与许可

本项目内置并重新组织了 [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) v6.7.0 的模型专项模块与资料，因此无需重复安装 Seedance Skill。主入口负责制作导演、创意发展、Scene/Cut、视觉故事板、项目状态和交付；内置 Seedance 模块负责提示词编译及镜头、动作、声音、续写和故障诊断。具体上游版本记录在 `upstream.lock.json`。

项目使用 [MIT License](LICENSE)。
