# weather-triggered-commodity

This repo hosts files related to the weather-triggered-commodity front end project

## aemo_price_script

The aemo_price_script directory houses all of the necessary files to gather historical pricing data from AEMO from its start year (1998) to the current year.  The current year is chosen programatically, so if the data needs to be regenerated in the future, no changes to the script should need to be made.

### Running the script

Open the aemo_price_script directory in bash or an ide of your choice.  Initialize a python venv in the directory with
```
python3 -m venv venv
```
Then, activate the environment.  If on bash, this can be done with
```
activate venv/bin/activate
```
If using a windows cmd environment, the command to activate the environment it
```
./venv/scripts/activate.bat
```

Now install any needed dependencies with
```
pip install -r requirements.txt
```
The script relies on the python Requests library to make API calls to AEMO.  It also uses a personal package called easy_reed to help configure the http 'user-agent' header from a config file.  It shouldn't matter what this is set to, just that it is present, but if the web calls fail, you can find your user-agent by searching 'my user agent' on google.

now just run the script to generate the files.