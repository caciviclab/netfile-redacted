import os
import subprocess
from gdrive_client.GDriveCopier import GDriveCopier

REPO_OWNER = os.getenv('REPO_OWNER','')
REPO_BRANCH = os.getenv('REPO_BRANCH','_LOCAL_')

if (REPO_OWNER in ['','ChenglimEar']):
    downloads_dir = '.local/downloads'
    os.makedirs(downloads_dir, exist_ok=True)
    copier = GDriveCopier('netfile_redacted', target_branch = REPO_BRANCH)
    copier.download_to(downloads_dir)
    print(f'Contents of downloads dir ({downloads_dir}):')
    subprocess.call(f'ls {downloads_dir}', shell=True)
