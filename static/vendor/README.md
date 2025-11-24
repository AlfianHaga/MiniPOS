Vendor assets placeholder

This folder contains lightweight loader wrappers for third-party libraries used by the project (jQuery and Select2).

Files:
- jquery/jquery.min.js        : loader that will dynamically load jQuery from CDN if not already present.
- select2/select2.min.js     : loader that will dynamically load Select2 from CDN once jQuery is available.
- select2/select2.min.css    : wrapper that @imports Select2 CSS from CDN.

For fully offline/local development, download the real minified files and replace these wrappers:
- https://code.jquery.com/jquery-3.6.0.min.js -> place at vendor/jquery/jquery.min.js
- https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js -> place at vendor/select2/select2.min.js
- https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css -> place at vendor/select2/select2.min.css

After replacing, the app will load assets locally without CDN fallbacks.
