param(
    [string]$RepositoryUrl = "https://github.com/Nasser934/motion-world.git"
)

$ErrorActionPreference = "Stop"

if (Test-Path ".git") {
    throw "This folder is already a Git repository."
}

git init
git add .
git commit -m "Initial public release of Motion World 0.3.0"
git branch -M main
git remote add origin $RepositoryUrl
git push -u origin main
