import os
from gdrive_client.GDriveCopier import GDriveCopier

REPO_BRANCH = os.getenv('REPO_BRANCH','_LOCAL_')
GDRIVE_FOLDER = os.getenv('GDRIVE_FOLDER','netfile_redacted') or 'netfile_redacted'
copier = GDriveCopier(GDRIVE_FOLDER, target_branch=REPO_BRANCH)
copier.upload_from('netfile_redacted')
