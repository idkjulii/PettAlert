# Script de prueba para la integración con n8n
# Este script verifica que todos los endpoints funcionen correctamente

Write-Host "`n=== Test de Integración con n8n ===" -ForegroundColor Cyan

# Configuración
$BACKEND_URL = "http://127.0.0.1:8003"

# Test 1: Health Check
Write-Host "`n1. Testing /n8n/health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/health" -Method GET
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Health OK" -ForegroundColor Green
    Write-Host "   Status: $($data.status)" -ForegroundColor White
    Write-Host "   Reports con imágenes: $($data.reports_with_images)" -ForegroundColor White
    Write-Host "   Total reportes activos: $($data.total_active_reports)" -ForegroundColor White
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Obtener reportes con imágenes
Write-Host "`n2. Testing /n8n/reports/with-images..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?limit=5" -Method GET
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Obtener reportes OK" -ForegroundColor Green
    Write-Host "   Total reportes retornados: $($data.count)" -ForegroundColor White
    if ($data.count -gt 0) {
        Write-Host "   Primer reporte:" -ForegroundColor White
        Write-Host "     - Report ID: $($data.reports[0].report_id)" -ForegroundColor Gray
        Write-Host "     - Image URL: $($data.reports[0].image_url)" -ForegroundColor Gray
        Write-Host "     - Species: $($data.reports[0].species)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Obtener reportes sin labels
Write-Host "`n3. Testing /n8n/reports/with-images?has_labels=false..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?has_labels=false&limit=5" -Method GET
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Obtener reportes sin labels OK" -ForegroundColor Green
    Write-Host "   Reportes sin procesar: $($data.count)" -ForegroundColor White
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Obtener reportes con labels
Write-Host "`n4. Testing /n8n/reports/with-images?has_labels=true..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?has_labels=true&limit=5" -Method GET
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Obtener reportes con labels OK" -ForegroundColor Green
    Write-Host "   Reportes procesados: $($data.count)" -ForegroundColor White
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Tests Completados ===" -ForegroundColor Cyan
Write-Host "`nPróximos pasos:" -ForegroundColor Yellow
Write-Host "1. Configura el workflow en n8n usando la guía: GUIA-INTEGRACION-N8N.md" -ForegroundColor White
Write-Host "2. Prueba el workflow manualmente en n8n" -ForegroundColor White
Write-Host "3. Verifica los resultados en Supabase" -ForegroundColor White









