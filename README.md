# DroneShuttlesApp documentation

Below is whole documentation for Multi Tier application.

## 1. Purpose and Objective

DroneShuttlesApp is web application that supports marketing efforts for the company. It will host information about new product that will be revolutionize the market.
This document describes how application will be hosted in Azure; the resources provisioned for it; and how the resources will relate and be interacted with.

## 2. System overview

DroneShuttlesApp is public web appliation used by company to expand their marketing efforts with modern blog capabilities. In addition, application provides scalability to handle incomming traffic ensuring all security standards and procedures. 

## 3. Infrastructure Overview



![image](https://github.com/PittyMeNot/droneShuttles/assets/80931908/be68590e-eba8-408a-9a93-2406dc61de5f)


DroneShuttlesApp will be hosted as cloud native web application, leveraging managed Azure Services:

- Azure App Services and App Services Plan
- Azure MySQL Servers
- Azure Function App
- Azure Storage Account
- Azure Front door
- Azure Application Gateway with WAF v2
- Container registry
- Network Security groups
- Virtual networks
- Azure DevOps with pipelines
- Application Insights
- Log analytics workspaces

### 3.1 App Service

| Environment  | Pricing Plan | App Insights | Region | Operating System | Autoscaling min. | Autoscaling default | Autoscaling max | 
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Production  | Premium v3 P1V3   | Yes | North europe and West Europe | Linux | 1 | 1 | 3 |
| Development  |  Deployment slot | Yes | North Europe and West Europe | Linux | 1 | 1 | 3 |

The App Service will host DroneShuttlesApp. It will be accesible by web browser using HTTPS, port 443. Dev environment is being placed in the same ASP as production to lower cost of additional App Services Plans and App Service. Team will use deployment slots to test their new version of application.

### 3.1.2 Monitoring

Application Insights will be enabled for every App Service instances.

### 3.1.3 Backup and Recovery

App Services will leverage deployment slots, which will keep the next and previous app versions for use during deployment and rollbacks.

### 3.2.1 Database

| Environment | Database Server | Workload | Compute + Storage | Size | Backup Storage |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Production | Azure databse for MYSQL | Production | General Purpose | D2ds_v4 | RA-GRS |
| Development | Azure database for MYSQL | Development | Burstable | B1ms | LRS |

DroneShuttles databases will be hosted on Azure Mysql. Application is using single database to store its schema. 

### 3.2.2 Disaster recovery

Production Database has a Read-Only Replica in Second region to provide redudancy and High Availabity. In case on Main region failure, read only SQL can be transformed into Main Database, where the first My SQL server will be restore from backup in case of failure/Regional Failure.

### 3.2.3 Database authentication

Authentication with the database will occur using credentials which are stored in Azure Key Vault.

### 3.2.4 Backup

Azure SQL provides automatic backups once a day.

### 3.2.5 Database restoration

Database can be restored using Azure Backup.

### 3.3.1 Azure Functions

| Environment | Runtime | Region | OS | Plan | Public Access | App Insights |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Production | Python 3.9 | North Europe | Linux | Serverless | No | Yes |

Azure function will be used to maintain script for deleting all blog posts at once.

```
function test() {
  console.log("notice the blank line before this function?");
}
```












