from django_pandas.io import read_frame

from .models import Experiment, Sample, Dna, Construct, Vector, Measurement

def make_search(params):
    qs = Measurement.objects.filter(name='OD', sample_id=156)
    df = read_frame(qs)

    json_df = df.to_json()
    return json_df
