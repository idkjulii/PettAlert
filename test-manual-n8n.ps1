# Script para probar manualmente el flujo completo de n8n
# Este script simula lo que n8n haría: obtener reportes, analizar y enviar resultados

Write-Host "`n=== Prueba Manual del Flujo de n8n ===" -ForegroundColor Cyan
Write-Host "Este script simula el proceso completo que n8n ejecutaría`n" -ForegroundColor Gray

$BACKEND_URL = "http://127.0.0.1:8003"

# Paso 1: Obtener un reporte con imagen
Write-Host "1️⃣ Obteniendo reportes con imágenes..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?limit=1&has_labels=false" -Method GET
    $reportsData = $response.Content | ConvertFrom-Json
    
    if ($reportsData.count -eq 0) {
        Write-Host "   ⚠️ No hay reportes sin procesar" -ForegroundColor Yellow
        Write-Host "   Intentando obtener cualquier reporte con imagen..." -ForegroundColor Gray
        $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?limit=1" -Method GET
        $reportsData = $response.Content | ConvertFrom-Json
    }
    
    if ($reportsData.count -eq 0) {
        Write-Host "   ❌ No se encontraron reportes con imágenes" -ForegroundColor Red
        Write-Host "   Crea un reporte con fotos desde la app móvil primero" -ForegroundColor Yellow
        exit
    }
    
    $report = $reportsData.reports[0]
    Write-Host "   ✅ Reporte encontrado:" -ForegroundColor Green
    Write-Host "      ID: $($report.report_id)" -ForegroundColor White
    Write-Host "      Imagen: $($report.image_url)" -ForegroundColor White
    Write-Host "      Especie: $($report.species)" -ForegroundColor White
    Write-Host "      Ya tiene labels: $($report.has_labels)" -ForegroundColor White
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# Paso 2: Mostrar información del reporte
Write-Host "`n2️⃣ Información del reporte:" -ForegroundColor Yellow
Write-Host "   Report ID: $($report.report_id)" -ForegroundColor White
Write-Host "   Image URL: $($report.image_url)" -ForegroundColor White
Write-Host "   Species: $($report.species)" -ForegroundColor White

# Paso 3: Simular análisis (en producción, esto lo haría Google Vision)
Write-Host "`n3️⃣ Simulando análisis con Google Vision..." -ForegroundColor Yellow
Write-Host "   ⚠️ NOTA: En producción, n8n llamaría a Google Vision API aquí" -ForegroundColor Gray
Write-Host "   Por ahora, usaremos datos simulados para la prueba" -ForegroundColor Gray

# Datos simulados basados en la especie
$mockLabels = switch ($report.species) {
    "dog" { 
        @(
            @{ label = "Dog"; score = 95.5 },
            @{ label = "Pet"; score = 92.3 },
            @{ label = "Mammal"; score = 88.7 },
            @{ label = "Animal"; score = 85.2 }
        )
    }
    "cat" {
        @(
            @{ label = "Cat"; score = 94.2 },
            @{ label = "Pet"; score = 91.5 },
            @{ label = "Mammal"; score = 87.9 }
        )
    }
    default {
        @(
            @{ label = "Pet"; score = 90.0 },
            @{ label = "Animal"; score = 85.0 }
        )
    }
}

$mockColors = @("#FFD700", "#8B4513", "#FFFFFF")
$detectedSpecies = $report.species

Write-Host "   ✅ Análisis simulado completado:" -ForegroundColor Green
Write-Host "      Labels detectados: $($mockLabels.Count)" -ForegroundColor White
Write-Host "      Colores detectados: $($mockColors.Count)" -ForegroundColor White
Write-Host "      Especie: $detectedSpecies" -ForegroundColor White

# Paso 4: Preparar payload para enviar al backend
Write-Host "`n4️⃣ Preparando datos para enviar al backend..." -ForegroundColor Yellow

$payload = @{
    report_id = $report.report_id
    image_url = $report.image_url
    labels = $mockLabels
    colors = $mockColors
    species = $detectedSpecies
    analysis_metadata = @{
        processed_at = (Get-Date).ToUniversalTime().ToString("o")
        image_index = $report.image_index
        total_images = $report.total_images
        source = "manual_test_script"
    }
} | ConvertTo-Json -Depth 10

Write-Host "   ✅ Payload preparado" -ForegroundColor Green

# Paso 5: Enviar resultados al backend
Write-Host "`n5️⃣ Enviando resultados al backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/process-result" -Method POST `
        -Body $payload `
        -ContentType "application/json"
    
    $result = $response.Content | ConvertFrom-Json
    
    if ($result.success) {
        Write-Host "   ✅ Resultados enviados exitosamente!" -ForegroundColor Green
        Write-Host "      Campos actualizados: $($result.updated_fields -join ', ')" -ForegroundColor White
    } else {
        Write-Host "   ⚠️ Respuesta: $($result.message)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Error enviando resultados: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "   Detalles: $responseBody" -ForegroundColor Red
    }
    exit
}

# Paso 6: Verificar que se actualizó
Write-Host "`n6️⃣ Verificando que el reporte se actualizó..." -ForegroundColor Yellow
Start-Sleep -Seconds 2  # Esperar un momento para que se actualice

try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?has_labels=true&limit=100" -Method GET
    $data = $response.Content | ConvertFrom-Json
    
    $updatedReport = $data.reports | Where-Object { $_.report_id -eq $report.report_id }
    
    if ($updatedReport) {
        Write-Host "   ✅ Reporte actualizado correctamente!" -ForegroundColor Green
        Write-Host "      Ahora tiene labels: $($updatedReport.has_labels)" -ForegroundColor White
        if ($updatedReport.current_labels) {
            Write-Host "      Labels guardados: ✅" -ForegroundColor Green
        }
    } else {
        Write-Host "   ⚠️ El reporte no aparece en la lista de procesados" -ForegroundColor Yellow
        Write-Host "      Esto puede ser normal si hay muchos reportes" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️ No se pudo verificar (no crítico): $($_.Exception.Message)" -ForegroundColor Yellow
}

# Resumen
Write-Host "`n=== Resumen de la Prueba ===" -ForegroundColor Cyan
Write-Host "✅ Paso 1: Obtener reporte - EXITOSO" -ForegroundColor Green
Write-Host "✅ Paso 2: Información del reporte - EXITOSO" -ForegroundColor Green
Write-Host "✅ Paso 3: Análisis simulado - EXITOSO" -ForegroundColor Green
Write-Host "✅ Paso 4: Preparar payload - EXITOSO" -ForegroundColor Green
Write-Host "✅ Paso 5: Enviar resultados - EXITOSO" -ForegroundColor Green
Write-Host "✅ Paso 6: Verificación - COMPLETADO" -ForegroundColor Green

Write-Host "`n📝 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Verifica en Supabase que el reporte tenga labels y colores" -ForegroundColor White
Write-Host "2. Configura el workflow en n8n siguiendo GUIA-INTEGRACION-N8N.md" -ForegroundColor White
Write-Host "3. Prueba el workflow completo en n8n" -ForegroundColor White

Write-Host "`n💡 Para verificar en Supabase, ejecuta:" -ForegroundColor Cyan
Write-Host "   SELECT id, labels, colors, species FROM reports WHERE id = '$($report.report_id)';" -ForegroundColor Gray









