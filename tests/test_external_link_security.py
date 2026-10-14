"""Network-free regressions for external link request boundaries."""
import importlib.util
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('link_security', ROOT / 'scripts/verify_knowledge_base.py')
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


def address(ip):
    family = socket.AF_INET6 if ':' in ip else socket.AF_INET
    sockaddr = (ip, 443, 0, 0) if family == socket.AF_INET6 else (ip, 443)
    return (family, socket.SOCK_STREAM, socket.IPPROTO_TCP, '', sockaddr)


class ExternalLinkSecurityTests(unittest.TestCase):
    def test_nonpublic_and_mixed_dns_never_connect(self):
        for ips in [('127.0.0.2',), ('10.0.0.1',), ('169.254.169.254',),
                    ('0.0.0.0',), ('224.0.0.1',), ('::1',), ('fc00::1',),
                    ('fe80::1',), ('fec0::1',), ('::ffff:127.0.0.1',),
                    ('8.8.8.8', '192.168.0.1')]:
            with self.subTest(ips=ips), \
                    patch.object(kb.socket, 'getaddrinfo', return_value=[address(ip) for ip in ips]), \
                    patch.object(kb.socket, 'socket') as connect:
                self.assertEqual(kb._probe('https://probe.invalid/', 1)[0], 'fail')
                connect.assert_not_called()

    def test_schemes_and_credentials_rejected_before_dns(self):
        for url in ['file:///etc/passwd', 'ftp://probe.invalid/file',
                    'https://user:pass@probe.invalid/', 'https://probe.invalid:bad/']:
            with self.subTest(url=url), patch.object(kb.socket, 'getaddrinfo') as dns:
                self.assertEqual(kb._probe(url, 1)[0], 'fail')
                dns.assert_not_called()

    def test_private_redirect_never_opens_second_connection(self):
        conn = Mock()
        conn.getresponse.return_value.status = 302
        conn.getresponse.return_value.getheader.return_value = 'http://127.0.0.2/admin'
        with patch.object(kb.socket, 'getaddrinfo', side_effect=[
                [address('8.8.8.8')], [address('127.0.0.2')]]), \
                patch.object(kb, 'PublicHTTPSConnection', return_value=conn) as https, \
                patch.object(kb, 'PublicHTTPConnection') as http:
            self.assertEqual(kb._probe('https://probe.invalid/', 1)[0], 'fail')
            https.assert_called_once()
            http.assert_not_called()
            conn.close.assert_called_once()

    def test_connection_uses_vetted_sockaddr_without_dns_lookup(self):
        vetted = [address('8.8.8.8')]
        sock = Mock()
        with patch.object(kb.socket, 'socket', return_value=sock), \
                patch.object(kb.socket, 'getaddrinfo') as dns:
            connection = kb.PublicHTTPConnection('probe.invalid', timeout=2)
            connection.public_addresses = vetted
            connection.connect()
            sock.connect.assert_called_once_with(vetted[0][4])
            dns.assert_not_called()
            connection.close()

    def test_tls_preserves_original_hostname(self):
        context = Mock()
        sock = Mock()
        with patch.object(kb, '_connect_public', return_value=sock):
            connection = kb.PublicHTTPSConnection('probe.invalid', context=context)
            connection.public_addresses = [address('8.8.8.8')]
            connection.connect()
            context.wrap_socket.assert_called_once_with(sock, server_hostname='probe.invalid')
            connection.close()

    def test_head_fallback_and_gated_status(self):
        with patch.object(kb, '_public_request', side_effect=[405, 200]) as request:
            self.assertEqual(kb._probe('https://probe.invalid/', 1), ('ok', None))
            self.assertEqual([call.args[1] for call in request.call_args_list], ['HEAD', 'GET'])
            self.assertEqual(request.call_args.args[2]['Range'], 'bytes=0-1023')
        with patch.object(kb, '_public_request', return_value=403) as request:
            self.assertEqual(kb._probe('https://probe.invalid/', 1)[0], 'warn')
            request.assert_called_once()

    def test_redirect_limit_and_relative_public_redirect(self):
        conn = Mock()
        conn.getresponse.return_value.status = 302
        conn.getresponse.return_value.getheader.return_value = '/next'
        with patch.object(kb.socket, 'getaddrinfo', return_value=[address('8.8.8.8')]), \
                patch.object(kb, 'PublicHTTPSConnection', return_value=conn):
            self.assertEqual(kb._probe('https://probe.invalid/', 1)[0], 'fail')
            self.assertEqual(conn.request.call_count, 6)
            self.assertEqual(conn.request.call_args.args[1], '/next')
            self.assertEqual(conn.close.call_count, 6)

    def test_ipv6_url_collection_and_host(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sample.md'
            path.write_text('[link](http://[::1]:8123/check)')
            self.assertEqual(kb._collect_urls(path), ['http://[::1]:8123/check'])
            self.assertEqual(kb._url_host('http://[::1]:8123/check'), '::1')


if __name__ == '__main__':
    unittest.main()
