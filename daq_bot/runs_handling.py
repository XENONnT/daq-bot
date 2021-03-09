import daq_bot
import datetime
import utilix
import pytz
import logging
import typing

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')
log = logging.getLogger()

run_col = utilix.rundb.xent_collection()


def get_runs(start: datetime.datetime,
             stop: typing.Optional[datetime.datetime]=None,
             detectors: str='tpc')->typing.List[str]:
    """Get all the runs at least partially contained in the interval start-stop"""
    if stop is None:
        stop = start + datetime.timedelta(days=10000)

    # Should query runs that are partially within the start, stop:
    # Run interval |1----|2----|3----|4----|
    # start stop      |------------|
    # Query will return runs interval 1,2,3.
    query = {"$or": [{"end": None},
                     {'end': {'$gt': start}}],
             "start": {"$lt": stop}}
    if detectors:
        query.update({'detectors': detectors})
    log.debug(f'Querying {query}')
    runs = [f"{r['number']:06}" for r in run_col.find(query,
                                                      projection={'number': 1})]
    # Make sure the runs are sorted before returning
    runs.sort()
    log.debug(f'Found {runs} between {start} and {stop}')
    return runs


def get_time_intervals(
        dt_hours: typing.Union[int, float]) -> typing.List[datetime.datetime]:
    """Starting from midnight, get a time interval spanning dt_hours"""
    dt = datetime.datetime.now(pytz.utc)
    dt = datetime.datetime(dt.year, dt.month, dt.day)
    interval = [dt, dt + datetime.timedelta(hours=dt_hours)]
    log.debug(f'Requested interval is {interval}')
    return interval
