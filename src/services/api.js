/**
 * Servicio de API para comunicarse con el backend
 */
import { BACKEND_URL, ENDPOINTS, buildUrl } from '../config/backend';

class ApiService {
  constructor() {
    this.baseUrl = BACKEND_URL;
    console.log('🔧 Backend URL configurada:', this.baseUrl);
  }

  /**
   * Realiza una petición HTTP
   */
  async request(endpoint, options = {}) {
    let url;
    if (typeof endpoint === 'string') {
      // Si es una cadena, agregar la URL base si no es una URL completa
      if (endpoint.startsWith('http://') || endpoint.startsWith('https://')) {
        url = endpoint;
      } else {
        url = `${this.baseUrl}${endpoint}`;
      }
    } else {
      url = buildUrl(endpoint.endpoint, endpoint.params);
    }
    
    // Detectar si es una URL de ngrok y agregar header para evitar página de bienvenida
    const isNgrok = url.includes('ngrok-free.dev') || url.includes('ngrok.io');
    
    // Preparar headers base
    const baseHeaders = {
      // Header para evitar la página de bienvenida de ngrok free (siempre incluir si es ngrok)
      ...(isNgrok && { 'ngrok-skip-browser-warning': 'true' }),
    };
    
    // Si no hay headers personalizados, usar Content-Type por defecto para JSON
    if (!options.headers || !options.headers['Content-Type']) {
      // Solo agregar Content-Type si el body es JSON (no FormData)
      if (options.body && typeof options.body === 'string' && !options.body.includes('FormData')) {
        baseHeaders['Content-Type'] = 'application/json';
      }
    }
    
    // Merge headers: base headers primero, luego los del usuario
    const finalHeaders = {
      ...baseHeaders,
      ...(options.headers || {})
    };
    
    const finalOptions = {
      ...options,
      headers: finalHeaders
    };

    try {
      console.log(`🌐 API Request: ${finalOptions.method || 'GET'} ${url}`);
      console.log(`🔗 URL completa: ${url}`);
      console.log(`📦 Body:`, finalOptions.body ? finalOptions.body.substring(0, 200) : 'No body');
      
      const response = await fetch(url, finalOptions);
      
      // Verificar el Content-Type antes de parsear JSON
      const contentType = response.headers.get('content-type');
      let responseText = await response.text();
      
      if (!response.ok) {
        // Si es HTML, es probablemente una página de error
        if (contentType && contentType.includes('text/html')) {
          throw new Error(`HTTP ${response.status}: El backend devolvió HTML en lugar de JSON. Verifica que el endpoint esté correcto y que el backend esté corriendo.`);
        }
        throw new Error(`HTTP ${response.status}: ${responseText.substring(0, 200)}`);
      }

      // Verificar que sea JSON antes de parsear
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error(`Respuesta no es JSON (Content-Type: ${contentType}). Respuesta: ${responseText.substring(0, 200)}`);
      }

      const data = JSON.parse(responseText);
      console.log(`✅ API Response: ${url}`, data);
      
      return { data, error: null };
    } catch (error) {
      console.error(`❌ API Error: ${url}`, error);
      return { data: null, error };
    }
  }

  /**
   * Verifica el estado del backend
   */
  async health() {
    return this.request(ENDPOINTS.HEALTH);
  }

  /**
   * Obtiene información de la versión
   */
  async version() {
    return this.request(ENDPOINTS.VERSION);
  }

  /**
   * Verifica el estado de Supabase
   */
  async supabaseStatus() {
    return this.request(ENDPOINTS.SUPABASE_STATUS);
  }

  /**
   * Obtiene todos los reportes
   */
  async getAllReports() {
    return this.request(ENDPOINTS.REPORTS);
  }

  /**
   * Obtiene reportes cercanos
   */
  async getNearbyReports(latitude, longitude, radiusKm = 10) {
    const url = `${buildUrl(ENDPOINTS.REPORTS_NEARBY)}?lat=${latitude}&lng=${longitude}&radius_km=${radiusKm}`;
    return this.request(url);
  }

  /**
   * Obtiene un reporte por ID
   */
  async getReportById(reportId) {
    return this.request({
      endpoint: ENDPOINTS.REPORTS_BY_ID,
      params: { report_id: reportId }
    });
  }

  /**
   * Crea un nuevo reporte
   */
  async createReport(reportData) {
    return this.request(ENDPOINTS.REPORTS, {
      method: 'POST',
      body: JSON.stringify(reportData)
    });
  }

  /**
   * Actualiza un reporte
   */
  async updateReport(reportId, updates) {
    return this.request({
      endpoint: ENDPOINTS.REPORTS_BY_ID,
      params: { report_id: reportId }
    }, {
      method: 'PUT',
      body: JSON.stringify(updates)
    });
  }

  /**
   * Resuelve un reporte
   */
  async resolveReport(reportId) {
    return this.request({
      endpoint: ENDPOINTS.REPORTS_RESOLVE,
      params: { report_id: reportId }
    }, {
      method: 'POST'
    });
  }

  /**
   * Elimina un reporte
   */
  async deleteReport(reportId) {
    return this.request({
      endpoint: ENDPOINTS.REPORTS_BY_ID,
      params: { report_id: reportId }
    }, {
      method: 'DELETE'
    });
  }

  /**
   * Auto-matching de reportes
   */
  async autoMatch(reportId, radiusKm = 10, topK = 5) {
    const url = `${buildUrl('AUTO_MATCH')}?report_id=${reportId}&radius_km=${radiusKm}&top_k=${topK}`;
    return this.request(url);
  }

  /**
   * Obtiene coincidencias pendientes para un reporte
   */
  async getMatchesForReport(reportId) {
    const url = `${buildUrl('MATCHES_PENDING')}?report_id=${reportId}`;
    return this.request(url);
  }

  /**
   * Reenvía un reporte a n8n para reprocesar coincidencias
   */
  async sendReportToN8n(reportId) {
    return this.request(ENDPOINTS.N8N_SEND_TO_WEBHOOK, {
      method: 'POST',
      body: JSON.stringify({ report_id: reportId })
    });
  }

  /**
   * Guarda etiquetas de un reporte
   */
  async saveLabels(reportId, labels) {
    return this.request({
      endpoint: ENDPOINTS.SAVE_LABELS,
      params: { report_id: reportId }
    }, {
      method: 'POST',
      body: JSON.stringify({ labels })
    });
  }
}

// Crear instancia singleton
const apiService = new ApiService();

export default apiService;
