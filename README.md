# netfile_redacted

This repo allows someone to develop the code for pulling NetFile data.  The code for pulling files are run on a schedule using GitHub Actcions.  When the GitHub workflow runs under ChenglimEar, the NetFile pull will be simulated using files in netfile_samples.  To enable the workflow to call the NetFile API, this repository has to be forked to a different organization/owner.  It will require an authorized user to update the fork with appropriate credentials for accessing NetFile, which will have to be added as a secret in the forked repository.

## GitHub Action

The GitHub Action associated with this repo runs on a schedule and can be run manually also.  When a fork is created, the workflow will require setup to allow it to check pulled Netfile files to be checked in to the repo.

### Enabling pulled NetFile files to be checked in by GitHub Action workflow

To enable files to be checked into the repo by the GitHub Action workflow, the `DEPLOY_KEY` secret has to be set after creating a deploy key.  A deploy key is simply an ssh key pair.  So, start by creating an ssh key pair.  Then go to `Settings` for the forked repository and add a deploy key.  The key you want to paste is the ssh public key that you created.  Put the ssh private key in the `DEPLOY_KEY` secret varible for the forked repository.

## TODO

* Add code for redacting raw NetFile data (make it configurable)
* Make sure code that calls NetFile API works when credentials are provided and puts files in the right place
