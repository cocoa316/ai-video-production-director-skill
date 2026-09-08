# 个人视频项目状态

根据任务规模使用最轻的有效状态。只记录已确认且会影响后续制作的事实。

## 一级：对话状态

适用于一次提示词、一次素材分析或一次返修，不创建项目文件。

```yaml
goal:
confirmed_input:
current_request:
active_references: []
output_language:
```

## 二级：轻量制作状态

适用于多轮创意、故事板、短片或若干 Cut。

```yaml
project:
  title:
  goal:
  duration:
  format:
  platform:
  current_stage:

creative:
  maturity: L0|L1|L2|L3
  core_idea:
  confirmed_story:
  emotional_arc:
  visual_direction:
  fixed_requirements: []
  exclusions: []

timeline:
  scenes: []
  cuts: []
  current_cut:
  reopened_cuts: []

visual_planning:
  storyboard_status: not_considered|recommended|declined|drafting|needs_review|accepted|rejected|superseded|retired
  storyboard_purpose:
  storyboard_version:
  accepted_storyboard:
  affected_cuts: []

continuity:
  characters: []
  wardrobe: []
  locations: []
  props: []
  screen_direction:
  accepted_end_state:

reference_registry:
  active: []
  analysis_only: []
  inspiration: []
  retired: []

production:
  approved_assets: []
  pending_assets: []
  accepted_clips: []
  failed_attempts: []
  active_modules: []
  current_deliverable:
  next_action:

interaction:
  output_language:
  output_format_preference:
  workflow_status: concise|hidden
  last_announced_stage:
```

## 三级：严格序列状态

出现以下情况时，读取 [Sequence Project State](sequence-project-state.md) 并升级：

- 多段生成之间存在父子素材依赖；
- 必须依据上一条真实结束状态继续；
- 多个 Scene/Cut 的生成结果会改变后续计划；
- 项目明确需要机器校验、可审计 lineage 或严格版本对账。

严格状态使用 `project_id`、`clip_id`、`parent_clip_id`、`canon_revision`、`state_revision`、实际开始/结束状态、take review 和 lineage。不要为单次简单任务建立严格 JSON。

普通跨会话项目、互不依赖的多 Cut、单片专业交付或仅需审批记录时，继续使用轻量状态和项目记录文件。

## 更新规则

- 用户明确确认、否定或替换某项内容时才更新为项目事实。
- 计划尾帧不能冒充实际成片；后续以已接受视频的可观察状态为准。
- 接受偏差时记录偏差，并复查受影响的 Cut、故事板和后续素材。
- 故事结构变化时，将受影响的故事板状态改为 `needs_review`，并标记相关 Cut 和提示词待复查；不自动推翻无关内容。
- 用户拒绝故事板后记录本次决定；除非故事或制作风险明显变化，不重复推荐。
- 用户要求忘记素材时移入 `retired`，后续不可继续调用。
- 不把每轮讨论都写入状态，只保存影响未来决策的内容。
