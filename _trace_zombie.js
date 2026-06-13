const { execSync } = require('child_process');
// Find ALL node processes and their command lines
const out = execSync('wmic process where name="node.exe" get processid,commandline /format:csv', { encoding: 'utf-8' });
out.split('\n').forEach(line => {
    if (line.includes('gbt-brain') || line.includes('intelligent-scheduler') || line.includes('daemon') || line.includes('scanner')) {
        console.log(line.trim());
    }
});
// Also check if daemon is running
console.log('\n--- Daemon check ---');
try {
    const d = execSync('powershell -c "Get-Process -Name powershell | Where-Object {$_.MainWindowTitle -like \'*gbt*\' -or $_.CommandLine -like \'*daemon*\'}"', { encoding: 'utf-8' });
    console.log(d || 'no daemon found');
} catch { console.log('no daemon'); }
