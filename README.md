# netfile_redacted

This repo allows someone to develop the code for pulling NetFile data.  The code for pulling files are run on a schedule using a GitHub Action workflow and the workflow can be run manually. 

## Enabling NetFile Access

When the GitHub workflow runs under ChenglimEar or without credentials on a local machine, the NetFile pull will be simulated using files in netfile_samples.  To enable the workflow to call the NetFile API, this repository has to be forked to a different organization/owner.  It will require an authorized user to update the fork with appropriate credentials for accessing NetFile, which will have to be added as a secret in the forked repository.  In other words, these two secret variables have to be set up in the forked repository:

* NETFILE_API_KEY
* NETFILE_API_SECRET

## Enabling Google Drive Upload

The GitHub workflow has the ability to upload redacted files in netfile_redacted to Google Drive.  To enable this, the following has to be done:

    1. A service account has to be created in a project with access to the Google Drive API.
       It's probably best to create a GCP project specifically just for access to the 
       Google Drive API and create the service account in that project.  
    2. The directory on Google Drive has to be shared with the service account.  This is
       done by getting the e-mail of the service account and sharing with that e-mail 
       instead of a real person's e-mail.
    3. A private key (in JSON) has to be created for the service account.  The private key 
       should be placed in an environment variable, SERVICE_ACCOUNT_KEY_JSON.  For
       GitHub Actions, we can simply get the value from a secret of the same name.

If SERVICE_ACCOUNT_KEY_JSON is not set, the redacted files will be copied to the repository.

A test for downloading the redacted files to a download directory is run when the workflow runs on ChenglimEar.

The upload and download can be tested locally by naming the key file as `.local/SERVICE_ACCOUNT_KEY_JSON.json`.  The `.local` directory is in the `.gitignore` file, so the file won't be checked in accidentally.

## Redaction Configuration

To add new redactions or modify an existing one, simply modify the `config.yaml` file, which contains a list of paths to all the fields to redact for each type of data.

For example, suppose we want to redact `line1` in the address list for a simplified filer entry like this:

```json
[
  {
    "filerNid": "123",
    "candidateName": "Smith, John",
    "addressList": [
      {
        "addressTypes": "Disclosure, Mailing",
        "line1": "210 Broadway",
        "line2": "",
        "city": "Oakland",
        "state": "CA",
        "zip": "90000"
      }
    ],
  }
]
```

The `config.yaml` file should have an entry like this:

```yaml
redaction_fields:
  filers:
  - addressList.[].line1
```

Notice the use of `[]` to indicate that all elements of the address list should be redacted by replacing the value in `line1` with `***`.  In other words, if we have more than one address listed, the `line1` field of all the addresses will be redacted.

The redacted file will look like this:

```json
[
  {
    "filerNid": "123",
    "candidateName": "Smith, John",
    "addressList": [
      {
        "addressTypes": "Disclosure, Mailing",
        "line1": "***",
        "line2": "",
        "city": "Oakland",
        "state": "CA",
        "zip": "90000"
      }
    ],
  }
]
```


## TODO

* Make sure code that calls NetFile API works when credentials are provided and puts files in the right place
