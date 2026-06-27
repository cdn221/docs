该项目是一个基于 **Hugo** 静态站点生成器构建的简单门户页面，主要用于发布客户端下载链接和服务状态更新。

### 1. 构建系统与方法
- **核心工具**: 使用 `Hugo` (Go语言编写的静态站点生成器) 进行构建。从 `public/index.html` 中的 meta 标签 `<meta name="generator" content="Hugo 0.148.0">` 可知当前使用的版本。
- **主题依赖**: 配置文件中指定了主题 `theme = "hugo-bearblog"`，这是一个极简主义的博客/文档主题。
- **构建方式**: 目前仓库中**没有发现**自动化的构建脚本（如 `Makefile`, `build.sh`）或 CI/CD 配置文件（如 `.github/workflows`, `.gitlab-ci.yml`）。这表明构建过程很可能是开发者在本地手动执行 `hugo` 命令，然后将生成的 `public/` 目录内容部署到服务器或 CDN。

### 2. 关键文件
- `config.toml`: Hugo 的核心配置文件，定义了站点的 `baseURL` (`https://fb.cdnn1.com/`)、语言、标题和主题。
- `public/`: 存放 Hugo 生成的静态 HTML、CSS 和 XML 文件的目录。这是实际部署的内容。
- `index.md`: 站点首页的 Markdown 源文件，包含客户端下载链接、FAQ 和联系方式。
- `CNAME`: 指示该站点可能托管在支持自定义域名的平台上（如 GitHub Pages），指向 `fb.cdnn1.com`。

### 3. 架构与约定
- **手动工作流**: 由于缺乏自动化脚本，项目遵循“本地修改 -> 本地构建 -> 手动推送/上传”的传统静态站点维护模式。
- **内容管理**: 内容主要以 Markdown (`index.md`) 形式存在，Hugo 将其渲染为 HTML。同时存在手写的 `index.html` 和 `public/index.html`，可能存在源文件与生成文件混合管理的情况，需注意区分源文件（根目录下的 `.md`）和生成物（`public/`）。
- **部署目标**: 通过 `CNAME` 文件和 `baseURL` 判断，站点最终部署在 `fb.cdnn1.com`，可能使用了 GitHub Pages 或类似的静态托管服务配合 CDN。

### 4. 开发者注意事项
- **构建命令**: 在本地安装 Hugo 后，运行 `hugo` 即可生成静态文件到 `public/` 目录。开发预览可使用 `hugo server`。
- **版本一致性**: 确保本地安装的 Hugo 版本与生成环境兼容，虽然静态站点通常兼容性较好，但主题可能依赖特定版本特性。
- **避免直接修改 public/**: 原则上应修改根目录下的 `.md` 文件或主题配置，然后重新生成 `public/` 目录，而不是直接编辑 `public/` 下的 HTML 文件，否则下次构建会被覆盖。