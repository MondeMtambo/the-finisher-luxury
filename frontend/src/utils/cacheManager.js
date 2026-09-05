/**
 * THE FINISHER LUXURY CRM — Enterprise Cache Management & Self-Healing Suite
 * 
 * Provides elite PWA cache management:
 * 1. Storage telemetry (CacheStorage & LocalStorage metrics)
 * 2. Intelligent dual-tier cache clearing (preserving executive authentication)
 * 3. Autonomous chunk loading error self-healing (eliminates post-deployment blank screens)
 */

const AUTH_KEYS_TO_PRESERVE = [
  'access_token',
  'refresh_token',
  'user',
  'theme',
  'finisher_animations',
  'selected_company_id'
];

/**
 * Returns human-readable storage metrics (CacheStorage + LocalStorage).
 */
export async function getStorageEstimate() {
  let cacheSize = 0;
  let cacheCount = 0;
  let localStorageSize = 0;

  try {
    // 1. Estimate LocalStorage usage
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key) {
        localStorageSize += (key.length + (localStorage.getItem(key) || '').length) * 2; // UTF-16
      }
    }

    // 2. Estimate CacheStorage usage via StorageManager API
    if (navigator.storage && navigator.storage.estimate) {
      const estimate = await navigator.storage.estimate();
      cacheSize = estimate.usage || 0;
    } else if ('caches' in window) {
      const keys = await caches.keys();
      cacheCount = keys.length;
    }
  } catch (err) {
    console.warn('[CacheManager] Telemetry warning:', err);
  }

  const totalBytes = cacheSize + localStorageSize;
  const mb = (totalBytes / (1024 * 1024)).toFixed(2);
  const kb = (totalBytes / 1024).toFixed(0);

  return {
    bytes: totalBytes,
    formatted: totalBytes > 1024 * 1024 ? `${mb} MB` : `${kb} KB`,
    cacheSize,
    localStorageSize,
    cacheCount,
    swActive: 'serviceWorker' in navigator && !!navigator.serviceWorker.controller
  };
}

/**
 * Intelligent Enterprise Cache Purge.
 * @param {Object} options
 * @param {boolean} options.preserveAuth - If true, preserves login session and preferences.
 */
export async function clearAppCache({ preserveAuth = true } = {}) {
  console.log(`[CacheManager] Executing cache purge (preserveAuth: ${preserveAuth})...`);

  // 1. Purge all ServiceWorker CacheStorage buckets
  if ('caches' in window) {
    try {
      const cacheNames = await caches.keys();
      await Promise.all(cacheNames.map((name) => caches.delete(name)));
      console.log('[CacheManager] CacheStorage buckets purged successfully.');
    } catch (err) {
      console.warn('[CacheManager] Failed to purge CacheStorage:', err);
    }
  }

  // 2. Unregister all active ServiceWorkers so fresh script is loaded
  if ('serviceWorker' in navigator) {
    try {
      const registrations = await navigator.serviceWorker.getRegistrations();
      await Promise.all(registrations.map((reg) => reg.unregister()));
      console.log('[CacheManager] ServiceWorkers unregistered.');
    } catch (err) {
      console.warn('[CacheManager] Failed to unregister ServiceWorkers:', err);
    }
  }

  // 3. Clear Storage while respecting preserveAuth
  if (preserveAuth) {
    // Preserve authenticated session and executive settings
    const preservedData = {};
    for (const key of AUTH_KEYS_TO_PRESERVE) {
      const val = localStorage.getItem(key);
      if (val !== null) {
        preservedData[key] = val;
      }
    }

    // Preserve any avatar preference
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('avatar_')) {
        preservedData[key] = localStorage.getItem(key);
      }
    }

    // Clear and restore
    localStorage.clear();
    sessionStorage.clear();

    for (const [key, val] of Object.entries(preservedData)) {
      localStorage.setItem(key, val);
    }
  } else {
    // Complete factory reset
    localStorage.clear();
    sessionStorage.clear();
  }

  // 4. Force hard reload with cache-busting query parameter
  const targetUrl = new URL(window.location.href);
  targetUrl.searchParams.set('purge', Date.now().toString());
  window.location.replace(targetUrl.toString());
}

/**
 * Autonomous Chunk Error Recovery (Self-Healing).
 * Listens for failed dynamic script imports caused by new deployments
 * and automatically refreshes to the latest bundle instead of crashing.
 */
export function initChunkErrorSelfHealing() {
  const RETRY_KEY = 'finisher_chunk_retry_ts';

  const handleChunkError = (errorMsg) => {
    const isChunkError = /Loading chunk [\d]+ failed|Failed to fetch dynamically imported module/i.test(errorMsg);
    if (!isChunkError) return;

    const lastRetry = parseInt(sessionStorage.getItem(RETRY_KEY) || '0', 10);
    const now = Date.now();

    // Prevent infinite reload loops (allow 1 retry per 10 seconds)
    if (now - lastRetry < 10000) {
      console.warn('[CacheManager] Chunk reload loop prevented.');
      return;
    }

    console.warn('[CacheManager] Stale bundle detected! Auto-healing via cache purge & re-sync...');
    sessionStorage.setItem(RETRY_KEY, now.toString());

    // Flush CacheStorage and reload to the latest bundle
    if ('caches' in window) {
      caches.keys().then((keys) => Promise.all(keys.map((k) => caches.delete(k)))).finally(() => {
        window.location.reload();
      });
    } else {
      window.location.reload();
    }
  };

  // Window error event
  window.addEventListener('error', (event) => {
    if (event.message) {
      handleChunkError(event.message);
    }
  });

  // Unhandled promise rejection (Vite dynamic import failures)
  window.addEventListener('unhandledrejection', (event) => {
    const reason = event.reason;
    const msg = (reason && (reason.message || reason.toString())) || '';
    handleChunkError(msg);
  });
}
