# 个人 Skill 包与 Agent 兼容性

本文件只说明个人定制版 `ai-video-production-director` 的源文件、安装方式和能力边界。上游 `seedance-2.0` 的跨客户端发布说明不作为本版本的安装合同。

## 权威位置

- Git 仓库中的 `skill/ai-video-production-director/` 是正式源。
- `$CODEX_HOME/skills/ai-video-production-director/` 或 `~/.codex/skills/ai-video-production-director/` 是部署副本。
- 修改先进入正式源，通过个人校验后再部署；不要直接把上游仓库覆盖到个人安装目录。
- `upstream.lock.json` 记录导入的上游版本。升级时先审查差异，再移植需要的模块和参考资料。

## Codex 包结构

```text
ai-video-production-director/
├── SKILL.md
├── agents/openai.yaml
├── skills/*/MODULE.md
├── references/
├── schemas/
├── scripts/
├── evals/
├── validation/
└── upstream.lock.json
```

`evals/` 中保留的材料主要用于追溯上游设计依据，不自动构成个人版的可执行合规证明。个人版结构与路由以 `validate_personal_skill.py` 为准；模型输出质量仍要结合真实任务审查。

只有根目录的 `SKILL.md` 参与 Skill 发现。内部专项能力使用 `MODULE.md`，避免被 Codex 当成相互竞争的独立 Skill。

## 安装与校验

从正式源目录运行：

```text
python scripts/validate_personal_skill.py .
python scripts/install_personal_skill.py
```

安装器会先校验源文件，在同一 Skills 根目录暂存新副本，并保留前一安装作为可回滚备份。安装后应再次运行已安装副本中的个人校验器。

`scripts/schema_check.py` 是可选的 Schema 开发检查器，需要额外安装 `jsonschema`；它不属于个人 Skill 安装和日常调用的前置条件。

## 调用策略

`agents/openai.yaml` 保持隐式调用开启，所以普通的 AI 视频创意、镜头、故事板、生成提示词、续写、审片和交付请求都可以触发本 Skill。用户也可以显式调用 `$ai-video-production-director`。

内部 Seedance 模块只由主 Skill 路由，不独立发现。若未来另外安装独立 Seedance Skill，一次任务仍只能选择一套 Seedance 编译规则。

## 能力边界

- Skill 提供导演判断、项目状态、提示词编译和本地辅助脚本，不等于视频生成 API。
- 是否能查看视频、听取声音、生成图像或控制 Canvas 取决于当前宿主与可用工具。
- 没有实际检查媒体时，不得把用户描述当作亲自观察到的事实。
- 模型版本、平台能力、价格和配额属于易变事实，使用前查证当前官方资料。
