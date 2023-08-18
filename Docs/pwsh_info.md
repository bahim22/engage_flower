
# PowerShell ^7

- [PowerShell ^7](#powershell-7)
	- [Examples](#examples)
		- [Remove accounts and Remote connections](#remove-accounts-and-remote-connections)
		- [Recursively copy](#recursively-copy)
		- [Script Blocks](#script-blocks)
		- [Get file length](#get-file-length)
		- [Operate on recent System events](#operate-on-recent-system-events)
		- [Create multiple jobs that run scripts in parallel](#create-multiple-jobs-that-run-scripts-in-parallel)

## Examples

### Remove accounts and Remote connections

```ps1
# purge accounts
Import-Csv '.\SP 23 Declines.csv' | foreach {
  $UPN = $_."PPU Email"
  $username = $UPN.Substring(0, $UPN.IndexOf('@'))
  get-aduser $username | Remove-ADUser
}

$Session = New-PSSession -ComputerName "Server02" -Credential "Contoso\User01" Copy-Item "D:\Folder002\" -Destination "C:\Folder002_Copy\" -ToSession $Session

Get-ADComputer -Filter 'Name -like "Fabrikam*"' -Properties IPv4Address | FT Name,DNSHostName,IPv4Address -A

$Session = New-PSSession -ComputerName "Server01" -Credential "Contoso\User01"
Copy-Item "C:\MyRemoteData\scripts" -Destination "D:\MyLocalData\" -FromSession $Session
```

### Recursively copy

```ps1
# copy the entire contents of a remote folder to the local computer
$Session = New-PSSession -ComputerName "Server01" -Credential "Contoso\User01"
Copy-Item "C:\MyRemoteData\scripts" -Destination "D:\MyLocalData\scripts" -FromSession $Session -Recurse

"Microsoft.PowerShell.Core", "Microsoft.PowerShell.Host" | ForEach-Object {$_.Split(".")}
"Microsoft.PowerShell.Core", "Microsoft.PowerShell.Host" | ForEach-Object -MemberName Split -ArgumentList "."
"Microsoft.PowerShell.Core", "Microsoft.PowerShell.Host" | Foreach Split "."

Get-Module -ListAvailable | ForEach-Object -MemberName Path

$user = 'username'

Copy-Item "K:\ITS\General\Microsoft Exam References" -Destination "C:\Users\$user\OneDrive - Point Park University" -Recurse
```

### Script Blocks

- Script block: You can use a script block to specify the operation.
  - Within the script block, use the `$_` variable to represent the current object.
  - The script block is the value of the Process parameter, and can contain any PowerShell script.

For example, the following command gets the value of the ProcessName property of each process on the computer.

```ps1
`Get-Process | ForEach-Object {$_.ProcessName}`
```

- `ForEach-Object` supports the `begin`, `process`, and `end` blocks as described in about_functions (about/about_functions.md#piping-objects-to-functions).

### Get file length

- Get the length of all the files in a directory

```ps1
Get-ChildItem $PSHOME | ForEach-Object -Process {if (!$_.PSIsContainer) {$_.Name; $_.Length / 1024; " " }}
```

- If the object is not a dir, the script block gets the name of the file, divides the value of its Length property by 1024, and adds a space (" ") to separate it from the next entry.
- The cmdlet uses the **PSISContainer** prop to determine whether an object is a dir.

### Operate on recent System events

```ps1
$Events = Get-EventLog -LogName System -Newest 1000
$events | ForEach-Object -Begin {Get-Date} -Process {Out-File -FilePath Events.txt -Append -InputObject $_.Message} -End {Get-Date}
```

- `Get-EventLog` gets the 1000 most recent events from the System event log and stores them in the `$Events` variable.
- `$Events` is then piped to the `ForEach-Object` cmdlet. The Begin param displays the current date and time.
- Next, the Process param uses the `Out-File` cmdlet to create a text file that is named events.txt and stores the message property of each of the events in that file.
- Last, the End param is used to display the date & time after all the processing has completed.

### Create multiple jobs that run scripts in parallel

```ps1
$jobs = for ($i=0; $i -lt 10; $i++) {
	1..10 | ForEach-Object -Parallel {
		./RunMyScript.ps1
	} -AsJob -ThrottleLimit 5
$jobs | Receive-Job -Wait
}
```

- This example creates 10 running jobs. Each job runs no more that 5 scripts concurrently. The total number of instances running concurrently is limited to 50 (10 jobs times the ThrottleLimit of 5).

```ps1
# get pwsh examples in vs-code
code (Get-ChildItem $HOME/.vscode/extensions/ms-vscode.powershell-*/examples)[-1]
```
