"""
HTTP request builder with error handling and timeout support
"""

import aiohttp
from typing import Dict, Optional, Any


class RequestBuilder:
    """Build and execute HTTP requests with proper error handling"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize request builder
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    def _build_url(self, path: str) -> str:
        """
        Build full URL from base and path
        
        Args:
            path: API endpoint path
        
        Returns:
            Complete URL
        """
        if path.startswith(('http://', 'https://')):
            return path
        if path.startswith('/'):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/{path}"
    
    async def get(
        self, 
        path: str = "", 
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Optional[aiohttp.ClientResponse]:
        """
        Execute GET request
        
        Args:
            path: API endpoint path
            params: Query parameters
            headers: Custom headers
        
        Returns:
            Response object or None if failed
        """
        url = self._build_url(path)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params, headers=headers) as response:
                    return response
        except asyncio.TimeoutError:
            print(f"Timeout error for GET {url}")
            return None
        except Exception as e:
            print(f"Error in GET {url}: {e}")
            return None
    
    async def post(
        self, 
        path: str = "", 
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Optional[aiohttp.ClientResponse]:
        """
        Execute POST request
        
        Args:
            path: API endpoint path
            data: Form data
            json_data: JSON data
            headers: Custom headers
        
        Returns:
            Response object or None if failed
        """
        url = self._build_url(path)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    url, 
                    data=data, 
                    json=json_data, 
                    headers=headers
                ) as response:
                    return response
        except asyncio.TimeoutError:
            print(f"Timeout error for POST {url}")
            return None
        except Exception as e:
            print(f"Error in POST {url}: {e}")
            return None