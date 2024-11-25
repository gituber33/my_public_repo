const puppeteer = require('puppeteer');
const http = require('http');
const url = require('url');

// Créer un serveur HTTP pour écouter les requêtes entrantes
const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    // Lorsque la route /get_latest_message est appelée
    if (parsedUrl.pathname === '/get_latest_message' && req.method === 'GET') {
        try {
            // Démarrer le navigateur Puppeteer
            const browser = await puppeteer.launch({
                headless: true, // Mode sans interface graphique
                args: ['--no-sandbox', '--disable-setuid-sandbox'] // Requis pour Docker
            });
            const page = await browser.newPage();
            await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0');
            await page.goto('http://172.25.25.12:8080/login');
            await page.type('input[name="username"]', 'admin');
            await page.type('input[name="password"]', '8d4a487d59054f96f19d05419c846b8a96f19d05419c84');
            await Promise.all([
                page.click('button[type="submit"]'),  // Cliquer sur le bouton de soumission
                page.waitForNavigation({ waitUntil: 'domcontentloaded' })  // Attendre la navigation après soumission
            ]);
            await page.goto('http://172.25.25.12:8080/get_latest_message');
            await page.waitForTimeout(3000);
            await browser.close();
        } catch (error) {
            res.writeHead(500, {'Content-Type': 'text/plain'});
            res.end('Erreur lors de l\'exécution de Puppeteer : ' + error.message);
        }
    } else {
        res.writeHead(404, {'Content-Type': 'text/plain'});
        res.end('Route inconnue');
    }
});

// Le serveur écoute sur le port 3000
server.listen(3000, () => {
    console.log('Puppeteer server listening on port 3000');
});
