"""Render registered legacy learning links without indexing old institutional pages."""
import html
import posixpath


def migration_url(current_url, target_url):
    return posixpath.relpath(target_url, posixpath.dirname(current_url) or '.')


def on_page_content(content, page, config, files):
    target = page.meta.get('redirect_target')
    if not target:
        return content
    dest = files.get_file_from_path(target)
    if dest is None:
        raise ValueError('Missing migration target: ' + target)
    url = html.escape(migration_url(page.file.url, dest.url), quote=True)
    return ('<meta http-equiv="refresh" content="0; url=' + url + '">'
            '<p>知识入口已迁移：<a href="' + url + '">打开新的知识页</a></p>' + content)
