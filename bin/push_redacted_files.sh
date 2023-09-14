# Add bash script to push redacted files into this repository, which will likely live under a netfile_redacted directory

echo "Pushing netfile_redacted to repo"
ls

echo "Adding to repo using git"
git status
git branch
git add netfile_redacted
git config --global user.name 'OpenDisclosure Deploybot'
git config --global user.email 'open-disclosure@gmail.com'
git status
echo "Committing"
git commit -m "netfile update"
#git push
