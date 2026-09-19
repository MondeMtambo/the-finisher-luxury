"""
THE FINISHER LUXURY — Institutional Geolocation & Anti-VPN Shield
Enforces strict Zero-Trust perimeter governance:
1. Restricts public onboarding and critical endpoints strictly to the Republic of South Africa (ZA).
2. Detects and blocks anonymous proxies, Tor exit nodes, and commercial VPN tunnels (NordVPN, ExpressVPN, Surfshark, etc.).
3. Protects the Supabase PostgreSQL cluster from foreign brute-force attacks and bot reconnaissance.
4. Includes fail-safe whitelisting for platform owners and localhost developers.
"""

import os
import logging
import urllib.request
import json
import time
from typing import Dict, Any, Optional
from django.conf import settings
from .utils import get_client_ip, TRUSTED_IP_WHITELIST, is_owner_admin_user

logger = logging.getLogger(__name__)

# In-memory cache for IP security lookups: {ip: (result_dict, timestamp)}
_IP_SECURITY_CACHE: Dict[str, tuple] = {}
CACHE_TTL_SECONDS = 86400  # 24 Hours

# Known Cloud/Datacenter ASNs commonly used by VPN providers
VPN_DATACENTER_KEYWORDS = [
    'amazon', 'aws', 'digitalocean', 'hetzner', 'linode', 'm247', 
    'ovh', 'choopa', 'vultr', 'leaseweb', 'nord', 'expressvpn', 
    'surfshark', 'datacenter', 'hosting', 'proxy', 'tor'
]

LOCAL_OR_PRIVATE_IPS = {'127.0.0.1', 'localhost', '::1', 'testserver'}


def is_private_ip(ip: str) -> bool:
    """Check if an IP address belongs to local or private network ranges."""
    if not ip or ip in LOCAL_OR_PRIVATE_IPS:
        return True
    if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
        return True
    return False


def inspect_proxy_headers(request) -> bool:
    """
    Sniffs incoming HTTP headers for standard proxy, VPN, and anonymizer fingerprints.
    """
    if not request:
        return False
    
    meta = request.META
    suspicious_headers = [
        'HTTP_VIA',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_FORWARDED',
        'HTTP_PROXY_CONNECTION',
        'HTTP_X_PROXY_ID',
        'HTTP_CF_CONNECTING_IP_PROXY',
    ]
    for h in suspicious_headers:
        if h in meta and meta[h]:
            return True
    return False


def verify_network_security(request) -> Dict[str, Any]:
    """
    Comprehensive Zero-Trust Security Verification:
    Checks:
      - Client IP extraction
      - Whitelist bypass (CEO / Owner / Localhost)
      - Header inspection
      - Geolocation check (strictly 'ZA')
      - Datacenter / VPN provider check
    Returns:
      {
        "allowed": bool,
        "client_ip": str,
        "country": str,
        "country_code": str,
        "is_vpn_or_proxy": bool,
        "reason": str
      }
    """
    client_ip = get_client_ip(request) or '127.0.0.1'

    # 1. Immediate Whitelist & Localhost Bypass (Safety for Developer & CEO)
    if is_private_ip(client_ip) or client_ip in TRUSTED_IP_WHITELIST:
        return {
            "allowed": True,
            "client_ip": client_ip,
            "country": "South Africa (Local / Whitelisted)",
            "country_code": "ZA",
            "is_vpn_or_proxy": False,
            "reason": "Whitelisted executive or local development connection."
        }

    # Optional Environment Override for testing/maintenance
    if os.environ.get('DISABLE_GEO_SHIELD', 'false').lower() == 'true':
        return {
            "allowed": True,
            "client_ip": client_ip,
            "country": "Bypass Active",
            "country_code": "ZA",
            "is_vpn_or_proxy": False,
            "reason": "DISABLE_GEO_SHIELD is active."
        }

    # 2. Check in-memory cache
    now = time.time()
    cached = _IP_SECURITY_CACHE.get(client_ip)
    if cached and (now - cached[1]) < CACHE_TTL_SECONDS:
        return cached[0]

    # 3. Header check for immediate proxy flags
    has_proxy_headers = inspect_proxy_headers(request)

    # 4. IP Intelligence Query (Fast, timeout-bounded 1.5s)
    country = "Unknown"
    country_code = "UNKNOWN"
    is_vpn_or_hosting = False
    org_or_isp = ""

    # Check Cloudflare IPCountry header if behind Cloudflare/Render
    cf_country = request.META.get('HTTP_CF_IPCOUNTRY')
    if cf_country and len(cf_country) == 2:
        country_code = cf_country.upper()

    try:
        # Query IP-API with fields: country, countryCode, org, isp, proxy, hosting
        url = f"http://ip-api.com/json/{client_ip}?fields=status,message,country,countryCode,org,isp,proxy,hosting"
        req = urllib.request.Request(url, headers={'User-Agent': 'TheFinisher-SecurityShield/1.0'})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                if data.get('status') == 'success':
                    country = data.get('country', 'Unknown')
                    country_code = data.get('countryCode', country_code).upper()
                    org_or_isp = f"{data.get('org', '')} {data.get('isp', '')}".lower()
                    is_vpn_or_hosting = bool(data.get('proxy') or data.get('hosting'))

                    # Check for VPN datacenter keywords
                    if any(kw in org_or_isp for kw in VPN_DATACENTER_KEYWORDS):
                        is_vpn_or_hosting = True
    except Exception as e:
        logger.warning(f"Geo-IP lookup query error for {client_ip}: {e}")
        # Fail safe: if query fails or network offline, fallback to South Africa if not flagged
        if country_code == "UNKNOWN":
            country_code = "ZA"
            country = "South Africa"

    # Flag if header proxy was detected
    if has_proxy_headers:
        is_vpn_or_hosting = True

    # 5. Evaluate Access Decision (South Africa Only & No VPNs)
    is_allowed_territory = (country_code == 'ZA')
    allowed = is_allowed_territory and not is_vpn_or_hosting

    reason = "Direct South African commercial network verified."
    if not is_allowed_territory:
        reason = f"Access restricted: Connection originates from outside South Africa ({country} - {country_code})."
    elif is_vpn_or_hosting:
        reason = "Access restricted: Anonymous VPN, Datacenter Relay, or Proxy connection detected."

    result = {
        "allowed": allowed,
        "client_ip": client_ip,
        "country": country,
        "country_code": country_code,
        "is_vpn_or_proxy": is_vpn_or_hosting,
        "reason": reason
    }

    # Store in cache
    _IP_SECURITY_CACHE[client_ip] = (result, now)
    return result
