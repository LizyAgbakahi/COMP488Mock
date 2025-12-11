const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// ---------- JSON Logging Middleware ----------
function logRequest(req, res, next) {
    const log = {
        level: 'INFO',
        message: 'HTTP request',
        method: req.method,
        path: req.path,
        time: new Date().toISOString()
    };
    console.log(JSON.stringify(log));
    next();
}

// Middleware
app.use(express.json());
app.use(logRequest);

// ---------- Health Check Endpoints ----------
app.get('/health', (req, res) => {
    console.log(JSON.stringify({
        level: 'INFO',
        message: 'Frontend health check',
        time: new Date().toISOString()
    }));

    res.status(200).json({
        status: 'healthy',
        service: 'frontend',
        timestamp: new Date().toISOString()
    });
});

app.get('/ready', (req, res) => {
    console.log(JSON.stringify({
        level: 'INFO',
        message: 'Frontend readiness check',
        time: new Date().toISOString()
    }));

    res.status(200).json({
        status: 'ready',
        service: 'frontend',
        timestamp: new Date().toISOString()
    });
});

// ---------- Root HTML Route ----------
app.get('/', (req, res) => {
    console.log(JSON.stringify({
        level: 'INFO',
        message: 'Rendering HTML homepage',
        time: new Date().toISOString()
    }));

    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>TechCommerce Frontend</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    max-width: 500px;
                    text-align: center;
                }
                h1 { color: #333; margin-bottom: 10px; }
                p { color: #555; }
                .status {
                    margin-top: 20px;
                    padding: 10px 15px;
                    background: #e3ffe3;
                    border: 1px solid #9ccd9c;
                    border-radius: 8px;
                    color: #2a662a;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to TechCommerce</h1>
                <p>Your microservices frontend is running successfully.</p>
                <div class="status">Status: OK ✓</div>
            </div>
        </body>
        </html>
    `);
});

// ---------- Start Server ----------
app.listen(PORT, () => {
    console.log(JSON.stringify({
        level: 'INFO',
        message: `Frontend service running on port ${PORT}`,
        port: PORT,
        time: new Date().toISOString()
    }));
});

module.exports = app;
