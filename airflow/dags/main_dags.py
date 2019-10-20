from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.capstone_plugin import (StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
from sub_dags import load_dimensional_tables_dag

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'ckatba',
    'start_date': datetime(2019, 9, 19),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    # 'retry_delay': timedelta(seconds=300),
    'catchup': False,
    'email_on_retry': False
}

start_date = datetime.utcnow()

dag_name='Udacity_Capstone_dag'
dag = DAG(dag_name,
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          max_active_runs=3
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


stage_tables_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table="events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstone-s3-bucket",
    s3_key="capstone_data",
    region="us-east-2",
    file_format="CSV",
    # json_path="s3://udacity-dend/log_json_path.json",
    execution_date=start_date
    
)

stage_Home_Values_to_redshift = StageToRedshiftOperator(
    task_id='Stage_Home_Values',
    dag=dag,
    provide_context=True,
    table="Home_Values",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstone-s3-bucket",
    s3_key="capstone_data",
    region="us-west-2",
    data_format="CSV",
    execution_date=start_date
)

stage_Rental_Values_to_redshift = StageToRedshiftOperator(
    task_id='Stage_Rental_Values',
    dag=dag,
    provide_context=True,
    table="Rental_Values",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstone-s3-bucket",
    s3_key="capstone_data",
    region="us-west-2",
    data_format="CSV",
    execution_date=start_date
)

stage_Demographics_to_redshift = StageToRedshiftOperator(
    task_id='Stage_Demographics',
    dag=dag,
    provide_context=True,
    table="Demographics",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="capstone-s3-bucket",
    s3_key="capstone_data",
    region="us-west-2",
    data_format="CSV",
    execution_date=start_date
)


load_City_Housing_Demographics_table = LoadFactOperator(
    task_id='Load_City_Housing_Demographics_fact_table',
    dag=dag,
    provide_context=True,
    aws_credentials_id="aws_credentials",
    redshift_conn_id='redshift',
    sql_query=SqlQueries.City_Housing_Demographics_table_insert
)


load_City_Housing_Costs_dimension_table_task_id='Load_City_Housing_Costs_dim_table'
load_City_Housing_Costs_dimension_table = SubDagOperator(
    subdag=load_dimensional_tables_dag(
        parent_dag_name=dag_name,
        task_id=load_City_Housing_Costs_dimension_table_task_id,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        start_date= datetime(2019, 9, 19),
        table="City_Housing_Costs",
        sql_query=SqlQueries.City_Housing_Costs_table_insert,
    ),
    task_id=load_City_Housing_Costs_dimension_table_task_id,
    dag=dag,
)


# load_song_dimension_table_task_id='Load_song_dim_table'
# load_song_dimension_table = SubDagOperator(
#     subdag=load_dimensional_tables_dag(
#         parent_dag_name=dag_name,
#         task_id=load_song_dimension_table_task_id,
#         redshift_conn_id="redshift",
#         aws_credentials_id="aws_credentials",
#         start_date= datetime(2019, 9, 19),
#         table="song_s",
#         sql_query=SqlQueries.song_table_insert,
#     ),
#     task_id=load_song_dimension_table_task_id,
#     dag=dag,
# )

# load_artist_dimension_table_task_id='Load_artist_dim_table'
# load_artist_dimension_table = SubDagOperator(
#     subdag=load_dimensional_tables_dag(
#         parent_dag_name=dag_name,
#         task_id=load_artist_dimension_table_task_id,
#         redshift_conn_id="redshift",
#         aws_credentials_id="aws_credentials",
#         table="artists",
#         start_date= datetime(2019, 9, 19),
#         sql_query=SqlQueries.artist_table_insert,
#     ),
#     task_id=load_artist_dimension_table_task_id,
#     dag=dag,
# )

# load_time_dimension_table_task_id='Load_time_dim_table'
# load_time_dimension_table = SubDagOperator(
#     subdag=load_dimensional_tables_dag(
#         parent_dag_name=dag_name,
#         task_id=load_time_dimension_table_task_id,
#         redshift_conn_id="redshift",
#         aws_credentials_id="aws_credentials",
#         table="time",
#         start_date= datetime(2019, 9, 19),
#         sql_query=SqlQueries.time_table_insert,
#     ),
#     task_id=load_time_dimension_table_task_id,
#     dag=dag,
# )

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag
)
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    provide_context=True,
    aws_credentials_id="aws_credentials",
    redshift_conn_id='redshift',
    tables=["Home_Values", "Rental_Values", "Demographics",
     "City_Housing_Costs", "City_Housing_Demographics"]
)
end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Setting tasks dependencies
# Step 1
# start_operator >> stage_events_to_redshift
# start_operator >> stage_songs_to_redshift
start_operator >>\
 [stage_Home_Values_to_redshift, stage_Rental_Values_to_redshift,
 stage_Demographics_to_redshift]

# Step 2
# stage_events_to_redshift >> load_songplays_table
# stage_songs_to_redshift >> load_songplays_table
[stage_Home_Values_to_redshift, stage_Rental_Values_to_redshift,
 stage_Demographics_to_redshift] >> \
load_City_Housing_Demographics_table

# Step 3
# load_songplays_table >> load_song_dimension_table
# load_songplays_table >> load_user_dimension_table
# load_songplays_table >> load_artist_dimension_table
# load_songplays_table >> load_time_dimension_table


# Step 4
# load_song_dimension_table >> run_quality_checks
# load_user_dimension_table >> run_quality_checks
# load_artist_dimension_table >> run_quality_checks
# load_time_dimension_table >> run_quality_checks

load_City_Housing_Demographics_table>>\
 [load_City_Housing_Costs_dimension_table] >>\
   run_quality_checks
# Step 5 - end
run_quality_checks >> end_operator