"""
Core security scanner engine for API vulnerability detection
"""

import time
from datetime import datetime
from typing import Dict, List, Optional

from ..utils.request_builder import RequestBuilder
from ..checks.rate_limiting import test_rate_limiting


class SecurityScanner:
    """Main security scanner class for API vulnerability detection"""
    
    def __init__(
        self,
        target_url: str,
        timeout: int = 30,
        threads: int = 10
    ):
        self.target_url = target_url.rstrip('/')
        self.timeout = timeout
        self.threads = threads
        self.request_builder = RequestBuilder(target_url, timeout)
        self.results = {
            "target": target_url,
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": [],
            "info_findings": [],
            "scan_summary": {}
        }
    
    async def run_scan(self) -> Dict:
        """Execute all security checks against the target"""
        start_time = time.time()
        
        # Test rate limiting
        try:
            rate_results = await test_rate_limiting(
                self.target_url,
                requests=30,
                concurrency=5,
                delay=0.05
            )
            
            if rate_results["rate_limited"] == 0:
                self.results["vulnerabilities"].append({
                    "check": "Rate Limiting",
                    "severity": "MEDIUM",
                    "finding": "No rate limiting detected",
                    "remediation": "Implement rate limiting to prevent brute force attacks",
                    "evidence": f"Sent {rate_results['total_requests']} requests, 0 were rate limited"
                })
            else:
                self.results["info_findings"].append({
                    "check": "Rate Limiting",
                    "status": "passed",
                    "details": f"Rate limiting active - {rate_results['rate_limited']} requests were limited"
                })
        except Exception as e:
            self.results["info_findings"].append({
                "check": "Rate Limiting",
                "status": "error",
                "error": str(e)
            })
        
        self.results["scan_summary"] = {
            "duration_seconds": round(time.time() - start_time, 2),
            "checks_performed": len(self.results["vulnerabilities"]) + len(self.results["info_findings"])
        }
        
        return self.results
    
    async def run_bulk_scan(self, endpoints: List[Dict]) -> Dict:
        """Run scans against multiple endpoints"""
        bulk_results = {
            "target": self.target_url,
            "timestamp": datetime.now().isoformat(),
            "endpoints_scanned": len(endpoints),
            "results": []
        }
        
        for endpoint in endpoints:
            original_url = self.target_url
            endpoint_url = endpoint.get('url', '')
            self.target_url = original_url + endpoint_url
            
            result = await self.run_scan()
            result["endpoint"] = endpoint
            bulk_results["results"].append(result)
            
            self.target_url = original_url
        
        return bulk_results