# 原稿局部修改版 — 不是重新设计

本版直接修改用户上传的 1.svg，保留原有六个页面、背景图片、渐变、配色、衬线字体、圆形精力图、列表、图表和弹窗结构。没有采用之前重做版的 Pace/Still 卡片布局。

## 下载

- Original_Layout_Touchup.zip：全部局部修改文件。
- Original_Layout_Touched_Up.svg：与你上传文件相同的 1400 × 2004 六屏总画布。
- screens：六个分开的 440 × 956 SVG，导入 Figma 更方便。
- Before_After.png：原稿与修改后的对照。
- Original_Layout_Preview.pdf：六页预览，保留六个手机页面。最终作业仍需在 Figma 中导出 PDF。

## 具体改动

1. Home：保留照片、水波圆和原按钮布局。调整名称字号和类型列位置，避免 Email review 与 Cognitive 紧挨；活动时长统一为分钟；已用显示 20 / 100。放大底部两个按钮，在现有区域增加 Log symptoms 文字入口。
2. History：保留蓝色布局和两天记录结构。用明确的日期和 used/budget 单位；130 / 100 下方说明 Over by 30，而不是只有红色百分比；放大症状选项；增加 24–72 小时提示及“不是因果证明”的表述。
3. Adjust budget：保留灰色弹窗和原滑尺。去除 80% 的文字重叠，明确当前选择 100；展示暂定估计说明、近期记录与降低额度的支持文字；扩大 Save/Cancel，修正 Save 的文字对比。
4. Log activity：保留粉色面板、三种消耗和原柱图。把空白示例改成实际 Cooking (12 min)，身体4、认知1、情绪0，合计5；柱图与数值对应；放大数值控件及保存按钮。
5. Plan：保留原活动列表和蓝色勾选状态。修正 Chating 拼写；用明确的 Select activities to adjust 取代没有标签的红色叉；在原来 Move to Tomorrow 的底部区域并排提供 Stop、Shorten、Tomorrow。休息行改为未选中，使示例只调整社交活动。
6. Activities：保留手风琴列表、展开柱图和原数据。修正 12+2+4 的总和为18，统一 units 及日期／时长格式；放大 Edit/Delete；去掉没有动作意义的编号字符。

## 导入 Figma

新建一个 Page，例如 Original — Touch-up。拖入 screens 中的六个 SVG；分别使用 Frame selection，确认尺寸为440×956，按01至06从左到右排列，再使用 File → Export frames to PDF。不要把总画布 SVG 放进一个 Frame 后作为六页PDF提交。

原 SVG 的旧文字大多已转换为轮廓。本版修改的文字是新 text 元素，其余未改动的文字仍是原轮廓。不是全部原文字都已变成可编辑文本；SVG 不保留 Auto Layout 或组件关系。

## 核查与限制

已查看修改后总览、核对18 units合计和活动记录4+1+0=5、渲染六个独立页面并检查六页PDF。数据是静态示例：Log activity 处于保存前，不会自动改变首页已用20。

这是按用户要求做的局部修正，不宣称六个静态页面已完整展示全部操作流程：计划Shorten的具体时长输入、推迟日期选择、额度变更及记录保存后的结果／撤销状态仍需要后续在现有页面基础上补充。背景照片和多色块按用户要求保留，低亮度阅读仍建议在Figma中实际检查。
