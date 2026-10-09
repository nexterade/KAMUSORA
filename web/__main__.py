"""Serve a static folder locally: python -m web [directory] --port 8080"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os


def main():
    parser = argparse.ArgumentParser(description="Run a local static web server for KAMUSORA.")
    parser.add_argument("directory", nargs="?", default=".", help="Folder containing index.html (default: current folder)")
    parser.add_argument("--port", type=int, default=8080, help="Port to use (default: 8080)")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address; use 0.0.0.0 to allow access from other devices (default: 127.0.0.1)")
    args = parser.parse_args()
    root = Path(args.directory).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"directory not found: {root}")
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    os.chdir(root)
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    display_host = "127.0.0.1" if args.host == "0.0.0.0" else args.host
    print(f"KAMUSORA local server: http://{display_host}:{args.port}")
    if args.host == "0.0.0.0":
        print("Listening on all network interfaces. Use your phone IP for LAN access; only share on trusted networks.")
    print(f"Serving folder: {root}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKAMUSORA server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
