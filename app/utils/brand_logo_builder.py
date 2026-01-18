from typing import Optional
from urllib.parse import urlparse
import re
from functools import lru_cache


class BrandLogoBuilder:
    """
    Builds Brandfetch CDN URLs for business logos from website URLs.
    
    Features:
    - URL normalization and cleaning
    - Domain extraction with validation
    - Subdomain handling (www removal)
    - LRU caching for repeated lookups
    - Comprehensive error handling
    """
    
    # Brandfetch CDN base URL
    BRANDFETCH_CDN = "https://cdn.brandfetch.io"
    
    # Common subdomains to strip (can be extended)
    STRIP_SUBDOMAINS = {"www", "m", "mobile"}
    
    def __init__(self, client_id: str):
        """
        Initialize the logo builder with Brandfetch client ID.
        
        Args:
            client_id: Brandfetch API client ID
            
        Raises:
            ValueError: If client_id is empty or invalid
        """
        if not client_id or not isinstance(client_id, str):
            raise ValueError("client_id must be a non-empty string")
        
        self._client_id = client_id.strip()
    
    @staticmethod
    @lru_cache(maxsize=1024)
    def _extract_domain(url: str) -> Optional[str]:
        """
        Extract and normalize the domain from a URL.
        
        This method is cached to improve performance for repeated URLs.
        
        Args:
            url: The URL to extract domain from
            
        Returns:
            Cleaned domain (e.g., 'example.com') or None if invalid
            
        Examples:
            >>> BrandLogoBuilder._extract_domain('https://www.example.com/path')
            'example.com'
            >>> BrandLogoBuilder._extract_domain('example.com')
            'example.com'
            >>> BrandLogoBuilder._extract_domain('www.example.com')
            'example.com'
        """
        if not url:
            return None
        
        # Normalize the URL
        url = url.strip().lower()
        
        # Add scheme if missing for proper parsing
        if not re.match(r'^https?://', url):
            url = f'https://{url}'
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split('/')[0]
            
            if not domain:
                return None
            
            # Remove common subdomains
            parts = domain.split('.')
            if len(parts) > 2 and parts[0] in BrandLogoBuilder.STRIP_SUBDOMAINS:
                domain = '.'.join(parts[1:])
            
            # Basic domain validation
            if not BrandLogoBuilder._is_valid_domain(domain):
                return None
            
            return domain
            
        except Exception:
            return None
    
    @staticmethod
    def _is_valid_domain(domain: str) -> bool:
        """
        Validate that a domain looks reasonable.
        
        Args:
            domain: Domain string to validate
            
        Returns:
            True if domain appears valid, False otherwise
        """
        if not domain or len(domain) < 3:
            return False
        
        # Basic domain pattern: at least one dot, valid characters
        domain_pattern = r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$'
        return bool(re.match(domain_pattern, domain))
    
    def build_logo_url(self, business_url: str) -> Optional[str]:
        """
        Build a Brandfetch CDN URL for a business logo.
        
        Args:
            business_url: The business website URL
            
        Returns:
            Brandfetch CDN URL or None if URL is invalid
            
        Examples:
            >>> builder = BrandLogoBuilder("abc123")
            >>> builder.build_logo_url("https://coverallroofing.ca/")
            'https://cdn.brandfetch.io/coverallroofing.ca?c=abc123'
            >>> builder.build_logo_url("www.example.com")
            'https://cdn.brandfetch.io/example.com?c=abc123'
        """
        domain = self._extract_domain(business_url)
        
        if not domain:
            return None
        
        return f"{self.BRANDFETCH_CDN}/{domain}?c={self._client_id}"
    
    def build_logo_urls_batch(self, business_urls: list[str]) -> dict[str, Optional[str]]:
        """
        Build logo URLs for multiple businesses efficiently.
        
        Args:
            business_urls: List of business website URLs
            
        Returns:
            Dictionary mapping input URLs to Brandfetch CDN URLs
            
        Example:
            >>> builder = BrandLogoBuilder("abc123")
            >>> urls = ["https://example.com", "https://test.org"]
            >>> builder.build_logo_urls_batch(urls)
            {
                'https://example.com': 'https://cdn.brandfetch.io/example.com?c=abc123',
                'https://test.org': 'https://cdn.brandfetch.io/test.org?c=abc123'
            }
        """
        return {url: self.build_logo_url(url) for url in business_urls}
    
    def clear_cache(self) -> None:
        """Clear the domain extraction cache."""
        self._extract_domain.cache_clear()
    
    @property
    def cache_info(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache hits, misses, size, and max size
        """
        info = self._extract_domain.cache_info()
        return {
            "hits": info.hits,
            "misses": info.misses,
            "current_size": info.currsize,
            "max_size": info.maxsize
        }

