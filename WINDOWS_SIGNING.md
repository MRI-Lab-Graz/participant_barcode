# Windows Code Signing Guide

## Option 1: Purchase Code Signing Certificate (Recommended for Production)
1. **Buy from**: DigiCert, Sectigo, SSL.com (~$100-400/year)
2. **Get an EV (Extended Validation)** certificate for instant trust (no SmartScreen warnings)
3. **Automatic signing** is already configured in `.github/workflows/release.yml`

### Setting up GitHub Actions Signing (Once you have a certificate)
1. **Export your certificate to PFX format** (if not already):
   ```powershell
   # If you have a .cer and .key file, convert to PFX
   openssl pkcs12 -export -out certificate.pfx -inkey private.key -in certificate.cer
   ```

2. **Convert PFX to Base64**:
   ```powershell
   # Windows PowerShell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("certificate.pfx")) | Out-File cert-base64.txt
   ```
   ```bash
   # macOS/Linux
   base64 -i certificate.pfx -o cert-base64.txt
   ```

3. **Add secrets to GitHub**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add `SIGNING_CERTIFICATE` = contents of `cert-base64.txt` (the base64 string)
   - Add `SIGNING_PASSWORD` = your PFX password
   
4. **Done!** Next push to main will automatically sign the Windows executable

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
