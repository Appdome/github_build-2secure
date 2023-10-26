# Appdome Android Fuse&Sign action

Appdome's Build-2Secure GitHub Action is an out-of-the-box GitHub CI/CD integration, making it easy for mobile developers to automate the build, signing, and certification of security, anti-fraud, and other protections in Android & iOS apps in GitHub CI/CD pipelines. No code and no SDKs are required.

The purpose of Appdome's Build-2Secure Action for GitHub is to streamline and accelerate cyber and anti-fraud delivery in CI/CD pipelines. To do this, the Build-2Secure Action for GitHub automates three important steps in delivering more secure mobile applications to your users fast: (1) building app-level protections into mobile apps, (2) code signing the protected mobile app, and (3) certifying the security of each protected mobile app. The Appdome Build-2Secure Action for GitHub can be used to deliver Certified Secure™ mobile app security, anti-fraud, anti-malware, mobile anti-bot, and other cyber defense updates to mobile apps on the Appdome Cyber Defense Automation Platform. Use this Action for GitHub as a stand-alone DevSecOps integration or in combination with other DevSecOps integrations in your CI/CD pipeline.  


# Usage

See [action.yml](action.yml)

### Android - AUTO_SIGNING
```yaml
name: Appdome build-2secure
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  appdome:
    runs-on: ubuntu-latest
    
    steps:
      - name: Appdome build-2secure
        uses: Appdome/github_build-2secure@latest
        with:
          APPDOME_API_TOKEN: ${{secrets.APPDOME_API_KEY}}
          TEAM-ID: "Your team id in appdome"
          APP_FILE: "# none_protected_application can be pass as path/on/repository OR https://download_link"
          FUSION_SET_ID: "Appdome Fusion Set_Id Android/iOS"
          SIGN_OPTIONS: "SIGN_ON_APPDOME"
          BUILD_WITH_LOGS: true - Optional
          KEYSTORE_FILE: ${{secrets.KEYSTORE}}
          KEYSTORE_PASSWORD: ${{secrets.KEYSTORE_PASSWORD}}
          KEYSTORE_ALIAS: ${{secrets.KEYSTORE_ALIAS}}
          KEYSTORE_KEY_PASSWORD: ${{secrets.KEYSTORE_KEY_PASS}}
          SECOND_OUTPUT: true - Optional - since version 1.1.0
          BUILD_TO_TEST: "lambdatest" | "bitbar" | "browserstack" | "saucelabs" - Optional - since version 1.1.0
          OUTPUT_APP_NAME: "Output_app_name" - Optional, will also apply for second output universal apk  - since version 1.2.0. # Note: Since version 1.3.2, this also supports a full path.
```

### Android - PRIVATE_SIGNING
```yaml
name: Appdome build-2secure
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  appdome:
    runs-on: ubuntu-latest
    
    steps:
      - name: Appdome build-2secure
        uses: Appdome/github_build-2secure@latest
        with:
          APPDOME_API_TOKEN: ${{secrets.APPDOME_API_KEY}}
          TEAM-ID: "Your team id in appdome"
          APP_FILE: "# none_protected_application can be pass as path/on/repository OR https://download_link"
          FUSION_SET_ID: "Appdome Fusion Set_Id Android"
          SIGN_OPTIONS: "PRIVATE_SIGNING"
          BUILD_WITH_LOGS: true - Optional
          SIGN_FINGERPRINT: ${{secrets.APPDOME_SIGN_FINGERPRINT}}
          GOOGLE-PLAY-SIGNING: "true" - Optional
          SECOND_OUTPUT: true - Optional - since version 1.1.0
          BUILD_TO_TEST: "lambdatest" | "bitbar" | "browserstack" | "saucelabs" - Optional - since version 1.1.0
          OUTPUT_APP_NAME: "Output_app_name" - Optional, will also apply for second output universal apk  - since version 1.2.0. # Note: Since version 1.3.2, this also supports a full path.
```

### Android - AUTO_DEV_SIGNING
```yaml
name: Appdome build-2secure
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  appdome:
    runs-on: ubuntu-latest
    
    steps:
      - name: Appdome build-2secure
        uses: Appdome/github_build-2secure@latest
        with:
          APPDOME_API_TOKEN: ${{secrets.APPDOME_API_KEY}}
          TEAM-ID: "Your team id in appdome"
          APP_FILE: "# none_protected_application can be pass as path/on/repository OR https://download_link"
          FUSION_SET_ID: "Appdome Fusion Set_Id Android"
          SIGN_OPTIONS: "AUTO_DEV_SIGNING"
          SIGN_FINGERPRINT: ${{secrets.APPDOME_SIGN_FINGERPRINT}}
          GOOGLE-PLAY-SIGNING: "true" - Optional
          BUILD_WITH_LOGS: true - Optional
          BUILD_TO_TEST: "lambdatest" | "bitbar" | "browserstack" | "saucelabs" - Optional - since version 1.1.0
          OUTPUT_APP_NAME: "Output_app_name" - Optional - since version 1.2.0. # Note: Since version 1.3.2, this also supports a full path.
```

### iOS - AUTO_SIGNING
```yaml
name: Appdome build-2secure
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  appdome:
    runs-on: ubuntu-latest
    
    steps:
      - name: Appdome build-2secure
        uses: Appdome/github_build-2secure@latest
        with:
          APPDOME_API_TOKEN: ${{secrets.APPDOME_API_KEY}}
          TEAM-ID: "Your team id in appdome"
          APP_FILE: "# none_protected_application can be pass as path/on/repository OR https://download_link"
          FUSION_SET_ID: "Appdome Fusion Set_Id iOS"
          SIGN_OPTIONS: "SIGN_ON_APPDOME"
          CERTIFICATE_FILE: ${{secrets.CERTIFICATE}}
          CERTIFICATE_PASSWORD: ${{secrets.CERTIFICATE_PASSWORD}}
          MOBILE_PROVISION_PROFILE_FILE: "<path/on/repository>,<path/on/repository>" ...
                                          OR “<https_download_link>,<https_download_link>” ...
                                          OR ${{secrets.PROVISION_PROFILE_BASE64}}
          ENTITLEMENTS_FILE: "<path/on/repository>,<path/on/repository>" ...
                              OR “<https_download_link>,<https_download_link>” ...
                              OR ${{secrets.ENTITLEMENTS_BASE64}}
                              OR ${{secrets.PROVISION_PROFILE_BASE64}}
          BUILD_WITH_LOGS: true - Optional
          BUILD_TO_TEST: "lambdatest" | "bitbar" | "browserstack" | "saucelabs" - Optional - since version 1.1.0
          OUTPUT_APP_NAME: "Output_app_name" - Optional - since version 1.2.0. # Note: Since version 1.3.2, this also supports a full path.
```

### iOS - PRIVATE_SIGNING
```yaml
name: Appdome build-2secure
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  appdome:
    runs-on: ubuntu-latest
    
    steps:
      - name: Appdome build-2secure
        uses: Appdome/github_build-2secure@latest
        with:
          APPDOME_API_TOKEN: ${{secrets.APPDOME_API_KEY}}
          TEAM-ID: "Your team id in appdome"
          APP_FILE: "# none_protected_application can be pass as path/on/repository OR https://download_link"
          FUSION_SET_ID: "Appdome Fusion Set_Id iOS"
          SIGN_OPTIONS: "PRIVATE_SIGNING"
          MOBILE_PROVISION_PROFILE_FILE: "<path/on/repository>,<path/on/repository>" ...
                                          OR “<https_download_link>,<https_download_link>” ...
                                          OR ${{secrets.PROVISION_PROFILE_BASE64}}
          ENTITLEMENTS_FILE: "<path/on/repository>,<path/on/repository>" ...
                              OR “<https_download_link>,<https_download_link>” ...
                              OR ${{secrets.ENTITLEMENTS_BASE64}}
          BUILD_WITH_LOGS: true - Optional
          BUILD_TO_TEST: "lambdatest" | "bitbar" | "browserstack" | "saucelabs" - Optional - since version 1.1.0
          OUTPUT_APP_NAME: "Output_app_name" - Optional - since version 1.2.0. # Note: Since version 1.3.2, this also supports a full path.
```

### iOS - AUTO_DEV_SIGNING
```yaml
name: Appdome build-2secure
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  appdome:
    runs-on: ubuntu-latest
    
    steps:
      - name: Appdome build-2secure
        uses: Appdome/github_build-2secure@latest
        with:
          APPDOME_API_TOKEN: ${{secrets.APPDOME_API_KEY}}
          TEAM-ID: "Your team id in appdome"
          APP_FILE: "# none_protected_application can be pass as path/on/repository OR https://download_link"
          FUSION_SET_ID: "Appdome Fusion Set_Id iOS"
          SIGN_OPTIONS: "AUTO_DEV_SIGNING"
          MOBILE_PROVISION_PROFILE_FILE: "<path/on/repository>,<path/on/repository>" ...
                                          OR “<https_download_link>,<https_download_link>” ...
                                          OR ${{secrets.PROVISION_PROFILE_BASE64}}
          ENTITLEMENTS_FILE: "<path/on/repository>,<path/on/repository>" ...
                              OR “<https_download_link>,<https_download_link>” ...
                              OR ${{secrets.ENTITLEMENTS_BASE64}}
          BUILD_WITH_LOGS: true - Optional
          BUILD_TO_TEST: "lambdatest" | "bitbar" | "browserstack" | "saucelabs" - Optional - since version 1.1.0
          OUTPUT_APP_NAME: "Output_app_name" - Optional - since version 1.2.0. # Note: Since version 1.3.2, this also supports a full path.
```

