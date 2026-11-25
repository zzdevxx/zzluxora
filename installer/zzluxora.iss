#ifndef MyAppVersion
  #define MyAppVersion "10.0.0"
#endif

[Setup]
AppId={{8D6E7B90-4A3F-4E91-B5F2-ZZLUXORA1000}
AppName=ZZLUXORA
AppVersion={#MyAppVersion}
AppVerName=ZZLUXORA v{#MyAppVersion}
AppPublisher=Andreas Restuawanta Christwara (@zzdevxx)
AppPublisherURL=https://zzdree.my.id/zzluxora/
AppSupportURL=https://github.com/zzdevxx/zzluxora
AppUpdatesURL=https://zzdree.my.id/zzluxora/
DefaultDirName={localappdata}\Programs\ZZLUXORA
DefaultGroupName=ZZLUXORA
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir=..\dist\installer
OutputBaseFilename=ZZLUXORA-Setup-{#MyAppVersion}
SetupIconFile=..\ui\assets\logo_zz.ico
UninstallDisplayIcon={app}\ZZLUXORA.exe
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\ZZLUXORA\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\ZZLUXORA"; Filename: "{app}\ZZLUXORA.exe"; IconFilename: "{app}\ZZLUXORA.exe"
Name: "{autodesktop}\ZZLUXORA"; Filename: "{app}\ZZLUXORA.exe"; Tasks: desktopicon; IconFilename: "{app}\ZZLUXORA.exe"

[Run]
Filename: "{app}\ZZLUXORA.exe"; Description: "{cm:LaunchProgram,ZZLUXORA}"; Flags: nowait postinstall skipifsilent
