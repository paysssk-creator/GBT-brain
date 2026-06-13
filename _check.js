const { execSync } = require('child_process');
const ps = 'Get-CimInstance Win32_Process -Filter "Name=\'node.exe\'" | Select-Object ProcessId, CommandLine | Where-Object { $_.CommandLine -like \'*brain*\' } | Format-Table -AutoSize';
const out = execSync('powershell -NoProfile -Command ' + JSON.stringify(ps), { encoding: 'utf-8', timeout: 10000 });
console.log(out);
