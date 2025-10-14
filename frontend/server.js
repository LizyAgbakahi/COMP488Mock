const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Health check endpoint (for Kubernetes liveness probe)
app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        service: 'frontend',
        timestamp: new Date().toISOString()
    });
});

// Readiness check endpoint (for Kubernetes readiness probe)
app.get('/ready', (req, res) => {
    res.status(200).json({
        status: 'ready',
        service: 'frontend',
        timestamp: new Date().toISOString()
    });
});

// Home route
app.get('/', (req, res) => {
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
    console.log(`Frontend service running on port ${PORT}`);
});

module.exports = app;