import os
from gdrive_client.GDriveCopier import GDriveCopier

REPO_OWNER = os.getenv('REPO_OWNER','')

if (REPO_OWNER in ['','ChenglimEar']):
    os.makedirs('downloads', exist_ok=True)
    copier = GDriveCopier('netfile_redacted')
    copier.download_to('downloads')
    print('Contents of downloads dir:')
    os.system('ls downloads')
