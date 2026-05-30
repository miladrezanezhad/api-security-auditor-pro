import re

async def test_sql_injection(request_builder, target_url: str) -> dict:
    """Test for SQL injection vulnerabilities."""
    sql_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "1' AND '1'='1",
        "1' AND '1'='2",
        "' UNION SELECT NULL--"
    ]
    
    for payload in sql_payloads:
        response = await request_builder.get(target_url, params={"id": payload})
        if response and response.text:
            if _detect_sql_error(response.text):
                return {
                    "finding": "SQL Injection",
                    "payload": payload,
                    "severity": "CRITICAL",
                    "remediation": "Use parameterized queries/prepared statements"
                }
    return None

async def test_xss(request_builder, target_url: str) -> dict:
    """Test for XSS vulnerabilities."""
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')"
    ]
    
    for payload in xss_payloads:
        response = await request_builder.get(target_url, params={"q": payload})
        if response and payload in response.text:
            return {
                "finding": "Reflected XSS",
                "payload": payload,
                "severity": "MEDIUM",
                "remediation": "Implement output encoding, use CSP"
            }
    return None

async def test_nosql_injection(request_builder, target_url: str) -> dict:
    """Test for NoSQL injection vulnerabilities."""
    nosql_payloads = [
        '{"$ne": null}',
        '{"$gt": ""}',
        '{"$regex": "^.*$"}'
    ]
    
    for payload in nosql_payloads:
        response = await request_builder.post(target_url, json=eval(payload))
        if response and response.status == 200:
            return {
                "finding": "Potential NoSQL Injection",
                "payload": payload,
                "severity": "CRITICAL",
                "remediation": "Validate input, use parameterized queries"
            }
    return None

def _detect_sql_error(text: str) -> bool:
    """Detect SQL error patterns."""
    sql_errors = [
        "SQL syntax",
        "mysql_fetch",
        "ORA-[0-9]{5}",
        "PostgreSQL",
        "SQLite",
        "ODBC Driver"
    ]
    
    for error in sql_errors:
        if re.search(error, text, re.IGNORECASE):
            return True
    return False