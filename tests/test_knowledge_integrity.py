import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


kb = module('kb', ROOT / 'scripts/verify_knowledge_base.py')
hooks = module('hooks', ROOT / 'scripts/mkdocs_hooks.py')


class IntegrityTests(unittest.TestCase):
    def fixture(self, root):
        docs = root / 'docs'
        docs.mkdir()
        (docs / 'source-register.csv').write_text(
            'source_id,verification_status\nSFC-24EC55,已读取编号PDF\n', encoding='utf-8')
        for name in ('concept.md', 'method.md', 'tool.md'):
            (docs / name).write_text('# Learning content', encoding='utf-8')
        fields = ['topic_id', 'concept_path', 'concept_status', 'method_paths',
                  'method_status', 'tool_paths', 'tool_status', 'source_ids',
                  'source_status', 'gaps']
        with (docs / 'coverage.csv').open('w', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=fields)
            writer.writeheader()
            for topic in sorted(kb.CORE_TOPICS):
                writer.writerow(dict(topic_id=topic, concept_path='concept.md',
                    concept_status='完整', method_paths='method.md', method_status='完整',
                    tool_paths='tool.md', tool_status='完整', source_ids='SFC-24EC55',
                    source_status='完整', gaps=''))
        return docs

    def test_complete_matrix_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            self.fixture(Path(folder))
            with patch.object(kb, 'ROOT', folder):
                self.assertEqual(kb.verify_coverage(), (11, []))

    def test_missing_evidence_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            docs = self.fixture(Path(folder))
            (docs / 'method.md').unlink()
            with patch.object(kb, 'ROOT', folder):
                self.assertTrue(any('路径无效' in e for e in kb.verify_coverage()[1]))

    def test_partial_without_gap_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            docs = self.fixture(Path(folder))
            path = docs / 'coverage.csv'
            path.write_text(path.read_text(encoding='utf-8').replace('完整', '部分'), encoding='utf-8')
            with patch.object(kb, 'ROOT', folder):
                self.assertTrue(any('必须说明缺口' in e for e in kb.verify_coverage()[1]))

    def test_docs_path_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as folder:
            docs = self.fixture(Path(folder))
            (Path(folder) / 'outside.md').write_text('outside', encoding='utf-8')
            with patch.object(kb, 'ROOT', folder):
                self.assertFalse(kb._docs_path_exists('../outside.md'))
                self.assertFalse(kb._docs_path_exists(str(Path(folder) / 'outside.md')))

    def test_redirect_target_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            docs = self.fixture(Path(folder))
            (docs / 'legacy.md').write_text('redirect_target: tool.md', encoding='utf-8')
            (docs / 'migrations.csv').write_text(
                'old_path,target_path,mode\nlegacy.md,concept.md,redirect\n', encoding='utf-8')
            with patch.object(kb, 'ROOT', folder):
                self.assertTrue(any('不一致' in e for e in kb.verify_migrations()[1]))

    def test_redirect_chain_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            docs = self.fixture(Path(folder))
            (docs / 'old.md').write_text('redirect_target: concept.md', encoding='utf-8')
            (docs / 'migrations.csv').write_text(
                'old_path,target_path,mode\nold.md,concept.md,redirect\nconcept.md,method.md,notice\n', encoding='utf-8')
            with patch.object(kb, 'ROOT', folder):
                self.assertTrue(any('不能形成跳转链' in e for e in kb.verify_migrations()[1]))

    def test_redirect_urls_work_at_project_subpath(self):
        self.assertEqual(hooks.migration_url('chapters/03/rag/index.html', 'topics/rag/index.html'),
                         '../../../topics/rag/index.html')
        self.assertEqual(hooks.migration_url('handbook/complete-handbook/index.html', 'coverage/index.html'),
                         '../../coverage/index.html')
        self.assertEqual(hooks.migration_url('old.html', 'concepts/rag.html'), 'concepts/rag.html')

    def test_count_drift_is_detected_before_rewrite(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'README.md').write_text('9 topic pages', encoding='utf-8')
            with patch.object(kb, 'ROOT', folder), patch.object(kb, 'compute_counts', return_value={'chapter_pages': 3}), \
                    patch.object(kb, 'COUNT_RULES', [('README.md', r'(\d+) topic pages', 'chapter_pages')]):
                self.assertTrue(kb.verify_counts()[1])
                self.assertEqual(Path(folder, 'README.md').read_text(encoding='utf-8'), '9 topic pages')
                kb.verify_counts(fix=True)
                self.assertEqual(Path(folder, 'README.md').read_text(encoding='utf-8'), '3 topic pages')


if __name__ == '__main__':
    unittest.main()
