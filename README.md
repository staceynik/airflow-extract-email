# Extract Email DAG using Apache Airflow

This project demonstrates how to use Apache Airflow to create a DAG (Directed Acyclic Graph) that extracts comments from an external API and stores comments with emails ending with '.us' in a PostgreSQL database.

## Project Structure

The project has the following structure:

```markdown

.
├── dags
│   └── extract_email_dag.py
├── plugins
│   ├── __init__.py
│   └── operators
│       ├── email_extract_operator.py
│       └── __init__.py
├── README.md
└── requirements.txt
```


