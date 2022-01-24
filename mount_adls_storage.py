# Databricks notebook source
storage_account_name = "demo1dl"
client_id = dbutils.secrets.get(scope="demo1-scope", key="databricks-app-client-id")
tenant_id = dbutils.secrets.get(scope="demo1-scope", key="databricks-app-tenant-id")
client_secret  = dbutils.secrets.get(scope="demo1-scope", key="databricks-app-client-secret")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": f"{client_id}",
           "fs.azure.account.oauth2.client.secret": f"{client_secret}",
           "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}

# COMMAND ----------

# MAGIC %md Mount Functions

# COMMAND ----------

# mount Mount function
def mount_adls(container_name: str):
    dbutils.fs.mount(
        source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/",
        mount_point = f"/mnt/{storage_account_name}/{container_name}",
        extra_configs = configs)
    
# delete all Mounts function
def delete_mounts(*args):
    dbutils.fs.mounts()  # before deletion: List all mounts in our workspace
    for mount in dbutils.fs.mounts():
        if mount.mountPoint.startswith('/mnt/'):
            dbutils.fs.unmount(mount.mountPoint)
    dbutils.fs.mounts()  # after deletion: List all mounts in our workspace

# COMMAND ----------

# MAGIC %md Raw inputs container

# COMMAND ----------

container_name = "rawinputs"
mount_adls(container_name)
dbutils.fs.mounts()

# COMMAND ----------

# MAGIC %md Processed container

# COMMAND ----------

container_name = "processed"
mount_adls(container_name)
dbutils.fs.mounts()
