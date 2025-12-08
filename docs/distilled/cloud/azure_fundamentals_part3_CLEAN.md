# Introduction to Cloud Infrastructure: Describe Azure Management and Governance

**Source**: https://learn.microsoft.com/en-us/training/paths/describe-azure-management-governance/
**Level**: Beginner
**Modules**: 4
**Total Units**: 28

## Overview

Management and governance focused portion of Introduction to Cloud Infrastructure training.

---

# Module 1: Describe Cost Management in Azure

Describe cost management in Azure

## 1.1 Introduction

# Introduction
, you’ll be introduced to factors that impact costs in Azure and tools to help you both predict potential costs and monitor and control costs.
## Learning objectives
After completing this module, you’ll be able to:
- Describe factors that can affect costs in Azure.
- Compare the Pricing calculator and Total Cost of Ownership (TCO) calculator.
- Describe the Microsoft Cost Management Tool.
- Describe the purpose of tags.

## 1.2 Describe factors that can affect costs in Azure

# Describe factors that can affect costs in Azure
The following video provides an introduction to things that can impact your costs in Azure.
Azure shifts development costs from the capital expense (CapEx) of building out and maintaining infrastructure and facilities to an operational expense (OpEx) of renting infrastructure as you need it, whether it’s compute, storage, networking, and so on.
That OpEx cost can be impacted by many factors. Some of the impacting factors are:
- Resource type
- Consumption
- Maintenance
- Geography
- Subscription type
- Azure Marketplace
## Resource type
A number of factors influence the cost of Azure resources. The type of resources, the settings for the resource, and the Azure region will all have an impact on how much a resource costs. When you provision an Azure resource, Azure creates metered instances for that resource. The meters track the resources' usage and generate a usage record that is used to calculate your bill.
### Examples
With a storage account, you specify a type such as blob, a performance tier, an access tier, redundancy settings, and a region. Creating the same storage account in different regions may show different costs and changing any of the settings may also impact the price.
With a virtual machine (VM), you may have to consider licensing for the operating system or other software, the processor and number of cores for the VM, the attached storage, and the network interface. Just like with storage, provisioning the same virtual machine in different regions may result in different costs.
## Consumption
Pay-as-you-go has been a consistent theme throughout, and that’s the cloud payment model where you pay for the resources that you use during a billing cycle. If you use more compute this cycle, you pay more. If you use less in the current cycle, you pay less. It’s a straight forward pricing mechanism that allows for maximum flexibility.
However, Azure also offers the ability to commit to using a set amount of cloud resources in advance and receiving discounts on those “reserved” resources. Many services, including databases, compute, and storage all provide the option to commit to a level of use and receive a discount, in some cases up to 72 percent.
When you reserve capacity, you’re committing to using and paying for a certain amount of Azure resources during a given period (typically one or three years). With the back-up of pay-as-you-go, if you see a sudden surge in demand that eclipses what you’ve pre-reserved, you just pay for the additional resources in excess of your reservation. This model allows you to recognize significant savings on reliable, consistent workloads while also having the flexibility to rapidly increase your cloud footprint as the need arises.
## Maintenance
The flexibility of the cloud makes it possible to rapidly adjust resources based on demand. Using resource groups can help keep all of your resources organized. In order to control costs, it’s important to maintain your cloud environment. For example, every time you provision a VM, additional resources such as storage and networking are also provisioned. If you deprovision the VM, those additional resources may not deprovision at the same time, either intentionally or unintentionally. By keeping an eye on your resources and making sure you’re not keeping around resources that are no longer needed, you can help control cloud costs.
## Geography
When you provision most resources in Azure, you need to define a region where the resource deploys. Azure infrastructure is distributed globally, which enables you to deploy your services centrally or closest to your customers, or something in between. With this global deployment comes global pricing differences. The cost of power, labor, taxes, and fees vary depending on the location. Due to these variations, Azure resources can differ in costs to deploy depending on the region.
Network traffic is also impacted based on geography. For example, it’s less expensive to move information within Europe than to move information from Europe to Asia or South America.
### Network Traffic
Billing zones are a factor in determining the cost of some Azure services.
Bandwidth refers to data moving in and out of Azure datacenters. Some inbound data transfers (data going into Azure datacenters) are free. For outbound data transfers (data leaving Azure datacenters), data transfer pricing is based on zones.
A zone is a geographical grouping of Azure regions for billing purposes. The bandwidth pricing page has additional information on pricing for data ingress, egress, and transfer.
## Subscription type
Some Azure subscription types also include usage allowances, which affect costs.
For example, an Azure free trial subscription provides access to a number of Azure products that are free for 12 months. It also includes credit to spend within your first 30 days of sign-up. You'll get access to more than 25 products that are always free (based on resource a

## 1.3 Explore the pricing calculator

# Explore the pricing calculator
The pricing calculator is a calculator that helps you understand potential Azure expenses. The pricing calculator is accessible from the internet and allows you to build out a configuration. The Total Cost of Ownership (TCO) calculator has been retired.
## Pricing calculator
The pricing calculator is designed to give you an estimated cost for provisioning resources in Azure. You can get an estimate for individual resources, build out a solution, or use an example scenario to see an estimate of the Azure spend. The pricing calculator’s focus is on the cost of provisioned resources in Azure.
Note
The Pricing calculator is for information purposes only. The prices are only an estimate. Nothing is provisioned when you add resources to the pricing calculator, and you won't be charged for any services you select.
With the pricing calculator, you can estimate the cost of any provisioned resources, including compute, storage, and associated network costs. You can even account for different storage options like storage type, access tier, and redundancy.

## 1.4 Exercise - Estimate workload costs by using the Pricing calculator

# Exercise - Estimate workload costs by using the Pricing calculator
In this exercise, you use the Pricing calculator to estimate the cost of running a basic web application on Azure.
Start by defining which Azure services you need.
Note
The Pricing calculator is for information purposes only. The prices are only an estimate, and you won't be charged for any services you select.
## Define your requirements
Before you run the Pricing calculator, you need a sense of what Azure services you need.
For a basic web application hosted in your datacenter, you might run a configuration similar to the following.
An ASP.NET web application that runs on Windows. The web application provides information about product inventory and pricing. There are two virtual machines that are connected through a central load balancer. The web application connects to a SQL Server database that holds inventory and pricing information.
To migrate to Azure, you might:
- Use Azure Virtual Machines instances, similar to the virtual machines used in your datacenter.
- Use Azure Application Gateway for load balancing.
- Use Azure SQL Database to hold inventory and pricing information.
Here's a diagram that shows the basic configuration:
In practice, you would define your requirements in greater detail. But here are some basic facts and requirements to get you started:
- The application is used internally. It's not accessible to customers.
- This application doesn't require a massive amount of computing power.
- The virtual machines and the database run all the time (730 hours per month).
- The network processes about 1 TB of data per month.
- The database doesn't need to be configured for high-performance workloads and requires no more than 32 GB of storage.
## Explore the Pricing calculator
Let's start with a quick tour of the Pricing calculator.
- Go to the Pricing calculator .
- Notice the following tabs:
- Products This is where you choose the Azure services that you want to include in your estimate. You'll likely spend most of your time here.
- Example scenarios Here you'll find several reference architectures , or common cloud-based solutions that you can use as a starting point.
- Saved estimates Here you'll find your ly saved estimates.
- FAQs Here you'll discover answers to frequently asked questions about the Pricing calculator.
## Estimate your solution
Here you add each Azure service that you need to the calculator. Then you configure each service to fit your needs.
Tip
Make sure you have a clean calculator with nothing listed in the estimate. You can reset the estimate by selecting the trash can icon to each item.
### Add services to the estimate
- On the Products tab, select the service from each of these categories:
Category 
Service 
Compute 
Virtual Machines 
Databases 
Azure SQL Database 
Networking 
Application Gateway 
- Scroll to the bottom of the page. Each service is listed with its default configuration.
### Configure services to match your requirements
- Under Virtual Machines , set these values:
Setting 
Value 
Region 
West US 
Operating system 
Windows 
Type 
(OS Only) 
Tier 
Standard 
Instance 
D2 v3 
Virtual machines 
2 x 730 Hours 
Leave the remaining settings at their current values.
- Under Azure SQL Database , set these values:
Setting 
Value 
Region 
West US 
Type 
Single Database 
Backup storage tier 
RA-GRS 
Purchase model 
vCore 
Service tier 
General Purpose 
Compute tier 
Provisioned 
Generation 
Gen 5 
Instance 
8 vCore 
Leave the remaining settings at their current values.
- Under Application Gateway , set these values:
Setting 
Value 
Region 
West US 
Tier 
Web Application Firewall 
Size 
Medium 
Gateway hours 
2 x 730 Hours 
Data processed 
1 TB 
Outbound data transfer 
5 GB 
Leave the remaining settings at their current values.
## Review, share, and save your estimate
At the bottom of the page, you see the total estimated cost of running the solution. You can change the currency type if you want.
At this point, you have a few options:
- Select Export to save your estimate as an Excel document.
- Select Save or Save as to save your estimate to the Saved Estimates tab for later.
- Select Share to generate a URL so you can share the estimate with your team.
You now have a cost estimate that you can share with your team. You can make adjustments as you discover any changes to your requirements.
Experiment with some of the options you worked with here, or create a purchase plan for a workload you want to run on Azure.

## 1.5 Describe the Microsoft Cost Management tool

# Describe the Microsoft Cost Management tool
Microsoft Azure is a global cloud provider, meaning you can provision resources anywhere in the world. You can provision resources rapidly to meet a sudden demand, or to test out a new feature, or on accident. If you accidentally provision new resources, you may not be aware of them until it’s time for your invoice. Cost Management is a service that helps avoid those situations.
## What is Cost Management?
Cost Management provides the ability to quickly check Azure resource costs, create alerts based on resource spend, and create budgets that can be used to automate management of resources.
Cost analysis is a subset of Cost Management that provides a quick visual for your Azure costs. Using cost analysis, you can quickly view the total cost in a variety of different ways, including by billing cycle, region, resource, and so on.
You use cost analysis to explore and analyze your organizational costs. You can view aggregated costs by organization to understand where costs are accrued and to identify spending trends. And you can see accumulated costs over time to estimate monthly, quarterly, or even yearly cost trends against a budget.
## Cost alerts
Cost alerts provide a single location to quickly check on all of the different alert types that may show up in the Cost Management service. The three types of alerts that may show up are:
- Budget alerts
- Credit alerts
- Department spending quota alerts.
### Budget alerts
Budget alerts notify you when spending, based on usage or cost, reaches or exceeds the amount defined in the alert condition of the budget. Cost Management budgets are created using the Azure portal or the Azure Consumption API.
In the Azure portal, budgets are defined by cost. Budgets are defined by cost or by consumption usage when using the Azure Consumption API. Budget alerts support both cost-based and usage-based budgets. Budget alerts are generated automatically whenever the budget alert conditions are met. You can view all cost alerts in the Azure portal. Whenever an alert is generated, it appears in cost alerts. An alert email is also sent to the people in the alert recipients list of the budget.
### Credit alerts
Credit alerts notify you when your Azure credit monetary commitments are consumed. Monetary commitments are for organizations with Enterprise Agreements (EAs). Credit alerts are generated automatically at 90% and at 100% of your Azure credit balance. Whenever an alert is generated, it's reflected in cost alerts, and in the email sent to the account owners.
### Department spending quota alerts
Department spending quota alerts notify you when department spending reaches a fixed threshold of the quota. Spending quotas are configured in the EA portal. Whenever a threshold is met, it generates an email to department owners, and appears in cost alerts. For example, 50 percent or 75 percent of the quota.
## Budgets
A budget is where you set a spending limit for Azure. You can set budgets based on a subscription, resource group, service type, or other criteria. When you set a budget, you will also set a budget alert. When the budget hits the budget alert level, it will trigger a budget alert that shows up in the cost alerts area. If configured, budget alerts will also send an email notification that a budget alert threshold has been triggered.
A more advanced use of budgets enables budget conditions to trigger automation that suspends or otherwise modifies resources once the trigger condition has occurred.

## 1.6 Describe the purpose of tags

# Describe the purpose of tags
As your cloud usage grows, it's increasingly important to stay organized. A good organization strategy helps you understand your cloud usage and can help you manage costs.
One way to organize related resources is to place them in their own subscriptions. You can also use resource groups to manage related resources. Resource tags are another way to organize resources. Tags provide extra information, or metadata, about your resources. This metadata is useful for:
- Resource management Tags enable you to locate and act on resources that are associated with specific workloads, environments, business units, and owners.
- Cost management and optimization Tags enable you to group resources so that you can report on costs, allocate internal cost centers, track budgets, and forecast estimated cost.
- Operations management Tags enable you to group resources according to how critical their availability is to your business. This grouping helps you formulate service-level agreements (SLAs). An SLA is an uptime or performance guarantee between you and your users.
- Security Tags enable you to classify data by its security level, such as public or confidential.
- Governance and regulatory compliance Tags enable you to identify resources that align with governance or regulatory compliance requirements, such as ISO 27001. Tags can also be part of your standards enforcement efforts. For example, you might require that all resources be tagged with an owner or department name.
- Workload optimization and automation Tags can help you visualize all of the resources that participate in complex deployments. For example, you might tag a resource with its associated workload or application name and use software such as Azure DevOps to perform automated tasks on those resources.
## How do I manage resource tags?
You can add, modify, or delete resource tags through Windows PowerShell, the Azure CLI, Azure Resource Manager templates, the REST API, or the Azure portal.
You can use Azure Policy to enforce tagging rules and conventions. For example, you can require that certain tags be added to new resources as they're provisioned. You can also define rules that reapply tags that have been removed. Resources don't inherit tags from subscriptions and resource groups, meaning that you can apply tags at one level and not have those tags automatically show up at a different level, allowing you to create custom tagging schemas that change depending on the level (resource, resource group, subscription, and so on).
### An example tagging structure
A resource tag consists of a name and a value. You can assign one or more tags to each Azure resource.
Name 
Value 
AppName 
The name of the application that the resource is part of. 
CostCenter 
The internal cost center code. 
Owner 
The name of the business owner who's responsible for the resource. 
Environment 
An environment name, such as "Prod," "Dev," or "Test." 
Impact 
How important the resource is to business operations, such as "Mission-critical," "High-impact," or "Low-impact." 
Keep in mind that you don't need to enforce that a specific tag is present on all of your resources. For example, you might decide that only mission-critical resources have the Impact tag. All non-tagged resources would then not be considered as mission-critical.

## 1.8 Summary

# Summary
, you learned about factors that impact costs in Azure and tools to help you both predict potential costs and monitor and control costs.
## Learning objectives
You should now be able to:
- Describe factors that can affect costs in Azure.
- Compare the Pricing calculator and Total Cost of Ownership (TCO) calculator.
- Describe the Microsoft Cost Management Tool.
- Describe the purpose of tags.
## Additional resources
The following resources provide more information on topics or related to this module.
- Control Azure spending and manage bills with Microsoft Cost Management + Billing is a learning path designed to give you a deeper understanding of cost management tools and strategies in Azure.

---

# Module 2: Describe features and tools in Azure for governance and compliance

Describe features and tools in Azure for governance and compliance

## 2.1 Introduction

# Introduction
, you’ll be introduced to some of the features and tools you can use to help with governance of your Azure environment. You’ll also learn about tools you can use to help keep resources in compliance with corporate or regulatory requirements.
## Learning objectives
After completing this module, you’ll be able to:
- Describe the purpose of Microsoft Purview.
- Describe the purpose of Azure Policy.
- Describe the purpose of resource locks.
- Describe the purpose of the Service Trust portal.

## 2.2 Describe the purpose of Microsoft Purview

# Describe the purpose of Microsoft Purview
Microsoft Purview is a family of data governance, risk, and compliance solutions that helps you get a single, unified view into your data. Microsoft Purview brings insights about your on-premises, multicloud, and software-as-a-service data together.
With Microsoft Purview, you can stay up-to-date on your data landscape thanks to:
- Automated data discovery
- Sensitive data classification
- End-to-end data lineage
Two main solution areas comprise Microsoft Purview: risk and compliance and unified data governance .
Microsoft Purview risk and compliance solutions
Microsoft 365 features as a core component of the Microsoft Purview risk and compliance solutions. Microsoft Teams, OneDrive, and Exchange are just some of the Microsoft 365 services that Microsoft Purview uses to help manage and monitor your data. Microsoft Purview, by managing and monitoring your data, is able to help your organization:
- Protect sensitive data across clouds, apps, and devices.
- Identify data risks and manage regulatory compliance requirements.
- Get started with regulatory compliance.
Unified data governance
Microsoft Purview has robust, unified data governance solutions that help manage your on-premises, multicloud, and software as a service data. Microsoft Purview’s robust data governance capabilities enable you to manage your data stored in Azure, SQL and Hive databases, locally, and even in other clouds like Amazon S3.
Microsoft Purview’s unified data governance helps your organization:
- Create an up-to-date map of your entire data estate that includes data classification and end-to-end lineage.
- Identify where sensitive data is stored in your estate.
- Create a secure environment for data consumers to find valuable data.
- Generate insights about how your data is stored and used.
- Manage access to the data in your estate securely and at scale.

## 2.3 Describe the purpose of Azure Policy

# Describe the purpose of Azure Policy
How do you ensure that your resources stay compliant? Can you be alerted if a resource's configuration has changed?
Azure Policy is a service in Azure that enables you to create, assign, and manage policies that control or audit your resources. These policies enforce different rules across your resource configurations so that those configurations stay compliant with corporate standards.
## How does Azure Policy define policies?
Azure Policy enables you to define both individual policies and groups of related policies, known as initiatives. Azure Policy evaluates your resources and highlights resources that aren't compliant with the policies you've created. Azure Policy can also prevent noncompliant resources from being created.
Azure Policies can be set at each level, enabling you to set policies on a specific resource, resource group, subscription, and so on. Additionally, Azure Policies are inherited, so if you set a policy at a high level, it will automatically be applied to all of the groupings that fall within the parent. For example, if you set an Azure Policy on a resource group, all resources created within that resource group will automatically receive the same policy.
Azure Policy comes with built-in policy and initiative definitions for Storage, Networking, Compute, Security Center, and Monitoring. For example, if you define a policy that allows only a certain size for the virtual machines (VMs) to be used in your environment, that policy is invoked when you create a new VM and whenever you resize existing VMs. Azure Policy also evaluates and monitors all current VMs in your environment, including VMs that were created before the policy was created.
In some cases, Azure Policy can automatically remediate noncompliant resources and configurations to ensure the integrity of the state of the resources. For example, if all resources in a certain resource group should be tagged with AppName tag and a value of "SpecialOrders," Azure Policy will automatically apply that tag if it is missing. However, you still retain full control of your environment. If you have a specific resource that you don’t want Azure Policy to automatically fix, you can flag that resource as an exception – and the policy won’t automatically fix that resource.
Azure Policy also integrates with Azure DevOps by applying any continuous integration and delivery pipeline policies that pertain to the pre-deployment and post-deployment phases of your applications.
## What are Azure Policy initiatives?
An Azure Policy initiative is a way of grouping related policies together. The initiative definition contains all of the policy definitions to help track your compliance state for a larger goal.
For example, Azure Policy includes an initiative named Enable Monitoring in Azure Security Center. Its goal is to monitor all available security recommendations for all Azure resource types in Azure Security Center.
Under this initiative, the following policy definitions are included:
- Monitor unencrypted SQL Database in Security Center This policy monitors for unencrypted SQL databases and servers.
- Monitor OS vulnerabilities in Security Center This policy monitors servers that don't satisfy the configured OS vulnerability baseline.
- Monitor missing Endpoint Protection in Security Center This policy monitors for servers that don't have an installed endpoint protection agent.
In fact, the Enable Monitoring in Azure Security Center initiative contains over 100 separate policy definitions.

## 2.4 Describe the purpose of resource locks

# Describe the purpose of resource locks
A resource lock prevents resources from being accidentally deleted or changed.
Even with Azure role-based access control (Azure RBAC) policies in place, there's still a risk that people with the right level of access could delete critical cloud resources. Resource locks prevent resources from being deleted or updated, depending on the type of lock. Resource locks can be applied to individual resources, resource groups, or even an entire subscription. Resource locks are inherited, meaning that if you place a resource lock on a resource group, all of the resources within the resource group will also have the resource lock applied.
## Types of Resource Locks
There are two types of resource locks, one that prevents users from deleting and one that prevents users from changing or deleting a resource.
- Delete means authorized users can still read and modify a resource, but they can't delete the resource.
- ReadOnly means authorized users can read a resource, but they can't delete or update the resource. Applying this lock is similar to restricting all authorized users to the permissions granted by the Reader role.
## How do I manage resource locks?
You can manage resource locks from the Azure portal, PowerShell, the Azure CLI, or from an Azure Resource Manager template.
To view, add, or delete locks in the Azure portal, go to the Locks section of any resource's Settings pane in the Azure portal.
## How do I delete or change a locked resource?
Although locking helps prevent accidental changes, you can still make changes by following a two-step process.
To modify a locked resource, you must first remove the lock. After you remove the lock, you can apply any action you have permissions to perform. Resource locks apply regardless of RBAC permissions. Even if you're an owner of the resource, you must still remove the lock before you can perform the blocked activity.

## 2.5 Exercise - Configure a resource lock

# Exercise - Configure a resource lock
In this exercise, you create a resource and configure a resource lock. Storage accounts are one of the easiest types of resource locks to quickly see the impact, so you use a storage account for this exercise.
This exercise is a Bring your own subscription exercise, meaning you need to provide your own Azure subscription to complete the exercise. Don’t worry though, the entire exercise can be for free with the 12 month free services when you for an Azure account.
For help with signing up for an Azure account, see the Create an Azure account learning module.
Once you’ve created your free account, follow the steps below. If you don’t have an Azure account, you can review the steps to see the process for adding a simple resource lock to a resource.
## Task 1: Create a resource
In order to apply a resource lock, you have to have a resource created in Azure. The first task focuses on creating a resource that you can then lock in subsequent tasks.
- to the Azure portal at https://portal.azure.com 
- Select Create a resource.
- Under Infrastructure Services, select Storage.
- Under Storage Account, select Create.
- On the Basics tab of the Create storage account blade, fill in the following information. Leave the defaults for everything else.
Setting 
Value 
Resource group 
Create new 
Storage account name 
enter a unique storage account name 
Location 
default 
Performance 
Standard 
Redundancy 
Locally redundant storage (LRS) 
- Select Review + Create to review your storage account settings and allow Azure to validate the configuration.
- Once validated, select Create. Wait for the notification that the account was successfully created.
- Select Go to resource.
## Task 2: Apply a read-only resource lock
In this task you apply a read-only resource lock to the storage account. What impact do you think that has on the storage account?
- Scroll down until you find the Settings section of the blade on the left of the screen.
- Select Locks.
- Select + Add.
- Enter a Lock name.
- Verify the Lock type is set to Read-only.
- Select OK.
## Task 3: Add a container to the storage account
In this task, you add a container to the storage account. This container is where you can store your blobs.
- Scroll up until you find the Data storage section of the blade on the left of the screen.
- Select Containers.
- Select + Container.
- Enter a container name and select Create.
- You should receive an error message: Failed to create storage container.
Note
The error message lets you know that you couldn't create a storage container because a lock is in place. The read-only lock prevents any create or update operations on the storage account, so you're unable to create a storage container.
## Task 4: Modify the resource lock and create a storage container
- Scroll down until you find the Settings section of the blade on the left of the screen.
- Select Locks.
- Select the read-only resource lock you created.
- Change the Lock type to Delete and select OK.
- Scroll up until you find the Data storage section of the blade on the left of the screen.
- Select Containers.
- Select + Container.
- Enter a container name and select Create.
- Your storage container should appear in your list of containers.
You can now understand how the read-only lock prevented you from adding a container to your storage account. Once the lock type was changed (you could have removed it instead), you were able to add a container.
## Task 5: Delete the storage account
You'll actually do this last task twice. Remember that there's a delete lock on the storage account, so you won't actually be able to delete the storage account yet.
- Scroll up until you find Overview at the top of the blade on the left of the screen.
- Select Overview.
- Select Delete.
You should get a notification letting you know you can't delete the resource because it has a delete lock. In order to delete the storage account, you need to remove the delete lock.
## Task 6: Remove the delete lock and delete the storage account
In the final task, you remove the resource lock and delete the storage account from your Azure account. This step is important. You want to make sure you don't have any idle resource just sitting in your account.
- Select your storage account name in the breadcrumb at the top of the screen.
- Scroll down until you find the Settings section of the blade on the left of the screen.
- Select Locks.
- Select Delete.
- Select Home in the breadcrumb at the top of the screen.
- Select Storage accounts
- Select the storage account you used for this exercise.
- Select Delete.
- To prevent accidental deletion, Azure prompts you to enter the name of the storage account you want to delete. Enter the name of the storage account and select Delete.
- You should receive a message that the storage account was deleted. If you go Home &gt; Storage accounts, you should see that the storage account you created for this exercise is gone.
Congratulations!

## 2.6 Describe the purpose of the Service Trust portal

# Describe the purpose of the Service Trust portal
The Microsoft Service Trust Portal is a portal that provides access to various content, tools, and other resources about Microsoft security, privacy, and compliance practices.
The Service Trust Portal contains details about Microsoft's implementation of controls and processes that protect our cloud services and the customer data therein. To access some of the resources on the Service Trust Portal, you must as an authenticated user with your Microsoft cloud services account (Microsoft Entra organization account). You'll need to review and accept the Microsoft non-disclosure agreement for compliance materials.
## Accessing the Service Trust Portal
You can access the Service Trust Portal at https://servicetrust.microsoft.com/ .
The Service Trust Portal features and content are accessible from the main menu. The categories on the main menu are:
- Service Trust Portal provides a quick access hyperlink to return to the Service Trust Portal home page.
- My Library lets you save (or pin) documents to quickly access them on your My Library page. You can also set up to receive notifications when documents in your My Library are updated.
- All Documents is a single landing place for documents on the service trust portal. From All Documents , you can pin documents to have them show up in your My Library .
Note
Service Trust Portal reports and documents are available to download for at least 12 months after publishing or until a new version of document becomes available.

## 2.8 Summary

# Summary
, you learned about some of the features and tools you can use to help with governance of your Azure environment. You also learned about tools you can use to help keep resources in compliance with corporate or regulatory requirements.
## Learning objectives
You should now be able to:
- Describe the purpose of Microsoft Purview.
- Describe the purpose of Azure Policy.
- Describe the purpose of resource locks.
- Describe the purpose of the Service Trust portal.
## Additional resources
The following resources provide more information on topics or related to this module.
- Intro to Azure Policy is a Microsoft Learn module that introduces you further to Azure Policy.

---

# Module 3: Describe features and tools for managing and deploying Azure resources

This module discusses tools and features that assist in managing and deploying resources within Azure.

## 3.1 Introduction

# Introduction
This module introduces you to features and tools for managing and deploying Azure resources. You learn about the Azure portal (a graphic interface for managing Azure resources), the command line, and scripting tools that help deploy or configure resources. You also learn about Azure services that help you manage your on-premises and multicloud environments from within Azure.
## Learning objectives
After completing this module, you’ll be able to:
- Describe the Azure portal.
- Describe Azure Cloud Shell, including Azure CLI and Azure PowerShell.
- Describe the purpose of Azure Arc.
- Describe Azure Resource Manager (ARM), ARM templates, and Bicep.

## 3.2 Describe tools for interacting with Azure

# Describe tools for interacting with Azure
To get the most out of Azure, you need a way to interact with the Azure environment, the management groups, subscriptions, resource groups, resources, and so on. Azure provides multiple tools for managing your environment, including the:
- Azure portal
- Azure PowerShell
- Azure Command Line Interface (CLI)
## What is the Azure portal?
The Azure portal is a web-based, unified console that provides an alternative to command-line tools. With the Azure portal, you can manage your Azure subscription by using a graphical user interface. You can:
- Build, manage, and monitor everything from simple web apps to complex cloud deployments
- Create custom dashboards for an organized view of resources
- Configure accessibility options for an optimal experience
The following video introduces you to the Azure portal:
The Azure portal is designed for resiliency and continuous availability. It maintains a presence in every Azure datacenter. This configuration makes the Azure portal resilient to individual datacenter failures and avoids network slowdowns by being close to users. The Azure portal updates continuously and requires no downtime for maintenance activities.
### Azure Cloud Shell
Azure Cloud Shell is a browser-based shell tool that allows you to create, configure, and manage Azure resources using a shell. Azure Cloud Shell support both Azure PowerShell and the Azure Command Line Interface (CLI), which is a Bash shell.
You can access Azure Cloud Shell via the Azure portal by selecting the Cloud Shell icon:
Azure Cloud Shell has several features that make it a unique offering to support you in managing Azure. Some of those features are:
- It is a browser-based shell experience, with no local installation or configuration required.
- It is authenticated to your Azure credentials, so when you log in it inherently knows who you are and what permissions you have.
- You choose the shell you’re most familiar with; Azure Cloud Shell supports both Azure PowerShell and the Azure CLI (which uses Bash).
## What is Azure PowerShell?
Azure PowerShell is a shell with which developers, DevOps, and IT professionals can run commands called command-lets (cmdlets). These commands call the Azure REST API to perform management tasks in Azure. Cmdlets can be run independently to handle one-off changes, or they may be combined to help orchestrate complex actions such as:
- The routine setup, teardown, and maintenance of a single resource or multiple connected resources.
- The deployment of an entire infrastructure, which might contain dozens or hundreds of resources, from imperative code.
Capturing the commands in a script makes the process repeatable and automatable.
In addition to be available via Azure Cloud Shell, you can install and configure Azure PowerShell on Windows, Linux, and Mac platforms.
## What is the Azure CLI?
The Azure CLI is functionally equivalent to Azure PowerShell, with the primary difference being the syntax of commands. While Azure PowerShell uses PowerShell commands, the Azure CLI uses Bash commands.
The Azure CLI provides the same benefits of handling discrete tasks or orchestrating complex operations through code. It’s also installable on Windows, Linux, and Mac platforms, as well as through Azure Cloud Shell.
Due to the similarities in capabilities and access between Azure PowerShell and the Bash based Azure CLI, it mainly comes down to which language you’re most familiar with.

## 3.3 Describe the purpose of Azure Arc

# Describe the purpose of Azure Arc
Managing hybrid and multi-cloud environments can rapidly get complicated. Azure provides a host of tools to provision, configure, and monitor Azure resources. What about the on-premises resources in a hybrid configuration or the cloud resources in a multi-cloud configuration?
In utilizing Azure Resource Manager (ARM), Arc lets you extend your Azure compliance and monitoring to your hybrid and multi-cloud configurations. Azure Arc simplifies governance and management by delivering a consistent multi-cloud and on-premises management platform.
Azure Arc provides a centralized, unified way to:
- Manage your entire environment together by projecting your existing non-Azure resources into ARM.
- Manage multi-cloud and hybrid virtual machines, Kubernetes clusters, and databases as if they are running in Azure.
- Use familiar Azure services and management capabilities, regardless of where they live.
- Continue using traditional ITOps while introducing DevOps practices to support new cloud and native patterns in your environment.
- Configure custom locations as an abstraction layer on top of Azure Arc-enabled Kubernetes clusters and cluster extensions.
## What can Azure Arc do outside of Azure?
Currently, Azure Arc allows you to manage the following resource types hosted outside of Azure:
- Servers
- Kubernetes clusters
- Azure data services
- SQL Server
- Virtual machines (preview)

## 3.4 Describe Azure Resource Manager and Azure ARM templates

# Describe Azure Resource Manager and Azure ARM templates
Azure Resource Manager (ARM) is the deployment and management service for Azure. It provides a management layer that enables you to create, update, and delete resources in your Azure account. Anytime you do anything with your Azure resources, ARM is involved.
When a user sends a request from any of the Azure tools, APIs, or SDKs, ARM receives the request. ARM authenticates and authorizes the request. Then, ARM sends the request to the Azure service, which takes the requested action. You see consistent results and capabilities in all the different tools because all requests are handled through the same API.
## Azure Resource Manager benefits
With Azure Resource Manager, you can:
- Manage your infrastructure through declarative templates rather than scripts. A Resource Manager template is a JSON file that defines what you want to deploy to Azure.
- Deploy, manage, and monitor all the resources for your solution as a group, rather than handling these resources individually.
- Re-deploy your solution throughout the development life-cycle and have confidence your resources are deployed in a consistent state.
- Define the dependencies between resources, so they're deployed in the correct order.
- Apply access control to all services because RBAC is natively integrated into the management platform.
- Apply tags to resources to logically organize all the resources in your subscription.
- Clarify your organization's billing by viewing costs for a group of resources that share the same tag.
The following video provides an overview of Azure Resource Manager.
## Infrastructure as code
Infrastructure as code is a concept where you manage your infrastructure as lines of code. At an introductory level, it's things like using Azure Cloud Shell, Azure PowerShell, or the Azure CLI to manage and configure your resources. As you get more comfortable in the cloud, you can use the infrastructure as code concept to manage entire deployments using repeatable templates and configurations. ARM templates and Bicep are two examples of using infrastructure as code with the Azure Resource Manager to maintain your environment.
### ARM templates
By using ARM templates, you can describe the resources you want to use in a declarative JSON format. With an ARM template, the deployment code is verified before any code is run. This ensures that the resources will be created and connected correctly. The template then orchestrates the creation of those resources in parallel. That is, if you need 50 instances of the same resource, all 50 instances are created at the same time.
Ultimately, the developer, DevOps professional, or IT professional needs only to define the desired state and configuration of each resource in the ARM template, and the template does the rest. Templates can even execute PowerShell and Bash scripts before or after the resource has been set up.
### Benefits of using ARM templates
ARM templates provide many benefits when planning for deploying Azure resources. Some of those benefits include:
- Declarative syntax : ARM templates allow you to create and deploy an entire Azure infrastructure declaratively. Declarative syntax means you declare what you want to deploy but don’t need to write the actual programming commands and sequence to deploy the resources.
- Repeatable results : Repeatedly deploy your infrastructure throughout the development lifecycle and have confidence your resources are deployed in a consistent manner. You can use the same ARM template to deploy multiple dev/test environments, knowing that all the environments are the same.
- Orchestration : You don't have to worry about the complexities of ordering operations. Azure Resource Manager orchestrates the deployment of interdependent resources, so they're created in the correct order. When possible, Azure Resource Manager deploys resources in parallel, so your deployments finish faster than serial deployments. You deploy the template through one command, rather than through multiple imperative commands.
- Modular files : You can break your templates into smaller, reusable components and link them together at deployment time. You can also nest one template inside another template. For example, you could create a template for a VM stack, and then nest that template inside of templates that deploy entire environments, and that VM stack will consistently be deployed in each of the environment templates.
- Extensibility : With deployment scripts, you can add PowerShell or Bash scripts to your templates. The deployment scripts extend your ability to set up resources during deployment. A script can be included in the template or stored in an external source and referenced in the template. Deployment scripts give you the ability to complete your end-to-end environment setup in a single ARM template.
### Bicep
Bicep is a language that uses declarative syntax to deploy Azure resources. A Bicep file defines the infr

## 3.6 Summary

# Summary
, you were introduced to features and tools for managing and deploying Azure resources. You learned about the Azure portal (a graphic interface for managing Azure resources), command line, and scripting tools that help deploy or configure resources. You also learned about Azure services that help you manage your on-premises and multicloud environment from Azure.
## Learning objectives
You should now be able to:
- Describe Azure portal.
- Describe Azure Cloud Shell, including Azure CLI and Azure PowerShell.
- Describe the purpose of Azure Arc.
- Describe Azure Resource Manager (ARM), ARM templates, and Bicep.
## Additional resources
The following resources provide more information on topics or related to this module.
- Implement resource management security in Azure is a Microsoft Learn learning path that provides more information on managing Azure resources.

---

# Module 4: Describe monitoring tools in Azure

Describe monitoring tools in Azure

## 4.1 Introduction

# Introduction
, you’ll be introduced to tools that help you monitor your environment and applications, both in Azure and in on-premises or multicloud environments.
## Learning objectives
After completing this module, you’ll be able to:
- Describe the purpose of Azure Advisor.
- Describe Azure Service Health.
- Describe Azure Monitor, including Azure Log Analytics, Azure Monitor Alerts, and Application Insights.

## 4.2 Describe the purpose of Azure Advisor

# Describe the purpose of Azure Advisor
Azure Advisor evaluates your Azure resources and makes recommendations to help improve reliability, security, and performance, achieve operational excellence, and reduce costs. Azure Advisor is designed to help you save time on cloud optimization. The recommendation service includes suggested actions you can take right away, postpone, or dismiss.
The recommendations are available via the Azure portal and the API, and you can set up notifications to alert you to new recommendations.
When you're in the Azure portal, the Advisor dashboard displays personalized recommendations for all your subscriptions. You can use filters to select recommendations for specific subscriptions, resource groups, or services. The recommendations are divided into five categories:
- Reliability is used to ensure and improve the continuity of your business-critical applications.
- Security is used to detect threats and vulnerabilities that might lead to security breaches.
- Performance is used to improve the speed of your applications.
- Operational Excellence is used to help you achieve process and workflow efficiency, resource manageability, and deployment best practices.
- Cost is used to optimize and reduce your overall Azure spending.
The following image shows the Azure Advisor dashboard.

## 4.3 Describe Azure Service Health

# Describe Azure Service Health
Microsoft Azure provides a global cloud solution to help you manage your infrastructure needs, reach your customers, innovate, and adapt rapidly. Knowing the status of the global Azure infrastructure and your individual resources may seem like a daunting task. Azure Service Health helps you keep track of Azure resource, both your specifically deployed resources and the overall status of Azure. Azure service health does this by combining three different Azure services:
- Azure Status is a broad picture of the status of Azure globally. Azure status informs you of service outages in Azure on the Azure Status page. The page is a global view of the health of all Azure services across all Azure regions. It’s a good reference for incidents with widespread impact.
- Service Health provides a narrower view of Azure services and regions. It focuses on the Azure services and regions you're using. This is the best place to look for service impacting communications about outages, planned maintenance activities, and other health advisories because the authenticated Service Health experience knows which services and resources you currently use. You can even set up Service Health alerts to notify you when service issues, planned maintenance, or other changes may affect the Azure services and regions you use.
- Resource Health is a tailored view of your actual Azure resources. It provides information about the health of your individual cloud resources, such as a specific virtual machine instance. Using Azure Monitor, you can also configure alerts to notify you of availability changes to your cloud resources.
By using Azure status, Service health, and Resource Health, Azure Service Health gives you a complete view of your Azure environment-all the way from the global status of Azure services and regions down to specific resources. Additionally, historical alerts are stored and accessible for later review. Something you initially thought was a simple anomaly that turned into a trend, can readily be reviewed and investigated thanks to the historical alerts.
Finally, in the event that a workload you’re running is impacted by an event, Azure Service Health provides links to support.

## 4.4 Describe Azure Monitor

# Describe Azure Monitor
Azure Monitor is a platform for collecting data on your resources, analyzing that data, visualizing the information, and even acting on the results. Azure Monitor can monitor Azure resources, your on-premises resources, and even multi-cloud resources like virtual machines hosted with a different cloud provider.
The following diagram illustrates just how comprehensive Azure Monitor is:
On the left is a list of the sources of logging and metric data that can be collected at every layer in your application architecture, from application to operating system and network.
In the center, the logging and metric data are stored in central repositories.
On the right, the data is used in several ways. You can view real-time and historical performance across each layer of your architecture or aggregated and detailed information. The data is displayed at different levels for different audiences. You can view high-level reports on the Azure Monitor Dashboard or create custom views by using Power BI and Kusto queries.
Additionally, you can use the data to help you react to critical events in real time, through alerts delivered to teams via SMS, email, and so on. Or you can use thresholds to trigger autoscaling functionality to scale to meet the demand.
## Azure Log Analytics
Azure Log Analytics is the tool in the Azure portal where you’ll write and run log queries on the data gathered by Azure Monitor. Log Analytics is a robust tool that supports both simple, complex queries, and data analysis. You can write a simple query that returns a set of records and then use features of Log Analytics to sort, filter, and analyze the records. You can write an advanced query to perform statistical analysis and visualize the results in a chart to identify a particular trend. Whether you work with the results of your queries interactively or use them with other Azure Monitor features such as log query alerts or workbooks, Log Analytics is the tool that you're going to use to write and test those queries.
## Azure Monitor Alerts
Azure Monitor Alerts are an automated way to stay informed when Azure Monitor detects a threshold being crossed. You set the alert conditions, the notification actions, and then Azure Monitor Alerts notifies when an alert is triggered. Depending on your configuration, Azure Monitor Alerts can also attempt corrective action.
Alerts can be set up to monitor the logs and trigger on certain log events, or they can be set to monitor metrics and trigger when certain metrics are crossed. For example, you could set a metric-based alert up to notify you when the CPU usage on a virtual machine exceeded 80%. Alert rules based on metrics provide near real time alerts based on numeric values. Rules based on logs allow for complex logic across data from multiple sources.
Azure Monitor Alerts use action groups to configure who to notify and what action to take. An action group is simply a collection of notification and action preferences that you associate with one or multiple alerts. Azure Monitor, Service Health, and Azure Advisor all use actions groups to notify you when an alert has been triggered.
## Application Insights
Application Insights, an Azure Monitor feature, monitors your web applications. Application Insights is capable of monitoring applications that are running in Azure, on-premises, or in a different cloud environment.
There are two ways to configure Application Insights to help monitor your application. You can either install an SDK in your application, or you can use the Application Insights agent. The Application Insights agent is supported in C#.NET, VB.NET, Java, JavaScript, Node.js, and Python.
Once Application Insights is up and running, you can use it to monitor a broad array of information, such as:
- Request rates, response times, and failure rates
- Dependency rates, response times, and failure rates, to show whether external services are slowing down performance
- Page views and load performance reported by users' browsers
- AJAX calls from web pages, including rates, response times, and failure rates
- User and session counts
- Performance counters from Windows or Linux server machines, such as CPU, memory, and network usage
Not only does Application Insights help you monitor the performance of your application, but you can also configure it to periodically send synthetic requests to your application, allowing you to check the status and monitor your application even during periods of low activity.

## 4.6 Summary

# Summary
, you were introduced to tools that help you monitor your environment and applications, both in Azure and in on-premises or multicloud environments.
## Learning objectives
You should now be able to:
- Describe the purpose of Azure Advisor.
- Describe Azure Service Health.
- Describe Azure Monitor, including Azure Log Analytics, Azure Monitor Alerts, and Application Insights.
## Additional resources
The following additional resources are intended to provide more information on topics or on additional topics related to this module.
- Get started with Azure Advisor is a Microsoft Learn module that helps you get started with Azure Advisor.
- Intro to Azure Service Health is a Microsoft Learn module that provides additional information about Azure Service Health.
- Monitor the usage, performance, and availability of resources with Azure Monitor is a Microsoft Learn learning path that dives deeper into Azure Monitor. It provides helpful guidance on setting up and getting the most from the Azure Monitor service.

---

# Key Concepts Index

- (OS Only)
- 1 TB
- 5 GB
- 730 Hours
- 8 vCore
- All Documents
- Application Gateway
- Azure Status
- Category
- Cost
- Cost management and optimization
- Declarative syntax
- Export
- Extensibility
- Gen 5
- Governance and regulatory compliance
- Modular files
- Modularity
- Monitor OS vulnerabilities in Security Center
- Monitor missing Endpoint Protection in Security Center
- Monitor unencrypted SQL Database in Security Center
- My Library
- Name
- Operational Excellence
- Operations management
- Orchestration
- Performance
- Products
- RA-GRS
- Reliability
- Repeatable results
- Resource Health
- Resource management
- Save
- Save as
- Saved Estimates
- Security
- Service Health
- Service Trust Portal
- Setting
- Simple syntax
- Single Database
- Standard
- Support for all resource types and API versions
- Value
- Virtual Machines
- West US
- Windows
- Workload optimization and automation
- risk and compliance
