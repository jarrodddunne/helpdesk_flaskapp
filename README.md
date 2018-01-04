# Rice OIT HelpDesk Kiosk
## A Flask App Designed to simplify submission of Walk-In Tickets and Printing Refunds at Rice's Office of Information Technology HelpDesk
### Built by Jarrod Dunne
## Setup
Note: Requires python2 for `python-rtkit`
See `requirements.txt` for list of packages that needs to be installed.
Add a `credentials.txt` file in the root directory, with the first line being the username, second line password, for the RT system.

Export the `FLASK_APP` environment variable with:
```
$> export FLASK_APP=rt.py
```
Then run flask with:
```
$> flask run
```
Go to `127.0.0.1:5000/walkin` for the walk-in kisok, or `127.0.0.1:5000/print_refund` for the printing refund.