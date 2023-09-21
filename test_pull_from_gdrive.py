import os
from gdrive_client.GDriveCopier import GDriveCopier

REPO_OWNER = os.getenv('REPO_OWNER','')
REPO_BRANCH = os.getenv('REPO_BRANCH','_LOCAL_')

if (REPO_OWNER in ['','ChenglimEar']):
    os.makedirs('.local/downloads', exist_ok=True)
    copier = GDriveCopier('netfile_redacted', target_branch = REPO_BRANCH)
    copier.download_to('.local/downloads')
    print('Contents of downloads dir:')
    os.system('ls .local/downloads')
