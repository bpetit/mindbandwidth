#!/usr/bin/env python3

import caldav
import click
import icalendar
import requests
from pprint import pprint

def download_file(url, filename=None):
    local_filename = filename if filename else url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

# Multiple caldav input url to check mismatches between tasks and meetings to schedule.
# One caldav url output to schedule tasks.
@click.command()
@click.option('--ical-share-url')
@click.option('--caldav-input-url', '-i')
@click.option('--caldav-input-username', '-u')
@click.option('--caldav-input-password', '-p')
@click.option('--caldav-output-url', '-o')
@click.option('--tasks-input-csv')
@click.option('--start-date')
@click.option('--stop-date')
@click.option('--events-input-csv')
@click.option('--events-output-csv')
@click.option('--limit', '-l')
@click.option('--warn-on-congestion', '-w', default=True, show_default=True)
@click.option('--prevent-congestion', default=True, show_default=True)
@click.option('--deep-work-max-minutes', '-m', default=25, show_default=True)
@click.option('--temp-ical-filename', default="calendar.ics", show_default=True)
def main(caldav_input_url, ical_share_url, caldav_input_username, caldav_input_password,
            caldav_output_url, tasks_input_csv, start_date, stop_date,
            events_input_csv, events_output_csv, limit, warn_on_congestion,
            prevent_congestion, deep_work_max_minutes, temp_ical_filename
    ):
    if caldav_input_url and len(caldav_input_url) > 0:
        print("Scanning events from caldav input url: {}\n".format(caldav_input_url))
        with caldav.DAVClient(
            url=caldav_input_url,
            username=caldav_input_username if caldav_input_username else "",
            password=caldav_input_password if caldav_input_password else ""
        ) as client:
            calendar = client.calendar(url=caldav_input_url)
            pprint(calendar.events())

    if ical_share_url and len(ical_share_url) > 0:
        print("Collecting events from ical shared url: {}".format(ical_share_url))
        download_file(ical_share_url, temp_ical_filename)
        with open(temp_ical_filename) as f:
            calendar = icalendar.Calendar.from_ical(f.read())
            for event in calendar.walk('VEVENT'):
                print(event.get("SUMMARY"))

    if caldav_output_url is not None and len(caldav_output_url) > 0:
        print("caldav output url: {}".format(caldav_output_url))
    if tasks_input_csv is not None and len(tasks_input_csv) > 0:
        print("tasks input csv: {}".format(tasks_input_csv))

if __name__ == '__main__':
    main()
