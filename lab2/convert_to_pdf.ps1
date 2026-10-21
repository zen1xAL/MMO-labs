$file = Get-ChildItem "D:\MMO\lab2\report\*.docx" | Select-Object -First 1
if (-not $file) {
    Write-Error "DOCX file not found in D:\MMO\lab2\report!"
    exit 1
}

$docxPath = $file.FullName
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")

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
}
catch {
    Write-Host "ERROR: $_"
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
