/* global requestAnimationFrame, window, document */
/* Copyright 2018 Tecnativa - Jairo Llopis
 * Copyright 2021 ITerra - Sergey Shebanin
 * Copyright 2023 Onestein - Anjeel Haria
 * Copyright 2023 Taras Shabaranskyi
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

import {debounce} from "@web/core/utils/timing";

// Fix for iOS Safari to set correct viewport height
// https://github.com/Faisal-Manzer/postcss-viewport-height-correction
export function setViewportProperty(doc) {
    function handleResize() {
        requestAnimationFrame(function () {
            doc.style.setProperty("--vh100", doc.clientHeight + "px");
        });
    }

    handleResize();
    return handleResize;
}

window.addEventListener(
    "resize",
    debounce(setViewportProperty(document.documentElement), 25)
);

// Register PWA Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js', { scope: '/' })
            .then((reg) => {
                console.log('Odoo PWA Service Worker registered successfully with scope:', reg.scope);
            })
            .catch((err) => {
                console.error('Odoo PWA Service Worker registration failed:', err);
            });
    });
}

// --- Premium Mobile Touch Gestures (Swipe & Pull-to-Refresh) ---
document.addEventListener("DOMContentLoaded", () => {
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;
    let isPulling = false;

    // Create a beautiful Pull-to-Refresh Spinner dynamically
    const spinner = document.createElement("div");
    spinner.id = "pwa-pull-spinner";
    spinner.innerHTML = `
        <div class="pwa-spinner-ring"></div>
        <span class="pwa-spinner-text">Release to Refresh</span>
    `;
    
    const style = document.createElement("style");
    style.innerHTML = `
        #pwa-pull-spinner {
            position: fixed;
            top: -60px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 99999;
            background: rgba(113, 75, 103, 0.9);
            color: white;
            padding: 10px 18px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.15s ease, opacity 0.15s ease, top 0.2s ease;
            opacity: 0;
            pointer-events: none;
            backdrop-filter: blur(5px);
        }
        .pwa-spinner-ring {
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255,255,255,0.3);
            border-top: 2px solid white;
            border-radius: 50%;
            animation: pwa-spin 0.8s linear infinite;
        }
        @keyframes pwa-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(spinner);

    // Track touch gestures
    document.addEventListener("touchstart", (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        
        const scrollable = document.querySelector(".o_content") || document.documentElement;
        if (scrollable.scrollTop === 0) {
            isPulling = true;
        } else {
            isPulling = false;
        }
    }, { passive: true });

    document.addEventListener("touchmove", (e) => {
        touchEndX = e.touches[0].clientX;
        touchEndY = e.touches[0].clientY;

        const deltaY = touchEndY - touchStartY;

        if (isPulling && deltaY > 0) {
            const pullDist = Math.min(deltaY * 0.4, 90);
            if (pullDist > 15) {
                spinner.style.top = `${pullDist - 30}px`;
                spinner.style.opacity = Math.min(pullDist / 60, 1);
            }
        }
    }, { passive: true });

    document.addEventListener("touchend", () => {
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;
        const absDeltaX = Math.abs(deltaX);
        const absDeltaY = Math.abs(deltaY);

        // 1. Swipe Left/Right to Open/Close App Drawer
        if (absDeltaX > 100 && absDeltaY < 60) {
            const isMenuOpen = document.body.classList.contains("o_apps_menu_opened");
            const btn = document.querySelector(".o_grid_apps_menu__button");
            
            if (deltaX > 0 && !isMenuOpen && touchStartX < 50) {
                if (btn) btn.click();
            } else if (deltaX < 0 && isMenuOpen) {
                if (btn) btn.click();
            }
        }

        // 2. Pull-to-Refresh execution
        if (isPulling && deltaY > 150) {
            spinner.style.top = "20px";
            spinner.innerHTML = `<div class="pwa-spinner-ring"></div><span>Refreshing...</span>`;
            
            setTimeout(() => {
                window.location.reload();
            }, 300);
        } else {
            spinner.style.top = "-60px";
            spinner.style.opacity = "0";
        }
        
        isPulling = false;
    }, { passive: true });
});


