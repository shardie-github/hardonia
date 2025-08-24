Param(
  [string]$RepoUrl = "https://github.com/shardie-github/hardonia.git",
  [string]$Path = "C:\work\hardonia"
)

if (!(Test-Path $Path)) { git clone $RepoUrl $Path }
Set-Location $Path

git config --global user.name "Scott Hardie"
git config --global user.email "scottrmhardie@gmail.com"

git add .
git commit -m "feat: add minimal Netlify functions + bookmarklet + docs"
git push -u origin main
