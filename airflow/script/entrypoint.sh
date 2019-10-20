#!/usr/bin/env bash 
 
TRY_LOOP="20" 
 
# Defaults and back-compat 
: "${AIRFLOW__CORE__FERNET_KEY:=${FERNET_KEY:=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")}}" 
: "${AIRFLOW__CORE__EXECUTOR:=${EXECUTOR:-Local}Executor}" 
 
export \ 
  AIRFLOW__CORE__EXECUTOR \ 
  AIRFLOW__CORE__FERNET_KEY \ 
  AIRFLOW__CORE__LOAD_EXAMPLES \ 
  AIRFLOW__CORE__SQL_ALCHEMY_CONN \ 
 
 
# Load DAGs exemples (default: Yes) 
if [[ -z "$AIRFLOW__CORE__LOAD_EXAMPLES" && "${LOAD_EX:=n}" == n ]] 
then 
  AIRFLOW__CORE__LOAD_EXAMPLES=False 
fi 
 
# Install custom python package if requirements.txt is present 
if [ -e "/requirements.txt" ]; then 
    $(which pip) install --user -r /requirements.txt 
fi 
 
case "$1" in 
  webserver) 
    airflow initdb 
    exec airflow webserver 
    ;; 
  worker|scheduler) 
    # To give the webserver time to run initdb. 
    sleep 10 
    exec airflow "$@" 
    ;; 
  flower) 
    sleep 10 
    exec airflow "$@" 
    ;; 
  version) 
    exec airflow "$@" 
    ;; 
  *) 
    # The command is something like bash, not an airflow subcommand. Just run it in the right environment. 
    exec "$@" 
    ;; 
esac 
 

