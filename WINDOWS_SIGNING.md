# Windows Code Signing Guide

## Option 1: Purchase Code Signing Certificate
1. Buy from: DigiCert, Sectigo, SSL.com (~$100-400/year)
2. Get an EV (Extended Validation) certificate for instant trust
3. Sign the executable during build

## Option 2: Free Alternative - Use signtool with self-signed cert (limited trust)
```powershell
# Create self-signed certificate (for testing only)
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=MRI Lab Graz" -CertStoreLocation Cert:\CurrentUser\My
$pwd = ConvertTo-SecureString -String "YourPassword" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "codesign.pfx" -Password $pwd

# Sign the executable
signtool sign /f codesign.pfx /p YourPassword /t http://timestamp.digicert.com ParticipantBarcodeTool.exe
```

## Option 3: Build Reputation Over Time
- Each download/run helps build reputation with Microsoft
- After ~100+ users, warnings may decrease
- Takes weeks/months

## Recommended for Open Source Projects
For academic/research projects without budget:
1. Document the workaround in README
2. Submit hash to Microsoft for reputation building
3. Consider open collective funding for code signing
