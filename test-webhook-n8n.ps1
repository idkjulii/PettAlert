# Script para probar el envío al webhook de n8n
Write-Host "=== Prueba de Envío al Webhook de n8n ===" -ForegroundColor Cyan

$BACKEND_URL = "http://127.0.0.1:8003"

# 1. Verificar salud
Write-Host "`n1. Verificando salud del endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/health" -Method GET
    $health = $response.Content | ConvertFrom-Json
    Write-Host "   ✅ Backend funcionando" -ForegroundColor Green
    Write-Host "   Webhook configurado: $($health.n8n_webhook)" -ForegroundColor White
    Write-Host "   Estado n8n: $($health.n8n_status)" -ForegroundColor White
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# 2. Obtener un reporte
Write-Host "`n2. Obteniendo reporte con imágenes..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?limit=1&has_labels=false" -Method GET
    $data = $response.Content | ConvertFrom-Json
    
    if ($data.count -eq 0) {
        Write-Host "   ⚠️ No hay reportes sin procesar" -ForegroundColor Yellow
        Write-Host "   Intentando obtener cualquier reporte..." -ForegroundColor Gray
        $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?limit=1" -Method GET
        $data = $response.Content | ConvertFrom-Json
    }
    
    if ($data.count -eq 0) {
        Write-Host "   ❌ No se encontraron reportes con imágenes" -ForegroundColor Red
        Write-Host "   Crea un reporte con fotos desde la app móvil primero" -ForegroundColor Yellow
        exit
    }
    
    $reportId = $data.reports[0].report_id
    $imageUrl = $data.reports[0].image_url
    Write-Host "   ✅ Reporte encontrado: $reportId" -ForegroundColor Green
    Write-Host "   Imagen: $imageUrl" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# 3. Enviar al webhook
Write-Host "`n3. Enviando reporte al webhook de n8n..." -ForegroundColor Yellow
$body = @{
    report_id = $reportId
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/send-to-webhook" -Method POST `
        -Body $body `
        -ContentType "application/json"
    
    $result = $response.Content | ConvertFrom-Json
    
    if ($result.success) {
        Write-Host "   ✅ Enviado exitosamente!" -ForegroundColor Green
        Write-Host "   Webhook: $($result.webhook_url)" -ForegroundColor White
        Write-Host "   Total imágenes: $($result.total_images)" -ForegroundColor White
        Write-Host "   Resultados:" -ForegroundColor White
        foreach ($r in $result.results) {
            Write-Host "     - Imagen $($r.image_index): $($r.status)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ⚠️ Respuesta: $($result.message)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Error enviando: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "   Detalles: $responseBody" -ForegroundColor Red
    }
}

# 4. Instrucciones
Write-Host "`n=== Próximos Pasos ===" -ForegroundColor Cyan
Write-Host "1. Ve a n8n: https://n8n.arc-ctes.shop" -ForegroundColor White
Write-Host "2. Revisa los logs del workflow para ver si recibió los datos" -ForegroundColor White
Write-Host "3. Verifica que n8n procese la imagen y envíe resultados al backend" -ForegroundColor White
Write-Host "4. Verifica en Supabase que el reporte se haya actualizado:" -ForegroundColor White
Write-Host "   SELECT id, labels, colors FROM reports WHERE id = '$reportId';" -ForegroundColor Gray









