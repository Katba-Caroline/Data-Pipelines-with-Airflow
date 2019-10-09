# Project Description
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Sparkify would like a Data Engineer to create high grade data pipelines that:
    - are dynamic
    - built from reusable tasks
    - can be monitored
    - allow easy backfills
  They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.
  
 ## Database schema design

**Staging Tables**
 - staging_events
 - staging_songs

**Fact Table**
  - songplays - records in event data associated with song plays i.e. records with page NextSong
      - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

**Dimension Tables**
  - songs - songs in music database
      - *song_id, title, artist_id, year, duration*
  - artists - artists in music database 
      - *artist_id, name, location, lattitude, longitude*
  - users - All app users
    - *user_id, first_name, last_name, gender, level*
  - time - timestamps of records in songplays broken down into specific units 
      - *start_time, hour, day, week, month, year, weekday*


# Project structure
This project includes the following script files:
  - **Dag Files**
    - *dags/main_dags.py*: Directed Acyclic Graph (DAG) definition with imports, tasks and task dependencies.
    - *dags/sub_dags.py*: Subdag designed to handle loading of Dimensional tables tasks.
  - **helper Class**
    - *plugins/helpers/sql_queries.py*: Contains Insert SQL statements.
  - **SQL Tables** 
    - *plugins/operators/create_tables.sql*: Contains SQL Table creations statements.
  - **perators**
    - *plugins/operators/stage_redshift.py*: Operator copies data from S3 buckets into redshift staging tables.
    - *plugins/operators/load_dimension.py*: Operator loads data from redshift staging tables into dimensional tables.
    - *plugins/operators/load_fact.py*: Operator loads data from redshift staging tables into fact table.
    - *plugins/operators/data_quality.py*: Operator validates data quality in redshift tables.

# Sparkify DAG Configuration Parameters:

    - The DAG does not have dependencies on past runs
    - DAG has schedule interval set to hourly
    - On failure, the tasks are retried 3 times
    - Retries happen every 5 minutes
    - Catchup is turned off
    - Do not email on retry
  
 ## After configuring the task dependencies, the graph view follows the flow shown in the image below:
 ![alt text](https://github.com/Katba-Caroline/Data-Pipelines-with-Airflow/blob/master/dag.png)
 
 ## Example of DAG running details
 ![alt text](https://github.com/Katba-Caroline/Data-Pipelines-with-Airflow/blob/master/dag_details.PNG)
 
 # Sparkify DAG Operators
We built four different operators that will stage the data, transform the data, and run checks on data quality. All of the operators and task instances run SQL statements against the Redshift database. Additionally, using parameters allows us to build flexible, reusable, and configurable operators that we can later apply to many kinds of data pipelines with Redshift and with other databases.

  **Stage Operator**
    
  The stage operator can load any JSON formatted files from S3 to Amazon Redshift. it creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters specify where in S3 the file is loaded and what is the target table.

  The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

  **Fact and Dimension Operators**
    
  SQL helper class helps us run data transformations. Most of the logic is within the SQL transformations and the operator takes as input a SQL statement and target database on which to run the query against. The target table that will contain the results of the transformation.

  Dimension loads are done with the truncate-insert pattern where the target table is emptied before the load. Thus, we have a parameter that allows switching between insert modes when loading dimensions. (Fact tables are usually so massive that they should only allow append type functionality.)

  **Data Quality Operator**
    
  The final operator is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each test, the test result and expected result needs to be checked and if there is no match, the operator raises an exception and the task retries and fails eventually.

  *For example*: one test could be a SQL statement that checks if certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs so expected result would be 0 and the test would compare the SQL statement's outcome to the expected result.
