import os
from gdrive_client.GDriveCopier import GDriveCopier

REPO_BRANCH = os.getenv('REPO_BRANCH','_LOCAL_')
copier = GDriveCopier('netfile_redacted', target_branch=REPO_BRANCH)
copier.upload_from('netfile_redacted')
