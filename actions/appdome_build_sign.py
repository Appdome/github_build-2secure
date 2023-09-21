import argparse
import glob
import sys
import os
import subprocess

DEFAULT_OUTPUT_NAME = "Appdome_secured_app"

def parse_args():
    """
    Command line arguments
    :return: args parser
    """
    parser = argparse.ArgumentParser("Appdome Build-2secure args")
    parser.add_argument("-sign", dest='sign_option', required=True,
                        help="SIGN_ON_APPDOME OR PRIVATE_SIGNING OR AUTO_DEV_SIGNING")
    parser.add_argument("-api_key", dest='appdome_api_key', required=True,
                        help='Appdome API key')
    parser.add_argument("-fs", dest='fusion_set', required=True,
                        help="Appdome fusion set")
    parser.add_argument("-kp", dest='keystore_pass', required=False,
                        help="keystore password", default="None")
    parser.add_argument("-cp", dest='certificate_pass', required=False,
                        help="certificate password", default="None")
    parser.add_argument("-ka", dest='keystore_alias', required=False,
                        help="keystore alias", default="None")
    parser.add_argument("-kkp", dest='keystore_key_pass', required=False,
                        help="keystore key pass", default="None")
    parser.add_argument("-team_id", dest='team_id', required=False,
                        help="team id", default="None")
    parser.add_argument("-google-play-signing", dest='google_play_signing', required=False,
                        help="google play signing", default="false")
    parser.add_argument("-signing_fingerprint", dest='signing_fingerprint', required=False,
                        help="signing_fingerprint", default="None")
    parser.add_argument("-bl", dest='build_with_logs', required=False,
                        help="Do you want to build with logs?")
    parser.add_argument("--sign_second_output", dest='sign_second_output', required=False,
                        help="Universal apk output for aab apps?")
    parser.add_argument("-bt", dest='build_to_test', required=False,
                        help="SAUCELABS OR BITBAR OR LAMBDATEST OR BROWSERSTACK")
    parser.add_argument("-o", dest='output_name', required=False,
                        help="Output app name")
    return parser.parse_args()

sys.path.extend([os.path.join(sys.path[0], '../..')])

new_env = os.environ.copy()

new_env["APPDOME_CLIENT_HEADER"] = "Github/1.0.0"

args = parse_args()


def validate_args(platform, arguments, keystore_file, provision_profiles, entitlements, keystore_pass):
    print("entered validate")
    error = False
    if arguments.sign_option is None or arguments.sign_option == "None":
        print("No signing option specified")
        error = True
    if arguments.appdome_api_key == "None":
        print("No API key specified")
        error = True
    if arguments.fusion_set == "None":
        print("No fusion set specified")
        error = True
    if platform == "ios":
        if len(provision_profiles) == 0:
            print("No mobile provisioning profile file specified")
            error = True
        if arguments.sign_option in ["SIGN_ON_APPDOME"]:
            if len(keystore_file) == 0:
                print("No certificate file specified")
                error = True
            if keystore_pass == "None":
                print("No certificate password specified")
                error = True
        if arguments.sign_option in ["SIGN_ON_APPDOME", "AUTO_DEV_SIGNING"]:
            if len(entitlements) == 0:
                print("No entitlements file specified")
                error = True
    else:
        if arguments.sign_option == "SIGN_ON_APPDOME":
            if len(keystore_file) == 0:
                print("No keystore file specified")
                error = True
            if keystore_pass == "None":
                print("No keystore password specified")
                error = True
            if arguments.keystore_alias == "None":
                print("No keystore alias specified")
                error = True
            if arguments.keystore_key_pass == "None":
                print("No keystore key pass specified")
                error = True
        else:
            if arguments.signing_fingerprint == "None":
                print("No signing fingerprint specified")
                error = True
    if error:
        sys.exit(1)


def main():
    print(args)
    os.makedirs('./output', exist_ok=True)
    sign_option = args.sign_option
    appdome_api_key = args.appdome_api_key
    fusion_set = args.fusion_set
    keystore_pass = args.keystore_pass
    certificate_pass = args.certificate_pass
    output_file_name = args.output_name if args.output_name != "None" else DEFAULT_OUTPUT_NAME
    output_file_name = os.path.basename(output_file_name)
    output_file_name, _ = os.path.splitext(output_file_name)
    extensions = ["*.apk", "*.aab", "*.ipa"]
    app_file = [file for extension in extensions for file in glob.glob(f"./files/{extension}")]
    if len(app_file) == 0:
        print("Couldn't locate non_protected app file on ./files/non_protected.*")
        sys.exit(1)
    app_file = app_file[0]
    app_name = os.path.basename(app_file)
    app_ext = app_name[-4:]
    platform = "ios" if app_ext == ".ipa" else "android"
    keystore_pass = keystore_pass if (keystore_pass and keystore_pass != "None") else certificate_pass
    keystore_file = glob.glob('./files/cert.*')
    provision_profiles = f"--provisioning_profiles {' '.join(glob.glob('./files/provision_profiles/*'))}" \
        if os.path.exists("./files/provision_profiles") else ""
    entitlements = f"--entitlements {' '.join(glob.glob('./files/entitlements/*'))}" \
        if os.path.exists("./files/entitlements") else ""

    validate_args(platform, args, keystore_file, provision_profiles, entitlements, keystore_pass)

    build_with_logs = " -bl" if args.build_with_logs != "false" else ""
    sign_second_output = f" --sign_second_output ./output/{output_file_name}_second_output.apk" if \
        (args.sign_second_output != "false" and app_ext == ".aab") else ""
    build_to_test = f" -bt {args.build_to_test}" if args.build_to_test != "None" else ""
    team_id = f"--team_id {args.team_id}" if args.team_id != "None" else ""

    # Build command according to signing option
    if sign_option == 'SIGN_ON_APPDOME':
        keystore_alias = f"--keystore_alias {args.keystore_alias}" if args.keystore_alias != "None" else ""
        keystore_key_pass = f"--key_pass {args.keystore_key_pass}" if args.keystore_key_pass != "None" else ""

        cmd = f"python3 appdome/appdome-api-python/appdome_api.py -key {appdome_api_key} --app {app_file} " \
              f"--sign_on_appdome -fs {fusion_set} {team_id} --keystore {keystore_file[0]} " \
              f"--keystore_pass {keystore_pass} --output ./output/{output_file_name}{app_ext} " \
              f"--certificate_output ./output/certificate.pdf {keystore_alias} {keystore_key_pass} " \
              f"{provision_profiles} {entitlements}{build_with_logs}{sign_second_output}{build_to_test}  " \
              f"--deobfuscation_script_output ./output/deobfuscation_scripts.zip"

        subprocess.check_output([i for i in cmd.split(" ") if i != ''], env=new_env)

    elif sign_option == 'PRIVATE_SIGNING':
        google_play_signing = f"--google_play_signing" if args.google_play_signing != "false" else ""
        signing_fingerprint = f"--signing_fingerprint {args.signing_fingerprint}" if args.signing_fingerprint != "None" else ""

        cmd = f"python3 appdome/appdome-api-python/appdome_api.py -key {appdome_api_key} " \
              f"--app {app_file} --private_signing -fs {fusion_set} {team_id} " \
              f"--output ./output/{output_file_name}{app_ext} --certificate_output ./output/certificate.pdf " \
              f"{google_play_signing} {signing_fingerprint} {provision_profiles}{build_with_logs}{sign_second_output}" \
              f"{build_to_test} --deobfuscation_script_output ./output/deobfuscation_scripts.zip"

        subprocess.check_output([i for i in cmd.split(" ") if i != ''], env=new_env)

    elif sign_option == 'AUTO_DEV_SIGNING':
        google_play_signing = f"--google_play_signing" if args.google_play_signing != "false" else ""
        signing_fingerprint = f"--signing_fingerprint {args.signing_fingerprint}" if args.signing_fingerprint != "None" else ""

        cmd = f"python3 appdome/appdome-api-python/appdome_api.py -key {appdome_api_key} " \
              f"--app {app_file} --auto_dev_private_signing -fs {fusion_set} {team_id} " \
              f"--output ./output/{output_file_name}.sh --certificate_output ./output/certificate.pdf " \
              f"{google_play_signing} {signing_fingerprint} {provision_profiles} {entitlements}{build_with_logs}" \
              f"{build_to_test}  --deobfuscation_script_output ./output/deobfuscation_scripts.zip"
        subprocess.check_output([i for i in cmd.split(" ") if i != ''], env=new_env)
    else:
        print("Signing option not found!\nValid signs: AUTO_SIGNING/PRIVATE_SIGNING/AUTO_DEV_SIGNING")


if __name__ == '__main__':
    main()
