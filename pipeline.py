import apache_beam as beam
from apache_beam.transforms.window import (
    TimestampedValue,
    Sessions,
    Duration
)
from apache_beam.io.textio import WriteToText


class AddTimeStampDoFn(beam.DoFn):
    """Adding timestamp for window function"""
    def process(self, element):
        unix_timestamp = element["timestamp"]
        element = (element["userId"], element["click"])
        yield TimestampedValue(element, unix_timestamp)

with beam.Pipeline() as p:
    events = p | beam.Create(
        [ 
            {'userId': "Andy", "click": 1, "timestamp": 1603112520}, # Event time: 13:02
            {'userId': "Andy", "click": 1, "timestamp": 1603113240}, # Event time: 13:14
            {'userId': "Andy", "click": 1, "timestamp": 1603115820}, # Event time: 13:57
            {'userId': "Andy", "click": 1, "timestamp": 1603113600}, # Event time: 13:20
        ]
    )

    timestamped_events = events | beam.ParDo(AddTimeStampDoFn())
    window_events = timestamped_events | beam.WindowInto(Sessions(gap_size=30*60))
    sum_clicks = window_events | beam.CombinePerKey(sum)
    sum_clicks | WriteToText(file_path_prefix="output")
