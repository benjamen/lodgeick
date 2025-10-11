import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read the built index.html
const builtIndexPath = path.join(__dirname, '..', 'lodgeick', 'public', 'frontend', 'index.html');
const targetPath = path.join(__dirname, '..', 'lodgeick', 'www', 'lodgeick.html');

let html = fs.readFileSync(builtIndexPath, 'utf-8');

// Fix favicon path first
html = html.replace('href="/favicon.png"', 'href="/assets/lodgeick/frontend/favicon.png"');

// Extract all module scripts from anywhere in the HTML
const moduleScriptRegex = /<script\s+type="module"[^>]*>[\s\S]*?<\/script>|<script\s+type="module"[^>]*\/>/g;
let moduleScripts = html.match(moduleScriptRegex) || [];

// Fix asset paths in module scripts
moduleScripts = moduleScripts.map(script =>
  script.replace(/\/assets\//g, '/assets/lodgeick/frontend/assets/')
);

// Remove module scripts from their current positions
html = html.replace(moduleScriptRegex, '');

// Now fix asset paths in the remaining HTML
// Replace /assets/ with /assets/lodgeick/frontend/assets/
html = html.replace(/\/assets\//g, '/assets/lodgeick/frontend/assets/');

// Prepare minimal frappe initialization + boot script
// This provides just enough for frappe-ui without breaking /desk and /app routes
const initScript = `
    <script>
      // Initialize minimal frappe object to prevent ReferenceErrors
      // This allows the Vue SPA to work while /desk and /app get the real Frappe framework
      if (!window.frappe) {
        window.frappe = {
          session: { user: '{{ user if user else "Guest" }}' },
          csrf_token: '{{ csrf_token if csrf_token else "" }}',
          boot: {
            lang: 'en',
            sysdefaults: {},
            user: '{{ user if user else "Guest" }}',
            user_roles: []
          },
          form: {},
          ui: {
            ScriptManager: function() {
              this.load = function() { return Promise.resolve() }
              this.loaded = {}
            }
          },
          call: function() { return Promise.resolve({ message: {} }) },
          xcall: function() { return Promise.resolve() },
        };
      }

      // Set additional globals
      window.site_name = '{{ site_name if site_name else "localhost" }}';
      window.csrf_token = '{{ csrf_token if csrf_token else "" }}';
      window.cur_frm = null;

      // Frappe boot data
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
