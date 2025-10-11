import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read the built index.html
const builtIndexPath = path.join(__dirname, '..', 'lodgeick', 'public', 'frontend', 'index.html');
const targetPath = path.join(__dirname, '..', 'lodgeick', 'www', 'lodgeick.html');

let html = fs.readFileSync(builtIndexPath, 'utf-8');

// Fix favicon path (Vite doesn't process this)
html = html.replace('href="/favicon.png"', 'href="/assets/lodgeick/frontend/favicon.png"');

// Extract all module scripts from anywhere in the HTML
const moduleScriptRegex = /<script\s+type="module"[^>]*>[\s\S]*?<\/script>|<script\s+type="module"[^>]*\/>/g;
let moduleScripts = html.match(moduleScriptRegex) || [];

// Remove module scripts from their current positions
html = html.replace(moduleScriptRegex, '');

// Vite's base path already adds /assets/lodgeick/frontend/, so no path fixing needed

// Prepare boot data script (frappe shim is already in <head>)
const initScript = `
    <script>
      // Frappe boot data - frappe object is already initialized in <head>
      {% for key in boot %}
      window["{{ key }}"] = {{ boot[key] | tojson }};
      {% endfor %}
    </script>

    <!-- Vue app module loads after frappe globals are set -->`;

// Inject initialization script and module scripts before </body>
const scriptsToInject = initScript + '\n    ' + moduleScripts.join('\n    ');
html = html.replace('</body>', `${scriptsToInject}\n  </body>`);

// Write to www/lodgeick.html
fs.writeFileSync(targetPath, html);

console.log('✅ Copied and updated lodgeick.html');
