# 个人能力地图

## 四层架构

### 1. 制作导演总控

- 识别用户当前阶段、任务规模和所需产物。
- 将模糊想法发展为故事、结构、时间轴和制作方案。
- 管理项目、Scene、Cut、Generation Clip、素材和节点之间的关系。
- 决定何时需要视觉预演、高风险测试、严格序列状态或后期交付。

### 2. 制作产物

- 故事和创意简报；
- 时间轴、Scene/Cut 表和当前 Cut 合同；
- 视觉故事板与审查；
- 素材清单和引用职责；
- 连续性、返修、后期和交付方案。

### 3. 模型编译器

- 将确认后的制作设计转换为目标模型提示词。
- Seedance 支持 T2V、I2V、V2V、R2V、首尾帧、编辑与续写。
- 其他模型应复用上层项目事实，只替换平台能力、模式和提示词格式。

### 4. 项目事实与结果

- 保存确认故事、素材、Cut、故事板和决策。
- 保存真实生成结果、接受偏差、结束状态和下游影响。
- 支持非线性返工、版本替换和跨会话恢复。

## 内部路由

| 当前任务 | 首选路径 |
|---|---|
| 模糊 Idea、平台未定的创意讨论 | 项目导演方法与故事框架 |
| 已确定使用 Seedance 的创意讨论 | `seedance-interview` 或快速访谈 |
| 故事成立、需要项目结构 | 项目导演方法与短片/MV 专项方法 |
| 需要视觉预演 | `visual-storyboard` |
| 单条视频提示词 | `seedance-prompt` |
| 多卡、长故事 | 平台无关项目规划；确定使用 Seedance 后再由 `seedance-sequence` 编译 |
| 延长视频、承接真实尾帧 | `seedance-continuation` |
| 当前镜头专项问题 | camera / motion / characters / lighting / audio / style / vfx |
| 结果不理想 | take triage，再按需 `seedance-troubleshoot` |
| API、平台、拼接和后期 | `seedance-pipeline` 与当前官方资料 |
| 专业交付 | professional filmmaking 与 delivery QC |

词汇、示例、Recipe、anti-slop 属于转换或辅助层，不负责改变故事和项目方向。

## 能力边界

- 静态同人图和 PixAI 角色素材由 `pixai-prompt-architect` 负责。
- 图像故事板依赖可用的图像生成能力。
- Canvas 读取和修改依赖产品接口；无接口时只提供方案与人工操作指导。
- 模型编译层当前以 Seedance 最完整；其他模型需要单独的平台 Profile。
