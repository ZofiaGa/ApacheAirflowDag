# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago




# Task 1.1 - Define DAG arguments

dag_args = {
    'owner': 'Zofia DummyName',
    'start_date': days_ago(0),
    'email': ['zofia@dummymail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Task 1.2 - Define the DAG

dag = DAG(
    dag_id='ETL_toll_data',
    schedule_interval=timedelta(days=1),
    default_args=dag_args,
    description='Apache Airflow Final Assignment',
)

# Task 1.3 - Create a task to unzip data

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzf tolldata.tgz -C airflow_test',
    dag=dag,
)

# Task 1.4 - Create a task to extract data from csv file

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1,2,3,4 vehicle-data.csv > csv_data.csv',  
    dag=dag,
)

# Task 1.5 - Create a task to extract data from tsv file

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5,6,7 tollplaza-data.tsv > tsv_data_TEST.csv',
    dag=dag,
)

# Task 1.6 - Create a task to extract data from fixed width file

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -c 59-61,62,63-67 payment-data.txt > fixed_width_data.csv',
    dag=dag,
)

# Task 1.7 - Create a task to consolidate data extracted from previous tasks

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d"," csv_data.csv tsv_data.csv fixed_width_data.csv | tr -d "\r" > extracted_data.csv',
    dag=dag,
)

# Task 1.8 - Transform and load the data

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='awk \'BEGIN {FS=OFS=","} { $4 = toupper($4) } 1\' extracted_data.csv > transformed_data.csv',
    dag=dag,
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data