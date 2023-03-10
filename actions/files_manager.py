import argparse
import os


def parse_args():
    """
    Command line arguments
    :return: args parser
    """
    parser = argparse.ArgumentParser("Appdome Build-2secure args")
    parser.add_argument("-a", dest='app_file', required=True,
                        help='None-protected application file')
    parser.add_argument("-k", dest='keystore', required=False,
                        help='Keystore file', default=None)
    parser.add_argument("-pp", dest='provision_profiles', required=False,
                        help="provision_profiles", default=None)
    parser.add_argument("-e", dest='entitlements', required=False,
                        help="entitlements", default=None)
    return parser.parse_args()


def is_base64(s):
    import base64
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode()
    except Exception:
        return False


def decode_base64(s, file_path):
    import base64
    with open(file_path, 'wb') as file:
        file.write(base64.b64decode(s))


def download_file(url, dest_file):
    import requests
    response = requests.get(url)
    if response.status_code < 300:
        with open(dest_file, "wb") as file:
            file.write(response.content)
    else:
        print(f"Error couldn't compose {url}")
        exit(1)


def copy_files(src_file, dest_file):
    import shutil
    shutil.copyfile(src_file, dest_file)


args = parse_args()


def main():
    app_file = args.app_file
    keystore = args.keystore
    provision_profiles = args.provision_profiles
    entitlements = args.entitlements

    ios_flag = True if app_file.endswith('.ipa') else False
    if not os.path.isdir("./files"):
        os.mkdir("./files")

    if app_file.startswith('htt'):
        download_file(app_file, f"./files/non_protected.{app_file[-3:]}")
    elif os.path.exists(app_file):
        copy_files(app_file, f"./files/non_protected.{app_file[-3:]}")
    else:
        print(f"Error couldn't compose {app_file}")
        exit(1)

    if keystore != "None":
        if keystore.startswith('htt'):
            download_file(keystore, f"./files/cert.p12") if ios_flag else download_file(keystore, f"./files/cert.keystore")
        elif os.path.exists(keystore):
            copy_files(keystore, f"./files/cert.p12") if ios_flag else copy_files(keystore, f"./files/cert.keystore")
        elif is_base64(keystore):
            decode_base64(keystore, f"./files/cert.p12") if ios_flag else decode_base64(keystore, f"./files/cert.keystore")
        else:
            print(f"Error couldn't compose {keystore}")
            exit(1)

    if provision_profiles != "None":
        if not os.path.exists("./files/provision_profiles"):
            os.mkdir("./files/provision_profiles")
        if is_base64(provision_profiles):
            decode_base64(provision_profiles, "./files/provision_profiles/0.mobileprovision")
        elif provision_profiles.startswith('htt'):
            for index, url in enumerate(provision_profiles.split(',')):
                download_file(url, f"./files/provision_profiles/{index}.mobileprovision")
        elif os.path.exists(provision_profiles.split(',')[0]):
            for index, path in enumerate(provision_profiles.split(',')):
                copy_files(path, f"./files/provision_profiles/{index}.mobileprovision")
        else:
            print(f"Error couldn't compose {provision_profiles}")
            exit(1)

    if entitlements != "None":
        if not os.path.exists("./files/entitlements"):
            os.mkdir("./files/entitlements")
        if is_base64(entitlements):
            decode_base64(entitlements, "./files/entitlements/0.plist")
        elif entitlements.startswith('htt'):
            for index, url in enumerate(entitlements.split(',')):
                download_file(url, f"./files/entitlements/{index}.plist")
        elif os.path.exists(entitlements.split(',')[0]):
            for index, path in enumerate(entitlements.split(',')):
                copy_files(path, f"./files/entitlements/{index}.plist")
        else:
            print(f"Error couldn't compose {entitlements}")
            exit(1)


if __name__ == '__main__':
    main()
