# Add bash script to push redacted files into this repository, which will likely live under a netfile_redacted directory

echo "Pushing netfile_redacted to repo"
ls netfile_redacted

git status
git add netfile_redacted
git commit -a -m "netfile update"
git push
