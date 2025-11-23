"""Simple cell client to probe a running AIOS cell and fetch metrics.

Usage:
    python -m ai.tools.cell_client --host http://localhost:8000 --metrics http://localhost:9091/metrics

This script uses the standard library only (urllib) so no extra deps are required.
"""
import argparse
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def http_get(url, timeout=5):
    req = Request(url, headers={"User-Agent": "aios-cell-client/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8'), resp.getcode(), dict(resp.getheaders())
    except HTTPError as e:
        return e.read().decode('utf-8') if e.fp else str(e), e.code, {}
    except URLError as e:
        return str(e), None, {}


def probe_host(host_url):
    print(f"Probing host: {host_url}")
    for path in ['/', '/health', '/status', '/v1/health', '/api/health']:
        url = host_url.rstrip('/') + path
        try:
            body, code, headers = http_get(url)
            print(f"GET {url} -> status={code}")
            if body and len(body) > 0:
                snippet = body[:1000]
                print(snippet)
        except Exception as e:
            print(f"GET {url} -> error: {e}")
        print('---')


def fetch_metrics(metrics_url):
    print(f"Fetching metrics: {metrics_url}")
    body, code, headers = http_get(metrics_url)
    if code not in (200,):
        print(f"Metrics fetch returned status: {code}")
    print(body[:2000])


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--host', help='Base HTTP host (e.g. http://localhost:8000)')
    p.add_argument('--metrics', help='Prometheus metrics URL (e.g. http://localhost:9091/metrics)')
    args = p.parse_args(argv)

    if not args.host and not args.metrics:
        p.print_help()
        sys.exit(1)

    if args.host:
        probe_host(args.host)
    if args.metrics:
        fetch_metrics(args.metrics)


if __name__ == '__main__':
    main()
