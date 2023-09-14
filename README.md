# netfile_redacted

This repo allows someone to develop the code for pulling NetFile data.  The code for pulling files are run on a schedule using a GitHub Action workflow and the workflow can be run manually. When the GitHub workflow runs under ChenglimEar, the NetFile pull will be simulated using files in netfile_samples.  To enable the workflow to call the NetFile API, this repository has to be forked to a different organization/owner.  It will require an authorized user to update the fork with appropriate credentials for accessing NetFile, which will have to be added as a secret in the forked repository.

## TODO

* Add code for redacting raw NetFile data (make it configurable)
* Make sure code that calls NetFile API works when credentials are provided and puts files in the right place
