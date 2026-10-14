# 浏览器依赖复核

> 更新日期：2026-10-14。内容性质：站点维护说明。

`package.json` 与 `package-lock.json` 记录站点加载的 Mermaid 及 ResizeObserver 兼容库的精确版本和传递依赖。`assets.json` 记录固定 CDN URL 与 SHA-384 SRI；图表文件已与 npm 官方包校验一致。

站点构建不需要 Node。维护者修改版本时，在此目录使用 `npm install --package-lock-only --ignore-scripts` 更新清单，核验 npm 包完整性及 CDN 文件、更新 SRI，再审计完整 npm 闭包并检查实际图表。不要只改 CDN 版本号。

Material 的内置浏览器依赖由 Python 锁定的主题版本确定；升级主题时须另核对该发行版本的 package-lock。初始化由 overrides/main.html 在 Material 脚本之前加载固定版本，旧浏览器兼容库仅在缺少原生 ResizeObserver 时加载。
