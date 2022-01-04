# Databricks notebook source
dbutils.widgets.text("input", "", "Send the parameter value")
input_param = dbutils.widgets.get("input")
print(input_param)

# COMMAND ----------

print("This is a Child Notebook")

# COMMAND ----------

dbutils.notebook.exit(100)