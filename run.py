import subprocess
import pkg_resources
import sys


def check_install_library(library_name):
    try:
        dist = pkg_resources.get_distribution(library_name)
        print(f"{dist.key} {dist.version} is already installed.")
    except pkg_resources.DistributionNotFound:
        print(f"{library_name} is not installed. Installing now...")
        subprocess.check_call(['pip', 'install', library_name])
        print(f"{library_name} has been installed successfully.")

'''if len(sys.argv) > 1 and sys.argv[1] == "69":
    print("Verified identity")
else:
    sys.exit(1)'''

required_libraries = ['librosa', 'numpy', 'scipy', 'pandas', 'soundfile']

for library in required_libraries:
    check_install_library(library)

subprocess.check_call(['python', 'main.py'])
