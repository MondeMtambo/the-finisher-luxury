const fs = require('fs');

// Ensure SPA routing files exist in dist for Render static sites
// Write _redirects directly (don't rely solely on public/ copy)
fs.writeFileSync('dist/_redirects', '/* /index.html 200\n');
fs.copyFileSync('dist/index.html', 'dist/200.html');
console.log('postbuild: _redirects + 200.html created in dist/');
