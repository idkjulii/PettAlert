/**
 * Configuración del backend
 */
import { NETWORK_CONFIG } from './network';

// URL del túnel temporal (Cloudflare quick tunnel en este caso)
const TUNNEL_URL =
  process.env.EXPO_PUBLIC_TUNNEL_URL ||
  process.env.EXPO_PUBLIC_BACKEND_URL ||
  'https://stock-presents-hip-individual.trycloudflare.com';

// URL base del backend - prioridad: variable de entorno > ngrok > red local > localhost
// Si ngrok está funcionando, se usará automáticamente
const BACKEND_URL =
  process.env.EXPO_PUBLIC_BACKEND_URL ||
  TUNNEL_URL ||
  NETWORK_CONFIG?.BACKEND_URL ||
  'http://127.0.0.1:8003';

// Log de depuración para ver qué URL se está usando
console.log('🔧 [BACKEND CONFIG]');
console.log('   EXPO_PUBLIC_BACKEND_URL:', process.env.EXPO_PUBLIC_BACKEND_URL || '(no definida)');
console.log('   TUNNEL_URL:', TUNNEL_URL);
console.log('   NETWORK_CONFIG.BACKEND_URL:', NETWORK_CONFIG?.BACKEND_URL || '(no definida)');
console.log('   BACKEND_URL final:', BACKEND_URL);

// Endpoints disponibles
const ENDPOINTS = {
  HEALTH: '/health',
  AI_SEARCH: '/ai-search',
  AI_SEARCH_HEALTH: '/ai-search/health',
  ANALYZE_IMAGE: '/analyze_image',
  CAPTION: '/caption',
  AUTO_MATCH: '/reports/auto-match',
  SAVE_LABELS: '/reports/{report_id}/labels',
  REPORTS: '/reports/',
  REPORTS_BY_ID: '/reports/{report_id}',
  REPORTS_RESOLVE: '/reports/{report_id}/resolve',
  MATCHES_PENDING: '/matches/pending',
  MATCHES_UPDATE: '/matches/{match_id}/status',
  // Embeddings
  EMBEDDINGS_GENERATE: '/embeddings/generate',
  EMBEDDINGS_INDEX: '/embeddings/index/{report_id}',
  EMBEDDINGS_SEARCH: '/embeddings/search_image',
  // RAG (Retrieval Augmented Generation)
  RAG_SEARCH: '/rag/search',
  RAG_SEARCH_WITH_LOCATION: '/rag/search-with-location',
  RAG_SAVE_EMBEDDING: '/rag/save-embedding/{report_id}',
  RAG_GET_EMBEDDING: '/rag/embedding/{report_id}',
  RAG_HAS_EMBEDDING: '/rag/has-embedding/{report_id}',
  RAG_STATS: '/rag/stats',
  // n8n Integration
  N8N_HEALTH: '/n8n/health',
  N8N_REPORTS_WITH_IMAGES: '/n8n/reports/with-images',
  N8N_SEND_TO_WEBHOOK: '/n8n/send-to-webhook',
  N8N_PROCESS_RESULT: '/n8n/process-result',
  N8N_BATCH_PROCESS: '/n8n/batch-process'
};

/**
 * Construye la URL completa para un endpoint
 * @param {string} endpoint - Nombre del endpoint
 * @param {Object} params - Parámetros para reemplazar en la URL
 * @returns {string} URL completa
 */
const buildUrl = (endpoint, params = {}) => {
  const endpointPath = ENDPOINTS[endpoint] ?? endpoint;

  let url;
  if (endpointPath.startsWith('http://') || endpointPath.startsWith('https://')) {
    url = endpointPath;
  } else {
    url = `${BACKEND_URL}${endpointPath}`;
  }
  
  // Sufstituir parámetros en la URL
  Object.keys(params).forEach(key => {
    url = url.replace(`{${key}}`, params[key]);
  });
  
  return url;
};

/**
 * Agrega headers de ngrok si es necesario
 * @param {Object} headers - Headers existentes (opcional)
 * @returns {Object} Headers con ngrok si es necesario
 */
const getNgrokHeaders = (headers = {}) => {
  const isNgrok =
    BACKEND_URL.includes('ngrok-free.dev') ||
    BACKEND_URL.includes('ngrok.io') ||
    BACKEND_URL.includes('trycloudflare.com');
  if (isNgrok) {
    return {
      ...headers,
      'ngrok-skip-browser-warning': 'true'
    };
  }
  return headers;
};

export {
  BACKEND_URL, buildUrl, ENDPOINTS, getNgrokHeaders
};

