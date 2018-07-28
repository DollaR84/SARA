Dim oShell
Set oShell = WScript.CreateObject ("WSCript.shell")
oShell.run "setup.cmd", 0
Set oShell = Nothing