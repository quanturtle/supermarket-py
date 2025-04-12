from os import path
from pprint import pprint
from typing import List, Dict
import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(data: List[Dict], **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'public'  # Specify the name of the schema to export data to
    table_name = 'product_urls'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    result = []
    
    for category in data:
        try:
            for product_links in category['product_links']:
                result.append(product_links)

        except:
            continue
    
    # clean dataframe from duplicates before inserting, drop links without description
    df = pd.DataFrame(result)
    df = df.dropna(subset=['description'])

    unique_descriptions = df['description'].unique()
    unique_urls = df['url'].unique()

    df = df.drop_duplicates(subset=['description', 'url'])
    
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
