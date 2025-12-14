# Windows setup
1. Install Powershell from WinGet. This is distinct from
[Windows Powershell](https://learn.microsoft.com/en-us/powershell/scripting/what-is-windows-powershell)
which is included with Windows.
```powershell
winget install Microsoft.PowerShell
```

2. Install [Scoop](https://scoop.sh)

3. Install Git, Hugo, and uv
```powershell
scoop install git hugo uv
```

4. Clone and enter the project
```powershell
git clone https://github.com/codenetwork/hugo-website.git
cd hugo-website
```

5. Start the Hugo web server and view the site at the URL displayed in your terminal.
```powershell
hugo server
```
