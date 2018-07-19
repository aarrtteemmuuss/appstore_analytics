import click
import os
from reporter import Reporter


@click.group()
def main():
    pass


@click.command()
@click.confirmation_option(prompt='This will delete your old token. Do you want to proceed?')
def generate_token():
    reporter = Reporter()
    click.echo(reporter.asc_generate_token())


@click.command(name='ViewToken')
def view_token():
    reporter = Reporter()
    click.echo(reporter.asc_view_token())


@click.command(name='DeleteToken')
@click.confirmation_option(prompt='This will delete your token. Do you want to proceed?')
def delete_token():
    reporter = Reporter()
    click.echo(reporter.asc_delete_token())


@click.command(name='GetAccounts')
@click.option('--service', type=click.Choice(['Sales', 'Finance']), prompt=True)
def get_accounts(service):
    reporter = Reporter()
    click.echo(reporter.asc_get_accounts(service))


@click.command(name='GetStatus')
@click.option('--service', type=click.Choice(['Sales', 'Finance']), prompt=True)
def get_status(service):
    reporter = Reporter()
    click.echo(reporter.asc_get_status(service))


@click.command(name='GetVendors')
@click.option('--account', prompt=True)
def get_vendors(account):
    reporter = Reporter()
    click.echo(reporter.asc_get_vendors(account))


@click.command(name='GetReportType')
@click.option('--report_type', type=click.Choice(['Sales', 'Subscription', 'SubscriptionEvent', 'Subscriber', 'Newsstand', 'Pre-Order']), prompt=True)
@click.option('--report_subtype', type=click.Choice(['Summary', 'Detailed', 'Opt-In']), prompt=True)
def get_report_version(report_type, report_subtype):
    reporter = Reporter()
    click.echo(reporter.asc_get_report_version(report_type, report_subtype))


@click.command()
@click.option('--account', prompt=True)
@click.option('--service', type=click.Choice(['Sales', 'Finance']), prompt=True)
def get_vendor_and_regions(account, service):
    reporter = Reporter()
    click.echo(reporter.asc_get_vendor_and_regions(account, service))


@click.command()
@click.option('--account', prompt=True)
@click.option('--vendor', prompt=True)
@click.option('--date_type', type=click.Choice(['Yearly', 'Monthly', 'Weekly', 'Daily']), prompt=True)
@click.option('--date', prompt=True)
@click.option('--path', default=os.getcwd(), prompt=True)
def get_sales_report(account, vendor, date_type, date, path):
    reporter = Reporter()
    try:
        result = reporter.asc_get_sales_report(account, vendor, date_type, date)
        filename = result.headers['filename']
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(result.content)
        click.echo('Report saved to {}'.format(os.path.join(path, filename)))
    except Exception as exc:
        click.echo(str(exc))


@click.command()
@click.option('--account', prompt=True)
@click.option('--vendor', prompt=True)
@click.option('--region', prompt=True)
@click.option('--fiscal_year', prompt=True)
@click.option('--fiscal_period', prompt=True)
@click.option('--path', default=os.getcwd(), prompt=True)
def get_financial_report(account, vendor, region, fiscal_year, fiscal_period, path):
    reporter = Reporter()
    try:
        result = reporter.asc_get_financial_report(account, vendor, region, fiscal_year, fiscal_period)
        filename = result.headers['filename']
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(result.content)
        click.echo('Report saved to {}'.format(os.path.join(path, filename)))
    except Exception as exc:
        click.echo(str(exc))


main.add_command(generate_token)
main.add_command(view_token)
main.add_command(delete_token)
main.add_command(get_accounts)
main.add_command(get_vendors)
main.add_command(get_status)
main.add_command(get_vendor_and_regions)
main.add_command(get_sales_report)
main.add_command(get_report_version)
main.add_command(get_financial_report)


if __name__ == "__main__":
    main()
