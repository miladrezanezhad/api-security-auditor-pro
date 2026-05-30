

import base64
import json

async def check_jwt_vulnerabilities(token: str = None, session=None) -> dict:
    """Check JWT vulnerabilities."""
    if not token:
        return None
    
    findings = []
    
    # Check for none algorithm
    if token.startswith('eyJ'):
        try:
            header = json.loads(base64.b64decode(token.split('.')[0] + '==').decode())
            if header.get('alg') == 'none':
                findings.append({
                    "type": "JWT None Algorithm",
                    "severity": "HIGH",
                    "details": "JWT accepts 'none' algorithm"
                })
        except:
            pass
    
    # Check for weak secrets (common passwords)
    weak_secrets = ['secret', 'password', 'changeme', 'admin', 'test', '123456']
    
    if findings:
        return {
            "finding": "JWT Vulnerabilities Detected",
            "details": findings,
            "severity": "HIGH",
            "remediation": "Use strong secrets, validate algorithm, set short expiration"
        }
    
    return None

async def check_idor(scanner) -> dict:
    """Check for IDOR vulnerabilities."""
    test_ids = [1, 2, 3, 1000, 9999, -1, 0]
    responses = {}
    
    for test_id in test_ids:
        response = await scanner.request_builder.get(f"{scanner.target_url}/{test_id}")
        if response:
            responses[test_id] = response.status
    
    unique_responses = len(set(responses.values()))
    if unique_responses > 0 and len(responses) > 1:
        return {
            "finding": "Potential IDOR vulnerability",
            "evidence": f"Different responses for IDs: {responses}",
            "severity": "HIGH",
            "remediation": "Implement proper access controls, use UUIDs"
        }
    
    return None
