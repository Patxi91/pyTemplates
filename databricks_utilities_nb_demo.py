# Databricks notebook source
# MAGIC %fs
# MAGIC ls

# COMMAND ----------

dbutils.fs.ls('/')  # List folders --> further see dbutils.fs.help()

# COMMAND ----------

for folder_name in dbutils.fs.ls('/'):
    print(folder_name)

# COMMAND ----------

# Information about the notebook module
dbutils.notebook.help()

# COMMAND ----------

dbutils.notebook.run('./child_notebook_demo', 10, {"input": "Called from main notebook"})

# COMMAND ----------

# MAGIC %pip install pandas

# COMMAND ----------

