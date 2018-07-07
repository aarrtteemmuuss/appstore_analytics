import json
import yaml
import requests
import xml.etree.ElementTree as ET

VERSION = '2.2'
ENDPOINT_SALES = 'https://reportingitc-reporter.apple.com/reportservice/sales/v1'
ENDPOINT_FINANCE = 'https://reportingitc-reporter.apple.com/reportservice/finance/v1'
CONFIG_LOCATION = 'config.yaml'


class Reporter:
    def __init__(self):
        self.config = self.load_config()
        self.email = self.config['email']
        self.password = self.config['password']
        self.mode = self.config['mode']
        self.token = self.config['token']

        self.request_payload = dict(
                userid=self.email,
                mode=self.mode,
                version=VERSION,
            )

    def load_config(self):
        config = yaml.load(open(CONFIG_LOCATION))
        if not config['token']:
            print("You don't have token. Please generate it first.")
        return config

    def build_json_query(self, command, params, url_params):
        self.request_payload['queryInput'] = command
        if params:
            self.request_payload.update(params)
        query = dict(jsonRequest=json.dumps(self.request_payload))
        if url_params:
            query.update(url_params)
        return query

    def post_request(self, endpoint, command, params=None, url_params=None):
        command = "[p=Reporter.properties, %s]" % command
        request_data = self.build_json_query(command, params, url_params)

        r = requests.post(endpoint, data=request_data)

        if r.status_code == 200:
            return r
        else:
            et = ET.fromstring(r.text)
            code = et.find('Code').text
            message = et.find('Message').text
            raise Exception(
                "Got error from reporter: {}, {}".format(code, message))

    def asc_generate_token(self):
        command = 'Sales.generateToken'

        params = dict(
            password=self.password
        )

        r = self.post_request(ENDPOINT_SALES, command, params)
        service_request_id = r.headers['service_request_id']

        try:
            result = self.post_request(
                ENDPOINT_SALES,
                command,
                url_params=dict(isExistingToken='Y',
                                requestId=service_request_id))

            et = ET.fromstring(result.text)
            token_tag = et.find('AccessToken')
            expiration_tag = et.find('ExpirationDate')

            self.config['token'] = token_tag.text
            with open(CONFIG_LOCATION, 'w') as f:
                yaml.dump(self.config, f,
                          allow_unicode=True,
                          default_flow_style=False)

            return dict(access_token=token_tag.text,
                        expiration_date=expiration_tag.text)

        except Exception as exc:
            return str(exc)

    def asc_view_token(self):
        command = 'Sales.viewToken'

        params = dict(
            password=self.password
        )
        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            et = ET.fromstring(result.text)
            token_tag = et.find('AccessToken')
            expiration_tag = et.find('ExpirationDate')
            return dict(access_token=token_tag.text,
                        expiration_date=expiration_tag.text)
        except Exception as exc:
            return str(exc)

    def asc_delete_token(self):
        command = 'Sales.deleteToken'

        params = dict(
            password=self.password
        )
        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            et = ET.fromstring(result.text)
            message_tag = et.find('Message')
            return dict(message=message_tag.text)
        except Exception as exc:
            return str(exc)

    def asc_get_accounts(self, service):
        command = service + '.getAccounts'

        params = dict(
            accesstoken=self.token
        )

        endpoint = ENDPOINT_SALES if service == 'Sales' else ENDPOINT_FINANCE
        try:
            result = self.post_request(endpoint, command, params=params)
            et = ET.fromstring(result.text)
            accounts = []
            for account in et.findall('Account'):
                accounts.append(dict(
                    name=account.find('Name').text,
                    number=account.find('Number').text
                ))
            return accounts
        except Exception as exc:
            return str(exc)

    def asc_get_vendors(self, account):
        command = 'Sales.getVendors'

        params = dict(
            account=account,
            accesstoken=self.token
        )

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            et = ET.fromstring(result.text)
            vendors = []
            for vendor in et.findall('Vendor'):
                vendors.append(vendor.text)
            return vendors
        except Exception as exc:
            return str(exc)

    def asc_get_sales_report(self, account, vendor, datetype, date):

        command = 'Sales.getReport, {0},Sales,Summary,{1},{2}'.format(
            vendor,
            datetype,
            date)

        params = dict(
            account=account,
            accesstoken=self.token
        )

        result = self.post_request(ENDPOINT_SALES, command, params=params)
        return result

    def asc_get_status(self, service):
        params = dict(
            accesstoken=self.token
        )

        command = service + '.getStatus'
        endpoint = ENDPOINT_SALES if service == 'Sales' else ENDPOINT_FINANCE
        try:
            result = self.post_request(endpoint, command, params=params)
            et = ET.fromstring(result.text)
            status = dict(
                code=et.find('Code').text,
                message=et.find('Message').text
            )
            return status
        except Exception as exc:
            return str(exc)

    def asc_get_vendor_and_regions(self, account, vendor):
        command = 'Finance.getVendorsAndRegions'

        params = dict(
            accesstoken=self.token,
            account=account,
            vendor=vendor
        )
        try:
            result = self.post_request(ENDPOINT_FINANCE, command, params=params)
            et = ET.fromstring(result.text)
            vendors_regions = dict(number=et.find('./Vendor/Number').text,
                                   regions=[])
            regions = et.findall('./Vendor/Region')
            for region in regions:
                vendors_regions['regions'].append(region.find('Code').text)
            return vendors_regions
        except Exception as exc:
            return str(exc)

    def asc_get_report_version(self, report_type, report_subtype):
        command = 'Sales.getReportVersion, {0},{1}'.format(report_type,
                                                           report_subtype)

        params = dict(
            accesstoken=self.token
        )

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            et = ET.fromstring(result.text)
            message_tag = et.find('Message')
            return dict(message=message_tag.text)
        except Exception as exc:
            return str(exc)

    # NOT ENABLED YET BELOW

    def asc_get_financial_report(self, vendor, region, fiscal_year, fiscal_period):
        command = 'Finance.getReport, {0},{1},Financial,{2},{3}'.format(vendor,
                                                                        region,
                                                                        fiscal_year,
                                                                        fiscal_period)
        params = dict(
            accesstoken=self.token
        )

        try:
            result = self.post_request(ENDPOINT_FINANCE, command, params=params)
            return result.text
        except Exception as exc:
            return str(exc)

    def asc_get_subscription_report(self, vendor, date, version):
        command = 'Sales.getReport, {0},Subscription,Summary,Daily,{1},{2}'.format(
            vendor, date, version)

        params = dict()

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            return result.text
        except Exception as exc:
            return str(exc)

    def asc_get_subscription_event_report(self, vendor, date, version):
        command = 'Sales.getReport, {0},SubscriptionEvent,Summary,Daily,{1},{2}'.format(
            vendor, date, version)

        params = dict()

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            return result.text
        except Exception as exc:
            return str(exc)

    def asc_get_subscriber_report(self, vendor, date, version):
        command = 'Sales.getReport, {0},Subscriber,Detailed,Daily,{1},{2}'.format(
            vendor, date, version)

        params = dict()

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            return result.text
        except Exception as exc:
            return str(exc)

    def asc_get_newsstand_report(self, vendor, date_type, date):
        command = 'Sales.getReport, {0},Newsstand,Detailed,{1},{2}'.format(
            vendor, date_type, date)

        params = dict()

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            return result.text
        except Exception as exc:
            return str(exc)

    def asc_get_opt_in_report(self, vendor, date):
        command = 'Sales.getReport, {0},Sales,Opt-In,Weekly,{1}'.format(vendor,
                                                                        date)

        params = dict()

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            return result.text
        except Exception as exc:
            return str(exc)

    def asc_get_pre_order_report(self, vendor, date_type, date):
        command = 'Sales.getReport, {0},Pre-Order,Summary,{1},{2}'.format(
            vendor, date_type, date)

        params = dict()

        try:
            result = self.post_request(ENDPOINT_SALES, command, params=params)
            return result.text
        except Exception as exc:
            return str(exc)
