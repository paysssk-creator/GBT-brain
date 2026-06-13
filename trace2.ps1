Start-Sleep -Seconds 3
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | 
    Select-Object ProcessId, ParentProcessId, @{N='Cmd';E={$_.CommandLine}} |
    Where-Object { $_.Cmd -like '*gbt-brain*' } |
    Format-Table -AutoSize
