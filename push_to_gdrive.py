import os
from gdrive_datastore.gdrive import GDriveCopier

REPO_BRANCH = os.getenv('REPO_BRANCH','_LOCAL_')
GDRIVE_FOLDER = os.getenv('GDRIVE_FOLDER','OpenDisclosureDev') or 'OpenDisclosureDev'
copier = GDriveCopier(GDRIVE_FOLDER, target_subfolder=REPO_BRANCH)
copier.upload_from('.local/netfile_redacted')
