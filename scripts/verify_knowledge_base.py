#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SFC AI 风险管理知识库 — 完整性与质量校验

用法:
    python scripts/verify_knowledge_base.py                 # 离线校验（CI 默认）
    python scripts/verify_knowledge_base.py --check-external  # 额外检查外链存活
    python scripts/verify_knowledge_base.py --fix-counts      # 从文件系统重写数量表述
    python scripts/verify_knowledge_base.py --json             # 机器可读输出

校验项:
    [1] 站内 Markdown 链接有效性
    [2] CSV 格式与 RFC 4180 兼容性
    [3] source_id 交叉引用完整性（正文引用 vs 来源登记册）
    [4] 跨文件重复内容检测
    [5] mkdocs nav 覆盖率
    [6] 数量表述与磁盘实际一致性
    [7] 页面元数据完整性（来源核实日期/发布日期）
    [8–10] 知识覆盖、旧路径迁移与内容边界
    [可选] 外链存活（--check-external，需要网络）

退出码: 0 = 全部通过, 1 = 存在 FAIL
"""

import argparse
import csv
import hashlib
import http.client
import ipaddress
import json
import os
import re
import sys
import socket
import ssl
from urllib.parse import urljoin, urlsplit
import unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SKIP_DIRS = {'.git', 'site', '.cache', '.workbuddy', '__pycache__', '.venv', 'node_modules'}

# 内容标记体系（见 CONTRIBUTING.md 第四节）
REQUIRED_MARKERS = [
    '监管要求',
    '监管附录示例',
    '技术解释',
    '参考方法',
    '教学示例',
    '可选工具/框架',
]


# ---------------------------------------------------------------------------
# 通用工具
# ---------------------------------------------------------------------------

def iter_files(root, exts):
    """遍历仓库文件，跳过构建产物与隐藏目录。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if os.path.splitext(f)[1].lower() in exts:
                yield os.path.join(dirpath, f)


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, '/')


def read(path):
    with open(path, 'r', encoding='utf-8') as fp:
        return fp.read()


def is_markdown_path(path):
    return os.path.splitext(path)[1].lower() == '.md'


# ---------------------------------------------------------------------------
# [1] 站内 Markdown 链接
# ---------------------------------------------------------------------------

def verify_links():
    broken = []
    count = 0
    pattern = re.compile(r'(?<!\!)\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')

    # GitHub 解析的虚拟路径，不存在于磁盘上
    virtual = (
        re.compile(r'^\.github/workflows/[^/]+/badge\.svg$'),
        re.compile(r'^blob/'),
        re.compile(r'^tree/'),
    )

    for path in iter_files(ROOT, {'.md'}):
        count += 1
        try:
            content = read(path)
        except Exception as exc:
            broken.append((rel(path), '<file>', 'ENCODING_ERROR: %s' % exc))
            continue

        for text, link in pattern.findall(content):
            link = link.strip()
            if link.startswith(('http://', 'https://', 'mailto:', 'ftp://', 'tel:')):
                continue
            if link.startswith('#'):
                continue
            target = link.split('#')[0].strip()
            if not target:
                continue
            # 去掉 query string
            target = target.split('?')[0]
            if any(rx.match(target) for rx in virtual):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                broken.append((rel(path), text, link))

    return count, broken


# ---------------------------------------------------------------------------
# [2] CSV 格式
# ---------------------------------------------------------------------------

def verify_csv():
    errors = []
    count = 0

    for path in iter_files(ROOT, {'.csv'}):
        count += 1
        r = rel(path)
        try:
            with open(path, 'r', encoding='utf-8-sig', newline='') as fp:
                reader = csv.reader(fp)
                rows = list(reader)
        except Exception as exc:
            errors.append('%s: 读取失败: %s' % (r, exc))
            continue

        if not rows:
            errors.append('%s: 空文件' % r)
            continue

        header = rows[0]
        cols = len(header)
        if any(not h.strip() for h in header):
            errors.append('%s: 表头存在空列名' % r)
        for idx, row in enumerate(rows[1:], start=2):
            if len(row) != cols:
                errors.append('%s 第 %d 行: 期望 %d 列, 实际 %d 列' % (r, idx, cols, len(row)))
    return count, errors


# ---------------------------------------------------------------------------
# [3] source_id 交叉引用
# ---------------------------------------------------------------------------

SOURCE_ID_IN_TEXT = re.compile(
    r'\b('
    r'SFC-\d{2}EC\d{2}(?:-[A-Z])?'   # SFC-24EC55, SFC-26EC11, SFC-26EC11-A
    r'|SFC-\d{2}PR\d+'               # SFC-26PR148
    r'|HKMA-\d{8}'                    # HKMA-20260827
    r'|GARAK-[A-Z-]+'                 # GARAK-README
    r'|NIST-[A-Z0-9-]+'               # NIST-AI-100-1
    r'|OWASP-[A-Z0-9-]+'              # OWASP-LLM-TOP10
    r'|MITRE-[A-Z0-9-]+'              # MITRE-ATLAS
    r')\b')


def verify_source_ids():
    register = os.path.join(ROOT, 'docs', 'source-register.csv')
    if not os.path.exists(register):
        return 0, ['docs/source-register.csv 不存在'], []

    with open(register, 'r', encoding='utf-8-sig', newline='') as fp:
        reader = csv.DictReader(fp)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    ids = set()
    empty_status = []
    for row in rows:
        sid = (row.get('source_id') or '').strip()
        if not sid:
            continue
        ids.add(sid)
        status = (row.get('verification_status') or '').strip()
        if not status:
            empty_status.append('%s: verification_status 为空' % sid)

    missing_col = [c for c in ('source_id', 'url', 'accessed_at', 'verification_status')
                   if c not in fieldnames]

    # 收集正文中的引用
    referenced = {}
    for path in iter_files(ROOT, {'.md'}):
        if rel(path).startswith('site/'):
            continue
        try:
            content = read(path)
        except Exception:
            continue
        for sid in SOURCE_ID_IN_TEXT.findall(content) + re.findall(r'source_id:\s*`?([A-Z][A-Z0-9-]+)', content):
            referenced.setdefault(sid, set()).add(rel(path))

    unknown = sorted(sid for sid in referenced if sid not in ids)
    orphans = sorted(ids - set(referenced))

    problems = []
    for sid in unknown:
        problems.append('正文引用了未登记的 source_id: %s (出现于 %s)'
                        % (sid, ', '.join(sorted(referenced[sid])[:3])))
    for col in missing_col:
        problems.append('source-register.csv 缺少必需列: %s' % col)
    problems.extend(empty_status)

    return len(ids), problems, orphans


# ---------------------------------------------------------------------------
# [4] 重复内容检测
# ---------------------------------------------------------------------------

def normalize_for_dup(text):
    """归一化后计算指纹：忽略空白差异与元数据行差异。"""
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        # 忽略 frontmatter 与元数据引用行（核实日期、页面状态、来源链接）
        if s.startswith(('---', '> 核实日期', '> 页面状态', '> 维护周期', '> 更新日期')):
            continue
        # 归一化全角/半角空白
        s = unicodedata.normalize('NFKC', s)
        lines.append(re.sub(r'\s+', ' ', s))
    return '\n'.join(lines)


def verify_duplicates():
    groups = {}
    for path in iter_files(ROOT, {'.md'}):
        r = rel(path)
        try:
            size = os.path.getsize(path)
            text = read(path)
        except Exception:
            continue
        if size < 2000:      # 太小的文件重复多半是模板片段
            continue
        norm = normalize_for_dup(text)
        if len(norm) < 1500:
            continue
        digest = hashlib.sha256(norm.encode('utf-8')).hexdigest()
        groups.setdefault(digest, []).append((r, size))

    problems = []
    for digest, members in sorted(groups.items()):
        if len(members) > 1:
            names = ', '.join('%s (%d B)' % (n, s) for n, s in members)
            problems.append('重复内容: %s' % names)

    total = sum(len(m) for m in groups.values())
    return total, problems


# ---------------------------------------------------------------------------
# [5] mkdocs nav 覆盖率
# ---------------------------------------------------------------------------

NAV_ENTRY = re.compile(r':\s*([A-Za-z0-9\-_/]+\.md)\s*$', re.M)


def verify_nav():
    cfg = os.path.join(ROOT, 'mkdocs.yml')
    if not os.path.exists(cfg):
        return 0, 0, ['mkdocs.yml 不存在']

    nav_files = set(NAV_ENTRY.findall(read(cfg)))

    docs = set()
    docs_root = os.path.join(ROOT, 'docs')
    for dirpath, dirnames, filenames in os.walk(docs_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith('.md'):
                docs.add(os.path.relpath(os.path.join(dirpath, f), docs_root).replace(os.sep, '/'))

    migrations = load_migrations()
    legacy = {row['old_path'] for row in migrations if row['old_path'].endswith('.md')}
    missing_nav = sorted(docs - nav_files - legacy)
    missing_docs = sorted(nav_files - docs)

    problems = []
    for f in missing_nav:
        problems.append('页面未加入 mkdocs nav: docs/%s' % f)
    for f in missing_docs:
        problems.append('nav 指向不存在的页面: %s' % f)
    if len(nav_files) != len(NAV_ENTRY.findall(read(cfg))):
        problems.append('mkdocs nav 中存在重复条目（会导致 --strict 构建失败）')

    return len(docs), len(nav_files), problems


# ---------------------------------------------------------------------------
# [6] 数量一致性
# ---------------------------------------------------------------------------

def compute_counts():
    docs = os.path.join(ROOT, 'docs')
    retired = {row['old_path'] for row in load_migrations()}

    def active(sub, exclude_index=True):
        folder = os.path.join(docs, sub)
        return sum(1 for name in os.listdir(folder)
                   if name.endswith('.md') and (not exclude_index or name != 'index.md')
                   and (sub + '/' + name) not in retired) if os.path.isdir(folder) else 0

    return {
        'concept_pages': active('concepts'),
        'methods': active('methods'),
        'tools': active('tools'),
        'topics': active('topics'),
        'legacy_entries': len(retired),
    }


# Optional public count claims are checked against active content, never old stubs.
COUNT_RULES = [
    ('README.md', r'(\d+) concept pages', 'concept_pages'),
    ('README.md', r'(\d+) evaluation methods', 'methods'),
    ('README.md', r'(\d+) tool references', 'tools'),
    ('README.zh-CN.md', r'(\d+) 个核心概念', 'concept_pages'),
    ('README.zh-CN.md', r'(\d+) 个实现方法', 'methods'),
    ('README.zh-CN.md', r'(\d+) 项工具参考', 'tools'),
]


def verify_counts(fix=False):
    counts = compute_counts()
    problems = []
    fixed = 0
    by_file = {}

    for relpath, pattern, key in COUNT_RULES:
        full = os.path.join(ROOT, relpath)
        if not os.path.exists(full):
            continue
        text = read(full)
        by_file.setdefault(relpath, text)

    for relpath, text in list(by_file.items()):
        original = text
        for rpath, pattern, key in COUNT_RULES:
            if rpath != relpath:
                continue
            expected = counts[key]

            def repl(m, val=expected):
                return m.group(0).replace(m.group(1), str(val), 1)

            for m in re.finditer(pattern, text):
                actual = int(m.group(1))
                if actual != expected:
                    problems.append('%s: 数量表述 %s，实际应为 %d (%s)' %
                                    (relpath, m.group(0), expected, key))
            new_text, n = re.subn(pattern, repl, text)
            if n == 0:
                continue
            # 检查实际写入值是否等于期望值
            for m in re.finditer(pattern, new_text):
                actual = int(m.group(1))
                if actual != expected:
                    problems.append('%s: 数量表述 "%s" = %d，实际应为 %d (%s)'
                                    % (relpath, m.group(0)[:40], actual, expected, key))
            text = new_text

        if fix and text != original:
            with open(os.path.join(ROOT, relpath), 'w', encoding='utf-8') as fp:
                fp.write(text)
            fixed += 1

    return counts, problems, fixed


# ---------------------------------------------------------------------------
# [7] 页面元数据
# ---------------------------------------------------------------------------

def verify_metadata():
    """页面元数据：页首必须出现核实/发布日期。

    页首格式在本库中并不统一（`核实日期`、`核实：`、`发布日期`、`维护周期`
    等都存在），因此检查的是**页首是否出现任何形式的日期**——这才是
    maintenance.md 第 2 节真正要求的「来源核实日期」。
    """
    problems = []
    checked = 0
    date_re = re.compile(r'\d{4}-\d{2}-\d{2}|\d{4}\s*年\s*\d{1,2}\s*月')

    for path in iter_files(ROOT, {'.md'}):
        r = rel(path)
        if not r.startswith('docs/'):
            continue

        try:
            text = read(path)
        except Exception:
            continue

        checked += 1
        head = '\n'.join(text.splitlines()[:15])
        if not date_re.search(head):
            problems.append('%s: 页首 15 行内没有日期（缺核实日期/发布日期）' % r)

    return checked, problems


# ---------------------------------------------------------------------------
# [8] 外链存活
# ---------------------------------------------------------------------------

#: 不做存活性检查的主机名——工具页里的本机端点（示例部署位置）与 RFC 2606
#: 保留域名不是可引用的外部来源，检查它们只会产生永久性假失败。
SKIP_HOSTS = re.compile(
    r'^(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|'
    r'(?:[\w-]+\.)*example\.(?:com|org|net)|'
    r'[\w-]*your[\w-]*|example)$',
    re.I,
)

#: URL 里不作为 URL 成分的字符。逗号和分号必须排除：RFC 4180 允许 CSV 字段
#: 内含逗号，直接对原始文本套正则会把「链接 + 后续各列」整行当成 URL。
_URL_RE = re.compile(r'https?://(?:\[[0-9A-Fa-f:.%]+\]|[^\s,;)\]\<>"])+')


def _url_host(url):
    try:
        return urlsplit(url).hostname or ''
    except ValueError:
        return ''


#: 围栏代码块内的示例 URL（例如 CONTRIBUTING.md 里的 CSV 范例）在构建站点中
#: 渲染为代码而非可点击链接，不属于外链失效范围，故整体排除。
_FENCE_RE = re.compile(r'^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$',
                       re.M | re.S | re.I)


def _collect_urls(path):
    """收集单个文件中的待检查 URL（CSV 按字段解析，避免整行误判）。"""
    text = read(path)
    if os.path.splitext(path)[1].lower() == '.csv':
        found = []
        for row in csv.reader(text.splitlines()):
            for cell in row:
                found.extend(_URL_RE.findall(cell))
    else:
        found = _URL_RE.findall(_FENCE_RE.sub('', text))
    return [u.rstrip('.,;)') for u in found]


class UnsafeLink(ValueError):
    """A link is outside the public HTTP(S) probe boundary."""


def _public_destination(url):
    parsed = urlsplit(url)
    if (parsed.scheme not in {'http', 'https'} or not parsed.hostname
            or parsed.username is not None or parsed.password is not None):
        raise UnsafeLink('only credential-free HTTP(S) links are permitted')
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    addresses = socket.getaddrinfo(parsed.hostname, port, type=socket.SOCK_STREAM)
    if not addresses:
        raise UnsafeLink('no destination addresses')
    for family, _, _, _, address in addresses:
        ip = ipaddress.ip_address(address[0].split('%', 1)[0])
        # IPv4-mapped IPv6 must obey the IPv4 policy too.
        mapped = getattr(ip, 'ipv4_mapped', None)
        if (family not in {socket.AF_INET, socket.AF_INET6}
                or not ip.is_global or ip.is_multicast or ip.is_reserved
                or getattr(ip, 'is_site_local', False)
                or (mapped is not None and not mapped.is_global)):
            raise UnsafeLink('non-public destination is not permitted')
    return parsed, addresses


def _connect_public(addresses, timeout):
    # Connect to the exact vetted sockaddr, without a second DNS lookup.
    last_error = None
    for family, socktype, protocol, _, address in addresses:
        sock = socket.socket(family, socktype, protocol)
        try:
            sock.settimeout(timeout)
            sock.connect(address)
            return sock
        except OSError as exc:
            sock.close()
            last_error = exc
    raise last_error or OSError('no usable public address')


class PublicHTTPConnection(http.client.HTTPConnection):
    def connect(self):
        self.sock = _connect_public(self.public_addresses, self.timeout)


class PublicHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        sock = _connect_public(self.public_addresses, self.timeout)
        try:
            # Keep certificate hostname validation and SNI for the original host.
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except Exception:
            sock.close()
            raise


def _public_request(url, method, headers, timeout):
    for _ in range(6):
        parsed, addresses = _public_destination(url)
        cls = PublicHTTPSConnection if parsed.scheme == 'https' else PublicHTTPConnection
        kwargs = {'context': ssl.create_default_context()} if parsed.scheme == 'https' else {}
        conn = cls(parsed.hostname, parsed.port, timeout=timeout, **kwargs)
        conn.public_addresses = addresses
        try:
            path = parsed.path or '/'
            if parsed.query:
                path += '?' + parsed.query
            conn.request(method, path, headers=headers)
            response = conn.getresponse()
            status = response.status
            location = response.getheader('Location')
        finally:
            conn.close()
        if status not in {301, 302, 303, 307, 308}:
            return status
        if not location:
            raise UnsafeLink('redirect has no destination')
        # Every redirect gets scheme, DNS and address validation before connecting.
        url = urljoin(url, location)
    raise UnsafeLink('too many redirects')


def _probe(url, timeout):
    """Probe public HTTP(S) links with pinned DNS and validated redirects.

    Try HEAD then a bounded-range GET; never read the response body, use
    environment proxies, pass URL credentials, or connect to non-public IPs.
    """
    gated = (401, 403, 429)
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; sfc-ai-riskmanagement-linkcheck/1.0)',
        'Accept': '*/*',
    }
    for method in ('HEAD', 'GET'):
        try:
            request_headers = dict(headers, Range='bytes=0-1023') if method == 'GET' else headers
            status = _public_request(url, method, request_headers, timeout)
            if status < 400:
                return 'ok', None
            if status in gated:
                return 'warn', 'HTTP %d（反爬或需鉴权，须人工确认）' % status
            if method == 'GET':
                return 'fail', 'HTTP %d' % status
        except (UnsafeLink, ValueError):
            return 'fail', '安全边界拒绝：仅允许无凭据、公开地址的 HTTP(S) 链接及跳转'
        except Exception as exc:
            if method == 'GET':
                return 'fail', '无法访问: %s' % type(exc).__name__



def verify_external(timeout=12):
    """返回 (待检查数, 失效列表, 待人工确认列表)。

    「待人工确认」指服务器有响应但拒绝自动核验（反爬 403、需鉴权 401、
    限流 429）。这类链接多数是活的，计为失败会让 CI 永久红灯，因此单独
    归类、在报告里提示，但不阻断校验。
    """
    problems = []
    warnings = []
    checked = 0
    urls = {}

    for path in iter_files(ROOT, {'.md', '.csv'}):
        try:
            found = _collect_urls(path)
        except Exception:
            continue
        for url in found:
            if SKIP_HOSTS.match(_url_host(url)):
                continue
            urls.setdefault(url, set()).add(rel(path))

    for url, locations in sorted(urls.items()):
        checked += 1
        state, reason = _probe(url, timeout)
        if state == 'fail':
            problems.append('%s -> %s (%s)'
                            % (url, reason, ', '.join(sorted(locations)[:2])))
        elif state == 'warn':
            warnings.append('%s -> %s (%s)'
                            % (url, reason, ', '.join(sorted(locations)[:2])))

    return checked, problems, warnings



# Knowledge coverage and migration validation. Content truth still needs review.
COVERAGE_STATES = {'完整', '部分', '缺失', '不适用'}
CORE_TOPICS = {'system', 'reliability', 'evaluation', 'rag', 'security', 'privacy',
               'fairness', 'agent', 'monitoring', 'resilience', 'human'}


def load_migrations():
    path = os.path.join(ROOT, 'docs', 'migrations.csv')
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8-sig', newline='') as fp:
        return list(csv.DictReader(fp))


def _docs_path_exists(value):
    base = os.path.realpath(os.path.join(ROOT, 'docs'))
    target = os.path.realpath(os.path.join(base, value))
    return (bool(value) and not os.path.isabs(value)
            and os.path.commonpath([base, target]) == base and os.path.isfile(target))


def verify_coverage():
    path = os.path.join(ROOT, 'docs', 'coverage.csv')
    if not os.path.exists(path):
        return 0, ['docs/coverage.csv 不存在']
    with open(path, encoding='utf-8-sig', newline='') as fp:
        rows = list(csv.DictReader(fp))
    with open(os.path.join(ROOT, 'docs', 'source-register.csv'), encoding='utf-8-sig', newline='') as fp:
        sources = {r['source_id']: r for r in csv.DictReader(fp)}
    issues = []
    ids = [r.get('topic_id', '') for r in rows]
    if set(ids) != CORE_TOPICS or len(ids) != len(CORE_TOPICS):
        issues.append('覆盖矩阵必须恰好包含十一类核心风险（不得缺失或重复）')
    for row in rows:
        prefix = row.get('topic_id', '?')
        for layer, field in [('concept', 'concept_path'), ('method', 'method_paths'),
                             ('tool', 'tool_paths'), ('source', 'source_ids')]:
            status = row.get(layer + '_status', '')
            if status not in COVERAGE_STATES:
                issues.append('%s: %s 覆盖状态无效' % (prefix, layer))
            values = row.get(field, '').split('|') if row.get(field) else []
            if status in {'完整', '部分'} and not values:
                issues.append('%s: %s 状态有覆盖却没有证据路径' % (prefix, layer))
            for value in values:
                if layer == 'source':
                    if value not in sources:
                        issues.append('%s: 未登记来源 %s' % (prefix, value))
                    elif status == '完整' and sources[value].get('verification_status', '') in {'待核实', '仅访问官方入口'}:
                        issues.append('%s: 未核实来源不能标为完整' % prefix)
                elif not _docs_path_exists(value):
                    issues.append('%s: 路径无效 %s' % (prefix, value))
            if status in {'部分', '缺失', '不适用'} and not row.get('gaps', '').strip():
                issues.append('%s: 非完整覆盖必须说明缺口或不适用原因' % prefix)
    return len(rows), issues


def verify_migrations():
    rows = load_migrations()
    issues = []
    paths = [r.get('old_path', '') for r in rows]
    if len(paths) != len(set(paths)):
        issues.append('迁移登记有重复旧路径')
    old_paths = set(paths)
    for row in rows:
        old = row.get('old_path', '')
        target = row.get('target_path', '')
        if not _docs_path_exists(old) or not _docs_path_exists(target):
            issues.append('迁移路径不存在或超出文档根目录: %s -> %s' % (old, target))
            continue
        if target in old_paths:
            issues.append('迁移目标必须是活动知识页，不能形成跳转链: %s' % old)
        mode = row.get('mode', '')
        text = read(os.path.join(ROOT, 'docs', old))
        if mode == 'redirect' and not re.search(r'^redirect_target: ' + re.escape(target) + r'\s*$', text, re.M):
            issues.append('迁移登记与页面跳转目标不一致: %s' % old)
        elif mode == 'notice' and '已退役' not in text and '已迁移' not in text:
            issues.append('迁移说明未标记状态: %s' % old)
        elif mode == 'retired-download' and not text.startswith('status,message,learning_resource'):
            issues.append('旧下载仍包含机构模板字段: %s' % old)
        elif mode not in {'redirect', 'notice', 'retired-download'}:
            issues.append('未知迁移类型: %s' % mode)
    for sub in ('chapters', 'handbook', 'templates'):
        folder = os.path.join(ROOT, 'docs', sub)
        for dirpath, _, filenames in os.walk(folder):
            for name in filenames:
                if name.endswith(('.md', '.csv')):
                    value = os.path.relpath(os.path.join(dirpath, name), os.path.join(ROOT, 'docs')).replace(os.sep, '/')
                    if value not in old_paths:
                        issues.append('旧产品页面未登记迁移: %s' % value)
    return len(rows), issues


def verify_content_boundaries():
    issues = []
    old = {r['old_path'] for r in load_migrations()}
    deprecated = ('[机构执行方法]', '[可选技术]')
    for path in iter_files(os.path.join(ROOT, 'docs'), {'.md'}):
        value = os.path.relpath(path, os.path.join(ROOT, 'docs')).replace(os.sep, '/')
        if value in old:
            continue
        text = read(path)
        for label in deprecated:
            if label in text:
                issues.append('%s: 旧内容标签 %s' % (value, label))
        for line in text.splitlines():
            if '[监管附录示例]' in line and ('完全合成' in line or '自编教学' in line):
                issues.append('%s: 自编教学示例误标为监管附录示例' % value)
        if '待创建' in text or '待制作' in text:
            issues.append('%s: 不应保留工具/模板建设占位' % value)
    return issues


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='SFC AI 风险管理知识库完整性校验')
    parser.add_argument('--check-external', action='store_true', help='额外检查外链存活（需要网络）')
    parser.add_argument('--fix-counts', action='store_true', help='从文件系统重写数量表述')
    parser.add_argument('--json', action='store_true', help='输出 JSON')
    parser.add_argument('--external-timeout', type=int, default=12, help='外链检查超时秒数')
    args = parser.parse_args()

    results = []
    failures = []
    ext_warnings = []

    # [1]
    md_count, broken = verify_links()
    results.append(('Markdown 站内链接', 'FAIL' if broken else 'PASS',
                    '%d 个文件, %d 处失效' % (md_count, len(broken)), broken))
    failures.extend(broken)

    # [2]
    csv_count, csv_errors = verify_csv()
    results.append(('CSV 格式 (RFC 4180)', 'FAIL' if csv_errors else 'PASS',
                    '%d 个文件, %d 处问题' % (csv_count, len(csv_errors)), csv_errors))
    failures.extend(csv_errors)

    # [3]
    sid_count, sid_problems, orphans = verify_source_ids()
    results.append(('source_id 交叉引用', 'FAIL' if sid_problems else 'PASS',
                    '%d 个已登记, %d 个问题, %d 个未被正文引用' % (sid_count, len(sid_problems), len(orphans)),
                    sid_problems))
    failures.extend(sid_problems)

    # [4]
    dup_count, dup_problems = verify_duplicates()
    results.append(('重复内容检测', 'FAIL' if dup_problems else 'PASS',
                    '%d 个文件参与指纹, %d 组重复' % (dup_count, len(dup_problems)), dup_problems))
    failures.extend(dup_problems)

    # [5]
    docs_n, nav_n, nav_problems = verify_nav()
    results.append(('mkdocs nav 覆盖率', 'FAIL' if nav_problems else 'PASS',
                    'docs %d 页 / nav %d 项' % (docs_n, nav_n), nav_problems))
    failures.extend(nav_problems)

    # [6]
    counts, count_problems, fixed = verify_counts(fix=args.fix_counts)
    count_label = ', '.join('%s=%d' % (k, v) for k, v in sorted(counts.items()))
    if args.fix_counts and fixed:
        count_label += ' | 已重写 %d 个文件' % fixed
    results.append(('数量一致性', 'FAIL' if count_problems else 'PASS',
                    count_label, count_problems))
    if not args.fix_counts:
        failures.extend(count_problems)

    # [7]
    meta_n, meta_problems = verify_metadata()
    results.append(('页面元数据', 'FAIL' if meta_problems else 'PASS',
                    '%d 页检查, %d 处缺失' % (meta_n, len(meta_problems)), meta_problems))
    failures.extend(meta_problems)

    coverage_n, coverage_issues = verify_coverage()
    results.append(('知识覆盖矩阵', 'FAIL' if coverage_issues else 'PASS',
                    '%d 个核心主题' % coverage_n, coverage_issues))
    failures.extend(coverage_issues)
    migration_n, migration_issues = verify_migrations()
    results.append(('旧路径迁移', 'FAIL' if migration_issues else 'PASS',
                    '%d 个兼容入口' % migration_n, migration_issues))
    failures.extend(migration_issues)
    boundary_issues = verify_content_boundaries()
    results.append(('内容边界与标签', 'FAIL' if boundary_issues else 'PASS',
                    '自动检查不能替代来源及教学质量审阅', boundary_issues))
    failures.extend(boundary_issues)

    # External checks are optional because upstream availability varies.
    if args.check_external:
        ext_n, ext_problems, ext_warnings = verify_external(args.external_timeout)
        detail = '%d 个链接, %d 处不可达' % (ext_n, len(ext_problems))
        if ext_warnings:
            detail += ', %d 处须人工确认' % len(ext_warnings)
        results.append(('外链存活', 'FAIL' if ext_problems else 'PASS',
                        detail, ext_problems))
        if ext_warnings and not args.json:
            print('    提示: %d 个链接被反爬/需鉴权，无法自动判定，未计为失败：'
                  % len(ext_warnings))
            for w in ext_warnings[:12]:
                print('      ~ %s' % (w,))
        failures.extend(ext_problems)

    if args.json:
        print(json.dumps({
            'results': [{'name': n, 'status': s, 'detail': d, 'issues': i[:50]}
                        for n, s, d, i in results],
            'failed': bool(failures),
            'warnings': ext_warnings,
        }, ensure_ascii=False, indent=2))
        return 1 if failures else 0

    print('=' * 68)
    print('SFC AI 风险管理知识库 — 完整性校验')
    print('仓库根目录: %s' % ROOT)
    print('=' * 68)

    for i, (name, status, detail, issues) in enumerate(results, start=1):
        mark = 'FAIL' if status == 'FAIL' else 'PASS'
        print('\n[%d] %-22s %s' % (i, name, mark))
        print('    %s' % detail)
        for issue in issues[:12]:
            print('      - %s' % (issue,))
        if len(issues) > 12:
            print('      ... 另有 %d 处' % (len(issues) - 12))

    print('\n' + '=' * 68)
    if failures:
        print('总体结果: FAILED（%d 处问题，见上）' % (len(failures),))
        print('=' * 68)
        return 1

    print('总体结果: PASSED ALL CHECKS')
    if orphans:
        print('提示: %d 个 source_id 已登记但正文未引用（可接受，但请确认是否遗漏引用）'
              % len(orphans))
        for o in orphans:
            print('      - %s' % o)
    print('=' * 68)
    return 0


if __name__ == '__main__':
    sys.exit(main())
