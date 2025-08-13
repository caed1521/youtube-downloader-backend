// Configuration for different environments
const CONFIG = {
    // Development (local)
    development: {
        API_BASE_URL: 'http://localhost:8000'
    },
    
    // Production (EasyPanel + Netlify)
    production: {
        API_BASE_URL: 'https://yd-backend-be.flsr8u.easypanel.host'
    }
};

// Auto-detect environment
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname === '';

// Export current config
window.APP_CONFIG = isDevelopment ? CONFIG.development : CONFIG.production;

console.log('Environment:', isDevelopment ? 'Development' : 'Production');
console.log('API Base URL:', window.APP_CONFIG.API_BASE_URL);
