Dim oShell
Set oShell = WScript.CreateObject ("WSCript.shell")
oShell.run "sara.cmd 2> errors.log", 0
Set oShell = Nothing