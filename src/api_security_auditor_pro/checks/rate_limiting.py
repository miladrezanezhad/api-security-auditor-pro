"""
Rate limiting detection module
Tests if an API implements rate limiting to prevent brute force attacks
"""

import asyncio
import aiohttp
from typing import Dict


async def test_rate_limiting(
    target_url: str,
    requests: int = 50,
    concurrency: int = 5,
    delay: float = 0.05
) -> Dict:
    """
    Test if API has rate limiting implemented
    
    Args:
        target_url: The API endpoint to test
        requests: Total number of requests to send
        concurrency: Number of concurrent connections
        delay: Delay between requests in seconds
    
    Returns:
        Dictionary containing test results
    """
    
    results = {
        "total_requests": 0,
        "successful": 0,
        "rate_limited": 0,
        "errors": 0,
        "rate_limit_headers": {}
    }
    
    async def make_request(session: aiohttp.ClientSession, url: str):
        """Send a single HTTP request"""
        try:
            async with session.get(url) as response:
                # Check for rate limit headers (GitHub, etc.)
                rate_limit = response.headers.get('X-RateLimit-Remaining')
                if rate_limit and int(rate_limit) == 0:
                    results["rate_limited"] += 1
                    results["rate_limit_headers"] = {
                        'limit': response.headers.get('X-RateLimit-Limit'),
                        'remaining': rate_limit,
                        'reset': response.headers.get('X-RateLimit-Reset')
                    }
                elif response.status == 429:
                    results["rate_limited"] += 1
                elif response.status == 200:
                    results["successful"] += 1
                else:
                    results["errors"] += 1
        except Exception:
            results["errors"] += 1
        results["total_requests"] += 1
    
    # Create connection limiter
    connector = aiohttp.TCPConnector(limit=concurrency)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        
        for i in range(requests):
            if delay > 0 and i > 0:  # Don't delay first request
                await asyncio.sleep(delay)
            
            tasks.append(make_request(session, target_url))
            
            # Execute batch of requests
            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []
        
        # Execute remaining requests
        if tasks:
            await asyncio.gather(*tasks)
    
    return results