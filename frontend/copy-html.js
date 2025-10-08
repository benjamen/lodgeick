import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read the built index.html
const builtIndexPath = path.join(__dirname, '..', 'lodgeick', 'public', 'frontend', 'index.html');
const targetPath = path.join(__dirname, '..', 'lodgeick', 'www', 'lodgeick.html');

let html = fs.readFileSync(builtIndexPath, 'utf-8');

// Add Frappe boot script before </body>
const bootScript = `
          <script>
              {% for key in boot %}
              window["{{ key }}"] = {{ boot[key] | tojson }};
              {% endfor %}
          </script>`;

html = html.replace('</body>', `${bootScript}\n          </body>`);

// Write to www/lodgeick.html
fs.writeFileSync(targetPath, html);

console.log('✅ Copied and updated lodgeick.html');
