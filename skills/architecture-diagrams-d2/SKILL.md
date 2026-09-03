# architecture-diagrams-d2

用于生成可维护、可导出、适合复杂系统架构表达的架构图。主路径使用 `D2 -> SVG`，不使用 Mermaid 作为高密度中文架构图的 canonical 出图方案。

## 适用场景

- 系统分层图
- 运行对象图
- 任务流图
- 模块关系图
- 需要长期维护的架构图

## 不适用场景

- 只需要在 Markdown 里插一个简单流程图
- 关系极少的临时草图
- 只为了快速示意、不需要长期维护的轻量图

## 本地工具位置

- D2 可执行文件：
  `%USERPROFILE%\.codex\tools\d2\...\bin\d2.exe`
- 中文字体：
  `C:\Windows\Fonts\simhei.ttf`

## 标准做法

1. 先确认图类型：
   - 分层图
   - 运行对象图
   - 任务流图
   - 模块图

2. 先写 `.d2` 源文件，不直接手画。

3. 导出为 `.svg` 作为 canonical 图示。

4. 文档里引用 `.svg`，并保留 `.d2` 作为唯一图源。

5. 旧图失效时，明确废弃或降级。

## 推荐命令

```powershell
$d2="$env:USERPROFILE\.codex\tools\d2\...\bin\d2.exe"
$font='C:\Windows\Fonts\simhei.ttf'

& $d2 input.d2 output.svg --layout elk --font-regular $font --font-bold $font --scale 1.2
```

## 输出要求

- 必须同时保留：
  - `.d2` 源文件
  - `.svg` 导出文件
- 图命名必须表达用途，例如：
  - `system-layer-architecture.d2`
  - `runtime-object-architecture.d2`

## 纪律

- 不混用图类型
- 不用缩写节点名糊弄
- 不在未验证渲染结果前宣称完成
- 高密度中文架构图默认不用 Mermaid
