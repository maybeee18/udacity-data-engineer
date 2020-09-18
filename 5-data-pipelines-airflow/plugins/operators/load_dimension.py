from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_query = "",
                 truncate = False,
                 table_name = "",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.table_name = table_name
        self.truncate = truncate

    def execute(self, context):
        """
        Inserts data into dimensional tables from staging tables.
        Support append or delete insertion modes.
        """

        redshift_hook = PostgresHook(postgres_conn_id = self.redshift_conn_id)

        if self.truncate:
            redshift_hook.run(f"truncate table {self.table_name}")

        self.log.info(f'Loading data into dimensional table {self.table_name} ...')
        redshift_hook.run(self.sql_query)
        self.log.info(f'Loading data into dimensional table {self.table_name} complete')
