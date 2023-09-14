# netfile_redacted

This repo allows someone to develop the code to pull netfile data, but it will require an authorized user to pull the changes from here to a fork in order to apply appropriate credentials for accessing netfile through a secret.

## Enabling pulled files to be checked in

To enable files to be checked into the repo, the `DEPLOY_KEY` secret has to be set after creating a deploy key.  A deploy key is simply an ssh key pair.  So, start by creating an ssh key pair.  Then go to `Settings` for the forked repository and add a deploy key.  The key you want to paste is the ssh public key that you created.  Put the ssh private key in the `DEPLOY_KEY` secret varible for the forked repository.
