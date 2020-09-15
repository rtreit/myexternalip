# dir where script is executing (%~dp0 equivalent)
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
$basetrigger = New-ScheduledTaskTrigger -Daily -At 11:00am 
$secondarytrigger = New-ScheduledTaskTrigger -Once -At 1am -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration (New-TimeSpan -Minutes 5)
$basetrigger.Repetition  = $secondarytrigger.Repetition 

$settings = New-ScheduledTaskSettingsSet -Hidden:$true -RunOnlyIfNetworkAvailable:$true -StartWhenAvailable:$true

Register-ScheduledTask -Action $action -Trigger $basetrigger -TaskName $taskName -Description "Save my External IP to OneDrive" -Settings $settings 
