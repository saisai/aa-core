import logging
import unittest
from datetime import datetime, timedelta, timezone

from nose.tools import assert_equal, assert_dict_equal, assert_raises, assert_list_equal

from .context.aw_core.models import Event
from .context.aw_core.transforms import chunk, filter_period_intersect, include_labels, exclude_labels


class ChunkTest(unittest.TestCase):
    # Tests the chunk transform

    def test_chunk(self):
        eventcount = 10
        events = []
        for i in range(eventcount):
            events.append(Event(label=["test", "test2"],
                                timestamp=datetime.now(timezone.utc) + timedelta(seconds=i),
                                duration=timedelta(seconds=1)))
        res = chunk(events)
        logging.debug(res)
        assert_equal(res['eventcount'], eventcount)
        assert_dict_equal(res['duration'], {"value": eventcount, "unit": "s"})
        assert_list_equal(res['chunks']['test']['other_labels'], ["test2"])
        assert_list_equal(res['chunks']['test2']['other_labels'], ["test"])
        assert_dict_equal(res['chunks']['test']['duration'], {"value": eventcount, "unit": "s"})
        assert_dict_equal(res['chunks']['test2']['duration'], {"value": eventcount, "unit": "s"})


class IncludeLabelsTest(unittest.TestCase):
    def test_include_labels(self):
        labels = ["a","c"]
        events = [
            Event(label=["a"]),
            Event(label=["b"]),
            Event(label=["c"]),
        ]
        included_labels = include_labels(events, labels)
        excluded_labels = exclude_labels(events, labels)
        assert_equal(len(included_labels), 2)
        assert_equal(len(excluded_labels), 1)


class FilterPeriodIntersectTest(unittest.TestCase):
    def test_filter_period_intersect(self):
        td1h = timedelta(hours=1)
        td30min = timedelta(minutes=30)
        now = datetime.now()

        # Filter 1h event with another 1h event at a 30min offset
        to_filter = [Event(label="lala", timestamp=now, duration=td1h)]
        filter_with = [Event(timestamp=now + timedelta(minutes=30), duration=td1h)]
        filtered_events = filter_period_intersect(to_filter, filter_with)
        assert_equal(filtered_events[0].duration, timedelta(minutes=30))

        # Filter 2x 30min events with a 15min gap with another 45min event in between intersecting both
        to_filter = [
            Event(label="lala", timestamp=now, duration=td30min),
            Event(label="lala", timestamp=now + timedelta(minutes=45), duration=td30min)
        ]
        filter_with = [Event(timestamp=now + timedelta(minutes=15), duration=timedelta(minutes=45))]
        filtered_events = filter_period_intersect(to_filter, filter_with)
        assert_equal(filtered_events[0].duration, timedelta(minutes=15))
        assert_equal(filtered_events[1].duration, timedelta(minutes=15))
