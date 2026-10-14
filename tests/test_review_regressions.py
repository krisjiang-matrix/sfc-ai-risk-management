"""Offline regressions for workflow outputs, search exclusion and JSON consumers."""
from contextlib import redirect_stdout
import importlib.util
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch

import test_built_site

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('review_kb', ROOT / 'scripts/verify_knowledge_base.py')
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


def workflow_run(name):
    text = (ROOT / '.github/workflows/sfc-watch.yml').read_text(encoding='utf-8')
    step = text.split('      - name: ' + name + '\n', 1)[1]
    block = step.split('        run: |\n', 1)[1].split('\n      - name:', 1)[0]
    return textwrap.dedent(block)


class ReviewRegressionTests(unittest.TestCase):
    def test_watch_diff_outputs_new_known_and_unavailable(self):
        run = workflow_run('Compare against registered circulars')
        script = run.split("python - <<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
        cases = [('{"refNo":"26EC99"}', 'ok', '26EC99', '1'),
                 ('{"refNo":"24EC55"}', 'ok', '', '1'),
                 (None, 'unavailable', '', '0')]
        for response, status, new, found in cases:
            with self.subTest(response=response), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / 'docs').mkdir()
                (root / 'docs/source-register.csv').write_text('version\n24EC55\n', encoding='utf-8')
                (root / '.sfc-watch').mkdir()
                if response is not None:
                    (root / '.sfc-watch/index.json').write_text(response, encoding='utf-8')
                output = root / 'outputs'
                result = subprocess.run([sys.executable, '-c', script], cwd=root,
                    env=dict(os.environ, GITHUB_OUTPUT=str(output)), capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                values = dict(line.split('=', 1) for line in output.read_text().splitlines())
                self.assertEqual(values, dict(status=status, known='1', found=found, new=new))

    def test_watch_probe_outputs_success_and_unavailable(self):
        script = workflow_run('Fetch SFC circulars index for AI-related documents')
        for response in ('{"refNo":"26EC99"}', ''):
            with self.subTest(response=response), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                executable = root / 'curl'
                executable.write_text('#!/bin/sh\nprintf "%s" "$WATCH_RESPONSE" > .sfc-watch/index.json\n')
                executable.chmod(0o755)
                output = root / 'outputs'
                result = subprocess.run(['bash', '-c', script], cwd=root,
                    env=dict(os.environ, GITHUB_OUTPUT=str(output), WATCH_RESPONSE=response,
                             PATH=str(root) + os.pathsep + os.environ['PATH']),
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                values = dict(line.split('=', 1) for line in output.read_text().splitlines())
                self.assertEqual(values['fetched'], str(len(response.encode())))

    def test_search_rejects_retired_directory_page_and_anchor(self):
        for location in ('chapters/old/', 'chapters/old/#section',
                         'handbook/old/', 'handbook/old/#section'):
            with self.subTest(location=location), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / 'docs').mkdir()
                (root / 'docs/migrations.csv').write_text(
                    'old_path,target_path,mode\n'
                    'chapters/old/index.md,concepts/rag.md,redirect\n'
                    'handbook/old.md,concepts/rag.md,redirect\n', encoding='utf-8')
                site = root / 'site'
                (site / 'search').mkdir(parents=True)
                index = site / 'search/search_index.json'
                entries = [{'location': 'concepts/rag/'}]
                with patch.object(test_built_site, 'ROOT', root), patch.object(test_built_site, 'SITE', site):
                    check = test_built_site.BuiltSiteTests('test_retired_content_is_not_in_search')
                    index.write_text(json.dumps({'docs': entries}))
                    check.test_retired_content_is_not_in_search()
                    index.write_text(json.dumps({'docs': entries + [{'location': location}]}))
                    with self.assertRaises(AssertionError):
                        check.test_retired_content_is_not_in_search()

    def test_external_json_preserves_warnings_and_failure_status(self):
        for issues, warnings, exit_code in [([], [], 0),
                ([], ['https://mock.invalid -> HTTP 403'], 0),
                (['https://mock.invalid -> HTTP 404'], ['gated source'], 1)]:
            with self.subTest(issues=issues, warnings=warnings):
                stdout = StringIO()
                with patch.object(sys, 'argv', ['verify', '--json', '--check-external']), \
                        patch.object(kb, 'verify_external', return_value=(1, issues, warnings)), \
                        redirect_stdout(stdout):
                    code = kb.main()
                payload = json.loads(stdout.getvalue())
                self.assertEqual(code, exit_code)
                self.assertEqual(payload['failed'], bool(issues))
                self.assertEqual(payload['warnings'], warnings)
                external = next(item for item in payload['results'] if item['name'] == '外链存活')
                self.assertEqual(external['issues'], issues)


if __name__ == '__main__':
    unittest.main()
