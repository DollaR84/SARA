Dim oShell
Set oShell = WScript.CreateObject ("WSCript.shell")
oShell.run "setup.cmd 2> errors.log", 0
Set oShell = Nothing