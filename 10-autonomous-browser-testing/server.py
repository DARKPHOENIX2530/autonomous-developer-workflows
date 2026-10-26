"""
Fullstack Web App Mock Harness
Simulates an authentication & dashboard service for autonomous QA testing.
Part 10 of Autonomous Developer Workflows Series (@SystemZeroTech)
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class MockAppHandler(BaseHTTPRequestHandler):
    def _send_response_with_headers(self, status: int, content_type: str, body: bytes):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        # Production security headers
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            body = json.dumps({"status": "healthy", "version": "2.4.0"}).encode("utf-8")
            self._send_response_with_headers(200, "application/json", body)
        elif parsed.path == "/":
            html = """<!DOCTYPE html>
<html>
<head><title>System Zero Cloud Portal</title></head>
<body>
    <h1>System Zero Developer Portal</h1>
    <form id="signup-form" action="/api/v1/auth/register" method="POST">
        <input name="email" type="email" placeholder="dev@company.com" required />
        <input name="password" type="password" required />
        <button type="submit" id="submit-btn">Create Account</button>
    </form>
</body>
</html>"""
            self._send_response_with_headers(200, "text/html", html.encode("utf-8"))
        else:
            self._send_response_with_headers(404, "application/json", json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        if parsed.path == "/api/v1/auth/register":
            try:
                payload = json.loads(post_data.decode("utf-8"))
            except Exception:
                payload = {}

            email = payload.get("email", "")
            password = payload.get("password", "")

            # Autonomous agent testing assertions:
            # 1. Reject XSS script injection
            if "<script>" in email.lower() or "<img" in email.lower():
                resp = {"success": False, "error": "Malicious payload detected (XSS Sanitize Filter)"}
                self._send_response_with_headers(400, "application/json", json.dumps(resp).encode("utf-8"))
                return

            # 2. Reject empty or weak password
            if len(password) < 8:
                resp = {"success": False, "error": "Password must be at least 8 characters"}
                self._send_response_with_headers(422, "application/json", json.dumps(resp).encode("utf-8"))
                return

            # 3. Successful registration
            resp = {
                "success": True,
                "user_id": "usr_99214ab",
                "email": email,
                "token": "bearer_jwt_prod_mock_token"
            }
            self._send_response_with_headers(201, "application/json", json.dumps(resp).encode("utf-8"))
        else:
            self._send_response_with_headers(404, "application/json", json.dumps({"error": "Route not found"}).encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress standard logging to keep test output clean
        return
