import { NETWORK_CONFIG } from '../config/network.js';
import { BACKEND_URL, getTunnelHeaders } from '../config/backend.js';

export async function searchImage(baseUrl = BACKEND_URL || NETWORK_CONFIG.BACKEND_URL, fileUri, lat, lng, maxKm, retryCount = 0) {
  const MAX_RETRIES = 2;
  const TIMEOUT_MS = 90000; // 90 segundos para dar tiempo al modelo
  
  try {
    const form = new FormData();
    // @ts-expect-error RN FormData file
    form.append("file", { uri: fileUri, name: "query.jpg", type: "image/jpeg" });
    const q = new URLSearchParams({ top_k: "10" });
    if (lat !== undefined && lng !== undefined && maxKm) {
      q.set("lat", String(lat));
      q.set("lng", String(lng));
      q.set("max_km", String(maxKm));
    }
    
    // Crear timeout manual ya que React Native fetch no soporta timeout nativo
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);
    
    try {
      const res = await fetch(`${baseUrl}/embeddings/search_image?${q.toString()}`, { 
        method: "POST", 
        body: form,
        headers: getTunnelHeaders(),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!res.ok) {
        const errorText = await res.text().catch(() => 'Error desconocido');
        throw new Error(`Error del servidor (${res.status}): ${errorText}`);
      }
      
      return await res.json();
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  } catch (error) {
    // Si es un error de timeout o red, intentar retry
    if ((error.name === 'AbortError' || error.message.includes('Network') || error.message.includes('Failed to fetch')) && retryCount < MAX_RETRIES) {
      console.log(`⚠️ Error en búsqueda, reintentando (${retryCount + 1}/${MAX_RETRIES})...`);
      await new Promise(resolve => setTimeout(resolve, 2000)); // Esperar 2 segundos antes de reintentar
      return searchImage(baseUrl, fileUri, lat, lng, maxKm, retryCount + 1);
    }
    
    // Si ya no hay más reintentos o es otro tipo de error
    if (error.name === 'AbortError') {
      throw new Error('La búsqueda tardó demasiado. El servidor puede estar procesando muchas solicitudes. Intenta de nuevo en unos momentos.');
    }
    
    throw error;
  }
}
