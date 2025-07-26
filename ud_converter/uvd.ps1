git clone https://github.com/UniversalDependencies/tools.git udtools
Remove-Item -Recurse -Force validate-data\*
Copy-Item -Recurse udtools\data\* validate-data\
Remove-Item -Recurse -Force udtools
