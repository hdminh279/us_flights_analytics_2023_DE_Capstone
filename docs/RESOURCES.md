# 📚 Documentation & Resources

## Course & Project Guidelines

### DataTalks.Club Data Engineering Zoomcamp
- [Course Website](https://datatalks.club/data-engineering-zoomcamp.html)
- [Cohort Schedule & Syllabus](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Project Rubric](https://github.com/DataTalksClub/data-engineering-zoomcamp/wiki/Course-Evaluation)
- [Projects Gallery](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/projects.md)

---

## Apache Airflow

### Core Documentation
- [Airflow Home](https://airflow.apache.org/)
- [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- [Airflow Installation](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)
- [Airflow Concepts](https://airflow.apache.org/docs/apache-airflow/stable/concepts/index.html)

### Docker & Deployment
- [Airflow Docker Compose Setup](https://airflow.apache.org/docs/docker-compose/stable/index.html)
- [Airflow Executor Types](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executors/index.html)
- [Running Airflow in Production](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

### Operators & Integrations
- [BashOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/bash/index.html)
- [PythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html)
- [SparkSubmitOperator](https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/operators.html)
- [AWS Providers](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html)

### Advanced Topics
- [DAG Modularization](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dynamically-mapping-tasks)
- [Task Dependencies](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#dependencies)
- [XCom (Cross-Communication)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)
- [Airflow Variables & Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html)

---

## Apache Spark

### Core Documentation
- [Apache Spark Home](https://spark.apache.org/)
- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)

### Data Processing
- [Spark DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Spark SQL](https://spark.apache.org/docs/latest/sql-getting-started.html)
- [Spark Streaming](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
- [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)

### Integration with AWS
- [Using Spark with S3](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-configure.html)
- [Hadoop AWS Package](https://hadoop.apache.org/docs/r3.3.2/hadoop-aws/tools/hadoop-aws/index.html)
- [Spark + EMR](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark.html)

### Performance & Optimization
- [Spark Tuning](https://spark.apache.org/docs/latest/tuning.html)
- [Spark SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
- [Partitioning Strategy](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html)

### File Formats
- [Parquet Format](https://parquet.apache.org/)
- [ORC Format](https://orc.apache.org/)
- [Spark with Parquet](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html)

---

## dbt (Data Build Tool)

### Core Documentation
- [dbt Home](https://www.getdbt.com/)
- [dbt Documentation](https://docs.getdbt.com/)
- [dbt CLI Reference](https://docs.getdbt.com/reference/dbt-cli-overview)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)

### Key Concepts
- [Models](https://docs.getdbt.com/docs/building-a-dbt-project/building-models)
- [Tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests)
- [Macros](https://docs.getdbt.com/docs/building-a-dbt-project/macros)
- [Packages](https://docs.getdbt.com/docs/building-a-dbt-project/packages)
- [Sources & Freshness](https://docs.getdbt.com/docs/building-a-dbt-project/sources)

### Materializations
- [View vs Table vs Incremental](https://docs.getdbt.com/docs/building-a-dbt-project/building-models/configuring-models)
- [Snapshots (SCD Type 2)](https://docs.getdbt.com/docs/building-a-dbt-project/snapshots)

### Athena Integration
- [dbt Athena Community Plugin](https://github.com/Tomme/dbt-athena)
- [dbt Athena Setup Guide](https://github.com/Tomme/dbt-athena#installation)
- [Athena-Specific Configurations](https://github.com/Tomme/dbt-athena#usage)

### Data Quality
- [Testing Best Practices](https://docs.getdbt.com/guides/best-practices#testing)
- [Custom Tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests#custom-tests)
- [dbt Great Expectations](https://docs.getdbt.com/guides/dbt-ecosystem/integrations/dataviz-integrations/great-expectations)

### Documentation
- [dbt Docs Generation](https://docs.getdbt.com/docs/building-a-dbt-project/documentation)
- [YAML Configuration](https://docs.getdbt.com/reference/yaml-configurations)

---

## AWS Services

### AWS General
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)

### S3 (Simple Storage Service)
- [S3 Home](https://docs.aws.amazon.com/s3/)
- [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/BestPractices.html)
- [S3 Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)

### Athena (SQL Query Engine)
- [Athena Home](https://docs.aws.amazon.com/athena/)
- [Getting Started with Athena](https://docs.aws.amazon.com/athena/latest/ug/getting-started.html)
- [Athena SQL Reference](https://docs.aws.amazon.com/athena/latest/ug/querying-supported-statements.html)
- [Athena Workgroups](https://docs.aws.amazon.com/athena/latest/ug/workgroups-create-update-delete.html)

### AWS Glue
- [AWS Glue Home](https://docs.aws.amazon.com/glue/)
- [Glue Crawler](https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html)
- [Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalogs-and-crawlers.html)
- [Glue Spark Jobs](https://docs.aws.amazon.com/glue/latest/dg/creating-etl-jobs.html)

### IAM (Identity and Access Management)
- [IAM Documentation](https://docs.aws.amazon.com/iam/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-overview.html)
- [Least Privilege Access](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege)

---

## Terraform (Infrastructure as Code)

### Core Documentation
- [Terraform Home](https://www.terraform.io/)
- [Terraform Documentation](https://www.terraform.io/docs/)
- [Terraform CLI Commands](https://www.terraform.io/cli/commands)

### AWS Provider
- [AWS Terraform Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [S3 Bucket Resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)
- [Glue Database Resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_catalog_database)

### Best Practices
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/recommended-practices/index.html)
- [Module Design](https://www.terraform.io/docs/modules/develop/index.html)
- [State Management](https://www.terraform.io/docs/state/index.html)
- [Variables & Outputs](https://www.terraform.io/docs/language/values/variables.html)

### Scaling Infrastructure
- [Remote State](https://www.terraform.io/docs/state/remote.html)
- [Workspaces](https://www.terraform.io/docs/state/workspaces.html)
- [Modules](https://www.terraform.io/docs/modules/index.html)

---

## Docker

### Core Documentation
- [Docker Home](https://www.docker.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Airflow-Specific
- [Airflow Docker Image](https://hub.docker.com/r/apache/airflow)
- [Building Custom Airflow Images](https://airflow.apache.org/docs/docker-compose/stable/index.html#customizing-docker-compose)

### Best Practices
- [Docker Security](https://docs.docker.com/engine/security/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## Data Visualization & BI Tools

### Metabase
- [Metabase Home](https://www.metabase.com/)
- [Metabase Documentation](https://www.metabase.com/docs/latest/)
- [Setting up Metabase](https://www.metabase.com/docs/latest/getting-started.html)
- [Dashboard Design](https://www.metabase.com/docs/latest/dashboards/introduction.html)

### Looker Studio (formerly Google Data Studio)
- [Looker Studio Home](https://datastudio.google.com/)
- [Looker Studio Help](https://support.google.com/datastudio)
- [Creating Dashboards](https://support.google.com/datastudio/answer/6283323)
- [Data Sources](https://support.google.com/datastudio/answer/6300774)

### Streamlit
- [Streamlit Home](https://streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Building Dashboards](https://docs.streamlit.io/library/get-started)
- [Data Visualization](https://docs.streamlit.io/library/api-reference/charts)

---

## SQL & Query Optimization

### SQL Resources
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Advanced SQL](https://mode.com/sql-tutorial/)
- [SQL Best Practices](https://use-the-index-luke.com/)

### Window Functions
- [Window Functions Explained](https://www.postgresql.org/docs/current/window-functions.html)
- [SQL Window Functions Tutorial](https://mode.com/sql-tutorial/sql-window-functions/)

### Query Optimization
- [Query Optimization Basics](https://docs.aws.amazon.com/athena/latest/ug/querying-with-athena.html)
- [Execution Plans](https://use-the-index-luke.com/sql/explain-plan)
- [Partitioning Strategy](https://docs.aws.amazon.com/athena/latest/ug/partitioning-data.html)

---

## Data Quality & Testing

### dbt Tests
- [dbt Test Reference](https://docs.getdbt.com/reference/test-configs)
- [Generic Tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests#generic-tests)
- [Singular Tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests#singular-tests)

### Data Quality Tools
- [Great Expectations](https://greatexpectations.io/)
- [SODA](https://www.soda.io/)
- [Monte Carlo Data](https://www.montecarlodata.com/)

---

## Learning Resources

### YouTube Channels
- [DataTalks.Club Channel](https://www.youtube.com/@DataTalksClub)
- [Apache Spark Tutorials](https://www.youtube.com/results?search_query=apache+spark+tutorial)
- [Terraform Tutorials](https://www.youtube.com/results?search_query=terraform+aws+tutorial)

### Online Courses
- [Udemy: Complete Hands-On Introduction to Apache Spark](https://www.udemy.com/course/apache-spark/)
- [Udemy: dbt Fundamentals](https://learn.getdbt.com/courses/fundamentals)
- [Coursera: Big Data Specialization](https://www.coursera.org/specializations/big-data)

### Blogs & Articles
- [dbt Blog](https://blog.getdbt.com/)
- [DataTalks.Club Blog](https://datatalks.club/)
- [Medium Data Engineering](https://medium.com/tag/data-engineering)
- [Towards Data Science](https://towardsdatascience.com/)

---

## Community & Support

### Slack Communities
- [DataTalks.Club Slack](https://datatalks.club/)
- [dbt Community Slack](https://community.getdbt.com/)
- [Apache Airflow Community](https://airflow.apache.org/community/)

### Forums & Discussions
- [Stack Overflow - Apache Airflow](https://stackoverflow.com/questions/tagged/airflow)
- [Stack Overflow - dbt](https://stackoverflow.com/questions/tagged/dbt)
- [Stack Overflow - Apache Spark](https://stackoverflow.com/questions/tagged/pyspark)
- [dbt Discourse](https://discourse.getdbt.com/)

### GitHub Resources
- [Airflow GitHub](https://github.com/apache/airflow)
- [dbt GitHub](https://github.com/dbt-labs/dbt-core)
- [Terraform GitHub](https://github.com/hashicorp/terraform)

---

## Tools & Utilities

### Terminal/CLI Tools
- [AWS CLI](https://aws.amazon.com/cli/)
- [Terraform CLI](https://www.terraform.io/downloads.html)
- [Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/)

### IDE & Editors
- [VS Code](https://code.visualstudio.com/)
- [VS Code Extensions for Python](https://marketplace.visualstudio.com/vsct?target=VSCode&category=Python)
- [DBeaver (SQL IDE)](https://dbeaver.io/)
- [DataGrip (SQL IDE)](https://www.jetbrains.com/datagrip/)

### Git & Version Control
- [GitHub](https://github.com/)
- [GitLab](https://about.gitlab.com/)
- [Git Documentation](https://git-scm.com/doc)

### Virtual Environment Management
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)
- [Poetry (Python Dependency Management)](https://python-poetry.org/)
- [Conda (Package Manager)](https://docs.conda.io/)

---

## Project Management

### CI/CD & Automation
- [GitHub Actions](https://github.com/features/actions)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [Jenkins](https://www.jenkins.io/)

### Monitoring & Alerting
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [AWS CloudWatch](https://docs.aws.amazon.com/cloudwatch/)

---

## Useful Commands Reference

### Airflow
```bash
airflow dags list
airflow dags trigger flight_delay_pipeline
airflow tasks list flight_delay_pipeline
airflow logs -f flight_delay_pipeline
```

### dbt
```bash
dbt run
dbt test
dbt docs generate
dbt debug
```

### Spark
```bash
spark-submit spark_preprocessing.py
spark-shell
pyspark
```

### Terraform
```bash
terraform init
terraform plan
terraform apply
terraform destroy
```

### AWS CLI
```bash
aws s3 ls
aws s3 cp file.txt s3://bucket/path/
aws athena start-query-execution --query-string "SELECT * FROM table"
```

---

## Quick References

### Data Types (SQL/Spark)
- `INTEGER`, `INT` - Whole numbers
- `DECIMAL(10,2)` - Fixed precision decimals
- `FLOAT`, `DOUBLE` - Floating point numbers
- `STRING`, `VARCHAR` - Text
- `DATE` - Date only (YYYY-MM-DD)
- `TIMESTAMP` - Date + Time
- `BOOLEAN` - True/False
- `ARRAY`, `STRUCT` - Complex types

### S3 Path Patterns
- `s3://bucket-name/raw/` - Raw data
- `s3://bucket-name/clean/` - Cleaned data
- `s3://bucket-name/business/` - Business tables
- `s3://bucket-name/logs/` - Application logs

### Model Stages
- **Staging** - Raw data standardization
- **Intermediate** - Feature engineering
- **Business** - Analytics-ready tables (Facts & Dimensions)

---

## Tips & Tricks

### Debug Airflow DAG
```bash
# Test a specific task
airflow tasks test flight_delay_pipeline download_kaggle_data

# Validate DAG syntax
python -m py_compile airflow/dags/flight_delay_pipeline.py
```

### Debug Spark Job
```bash
# Check input data
df.show(10)
df.printSchema()
df.describe().show()

# Debug transformations
df.filter(col("column").isNull()).show()
df.groupBy("column").count().show()
```

### Debug dbt Models
```bash
# Show compiled SQL
dbt compile --select stg_flights

# Run specific test
dbt test --select test_unique_stg_flights_flight_key

# Profile execution time
dbt run --select model_name --profiles-dir . | grep "Completed in"
```

---

## Keeping Documentation Updated

As the project evolves:
1. Update relevant README files
2. Add new concepts to docs/RESOURCES.md
3. Document code changes with comments
4. Keep dbt model documentation current
5. Update architecture diagrams as needed

---

**Last Updated**: March 25, 2026  
**Maintained By**: Data Engineering Team  
**License**: Educational Use (DataTalks.Club Course)
