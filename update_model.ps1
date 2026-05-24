$base = 'c:\Users\Awinda\MisProyectos\facebook_post_assistant'
$files = @(
    'crear_frase_viral.py',
    'crear_video_viral.py',
    'crear_video_seedboy.py',
    'crear_quiz_viral.py',
    'engine_agentes.py',
    'generar_nueva_semana.py',
    'generar_test_10.py',
    'fix_quizzes_emergency.py',
    'fix_quizzes_one_by_one.py'
)

foreach ($file in $files) {
    $path = Join-Path $base $file
    if (Test-Path $path) {
        $content = Get-Content $path -Raw -Encoding UTF8
        $updated = $content -replace 'gemini-2\.0-flash', 'gemini-2.5-flash'
        Set-Content $path $updated -Encoding UTF8 -NoNewline
        Write-Host "ACTUALIZADO: $file"
    } else {
        Write-Host "NO ENCONTRADO: $file"
    }
}
Write-Host ""
Write-Host "===== LISTO ====="
