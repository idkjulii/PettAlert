// src/lib/api.js
import { NETWORK_CONFIG } from '../config/network.js';
import { BACKEND_URL } from '../config/backend.js';

export const API_URL = process.env.EXPO_PUBLIC_API_URL || BACKEND_URL || NETWORK_CONFIG.BACKEND_URL;

export async function postImage(endpoint, { uri, name = "photo.jpg", type = "image/jpeg" }) {
  const form = new FormData();
  form.append("file", { uri, name, type });
  
  // Detectar si es ngrok y agregar header
  const isNgrok = API_URL.includes('ngrok-free.dev') || API_URL.includes('ngrok.io');
  const headers = {};
  if (isNgrok) {
    headers['ngrok-skip-browser-warning'] = 'true';
  }
  // Don't set Content-Type manually; fetch will add the multipart boundary.
  
  const res = await fetch(`${API_URL}${endpoint}`, { 
    method: "POST", 
    body: form,
    headers: headers
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Upload failed ${res.status}: ${text}`);
  }
  return res.json();
}
