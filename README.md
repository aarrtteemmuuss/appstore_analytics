# Appstore (Itunes) Analytics Tool
### Pure Python version of Apple Reporter Tool 

This is the alternative to official Apple Reporter tool written in Java. This tool is
very easy to use and can be integrated with other projects with no need to provide
Java dependecy and external calls to Java installation. 

### Requirements
Requires python3 to be installed in your system

### Install
TBD (it will support installation through pip install soon)

### Usage
There is a config file `config.yaml` in the root directory of the project. 
Enter your `email` and `password`. You can also enter your `token` if you already
have it, or you can use command `generate_token` to create new one.
```
python reporter_cli.py <command>
```
When you enter the command from list of supported commands, you will be prompted to 
enter all the required parameters. You will see the response in the console window 
or in case or reports, report will be downloaded to the path specified.

### Available commands
* ViewToken - get information about current token. 
Response format:
```
{'access_token': 'token', 'expiration_date': '2019-01-01'}
```

* GetStatus - get reports availability. Required params: `service`, available options
are: `Sales` and `Finance`. Response format:
```
{'code': '0', 'message': 'Sales and Trends Reporter is currently available.'}
```

* GenerateToken - generate new token. This command will override current token from 
`config.yaml`. You will be prompted to confirm this operation before it will be
completed.

* DeleteToken - delete current token. You will be prompted to confirm this operation before it will be
completed.

* GetAccounts - get available account numbers. Required parameters: `service`, available
options are `Sales` and `Finance`. 

* GetVendors - get available vendor numbers for selected account. Required parameters:
`account`, you will be prompted to enter account number. 

* GetReportVersion - get latest report version for selected report type. Required params are:
`report_type` and `report_subtype`, available options for `report_type` are: 
`Sales`, `Subscription`, `SubscriptionEvent`, `Subscriber`, `Newsstand`, `Pre-Order`; for 
`report_subtype`: `Summary`, `Detailed`, `Opt-In`. Response format:
```
{'message': 'The latest version of the sales (summary) report is 1_0.'}
```

* GetVendorsAndRegions - get vendors and regions for generating finance report. 
Required params are: `account` and `service`. Available options for `service` are:
`Sales` and `Finance`.

* GetSalesReport - generate and download sales report. Required params are: 
`account` - account number, `vendor` - vendor number, `date_type` - date type (available options:
`Daily`, `Weekly`, `Monthly`, `Yearly`), `date` - date (supported format: `YYYYMMDD` for `Daily`,
`YYYYMMDD` for `Weekly` (enter last day of the week), `YYYYMM` for `Monthly` and `YYYY` for `Yearly`) 
and `path` - where to save the report (by default it will save to the current working directory)

* GetFinanceReport - generate and download sales report. Required params are: 
`account` - account number, `vendor` - vendor number, `fiscal_year` - Apple fiscal year, format: `YYYY`, 
`fiscal_period` - Apple fiscal month, format: `MM` and `path` - where to save the report (by default it will save to the current working directory)

* More options will be added soon...