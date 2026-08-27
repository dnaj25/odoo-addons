# -*- coding: utf-8 -*-
import json
from odoo import http

class PWAController(http.Controller):

    @http.route('/manifest.json', type='http', auth='public', methods=['GET'], csrf=False)
    def manifest(self):
        manifest_data = {
            "name": "Odoo Community Client",
            "short_name": "Odoo",
            "description": "Premium responsive Odoo client with web application capabilities.",
            "start_url": "/web",
            "display": "standalone",
            "background_color": "#714B67",
            "theme_color": "#714B67",
            "orientation": "any",
            "icons": [
                {
                    "src": "/web_responsive_pro/static/description/icon.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ]
        }
        return http.Response(
            json.dumps(manifest_data),
            headers=[
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Access-Control-Allow-Origin', '*')
            ]
        )

    @http.route('/service-worker.js', type='http', auth='public', methods=['GET'], csrf=False)
    def service_worker(self):
        # A simple, robust network-first service worker that logs fetches and satisfies PWA requirements
        sw_code = """
const CACHE_NAME = 'odoo-pwa-cache-v1';
const ASSETS_TO_CACHE = [
    '/web/login',
    '/web_responsive_pro/static/description/icon.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    // Network-first strategy with cache fallback
    if (event.request.method === 'GET' && event.request.url.startsWith(self.location.origin)) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    return response;
                })
                .catch(() => {
                    return caches.match(event.request).then((cachedResponse) => {
                        if (cachedResponse) {
                            return cachedResponse;
                        }
                        return new Response('Offline: Connection lost.', {
                            status: 503,
                            statusText: 'Service Unavailable',
                            headers: new Headers({ 'Content-Type': 'text/plain' })
                        });
                    });
                })
        );
    }
});
"""
        return http.Response(
            sw_code,
            headers=[
                ('Content-Type', 'application/javascript; charset=utf-8'),
                ('Service-Worker-Allowed', '/'),
                ('Access-Control-Allow-Origin', '*')
            ]
        )
