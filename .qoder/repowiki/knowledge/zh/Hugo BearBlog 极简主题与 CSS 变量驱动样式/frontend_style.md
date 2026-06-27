## 1. 核心系统与工具
- **构建框架**: 使用 **Hugo** 静态站点生成器。
- **主题系统**: 采用 `hugo-bearblog` 主题（在 `config.toml` 中声明）。该主题以极简主义、高可读性和无 JavaScript 依赖为特点。
- **样式方法**: 
  - **CSS 变量 (Design Tokens)**: 样式高度依赖 CSS 自定义属性（如 `--background-color`, `--link-color`）来管理颜色和字体，便于维护全局一致性。
  - **原生 CSS**: 未使用 Sass/Less 或 Tailwind 等预处理器/框架，直接使用原生 CSS。
  - **内联样式**: 大量样式直接内联在 HTML `<head>` 的 `<style>` 标签中（由 Hugo 模板渲染生成），减少了外部请求但降低了样式的复用性。

## 2. 关键文件与位置
- **`config.toml`**: 定义站点基础配置及主题引用 (`theme = "hugo-bearblog"`)。注释中曾尝试引用 `custom.css`。
- **`public/css/custom.css`**: 唯一的独立样式文件，仅包含针对深色模式的简单媒体查询覆盖。
- **`public/index.html` / `public/_index-copy/index.html`**: 展示了由主题生成的完整样式结构，包括 `:root` 变量定义和响应式布局逻辑。
- **`index.html`**: 根目录下的手动维护文件，使用了 VS Code Markdown 预览的默认样式库（通过 CDN 引入），与 Hugo 生成的站点风格不一致。

## 3. 架构与设计约定
- **响应式策略**: 
  - 采用固定最大宽度 (`--width: 720px`) 配合 `margin: auto` 实现居中布局，确保在大屏上的阅读体验。
  - 使用 `max-width: 100%` 处理图片和表格，防止内容溢出。
- **深色模式 (Dark Mode)**: 
  - 通过 `@media (prefers-color-scheme: dark)` 自动切换。 
  - 定义了完整的深色配色方案（背景 `#01242e`，文本 `#ddd`，链接 `#8cc2dd`）。
  - `custom.css` 中存在另一套更简单的深色覆盖逻辑（背景 `#000`），表明可能存在样式冲突或未清理的实验代码。
- **排版规范**: 
  - 主字体栈: `Verdana, sans-serif`。
  - 行高: `1.5` 至 `1.6`，强调内容可读性。
  - 链接样式: 默认无下划线，悬停时显示下划线 (`text-decoration: underline`)。

## 4. 开发者注意事项
- **样式修改**: 优先修改 `config.toml` 对应的主题参数或通过 `custom.css` 覆盖 CSS 变量。避免直接修改 `public/` 下生成的 HTML 中的内联样式，因为它们会在下次 Hugo 构建时被覆盖。
- **多版本并存**: 仓库中同时存在 Hugo 生成的页面 (`public/`) 和手动编写的 HTML (`index.html`)。手动页面引入了外部 CDN 样式（VS Code Markdown 样式），导致视觉风格割裂。建议统一使用 Hugo 主题进行渲染。
- **自定义脚本**: 页面底部集成了 Crisp 客服聊天脚本，其样式由第三方控制，需注意其与深色模式的兼容性。