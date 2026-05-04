# run_batch.ps1 - Automatización de Publicación en Facebook
# Configuración
$PAGE_ID = "TU_PAGE_ID_AQUÍ"
$ACCESS_TOKEN = "TU_ACCESS_TOKEN_AQUÍ"
$CONTENT_FILE = "posts_content.json"
$TRACKER_FILE = "tracker.json"
$IMAGE_DIR = "fb_images"

# Cargar datos
$posts = Get-Content $CONTENT_FILE | ConvertFrom-Json
$tracker = Get-Content $TRACKER_FILE | ConvertFrom-Json

Write-Host "🚀 Iniciando proceso de publicación..." -ForegroundColor Cyan

foreach ($post in $posts) {
    if ($post.id -le $tracker.last_processed_id) {
        Write-Host "⏭️ Saltando Post $($post.id): Ya procesado." -ForegroundColor Yellow
        continue
    }

    $imagePath = Join-Path $PWD "$IMAGE_DIR/post_$($post.id).png"
    if (-not (Test-Path $imagePath)) {
        Write-Host "❌ Error: Imagen no encontrada para el Post $($post.id) en $imagePath" -ForegroundColor Red
        continue
    }

    Write-Host "📤 Publicando Post $($post.id): $($post.title)..." -ForegroundColor Green
    
    # Simulación de subida (Descomentar para real)
    # $uri = "https://graph.facebook.com/v19.0/$PAGE_ID/photos"
    # $body = @{
    #     message = $post.postES + "`n`n#Noticias #Futuro #IA #Ciencia #Tecnologia"
    #     source = Get-Item $imagePath
    #     access_token = $ACCESS_TOKEN
    # }
    # $response = Invoke-RestMethod -Uri $uri -Method Post -Form $body
    
    # Simulación exitosa para el ejemplo
    $response = @{ id = "SIM_123456789" }

    if ($response.id) {
        Write-Host "✅ Éxito! ID de publicación: $($response.id)" -ForegroundColor DarkGreen
        $tracker.last_processed_id = $post.id
        $tracker.successful_posts += $post.id
        $tracker | ConvertTo-Json | Set-Content $TRACKER_FILE
        
        Write-Host "⏳ Esperando 35 segundos para evitar bloqueos..."
        Start-Sleep -Seconds 35
    } else {
        Write-Host "😱 Error publicando el Post $($post.id)" -ForegroundColor DarkRed
        $tracker.failed_posts += $post.id
        $tracker | ConvertTo-Json | Set-Content $TRACKER_FILE
    }
}

Write-Host "🏁 Proceso finalizado." -ForegroundColor Cyan
