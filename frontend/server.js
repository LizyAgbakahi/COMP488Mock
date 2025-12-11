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

// Health check endpoint (for Kubernetes liveness probe)
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

// Readiness check endpoint (for Kubernetes readiness probe)
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

// Home route
app.get('/', (req, res) => {
    console.log(JSON.stringify({
        level: 'INFO',
        message: 'Rendering root frontend endpoint',
        time: new Date().toISOString()
    }));

    res.json({
        message: 'TechCommerce Frontend',
        version: '1.0.0',
        endpoints: {
            health: '/health',
            ready: '/ready'
        }
    });
});

// Start server
app.listen(PORT, () => {
    console.log(JSON.stringify({
        level: 'INFO',
        message: `Frontend service running on port ${PORT}`,
        port: PORT,
        time: new Date().toISOString()
    }));
});

module.exports = app;
