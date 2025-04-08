from typing import Dict, List
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(users: List[Dict], **kwargs):
    print(users)