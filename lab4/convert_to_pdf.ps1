$file = Get-ChildItem "D:\MMO\lab4\report\*.docx" | Select-Object -First 1
if (-not $file) {
    Write-Error "DOCX file not found in D:\MMO\lab4\report!"
    exit 1
}

$docxPath = $file.FullName
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
$rootPdfPath = "D:\MMO\lab4\" + [System.IO.Path]::GetFileName($pdfPath)

Write-Host "DOCX Path: $docxPath"
Write-Host "PDF Path:  $pdfPath"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    # wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Host "SUCCESS: PDF created successfully at: $pdfPath"
    Copy-Item -Path $pdfPath -Destination $rootPdfPath -Force
    Write-Host "SUCCESS: Copied PDF to root: $rootPdfPath"
}
catch {
    Write-Host "ERROR: $_"
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
