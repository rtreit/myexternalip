# run this script as an administrator
# this will register the powershell script to run as a scheduled task on a fixed interval without flashing a command prompt window temporarily
function Get-ScriptDirectory
{
    $Invocation = (Get-Variable MyInvocation -Scope 1).Value
    Split-Path $Invocation.MyCommand.Definition
}

$taskName = "myexternalip"
$taskExists = Get-ScheduledTask | Where-Object {$_.TaskName -like $taskName }
if ($taskExists)
{
    Unregister-ScheduledTask -TaskName "myexternalip" -Confirm:$false
}

$thisdirectory = Get-ScriptDirectory
#$thisdirectory = $thisdirectory.Path
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -WorkingDirectory $thisdirectory -Argument "-WindowStyle Hidden -File run_save_ip_to_onedrive.ps1"
$principal = New-ScheduledTaskPrincipal -LogonType S4U -User "$env:USERDOMAIN\$env:USERNAME"
$basetrigger = New-ScheduledTaskTrigger -Daily -At 1am
$secondarytrigger = New-ScheduledTaskTrigger -Once -At 1am -RepetitionInterval (New-TimeSpan -Hours 1) 
$basetrigger.Repetition  = $secondarytrigger.Repetition 
$settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable:$true -StartWhenAvailable:$true

Register-ScheduledTask -Action $action -Trigger $basetrigger -TaskName $taskName -Description "Save my External IP to OneDrive" -Settings $settings -Principal $principal 
