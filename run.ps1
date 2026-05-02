# Download and run Maven if not present
$mavenVersion = "3.9.6"
$mavenDir = "$env:USERPROFILE\.m2\wrapper\dists\apache-maven-$mavenVersion-bin"
$mavenHome = "$mavenDir\apache-maven-$mavenVersion"

if (-not (Test-Path "$mavenHome\bin\mvn.cmd")) {
    Write-Host "Downloading Maven $mavenVersion..." -ForegroundColor Yellow
    $zipUrl = "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/$mavenVersion/apache-maven-$mavenVersion-bin.zip"
    $zipFile = "$env:TEMP\maven.zip"
    
    New-Item -ItemType Directory -Force -Path $mavenDir | Out-Null
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile
    Expand-Archive -Path $zipFile -DestinationPath $mavenDir -Force
    Remove-Item $zipFile
    Write-Host "Maven downloaded successfully!" -ForegroundColor Green
}

$env:MAVEN_HOME = $mavenHome
$env:Path = "$mavenHome\bin;$env:Path"

Write-Host "Starting Expense Tracker..." -ForegroundColor Green
mvn.cmd spring-boot:run