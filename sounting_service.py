# // Implement a thread-safe counting service without any timestamp ordering assumption
# // Time bucket to aggregate count by.
# # enum Granularity {
#   SECOND, MINUTE, HOUR, DAY
# }
# interface CounterService {
#   // timestamp: epoch time in milliseconds 
#   // Record an event that occurred at a time t.
#   public void recordEvent(String event, long timestamp);
#   // start, end: epoch time in milliseconds
#   // Get an aggregate recorded event count for a time window
#   public long getEventCount(String event, long start, long end);
#   // start, end: epoch time in milliseconds
#   // Get an aggregate recorded event count for a time window broken out by         
#   // time granularity.
#   public long[] getEventCount(
#       String event, long start, long end, Granularity granularity);
#   }
# }
from enum import Enum
import datetime as dt
import time

class Granularity(Enum):
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4

def get_date_format(granularity):
    """
    Returns the respective date format based on granularity
    ignoring the unnecessary data.

    :param granularity Granularity:
    :returns str:
    """   
    if granularity == Granularity.SECOND:
        return "%Y-%m-%d %H:%M:%S"

    elif granularity == Granularity.MINUTE:
        return "%Y-%m-%d %H:%M"

    elif granularity == Granularity.HOUR:
        return "%Y-%m-%d %H"

    elif granularity == Granularity.DAY:
        return "%Y-%m-%d"

    else:
        raise Exception("Granularity not recognized")


def get_range(granularity, start, end):
    """
    Gets the delta between two datetimes and returns the value according to granularity

    :param granularity Granularity:
    :param start datetime:
    :param end datetime:
    :return int:
    """    
    if granularity == Granularity.SECOND:
        return (end-start).seconds+2

    elif granularity == Granularity.MINUTE:
        return (end-start).minures+2

    elif granularity == Granularity.HOUR:
        return (end-start).hours+2

    elif granularity == Granularity.DAY:
        return (end-start).days+2

    else:
        raise Exception("Granularity not recognized")


def get_delta(granularity, t):
    """
    Builds a timedelta according to granularity

    :param granulatiry Granularity:
    :param t int: A given time
    :return timedelta:
    """    
    if granularity == Granularity.SECOND:
        return dt.timedelta(seconds=t)

    elif granularity == Granularity.MINUTE:
        return dt.timedelta(minutes=t)

    elif granularity == Granularity.HOUR:
        return dt.timedelta(hours=t)

    elif granularity == Granularity.DAY:
        return dt.timedelta(days=t)

    else:
        raise Exception("Granularity not recognized")


class CounterService :

    def __init__(self):
        self.events = dict()
        self.events_second = dict()
        self.events_minute = dict()
        self.events_hour = dict()
        self.events_day = dict()
        
    def record_event(self, event, timestamp):
        """
        Record an event that occurred at a time t.

        :param event str: event to be recorded
        :param timestamp int: time when the event occurred
        """
        event_date = dt.datetime.fromtimestamp(timestamp)
        self.add_event(self.events, event, timestamp)
        self.add_event(self.events_day, event, event_date.strftime(get_date_format(Granularity.DAY)))
        self.add_event(self.events_hour, event, event_date.strftime(get_date_format(Granularity.HOUR)))
        self.add_event(self.events_minute, event, event_date.strftime(get_date_format(Granularity.MINUTE)))
        self.add_event(self.events_second, event, event_date.strftime(get_date_format(Granularity.SECOND)))

    def add_event(self, dict_obj, new_event, date):
        """
        Add event entry to dictionary if it is already created. Otherwise creates
        a new event entry and call add dict to calculate dates count.

        :param dict_obj dict:
        :param new_event str:
        :param date timestamp|datetime:
        """
        if new_event in dict_obj:
            dict_obj[new_event] = self.add_dict_count(dict_obj[new_event], date)
        else:
            dict_obj[new_event] = {date: 1}

    def add_dict_count(self, dict_obj, key):
        """
        Checks if key exist to increment count. Otherwise, creates an entry

        :param dict_obj dict:
        :param key str, int:

        :return dict_obj dict: dictionaty updated with the key count
        """
        if key in dict_obj:
            dict_obj[key] += 1
        else:
            dict_obj[key] = 1

        return dict_obj

    def get_event_count(self, event, start, end):
        """
        :param event str: event to get count
        :param start int: initial range timestamp for the time window
        :param end int: timestamp to indicate the end of the time window for counting
        :return int: number of events in a time frame
        """
        if event not in self.events:
            return 0

        acum = 0
        for t, value in self.events[event].items():
            if t >= start and t <= end:
                acum += value

        return acum

    def get_event_count_granularity(self, event, start, end, granularity):
        """
        Calls get_counts with the proper dictionary for the granularity in a time window

        :param event str: event to count
        :param start int: start of the time frame
        :param end int: end of the time frame
        :return list(int): number of events in a time frame with the specific granularity
        """
        if granularity == Granularity.SECOND:
            return self.get_counts(self.events_second, event, start, end, granularity)

        elif granularity == Granularity.MINUTE:
            return self.get_counts(self.events_minute, event, start, end, granularity)

        elif granularity == Granularity.HOUR:
            return self.get_counts(self.events_hour, event, start, end, granularity)

        elif granularity == Granularity.DAY:
            return self.get_counts(self.events_day, event, start, end, granularity)       

        else:
            raise Exception("Granularity not recognized")

    def get_counts(self, dict_obj, event, start, end, granularity):
        """
        Auxiliar method to append all dictionaries in time window

        :param dict_obj dict: dictionary with the events
        :param event str: event to count
        :param start timestamp: initial time window
        :param end timestamp: end of the time window
        :param granularity int: 
        :return list(): count per unity in granularity
        """
        if event not in dict_obj:
            return [] # should I return empty list if the event does not exist or raise an error?

        results = []
        event_dict = dict_obj[event] 
        date_format = get_date_format(granularity)
        start = dt.datetime.fromtimestamp(start)
        end = dt.datetime.fromtimestamp(end)

        for current_date in self.daterange(granularity, start, end):
            # converts current timestamps to datetime in the format according to granularity
            current_date = current_date.strftime(date_format)
            if current_date in event_dict:
                results.append({current_date: event_dict[current_date]})

        return results

    def daterange(self, granularity, start, end):
        """
        Yields a datetime in range from a start to end

        :param granularity Granularity:
        :param start datetime:
        :param end datetime:
        :yield datetime:
        """
        for t in range(get_range(granularity, start, end)):
            yield start + get_delta(granularity, t)


start = dt.datetime.now().timestamp()
cs = CounterService()
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("register_user", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime(2021, 2, 14, 23, 49, 50).timestamp())
cs.record_event("log", dt.datetime(2021, 2, 14, 23, 49, 50).timestamp())
cs.record_event("log", dt.datetime(2021, 2, 14, 23, 49, 50).timestamp())
cs.record_event("log", dt.datetime(2021, 2, 14, 23, 49, 50).timestamp())
cs.record_event("log", dt.datetime(2021, 2, 14, 23, 49, 50).timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
cs.record_event("log", dt.datetime.now().timestamp())
print("Second " + str(cs.events_second))
print("Minute " + str(cs.events_minute))
print("Hour " + str(cs.events_hour))
print("Day " + str(cs.events_day))
# time.sleep(5)
end = dt.datetime(2021, 2, 15, 23, 49, 50).timestamp()
print(str(cs.get_event_count("log", start, end)))
print(str(cs.get_event_count_granularity("log", start, end, Granularity.DAY)))
