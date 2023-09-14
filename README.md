# netfile_redacted

This repo allows someone to develop the code for pulling NetFile data.  The code for pulling files are run on a schedule using a GitHub Action workflow and the workflow can be run manually. 

## Enabling NetFile Access

When the GitHub workflow runs under ChenglimEar, the NetFile pull will be simulated using files in netfile_samples.  To enable the workflow to call the NetFile API, this repository has to be forked to a different organization/owner.  It will require an authorized user to update the fork with appropriate credentials for accessing NetFile, which will have to be added as a secret in the forked repository.  In other words, these two secret variables have to be set up in the forked repository:

* NETFILE_API_KEY
* NETFILE_API_SECRET

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

* Add code for redacting raw NetFile data (make it configurable)
* Make sure code that calls NetFile API works when credentials are provided and puts files in the right place
