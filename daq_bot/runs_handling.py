import daq_bot
import datetime
import utilix
import pytz
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')
log = logging.getLogger()

run_col = utilix.rundb.xent_collection()


def get_runs(start, stop=None, detectors='tpc'):
    if stop is None:
        stop = start + datetime.timedelta(days=10000)
    query = {'start': {'$gt': start, "$lt": stop}}
    if detectors:
        query.update({'detectors': detectors})
    log.debug(f'Querying {query}')
    runs = [f"{r['number']:06}" for r in run_col.find(query,
                                                      projection={'number': 1})]
    runs.sort()
    log.debug(f'Found {runs} between {start} and {stop}')
    return runs

def get_time_intervals(dt_hours):
    dt = datetime.datetime.now(pytz.utc)
    dt = datetime.datetime(dt.year, dt.month, dt.day)
    interval = [dt, dt + datetime.timedelta(hours=dt_hours)]
    log.debug(f'Requested interval is {interval}')
    return interval