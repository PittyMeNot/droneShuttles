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

