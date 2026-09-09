# 故事板生成与交接合同

本合同用于把已确认的叙事或非叙事方案稳定地转换为故事板图片，并把故事板安全交给视频生成阶段。生成前先固定规格；生成后按同一规格验收。不要依靠“电影感故事板”一类宽泛措辞让图像模型自行决定颜色、格数、画幅或版式。

## 生成前规格

每次至少确定以下字段：

```yaml
purpose: director_review|video_generation|production_overview
control_targets: [narrative_performance|production_overview|action_spatial_continuity]
visual_fidelity: mannequin|same_character_low_render|detailed_director_board
target_video_aspect_ratio: 16:9|9:16|1:1|custom
panel_count:
grid_columns:
grid_rows:
board_canvas_aspect_ratio:
color_policy: strict_grayscale|limited_spot_color|full_color
label_policy: external_deterministic|image_model_preview|text_legend_only
panel_to_cut_map:
```

默认的视频生成执行板使用 `same_character_low_render + strict_grayscale + external_deterministic`。只有用户明确要求彩色，或颜色本身承担连续性信息时，才使用识别色或全彩。

## 画幅与画布

目标视频画幅属于**每个分镜格**，不能直接当作整张故事板画布比例。

忽略边距时：

```text
整板宽高比 ≈ 列数 × 单格宽高比 ÷ 行数
```

例如六格故事板：

- 单格为 `16:9`，采用 2 列 × 3 行时，整板约为 `32:27`，适合接近方形的画布；
- 单格为 `9:16`，采用 3 列 × 2 行时，整板约为 `27:32`，同样接近方形；
- 若采用 3 列 × 2 行承载横向 `16:9` 单格，整板约为 `8:3`，图像生成器很可能压扁单格或改写版式。

优先选择能让整板比例接近生成工具可用画幅的网格。如果用户要求精确像素、严格单格比例或图像工具无法可靠生成该整板比例，分别生成各分镜格，再用确定性排版工具合成；不要让模型通过拉伸人物或裁切动作来填满错误画布。

## 颜色与渲染锁

`strict_grayscale` 必须写成可检查的硬约束：

```text
整张图只使用黑、白和中性灰，饱和度为零。角色的头发、眼睛、服装、皮肤、灯光和背景都不得出现彩色或识别色。使用平涂灰阶和简化线条，不使用彩色光、彩色阴影、渐变虹彩、成片级材质或精细皮肤质感。
```

同角色低渲染通过轮廓、发型、发饰形状、身高比例和服装结构保持身份，不依赖粉色头发、异色瞳等颜色信息。若颜色是剧情或道具状态的唯一载体，使用 `limited_spot_color`，列出唯一允许的颜色和对象，其余部分仍为灰阶。

## 格数、编号与文字

- 明确“严格 N 格、C 列 × R 行、不得增加封面格、角色设定格、色板或装饰格”。
- 每格边界完整、大小一致、顺序按从左到右、从上到下。
- 图像模型不可靠地拼写文字。生产版默认先生成无文字画面，再在格外用确定性排版添加 `P01…Pnn`。
- `Pxx` 表示分镜面板；只有确认存在真实剪辑切点时才同时标记 `Cut xx`。连续动作节点不能仅因分成多格就被标成多个 Cut。
- 如果当前工具不能确定性添加编号，把编号和 Cut 对应关系作为图片外的文字图例交付，不声称图片内文字准确。

## 图像生成提示词结构

使用中文提示词时按以下顺序组织；删除与当前任务无关的行：

```text
用途：用于视频生成前的视觉故事板执行板。

输出规格：严格 <N> 格，<C> 列 × <R> 行；整板画布为 <board ratio>；每格内部构图严格遵循目标视频画幅 <panel ratio>；所有格等大、边框完整，按从左到右、从上到下排列；不得增加任何额外面板、封面、设定图、色板或装饰区。

视觉规则：<visual fidelity>。整张图只使用黑、白和中性灰，饱和度为零。使用清楚的轮廓、平涂灰阶、低材质细节和统一线宽。不是彩色插画，不是漫画成稿，不是角色立绘合集，不是电影剧照拼贴。

角色参考职责：参考图只负责角色身份、身体比例、发型轮廓、标志发饰形状和服装结构。不得复制参考图的站姿、三视图排版、白色背景或与本故事无关的构图。<必要身份锁>

场景与连续性锁：<固定空间参照、人物左右关系、出入口、家具、光源方向>。
道具连续性锁：<初始位置、持有人、拿取过程、接触节点、结束位置>。
摄影规则：<各格景别与视角原则>。摄影机运动与人物动作分开表达。

P01：<单一关键状态；人物、动作、视线、构图、道具状态>。
P02：<单一关键状态>。
……
Pnn：<完成后的可见结束状态>。

禁止：彩色、识别色、精细五官渲染、写实材质、景深光斑、成片级灯光、额外人物、额外肢体、错误持物、道具复制、道具漂移、格数变化、面板重叠、画中画、对话气泡、说明文字、箭头、水印、Logo、UI、页眉、页脚。
```

如果选择 `limited_spot_color` 或 `full_color`，必须主动替换灰阶段落，不能同时留下互相冲突的“全彩”和“饱和度为零”。

## 生成策略

满足以下任一条件时，优先逐格生成后合成：

- 用户要求精确像素或严格单格画幅；
- 超过六格或面板信息密度较高；
- 角色、手部、道具交接需要逐格修正；
- 整板理论比例与工具支持画幅差异明显；
- 已有整板尝试出现格数、尺寸、颜色或文字失控。

一次生成整板适合快速讨论稿和低成本结构验证。无论采用哪种方式，都要检查实际文件尺寸、整板比例、格数、单格比例、颜色和彩色像素倾向；不要只根据提示词判断成功。

## 视频生成交接

故事板确认后，为对应 Cut 输出：

```yaml
storyboard_purpose:
panel_to_cut_map:
inherit_from_storyboard:
  - event_order
  - composition
  - blocking
  - action_nodes
  - prop_state
  - performance_timing
do_not_inherit:
  - line_art
  - grayscale_rendering
  - mannequin_features
  - panel_borders
  - panel_numbers
  - written_text
  - whole_board_layout
character_authority:
sound_authority:
prop_start_state:
prop_end_state:
continuity_notes:
```

最终视频提示词只写本次生成需要继承的画面事实和明确排除项，不把整份 YAML、面板说明或内部字段机械复制进去。
