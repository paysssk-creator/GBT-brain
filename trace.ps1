Get-CimInstance Win32_Process -Filter "Name='node.exe'" | 
    Select-Object ProcessId, ParentProcessId, @{N='Cmd';E={$_.CommandLine}} |
    Where-Object { $_.Cmd -like '*gbt*' -or $_.Cmd -like '*brain*' -or $_.Cmd -like '*scheduler*' } |
    Format-Table -AutoSize
