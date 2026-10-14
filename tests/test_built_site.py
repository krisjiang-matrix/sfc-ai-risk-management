import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'


@unittest.skipUnless((SITE / 'search/search_index.json').exists(), 'Build site before running output checks')
class BuiltSiteTests(unittest.TestCase):
    def test_retired_content_is_not_in_search(self):
        index = json.loads((SITE / 'search/search_index.json').read_text(encoding='utf-8'))
        with (ROOT / 'docs/migrations.csv').open(encoding='utf-8', newline='') as fp:
            retired = []
            for row in csv.DictReader(fp):
                old = Path(row['old_path'])
                if old.suffix == '.md':
                    url = old.parent if old.name == 'index.md' else old.with_suffix('')
                    retired.append(url.as_posix().rstrip('/') + '/')
        for entry in index['docs']:
            self.assertFalse(any(entry['location'].startswith(path) for path in retired), entry['location'])
        self.assertTrue(any(entry['location'].startswith('concepts/rag/') for entry in index['docs']))

    def test_every_redirect_resolves_to_built_target(self):
        with (ROOT / 'docs/migrations.csv').open(encoding='utf-8', newline='') as fp:
            rows = list(csv.DictReader(fp))
        for row in rows:
            if row['mode'] != 'redirect':
                continue
            old = Path(row['old_path'])
            source = SITE / (old.parent if old.name == 'index.md' else old.with_suffix('')) / 'index.html'
            content = source.read_text(encoding='utf-8')
            match = re.search(r'<meta http-equiv="refresh" content="0; url=([^"<>]+)"', content)
            self.assertIsNotNone(match, row['old_path'])
            resolved = (source.parent / match.group(1)).resolve()
            target = Path(row['target_path'])
            expected = (SITE / (target.parent if target.name == 'index.md' else target.with_suffix(''))).resolve()
            self.assertEqual(resolved, expected, row['old_path'])
            self.assertTrue((resolved / 'index.html').is_file(), row['target_path'])

    def test_clear_primary_navigation_entries(self):
        content = (SITE / 'index.html').read_text(encoding='utf-8')
        for title in ['首页', 'SFC 要求', '风险知识', '实现方法', '工具参考']:
            self.assertIn(title, content)
        self.assertNotIn('执行手册与导读', content)
        self.assertNotIn('模板与案例', content)
        self.assertNotIn('专题与资源', content)
        self.assertNotIn('知识导航', content)


if __name__ == '__main__':
    unittest.main()
