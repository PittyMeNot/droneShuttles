Application can be accessed here: https://droneshuttles.azurefd.net


# DroneShuttlesApp documentation

Below is whole documentation for Multi Tier application.

## 1. Purpose and Objective

DroneShuttlesApp is web application that supports marketing efforts for the company. It will host information about new product that will be revolutionize the market.
This document describes how application will be hosted in Azure; the resources provisioned for it; and how the resources will relate and be interacted with.

## 2. System overview

DroneShuttlesApp is public web appliation used by company to expand their marketing efforts with modern blog capabilities. In addition, application provides scalability to handle incomming traffic ensuring all security standards and procedures. 

## 3. Infrastructure Overview



![image](https://github.com/PittyMeNot/droneShuttles/assets/80931908/f982e8ee-5998-4d74-ba72-4bf9f2e36158)



DroneShuttlesApp will be hosted as cloud native web application, leveraging managed Azure Services:

- Azure App Services and App Services Plan
- Azure MySQL Servers
- Azure Function App
- Azure Storage Account
- Azure Front door
- Azure Application Gateway with WAF v2
- Container registry
- Network Security groups
- Virtual networks with subnets
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

Example script:

```python
import os
import json
import logging
import requests

import azure.functions as func

### Please provide needed URL and KEY below ###

GHOST_API_URL = os.environ['GHOST_API_URL']
GHOST_API_KEY = os.environ['GHOST_API_KEY']

def delete_all_posts():
    headers = {
        'Authorization': f'Ghost {GHOST_API_KEY}'
    }

    posts_url = f'{GHOST_API_URL}/admin/posts/'
    response = requests.get(posts_url, headers=headers)
    response.raise_for_status()

    posts = response.json().get('posts', [])

    for post in posts:
        post_id = post['id']
        delete_url = f'{GHOST_API_URL}/admin/posts/{post_id}/'
        delete_response = requests.delete(delete_url, headers=headers)
        delete_response.raise_for_status()
        logging.info(f'Deleted post with ID {post_id}')

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        delete_all_posts()
        return func.HttpResponse("All posts have been deleted", status_code=200)
    except Exception as e:
        logging.error(f'Error while deleting posts: {e}')
        return func.HttpResponse("Failed to delete all posts", status_code=500)
```

### 3.4.1 Storage Account

| Environment | Region | Performance | Redudancy | Access tier | Soft deletion retention | Encryption support |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Production | North Europe and West Europe | Standard | RA-GRS | Hot | 7 | Blobs and files only |

Application will store its static content in Storage accounts.

### 3.5.1 Azure Front door

Azure front door will provide CDN, and lower latency for DroneShuttlesApp. Moreover, web application Firewall will be attached to it in order to prevent obvious attacks.
As a backend, application gateway will be hosted to accept HTTPS protocol and forward HTTP protocol to HTTPS. SKU will be standard


![image](https://github.com/PittyMeNot/droneShuttles/assets/80931908/cea570bd-f535-4e99-baa3-cea127e564fa)

### 3.6.1 Application Gateway

| Environment  | Pricing Plan | App Insights | Region | FrontEnd IP | Autoscaling min. | Autoscaling default | Autoscaling max | 
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Production  | WAF V2   | Yes | North europe | Public IP | 1 | 1 | 3 |

Application gateway will distribute incomming trafic between two regions, North Europe and West europe. Application gateway will use two app services as a backend pool and will be accepting HTTPS protocol.
Health probes will be configured to monitor app services every 30 seconds to avoid generating too much costs.

### 3.7.1 Azure Container Registry

| Environment  | Pricing Plan | Backup | Region |
| ------------- | ------------- | ------------- | ------------- |
| Production and Development | Premium | ZRS | North Europe |

Container Registry will be used to provide CI/CD from Azure DevOps to App Services. Containers will be stored in the private repository ( Prod and dev ).

### 3.8.1 Network security groups

NSG will be applied to 2 vNets (North europe and West Europe) to accept internal traffic (Standard Azure rules) and HTTPS from Application Gateway.

### 3.9.1 Virtual Networks

There will be two Virtual Networks. One will be hosted in North europe, and the Second one in West Europe. Both of them will have 5 subnets and integrated with specific Azure Resources.

| Environment | Address Space | Address Range | Address count | Subnets | Peerings |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Production | 10.0.0.0/24 | 10.0.0.0 - 10.0.0.255 | 256 | 5 | Yes, to vNet 2 |
| Production | 172.16.0.0/24 | 172.16.0.0 - 172.16.0.255 | 256 | 5 | Yes, to vNet 1 |

### 3.9.2 Subnets

| Name | Address Space | Address Range | Address count | Delegated to |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| sbn101 | 10.0.0.0/27 | 10.0.0.0 - 10.0.0.31 | 27 + 5 Azure Reserved addresses | Microsoft.DBforMySQL/flexibleServers |
| sbn102 | 10.0.0.32/27 | 10.0.0.32 - 10.0.0.63 | 27 + 5 Azure Reserved addresses | Microsoft.Web/serverfarms |
| sbn103 | 10.0.0.64/27 | 10.0.0.64 - 10.0.0.95 | 27 + 5 Azure Reserved addresses | N/A |
| sbn104 | 10.0.0.96/27 | 10.0.0.96 - 10.0.0.127 | 27 + 5 Azure Reserved addresses | N/A |
| sbn105 | 10.0.0.128/27 | 10.0.0.128 - 10.0.0.159 | 27 + 5 Azure Reserved addresses | N/A |
| sbn201 | 172.16.0.0/27 | 172.16.0.0 - 172.16.0.31 | 27 + 5 Azure Reserved addresses | Microsoft.DBforMySQL/flexibleServers |
| sbn202 | 172.16.0.32/27 | 172.16.0.32 - 172.16.0.63 | 27 + 5 Azure Reserved addresses | Microsoft.Web/serverfarms |
| sbn203 | 172.16.0.64/27 | 172.16.0.64 - 172.16.0.95 | 27 + 5 Azure Reserved addresses | N/A |
| sbn204 | 172.16.0.96/27 | 172.16.0.96 - 172.16.0.127 | 27 + 5 Azure Reserved addresses | N/A |
| sbn205 | 172.16.0.128/27 | 172.16.0.128 - 172.16.0.159 | 27 + 5 Azure Reserved addresses | N/A |

### 3.10.1 Azure DevOps

CI/CD will be provided by Azure DevOps. DevOps teams will use private repositories along with Azure premium Container registry to push new images to the Service Apps. 

![image](https://github.com/PittyMeNot/droneShuttles/assets/80931908/dd4802aa-d18e-4290-b317-53f63437621e)

### 3.10.2 Deployment Process

Push new image from Azure Devops to Container registry --> App Services download latest image

### 3.11.1 Application Insights

Application Insights will be used to monitora all App Services depedencies.

### 3.12.1 Log workspace analytics

LWA will store all logs from App Services.






















