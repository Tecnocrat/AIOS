# Introduction to Cloud Infrastructure: Describe Azure Architecture and Services

**Source**: https://learn.microsoft.com/en-us/training/paths/azure-fundamentals-describe-azure-architecture-services/
**Level**: Beginner
**Modules**: 4
**Total Units**: 43

## Overview

Architecture and services component of the Introduction to Cloud Infrastructure training

---

# Module 1: Describe the core architectural components of Azure

Describe the core architectural components of Azure

## 1.1 Introduction

# Introduction
, you’ll be introduced to the core architectural components of Azure. You’ll learn about the physical organization of Azure: datacenters, availability zones, and regions; and you’ll learn about the organizational structure of Azure: resources and resource groups, subscriptions, and management groups.
## Learning objectives
After completing this module, you’ll be able to:
- Describe Azure regions, region pairs, and sovereign regions.
- Describe Availability Zones.
- Describe Azure datacenters.
- Describe Azure resources and Resource Groups.
- Describe subscriptions.
- Describe management groups.
- Describe the hierarchy of resource groups, subscriptions, and management groups.

## 1.2 What is Microsoft Azure

# What is Microsoft Azure
Azure is a continually expanding set of cloud services that help you meet current and future business challenges. Azure gives you the freedom to build, manage, and deploy applications on a massive global network using your favorite tools and frameworks.
## What does Azure offer?
Limitless innovation. Build intelligent apps and solutions with advanced technology, tools, and services to take your business to the level. Seamlessly unify your technology to simplify platform management and to deliver innovations efficiently and securely on a trusted cloud.
- Bring ideas to life: Build on a trusted platform to advance your organization with industry-leading AI and cloud services.
- Seamlessly unify: Efficiently manage all your infrastructure, data, analytics, and AI solutions across an integrated platform.
- Innovate on trust: Rely on trusted technology from a partner who's dedicated to security and responsibility.
## What can I do with Azure?
Azure provides more than 100 services that enable you to do everything from running your existing applications on virtual machines to exploring new software paradigms, such as intelligent bots and mixed reality.
Many teams start exploring the cloud by moving their existing applications to virtual machines (VMs) that run in Azure. Migrating your existing apps to VMs is a good start, but the cloud is much more than a different place to run your VMs.
For example, Azure provides artificial intelligence (AI) and machine-learning (ML) services that can naturally communicate with your users through vision, hearing, and speech. It also provides storage solutions that dynamically grow to accommodate massive amounts of data. Azure services enable solutions that aren't feasible without the power of the cloud.

## 1.3 Get started with Azure accounts

# Get started with Azure accounts
To create and use Azure services, you need an Azure subscription. When you're working with your own applications and business needs, you need to create an Azure account, and a subscription will be created for you. After you've created an Azure account, you're free to create additional subscriptions. For example, your company might use a single Azure account for your business and separate subscriptions for development, marketing, and sales departments. After you've created an Azure subscription, you can start creating Azure resources within each subscription.
If you're new to Azure, you can for a free account on the Azure website to start exploring at no cost to you. When you're ready, you can choose to upgrade your free account. You can also create a new subscription that enables you to start paying for Azure services you need beyond the limits of a free account.
## Create an Azure account
You can purchase Azure access directly from Microsoft by signing up on the Azure website or through a Microsoft representative. You can also purchase Azure access through a Microsoft partner. Cloud Solution Provider partners offer a range of complete managed-cloud solutions for Azure.
### What is the Azure free account?
The Azure free account includes:
- Free access to popular Azure products for 12 months.
- A credit to use for the first 30 days.
- Access to more than 25 products that are always free.
The Azure free account is an excellent way for new users to get started and explore. To , you need a phone number, a credit card, and a Microsoft or GitHub account. The credit card information is used for identity verification only. You won't be charged for any services until you upgrade to a paid subscription.
### What is the Azure free student account?
The Azure free student account offer includes:
- Free access to certain Azure services for 12 months.
- A credit to use in the first 12 months.
- Free access to certain software developer tools.
The Azure free student account is an offer for students that gives $100 credit and free developer tools. Also, you can without a credit card.
Most of the exercises in the Introduction to Azure learning paths and modules are bring your own subscription (BYOS). BYOS requires you to have a subscription to complete the exercise.
Each exercise has a clean up step at the end. It's important to complete the clean up step in order to avoid unanticipated Azure costs.

## 1.4 Exercise - Explore Interacting with Azure

# Exercise - Explore interacting with Azure
In this exercise, you explore ways to interact with Microsoft Azure. You can interact with Azure in different ways, including through the web portal or using the Azure command line interface (CLI) with PowerShell or Bash commands.
## Access the Azure Portal
The Azure portal provides a graphic user interface (GUI) to interact with Azure services. You can navigate to different service areas, manage subscriptions and accounts, search for specific services or settings, and so on.
The Azure portal is accessed at https://portal.azure.com 
Once you're logged into the portal, you can navigate around Azure using the interface, or you can use the command line interface with PowerShell and BASH commands.
## Use the command line interface
You can use the CLI from within the Azure portal. Once logged into Azure, access the CLI by selecting the Cloud Shell icon. Launching Cloud Shell brings up a CLI window in PowerShell or BASH mode. If you’re familiar with PowerShell, you can manage your Azure environment using PowerShell commands.
To access CloudShell from the Azure portal, select the CloudShell icon.
You can quickly change between PowerShell and BASH in the CLI by selecting the Switch to ... button or entering BASH or PWSH .
Tip
When in PowerShell mode, the command line starts with PS. When in BASH mode, the command line starts with your user name@azure.
### Use PowerShell in the CLI
Use the PowerShell Get-date command to get the current date and time.
The Get-date command is a PowerShell specific command. Most Azure specific commands start with the letters az . Let's try an Azure command to check what version of the CLI you're using right now.
az version
### Use BASH in the CLI
If you’re more familiar with BASH, you can use BASH commands instead by shifting to the BASH CLI.
Enter bash to switch to the BASH CLI.
Tip
You can tell you're in BASH mode by the username displayed on the command line, your username@azure.
Again, use the Get-date command to get the current date and time.
You received an error because Get-date is a PowerShell specific command.
Use the date command to get the current date and time.
Just like in the PowerShell mode of the CLI, use the letters az to start an Azure command in the BASH mode. Try to run an update to the CLI with az upgrade .
You can change back to PowerShell mode by entering pwsh on the BASH command line.
## Use Azure CLI interactive mode
Another way to interact is using the Azure CLI interactive mode. This changes CLI behavior to more closely resemble an integrated development environment (IDE). Interactive mode provides autocompletion, command descriptions, and even examples. If you’re unfamiliar with BASH and PowerShell, but want to use the command line, interactive mode may help you.
Enter az interactive to enter interactive mode.
Decide whether you wish to send telemetry data and enter YES or NO .
You may have to wait a minute or two to allow the interactive mode to fully initialize. Then, enter the letter “a” and auto-completion should start to work. If auto-completion isn’t working, wait a bit longer and try again.
Once initialized, you can use the arrow keys or tab to help complete your commands. Interactive mode is set up specifically for Azure, so you don't need to enter az to start a command. Try the upgrade or version commands again, but this time without az in front.
The commands should have worked the same as before, and given you the same results. Use the exit command to leave interactive mode.

You're all set. Continue on with the training.

## 1.5 Describe Azure physical infrastructure

# Describe Azure physical infrastructure
Throughout your journey with Microsoft Azure, you’ll hear and use terms like Regions, Availability Zones, Resources, Subscriptions, and more. This module focuses on the core architectural components of Azure. The core architectural components of Azure may be broken down into two main groupings: the physical infrastructure, and the management infrastructure.
## Physical infrastructure
The physical infrastructure for Azure starts with datacenters. Conceptually, the datacenters are the same as large corporate datacenters. They’re facilities with resources arranged in racks, with dedicated power, cooling, and networking infrastructure.
As a global cloud provider, Azure has datacenters around the world. However, these individual datacenters aren’t directly accessible. Datacenters are grouped into Azure Regions or Azure Availability Zones that are designed to help you achieve resiliency and reliability for your business-critical workloads.
The Global infrastructure site gives you a chance to interactively explore the underlying Azure infrastructure.
### Regions
A region is a geographical area on the planet that contains at least one, but potentially multiple datacenters that are nearby and networked together with a low-latency network. Azure intelligently assigns and controls the resources within each region to ensure workloads are appropriately balanced.
When you deploy a resource in Azure, you'll often need to choose the region where you want your resource deployed.
Note
Some services or virtual machine (VM) features are only available in certain regions, such as specific VM sizes or storage types. There are also some global Azure services that don't require you to select a particular region, such as Microsoft Entra ID, Azure Traffic Manager, and Azure DNS.
### Availability Zones
Availability zones are physically separate datacenters within an Azure region. Each availability zone is made up of one or more datacenters equipped with independent power, cooling, and networking. An availability zone is set up to be an isolation boundary. If one zone goes down, the other continues working. Availability zones are connected through high-speed, private fiber-optic networks.
Important
To ensure resiliency, a minimum of three separate availability zones are present in all availability zone-enabled regions. However, not all Azure Regions currently support availability zones.
#### Use availability zones in your apps
You want to ensure your services and data are redundant so you can protect your information in case of failure. When you host your infrastructure, setting up your own redundancy requires that you create duplicate hardware environments. Azure can help make your app highly available through availability zones.
You can use availability zones to run mission-critical applications and build high-availability into your application architecture by co-locating your compute, storage, networking, and data resources within an availability zone and replicating in other availability zones. Keep in mind that there could be a cost to duplicating your services and transferring data between availability zones.
Availability zones are primarily for VMs, managed disks, load balancers, and SQL databases. Azure services that support availability zones fall into three categories:
- Zonal services: You pin the resource to a specific zone (for example, VMs, managed disks, IP addresses).
- Zone-redundant services: The platform replicates automatically across zones (for example, zone-redundant storage, SQL Database).
- Non-regional services: Services are always available from Azure geographies and are resilient to zone-wide outages as well as region-wide outages.
Even with the additional resiliency that availability zones provide, it’s possible that an event could be so large that it impacts multiple availability zones in a single region. To provide even further resilience, Azure has Region Pairs.
### Region pairs
Most Azure regions are paired with another region within the same geography (such as US, Europe, or Asia) at least 300 miles away. This approach allows for the replication of resources across a geography that helps reduce the likelihood of interruptions because of events such as natural disasters, civil unrest, power outages, or physical network outages that affect an entire region. For example, if a region in a pair was affected by a natural disaster, services would automatically fail over to the other region in its region pair.
Important
Not all Azure services automatically replicate data or automatically fall back from a failed region to cross-replicate to another enabled region. In these scenarios, recovery and replication must be configured by the customer.
Examples of region pairs in Azure are West US paired with East US and South-East Asia paired with East Asia. Because the pair of regions are directly connected and far enough apart to be isolated from regional disasters, you can us

## 1.6 Describe Azure management infrastructure

# Describe Azure management infrastructure
The management infrastructure includes Azure resources and resource groups, subscriptions, and accounts. Understanding the hierarchical organization will help you plan your projects and products within Azure.
## Azure resources and resource groups
A resource is the basic building block of Azure. Anything you create, provision, deploy, etc. is a resource. Virtual Machines (VMs), virtual networks, databases, cognitive services, etc. are all considered resources within Azure.
Resource groups are simply groupings of resources. When you create a resource, you’re required to place it into a resource group. While a resource group can contain many resources, a single resource can only be in one resource group at a time. Some resources may be moved between resource groups, but when you move a resource to a new group, it will no longer be associated with the former group. Additionally, resource groups can't be nested, meaning you can’t put resource group B inside of resource group A.
Resource groups provide a convenient way to group resources together. When you apply an action to a resource group, that action will apply to all the resources within the resource group. If you delete a resource group, all the resources will be deleted. If you grant or deny access to a resource group, you’ve granted or denied access to all the resources within the resource group.
When you’re provisioning resources, it’s good to think about the resource group structure that best suits your needs.
For example, if you’re setting up a temporary dev environment, grouping all the resources together means you can deprovision all of the associated resources at once by deleting the resource group. If you’re provisioning compute resources that will need three different access schemas, it may be best to group resources based on the access schema, and then assign access at the resource group level.
There aren’t hard rules about how you use resource groups, so consider how to set up your resource groups to maximize their usefulness for you.
## Azure subscriptions
In Azure, subscriptions are a unit of management, billing, and scale. Similar to how resource groups are a way to logically organize resources, subscriptions allow you to logically organize your resource groups and facilitate billing.
Using Azure requires an Azure subscription. A subscription provides you with authenticated and authorized access to Azure products and services. It also allows you to provision resources. An Azure subscription links to an Azure account, which is an identity in Microsoft Entra ID or in a directory that Microsoft Entra ID trusts.
An account can have multiple subscriptions, but it’s only required to have one. In a multi-subscription account, you can use the subscriptions to configure different billing models and apply different access-management policies. You can use Azure subscriptions to define boundaries around Azure products, services, and resources. There are two types of subscription boundaries that you can use:
- Billing boundary : This subscription type determines how an Azure account is billed for using Azure. You can create multiple subscriptions for different types of billing requirements. Azure generates separate billing reports and invoices for each subscription so that you can organize and manage costs.
- Access control boundary : Azure applies access-management policies at the subscription level, and you can create separate subscriptions to reflect different organizational structures. An example is that within a business, you have different departments to which you apply distinct Azure subscription policies. This billing model allows you to manage and control access to the resources that users provision with specific subscriptions.
### Create additional Azure subscriptions
Similar to using resource groups to separate resources by function or access, you might want to create additional subscriptions for resource or billing management purposes. For example, you might choose to create additional subscriptions to separate:
- Environments : You can choose to create subscriptions to set up separate environments for development and testing, security, or to isolate data for compliance reasons. This design is particularly useful because resource access control occurs at the subscription level.
- Organizational structures : You can create subscriptions to reflect different organizational structures. For example, you could limit one team to lower-cost resources, while allowing the IT department a full range. This design allows you to manage and control access to the resources that users provision within each subscription.
- Billing : You can create additional subscriptions for billing purposes. Because costs are first aggregated at the subscription level, you might want to create subscriptions to manage and track costs based on your needs. For instance, you might want to create one subscription for your production wor

## 1.7 Exercise - Create an Azure resource

# Exercise - Create an Azure resource
In this exercise, you’ll use the Azure portal to create a resource. The focus of the exercise is observing how Azure resource groups populate with created resources.
Important
You have the opportunity to create a resource group when you create the virtual machine. If you name the resource group the same as the recommended name, it makes clean-up easier at the end of the exercise.
## Task 1: Create a virtual machine
In this task, you’ll create a virtual machine using the Azure portal.
- to the Azure portal .
- Select Create a resource &gt; Compute &gt; Virtual Machine &gt; Create.
- The Create a virtual machine pane opens to the basics tab.
- Verify or enter the following values for each setting. If a setting isn’t specified, leave the default value.
Basics tab 
Setting 
Value 
Subscription 
Select the subscription you want to use for the exercise. 
Resource group 
Select Create new and enter IntroAzureRG and select OK 
Virtual machine name 
my-VM 
Region 
Leave default 
Availability options 
Leave default 
Zone Options 
Self-selected zone 
Availability zone 
Leave default 
Security type 
Leave default 
Image 
Leave default 
VM architecture 
Leave default 
Run with Azure Spot discount 
Unchecked 
Size 
Leave default 
Authentication type 
Password 
Username 
azureuser 
Password 
Enter a custom password 
Confirm password 
Reenter the custom password 
Public inbound ports 
None 
- Select Review and Create.
Important
Product details will include a cost associated with creating the virtual machine. This is a system function. If you’re creating the VM in the Learn sandbox, you won’t actually incur any costs.
- Select Create
Wait while the VM is provisioned. Deployment is will change to Deployment is complete when the VM is ready.
## Task 2: Verify resources created
Once the deployment is created, you can verify that Azure created not only a VM, but all of the associated resources the VM needs.
- Select Home.
- Under Azure services, select Resource groups.
- Select the IntroAzureRG resource group.
You should see a list of resources in the resource group. The resources were created when you created the virtual machine. By default, Azure gave them all a similar name to help with association and grouped them in the same resource group.
Congratulations! You've created a resource in Azure and had a chance to see how resources get grouped on creation.
## Clean up
To clean up the assets created in this exercise and avoid unnecessary costs, delete the resource group (and all associated resources).
- From the Azure home page, under Azure servces, select Resource groups .
- Select the IntroAzureRG resource group.
- Select Delete resource group .
- Enter IntroAzureRG to confirm deletion of the resource group and select delete.

## 1.9 Summary

# Summary
, you learned about the physical and management structure of Microsoft Azure. You were introduced to the relationship between datacenters, availability zones, and regions. You explored how the infrastructure supports the benefits of the cloud, such as high availability and reliability. You also learned about the management infrastructure of Azure. You explored how resources and resource groups are related, and how subscriptions and management groups can help manage resources.
## Learning objectives
You should now be able to:
- Describe Azure regions, region pairs, and sovereign regions.
- Describe Availability Zones.
- Describe Azure datacenters.
- Describe Azure resources and Resource Groups.
- Describe subscriptions.
- Describe management groups.
- Describe the hierarchy of resource groups, subscriptions, and management groups.

---

# Module 2: Describe Azure Compute and Networking Services

Introduction to Azure compute services (virtual machines, Azure Virtual Desktop, Azure Functions) and networking services (virtual networks, ExpressRoute, DNS, etc.).

## 2.1 Introduction

# Introduction
This module introduces you to the compute and networking services of Azure. You learn about three of the compute options (virtual machines, containers, and Azure functions). You also learn about some of the networking features, such as Azure virtual networks, Azure DNS, and Azure ExpressRoute.
## Learning objectives
After completing this module, you’ll be able to:
- Compare compute types, including container instances, virtual machines, and functions.
- Describe virtual machine options, including virtual machines (VMs), virtual machine scale sets, virtual machine availability sets, and Azure Virtual Desktop.
- Describe resources required for virtual machines.
- Describe application hosting options, including Azure Web Apps, containers, and virtual machines.
- Describe virtual networking, including the purpose of Azure Virtual Networks, Azure virtual subnets, peering, Azure DNS, VPN Gateway, and ExpressRoute.
- Define public and private endpoints.

## 2.2 Describe Azure virtual machines

# Describe Azure virtual machines
With Azure Virtual Machines (VMs), you can create and use VMs in the cloud. VMs provide infrastructure as a service (IaaS) in the form of a virtualized server and can be used in many ways. Just like a physical computer, you can customize all of the software running on your VM. VMs are an ideal choice when you need:
- Total control over the operating system (OS).
- The ability to run custom software.
- To use custom hosting configurations.
An Azure VM gives you the flexibility of virtualization without having to buy and maintain the physical hardware that runs the VM. However, as an IaaS offering, you still need to configure, update, and maintain the software that runs on the VM.
You can even create or use an already created image to rapidly provision VMs. You can create and provision a VM in minutes when you select a preconfigured VM image. An image is a template used to create a VM and may already include an OS and other software, like development tools or web hosting environments.
## Scale VMs in Azure
You can run single VMs for testing, development, or minor tasks. Or you can group VMs together to provide high availability, scalability, and redundancy. Azure can also manage the grouping of VMs for you with features such as scale sets and availability sets.
### Virtual machine scale sets
Virtual machine scale sets let you create and manage a group of identical, load-balanced VMs. If you simply created multiple VMs with the same purpose, you’d need to ensure they were all configured identically and then set up network routing parameters to ensure efficiency. You’d also have to monitor the utilization to determine if you need to increase or decrease the number of VMs.
Instead, with virtual machine scale sets, Azure automates most of that work. Scale sets allow you to centrally manage, configure, and update a large number of VMs in minutes. The number of VM instances can automatically increase or decrease in response to demand, or you can set it to scale based on a defined schedule. Virtual machine scale sets also automatically deploy a load balancer to make sure that your resources are being used efficiently. With virtual machine scale sets, you can build large-scale services for areas such as compute, big data, and container workloads.
### Virtual machine availability sets
Virtual machine availability sets are another tool to help you build a more resilient, highly available environment. Availability sets are designed to ensure that VMs stagger updates and have varied power and network connectivity, preventing you from losing all your VMs with a single network or power failure.
Availability sets accomplish these objectives by grouping VMs in two ways: update domain and fault domain.
- Update domain : The update domain groups VMs that can be rebooted at the same time. This setup allows you to apply updates while knowing that only one update domain grouping is offline at a time. All of the machines in one update domain update. An update group going through the update process is given a 30-minute time to recover before maintenance on the update domain starts.
- Fault domain : The fault domain groups your VMs by common power source and network switch. By default, an availability set splits your VMs across up to three fault domains. This helps protect against a physical power or networking failure by having VMs in different fault domains (thus being connected to different power and networking resources).
Best of all, there’s no additional cost for configuring an availability set. You only pay for the VM instances you create.
## Examples of when to use VMs
Some common examples or use cases for virtual machines include:
- During testing and development . VMs provide a quick and easy way to create different OS and application configurations. Test and development personnel can then easily delete the VMs when they no longer need them.
- When running applications in the cloud . The ability to run certain applications in the public cloud as opposed to creating a traditional infrastructure to run them can provide substantial economic benefits. For example, an application might need to handle fluctuations in demand. Shutting down VMs when you don't need them or quickly starting them up to meet a sudden increase in demand means you pay only for the resources you use.
- When extending your datacenter to the cloud : An organization can extend the capabilities of its own on-premises network by creating a virtual network in Azure and adding VMs to that virtual network. Applications like SharePoint can then run on an Azure VM instead of running locally. This arrangement makes it easier or less expensive to deploy than in an on-premises environment.
- During disaster recovery : As with running certain types of applications in the cloud and extending an on-premises network to the cloud, you can get significant cost savings by using an IaaS-based approach to disaster recovery. If a primary datac

## 2.3 Exercise - Create an Azure virtual machine

# Exercise - Create an Azure virtual machine
In this exercise, you create an Azure virtual machine (VM) and install a web server (Nginx).
You could use the Azure portal, the Azure CLI, or an Azure Resource Manager (ARM) template.
In this instance, you're going to use the Azure CLI.
Important
This exercise creates a VM that is used in a later exercise with. To avoid leaving a VM running for an extended period of time, it's recommended that you complete the full module in one sitting.
## Task 1: Create a resource group
- Log into the Azure portal .
- Select the Azure Cloud Shell icon to bring up Cloud Shell.
- From the Azure CLI, create a resource group named IntroAzureRG .
az group create --name IntroAzureRG --location eastus
## Task 2: Create a Linux virtual machine
- Use the following Azure CLI command to create a Linux VM.
- From Cloud Shell, run the following az vm create command to create a Linux VM:
az vm create \
--resource-group "IntroAzureRG" \
--name my-vm \
--size Standard_D2s_v5 \
--public-ip-sku Standard \
--image Ubuntu2204 \
--admin-username azureuser \
--generate-ssh-keys 
Your VM takes a few moments to come up. You named the VM my-vm . You use this name to refer to the VM in later steps.
## Task 3: Install Nginx
After your VM is created, you'll use a Custom Script Extension to install Nginx. The Custom Script Extension is an easy way to download and run scripts on your Azure VMs. It's just one of the many ways you can configure the system after your VM is up and running.
- Run the following az vm extension set command to configure Nginx on your VM:
az vm extension set \
--resource-group "IntroAzureRG" \
--vm-name my-vm \
--name customScript \
--publisher Microsoft.Azure.Extensions \
--version 2.1 \
--settings '{"fileUris":["https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-nginx.sh"]}' \
--protected-settings '{"commandToExecute": "./configure-nginx.sh"}' 
This command uses the Custom Script Extension to run a Bash script on your VM. The script is stored on GitHub. While the command runs, you can choose to examine the Bash script from a separate browser tab. To summarize, the script:
- Runs apt-get update to download the latest package information from the internet. This step helps ensure that the command can locate the latest version of the Nginx package.
- Installs Nginx.
- Sets the home page, /var/www/html/index.html , to print a welcome message that includes your VM's host name.

This exercise is complete for now. You'll use this VM later .

## 2.4 Describe Azure virtual desktop

# Describe Azure virtual desktop
Another type of virtual machine is the Azure Virtual Desktop. Azure Virtual Desktop is a desktop and application virtualization service that runs on the cloud. It enables you to use a cloud-hosted version of Windows from any location. Azure Virtual Desktop works across devices and operating systems, and works with apps that you can use to access remote desktops or most modern browsers.
The following video gives you an overview of Azure Virtual Desktop:
## Enhance security
Azure Virtual Desktop provides centralized security management for users' desktops with Microsoft Entra ID. You can enable multifactor authentication to secure user sign-ins. You can also secure access to data by assigning granular role-based access controls (RBACs) to users.
With Azure Virtual Desktop, the data and apps are separated from the local hardware. The actual desktop and apps are running in the cloud, meaning the risk of confidential data being left on a personal device is reduced. Additionally, user sessions are isolated in both single and multi-session environments.
## Multi-session Windows 10 or Windows 11 deployment
Azure Virtual Desktop lets you use Windows 10 or Windows 11 Enterprise multi-session, the only Windows client-based operating system that enables multiple concurrent users on a single VM. Azure Virtual Desktop also provides a more consistent experience with broader application support compared to Windows Server-based operating systems.

## 2.5 Describe Azure containers

# Describe Azure containers
While virtual machines are an excellent way to reduce costs versus the investments that are necessary for physical hardware, they're still limited to a single operating system per virtual machine. If you want to run multiple instances of an application on a single host machine, containers are an excellent choice.
## What are containers?
Containers are a virtualization environment. Much like running multiple virtual machines on a single physical host, you can run multiple containers on a single physical or virtual host. Unlike virtual machines, you don't manage the operating system for a container. Virtual machines appear to be an instance of an operating system that you can connect to and manage. Containers are lightweight and designed to be created, scaled out, and stopped dynamically. It's possible to create and deploy virtual machines as application demand increases, but containers are a lighter weight, more agile method. Containers are designed to allow you to respond to changes on demand. With containers, you can quickly restart if there's a crash or hardware interruption. One of the most popular container engines is Docker, and Azure supports Docker.
## Compare virtual machines to containers
The following video highlights several of the important differences between virtual machines and containers:
### Azure Container Instances
Azure Container Instances offer the fastest and simplest way to run a container in Azure; without having to manage any virtual machines or adopt any additional services. Azure Container Instances are a platform as a service (PaaS) offering. Azure Container Instances allow you to upload your containers and then the service runs the containers for you.
### Azure Container Apps
Azure Container Apps are similar in many ways to a container instance. They allow you to get up and running right away, they remove the container management piece, and they're a PaaS offering. Container Apps have extra benefits such as the ability to incorporate load balancing and scaling. These other functions allow you to be more elastic in your design.
### Azure Kubernetes Service
Azure Kubernetes Service (AKS) is a container orchestration service. An orchestration service manages the lifecycle of containers. When you're deploying a fleet of containers, AKS can make fleet management simpler and more efficient.
### Use containers in your solutions
Containers are often used to create solutions by using a microservice architecture. This architecture is where you break solutions into smaller, independent pieces. For example, you might split a website into a container hosting your front end, another hosting your back end, and a third for storage. This split allows you to separate portions of your app into logical sections that can be maintained, scaled, or updated independently.
Imagine your website back-end reaches capacity, but the front end and storage aren't stressed. With containers, you could scale the back-end separately to improve performance. If something necessitated such a change, you could also choose to change the storage service or modify the front end without impacting any of the other components.

## 2.6 Describe Azure functions

# Describe Azure functions
Azure Functions is an event-driven, serverless compute option that doesn’t require maintaining virtual machines or containers. If you build an app using VMs or containers, those resources have to be “running” in order for your app to function. With Azure Functions, an event wakes the function, alleviating the need to keep resources provisioned when there are no events.
## Serverless computing in Azure
## Benefits of Azure Functions
Using Azure Functions is ideal when you're only concerned about the code running your service and not about the underlying platform or infrastructure. Functions are commonly used when you need to perform work in response to an event (often via a REST request), timer, or message from another Azure service, and when that work can be quickly, within seconds or less.
Functions scale automatically based on demand, so they may be a good choice when demand is variable.
Azure Functions runs your code when it triggers and automatically deallocates resources when the function is finished. In this model, Azure only charges you for the CPU time used while your function runs.
Functions can be either stateless or stateful. When they're stateless (the default), they behave as if they restart every time they respond to an event. When they're stateful (called Durable Functions), a context is passed through the function to track prior activity.
Functions are a key component of serverless computing. They're also a general compute platform for running any type of code. If the needs of the developer's app change, you can deploy the project in an environment that isn't serverless. This flexibility allows you to manage scaling, run on virtual networks, and even completely isolate the functions.

## 2.7 Describe application hosting options

# Describe application hosting options
If you need to host your application on Azure, you might initially turn to a virtual machine (VM) or containers. Both VMs and containers provide excellent hosting solutions. VMs give you maximum control of the hosting environment and allow you to configure it exactly how you want. VMs also may be the most familiar hosting method if you’re new to the cloud. Containers, with the ability to isolate and individually manage different aspects of the hosting solution, can also be a robust and compelling option.
There are other hosting options that you can use with Azure, including Azure App Service.
## Azure App Service
App Service enables you to build and host web apps, background jobs, mobile back-ends, and RESTful APIs in the programming language of your choice without managing infrastructure. It offers automatic scaling and high availability. App Service supports Windows and Linux. It enables automated deployments from GitHub, Azure DevOps, or any Git repo to support a continuous deployment model.
Azure App Service is a robust hosting option that you can use to host your apps in Azure. Azure App Service lets you focus on building and maintaining your app, and Azure focuses on keeping the environment up and running.
Azure App Service is an HTTP-based service for hosting web applications, REST APIs, and mobile back ends. Azure App Service supports multiple technologies, including programming languages like Java, PHP, Python, and JavaScript (via Node.js), as well as frameworks such as .NET and .NET Core. Azure App Service supports both Windows and Linux environments.
### Types of app services
With App Service, you can host most common app service styles like:
- Web apps
- API apps
- WebJobs
- Mobile apps
App Service handles most of the infrastructure decisions you deal with in hosting web-accessible apps:
- Deployment and management are integrated into the platform.
- Endpoints can be secured.
- Sites can be scaled quickly to handle high traffic loads.
- The built-in load balancing and traffic manager provide high availability.
All of these app styles are hosted in the same infrastructure and share these benefits. This flexibility makes App Service the ideal choice to host web-oriented applications.
### Web apps
App Service includes full support for hosting web apps by using ASP.NET, ASP.NET Core, Java, Ruby, Node.js, PHP, or Python. You can choose either Windows or Linux as the host operating system.
### API apps
Much like hosting a website, you can build REST-based web APIs by using your choice of language and framework. You get full Swagger support and the ability to package and publish your API in Azure Marketplace. The produced apps can be consumed from any HTTP- or HTTPS-based client.
### WebJobs
You can use the WebJobs feature to run a program (.exe, Java, PHP, Python, or Node.js) or script (.cmd, .bat, PowerShell, or Bash) in the same context as a web app, API app, or mobile app. They can be scheduled or run by a trigger. WebJobs are often used to run background tasks as part of your application logic.
### Mobile apps
Use the Mobile Apps feature of App Service to quickly build a back end for iOS and Android apps. With just a few actions in the Azure portal, you can:
- Store mobile app data in a cloud-based SQL database.
- Authenticate customers against common social providers, such as MSA, Google, X, and .
- Send push notifications.
- Execute custom back-end logic in C# or Node.js.
On the mobile app side, there's SDK support for native iOS and Android, Xamarin, and React native apps.

## 2.8 Describe Azure virtual networking

# Describe Azure virtual networking
Azure virtual networks and virtual subnets enable Azure resources, such as VMs, web apps, and databases, to communicate with each other, with users on the internet, and with your on-premises client computers. You can think of an Azure network as an extension of your on-premises network with resources that link other Azure resources.
Azure virtual networks provide the following key networking capabilities:
- Isolation and segmentation
- Internet communications
- Communicate between Azure resources
- Communicate with on-premises resources
- Route network traffic
- Filter network traffic
- Connect virtual networks
Azure virtual networking supports both public and private endpoints to enable communication between external or internal resources with other internal resources.
- Public endpoints have a public IP address and can be accessed from anywhere in the world.
- Private endpoints exist within a virtual network and have a private IP address from within the address space of that virtual network.
## Isolation and segmentation
Azure virtual network allows you to create multiple isolated virtual networks. When you set up a virtual network, you define a private IP address space by using either public or private IP address ranges. The IP range only exists within the virtual network and isn't internet routable. You can divide that IP address space into subnets and allocate part of the defined address space to each named subnet.
For name resolution, you can use the name resolution service built into Azure. You also can configure the virtual network to use either an internal or an external DNS server.
## Internet communications
You can enable incoming connections from the internet by assigning a public IP address to an Azure resource, or putting the resource behind a public load balancer.
## Communicate between Azure resources
You want to enable Azure resources to communicate securely with each other. You can do that in one of two ways:
- Virtual networks can connect not only VMs but other Azure resources, such as the App Service Environment for Power Apps, Azure Kubernetes Service, and Azure virtual machine scale sets.
- Service endpoints can connect to other Azure resource types, such as Azure SQL databases and storage accounts. This approach enables you to link multiple Azure resources to virtual networks to improve security and provide optimal routing between resources.
## Communicate with on-premises resources
Azure virtual networks enable you to link resources together in your on-premises environment and within your Azure subscription. In effect, you can create a network that spans both your local and cloud environments. There are three mechanisms for you to achieve this connectivity:
- Point-to-site virtual private network connections are from a computer outside your organization back into your corporate network. In this case, the client computer initiates an encrypted VPN connection to connect to the Azure virtual network.
- Site-to-site virtual private networks link your on-premises VPN device or gateway to the Azure VPN gateway in a virtual network. In effect, the devices in Azure can appear as being on the local network. The connection is encrypted and works over the internet.
- Azure ExpressRoute provides a dedicated private connectivity to Azure that doesn't travel over the internet. ExpressRoute is useful for environments where you need greater bandwidth and even higher levels of security.
## Route network traffic
By default, Azure routes traffic between subnets on any connected virtual networks, on-premises networks, and the internet. You also can control routing and override those settings, as follows:
- Route tables allow you to define rules about how traffic should be directed. You can create custom route tables that control how packets are routed between subnets.
- Border Gateway Protocol (BGP) works with Azure VPN gateways, Azure Route Server, or Azure ExpressRoute to propagate on-premises BGP routes to Azure virtual networks.
## Filter network traffic
Azure virtual networks enable you to filter traffic between subnets by using the following approaches:
- Network security groups are Azure resources that can contain multiple inbound and outbound security rules. You can define these rules to allow or block traffic, based on factors such as source and destination IP address, port, and protocol.
- Network virtual appliances are specialized VMs that can be compared to a hardened network appliance. A network virtual appliance carries out a particular network function, such as running a firewall or performing wide area network (WAN) optimization.
## Connect virtual networks
You can link virtual networks together by using virtual network peering. Peering allows two virtual networks to connect directly to each other. Network traffic between peered networks is private, and travels on the Microsoft backbone network, never entering the public internet. Peering enables resou

## 2.9 Exercise - Configure network access

# Exercise - Configure network access
In this exercise, you configure the access to the virtual machine (VM) you created earlier .
Important
The VM for this exercise was createdly ly . If you deleted the VM or resource group created in unit 3, you'll need to redo the exercise ( Exercise - Create an Azure virtual machine ).
Right now, the VM you created and installed Nginx on during the exercise isn't accessible from the internet. In this exercise, you'll create a network security group that changes that by allowing inbound HTTP access on port 80.
Note
It's important that you're in the BASH version of Cloud Shell for some of the commands in this exercise. You can use the Switch to... button if you're currently in PowerShell mode.
## Task 1: Access your web server
In this procedure, you get the IP address for your VM and attempt to access your web server's home page.
- Run the following az vm list-ip-addresses command to get your VM's IP address and store the result as a Bash variable:
IPADDRESS="$(az vm list-ip-addresses \
--resource-group "IntroAzureRG" \
--name my-vm \
--query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
--output tsv)" 
- Run the following curl command to download the home page:
curl --connect-timeout 5 http://$IPADDRESS
The --connect-timeout argument specifies to allow up to five seconds for the connection to occur. After five seconds, you see an error message that states that the connection timed out:
curl: (28) Connection timed out after 5001 milliseconds
This message means that the VM wasn't accessible within the timeout period.
- As an optional step, try to access the web server from a browser:
- Run the following to print your VM's IP address to the console:
echo $IPADDRESS 
You see an IP address, for example, 23.102.42.235 .
- Copy the IP address that you see to the clipboard.
- Open a new browser tab and go to your web server. After a few moments, you see that the connection isn't happening. If you wait for the browser to time out, you see something like this:
- Keep this browser tab open for later.
## Task 2: List the current network security group rules
Your web server wasn't accessible. To find out why, let's examine your current NSG rules.
- Run the following az network nsg list command to list the network security groups that are associated with your VM:
az network nsg list \
--resource-group "IntroAzureRG" \
--query '[].name' \
--output tsv 
You see this output:
my-vmNSG
Every VM on Azure is associated with at least one network security group. In this case, Azure created an NSG for you called my-vmNSG .
- Run the following az network nsg rule list command to list the rules associated with the NSG named my-vmNSG :
az network nsg rule list \
--resource-group "IntroAzureRG" \
--nsg-name my-vmNSG 
You see a large block of text in JSON format in the output. In the step, you'll run a similar command that makes this output easier to read.
- Run the az network nsg rule list command a second time. This time, use the --query argument to retrieve only the name, priority, affected ports, and access ( Allow or Deny ) for each rule. The --output argument formats the output as a table so that it's easy to read.
az network nsg rule list \
--resource-group "IntroAzureRG" \
--nsg-name my-vmNSG \
--query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' \
--output table 
You see this output:
Name Priority Port Access
----------------- ---------- ------ --------
default-allow-ssh 1000 22 Allow
You see the default rule, default-allow-ssh . This rule allows inbound connections over port 22 (SSH). SSH (Secure Shell) is a protocol that's used on Linux to allow administrators to access the system remotely. The priority of this rule is 1000. Rules are processed in priority order, with lower numbers processed before higher numbers.
By default, a Linux VM's NSG allows network access only on port 22. This port enables administrators to access the system. You need to also allow inbound connections on port 80, which allows access over HTTP.
## Task 3: Create the network security rule
Here, you create a network security rule that allows inbound access on port 80 (HTTP).
- Run the following az network nsg rule create command to create a rule called allow-http that allows inbound access on port 80:
az network nsg rule create \
--resource-group "IntroAzureRG" \
--nsg-name my-vmNSG \
--name allow-http \
--protocol tcp \
--priority 100 \
--destination-port-range 80 \
--access Allow 
For learning purposes, here you set the priority to 100. In this case, the priority doesn't matter. You would need to consider the priority if you had overlapping port ranges.
- To verify the configuration, run az network nsg rule list to see the updated list of rules:
az network nsg rule list \
--resource-group "IntroAzureRG" \
--nsg-name my-vmNSG \
--query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' \
--output table 
You see both the default-allow-ssh rul

## 2.10 Describe Azure virtual private networks

# Describe Azure virtual private networks
A virtual private network (VPN) uses an encrypted tunnel within another network. VPNs are typically deployed to connect two or more trusted private networks to one another over an untrusted network (typically the public internet). Traffic is encrypted while traveling over the untrusted network to prevent eavesdropping or other attacks. VPNs can enable networks to safely and securely share sensitive information.
## VPN gateways
A VPN gateway is a type of virtual network gateway. Azure VPN Gateway instances are deployed in a dedicated subnet of the virtual network and enable the following connectivity:
- Connect on-premises datacenters to virtual networks through a site-to-site connection.
- Connect individual devices to virtual networks through a point-to-site connection.
- Connect virtual networks to other virtual networks through a network-to-network connection.
All data transfer is encrypted inside a private tunnel as it crosses the internet. You can deploy only one VPN gateway in each virtual network. However, you can use one gateway to connect to multiple locations, which includes other virtual networks or on-premises datacenters.
When setting up a VPN gateway, you must specify the type of VPN - either policy-based or route-based. The primary distinction between these two types is how they determine which traffic needs encryption. In Azure, regardless of the VPN type, the method of authentication employed is a preshared key.
- Policy-based VPN gateways specify statically the IP address of packets that should be encrypted through each tunnel. This type of device evaluates every data packet against those sets of IP addresses to choose the tunnel where that packet is going to be sent through.
- In Route-based gateways, IPSec tunnels are modeled as a network interface or virtual tunnel interface. IP routing (either static routes or dynamic routing protocols) decides which one of these tunnel interfaces to use when sending each packet. Route-based VPNs are the preferred connection method for on-premises devices. They're more resilient to topology changes such as the creation of new subnets.
Use a route-based VPN gateway if you need any of the following types of connectivity:
- Connections between virtual networks
- Point-to-site connections
- Multisite connections
- Coexistence with an Azure ExpressRoute gateway
## High-availability scenarios
If you’re configuring a VPN to keep your information safe, you also want to be sure that it’s a highly available and fault tolerant VPN configuration. There are a few ways to maximize the resiliency of your VPN gateway.
### Active/standby
By default, VPN gateways are deployed as two instances in an active/standby configuration, even if you only see one VPN gateway resource in Azure. When planned maintenance or unplanned disruption affects the active instance, the standby instance automatically assumes responsibility for connections without any user intervention. Connections are interrupted during this failover, but they typically restore within a few seconds for planned maintenance and within 90 seconds for unplanned disruptions.
### Active/active
With the introduction of support for the BGP routing protocol, you can also deploy VPN gateways in an active/active configuration. In this configuration, you assign a unique public IP address to each instance. You then create separate tunnels from the on-premises device to each IP address. You can extend the high availability by deploying an additional VPN device on-premises.
### ExpressRoute failover
Another high-availability option is to configure a VPN gateway as a secure failover path for ExpressRoute connections. ExpressRoute circuits have resiliency built in. However, they aren't immune to physical problems that affect the cables delivering connectivity or outages that affect the complete ExpressRoute location. In high-availability scenarios, where there's risk associated with an outage of an ExpressRoute circuit, you can also provision a VPN gateway that uses the internet as an alternative method of connectivity. In this way, you can ensure there's always a connection to the virtual networks.
### Zone-redundant gateways
In regions that support availability zones, VPN gateways and ExpressRoute gateways can be deployed in a zone-redundant configuration. This configuration brings resiliency, scalability, and higher availability to virtual network gateways. Deploying gateways in Azure availability zones physically and logically separates gateways within a region while protecting your on-premises network connectivity to Azure from zone-level failures. These gateways require different gateway stock keeping units (SKUs) and use Standard public IP addresses instead of Basic public IP addresses.

## 2.11 Describe Azure ExpressRoute

# Describe Azure ExpressRoute
Azure ExpressRoute lets you extend your on-premises networks into the Microsoft cloud over a private connection, with the help of a connectivity provider. This connection is called an ExpressRoute Circuit. With ExpressRoute, you can establish connections to Microsoft cloud services, such as Microsoft Azure and Microsoft 365. This feature allows you to connect offices, datacenters, or other facilities to the Microsoft cloud. Each location would have its own ExpressRoute circuit.
Connectivity can be from an any-to-any (IP VPN) network, a point-to-point Ethernet network, or a virtual cross-connection through a connectivity provider at a colocation facility. ExpressRoute connections don't go over the public Internet. This setup allows ExpressRoute connections to offer more reliability, faster speeds, consistent latencies, and higher security than typical connections over the Internet.
## Features and benefits of ExpressRoute
There are several benefits to using ExpressRoute as the connection service between Azure and on-premises networks.
- Connectivity to Microsoft cloud services across all regions in the geopolitical region.
- Global connectivity to Microsoft services across all regions with the ExpressRoute Global Reach.
- Dynamic routing between your network and Microsoft via Border Gateway Protocol (BGP).
- Built-in redundancy in every peering location for higher reliability.
### Connectivity to Microsoft cloud services
ExpressRoute enables direct access to the following services in all regions:
- Microsoft Office 365
- Microsoft Dynamics 365
- Azure compute services, such as Azure Virtual Machines
- Azure cloud services, such as Azure Cosmos DB and Azure Storage
### Global connectivity
You can enable ExpressRoute Global Reach to exchange data across your on-premises sites by connecting your ExpressRoute circuits. For example, say you had an office in Asia and a datacenter in Europe, both with ExpressRoute circuits connecting them to the Microsoft network. You could use ExpressRoute Global Reach to connect those two facilities, allowing them to communicate without transferring data over the public internet.
### Dynamic routing
ExpressRoute uses the BGP. BGP is used to exchange routes between on-premises networks and resources running in Azure. This protocol enables dynamic routing between your on-premises network and services running in the Microsoft cloud.
### Built-in redundancy
Each connectivity provider uses redundant devices to ensure that connections established with Microsoft are highly available. You can configure multiple circuits to complement this feature.
## ExpressRoute connectivity models
ExpressRoute supports four models that you can use to connect your on-premises network to the Microsoft cloud:
- CloudExchange colocation
- Point-to-point Ethernet connection
- Any-to-any connection
- Directly from ExpressRoute sites
### Colocation at a cloud exchange
Colocation refers to your datacenter, office, or other facility being physically colocated at a cloud exchange, such as an ISP. If your facility is colocated at a cloud exchange, you can request a virtual cross-connect to the Microsoft cloud.
### Point-to-point Ethernet connection
Point-to-point ethernet connection refers to using a point-to-point connection to connect your facility to the Microsoft cloud.
### Any-to-any networks
With any-to-any connectivity, you can integrate your wide area network (WAN) with Azure by providing connections to your offices and datacenters. Azure integrates with your WAN connection to provide a connection like you would have between your datacenter and any branch offices.
### Directly from ExpressRoute sites
You can connect directly into the Microsoft's global network at a peering location strategically distributed across the world. ExpressRoute Direct provides dual 100 Gbps or 10-Gbps connectivity, which supports Active/Active connectivity at scale.
## Security considerations
With ExpressRoute, your data doesn't travel over the public internet, reducing the risks associated with internet communications. ExpressRoute is a private connection from your on-premises infrastructure to your Azure infrastructure. Even if you have an ExpressRoute connection, DNS queries, certificate revocation list checking, and Azure Content Delivery Network requests are still sent over the public internet.

## 2.12 Describe Azure DNS

# Describe Azure DNS
Azure DNS is a hosting service for DNS domains that provides name resolution by using Microsoft Azure infrastructure. By hosting your domains in Azure, you can manage your DNS records using the same credentials, APIs, tools, and billing as your other Azure services.
## Benefits of Azure DNS
Azure DNS uses the scope and scale of Microsoft Azure to provide numerous benefits, including:
- Reliability and performance
- Security
- Ease of Use
- Customizable virtual networks
- Alias records
### Reliability and performance
DNS domains in Azure DNS are hosted on Azure's global network of DNS name servers, providing resiliency and high availability. Azure DNS uses anycast networking, so the closest available DNS server answers each DNS query, providing fast performance and high availability for your domain.
### Security
Azure DNS is based on Azure Resource Manager, which provides features such as:
- Azure role-based access control (Azure RBAC) to control who has access to specific actions for your organization.
- Activity logs to monitor how a user in your organization modified a resource or to find an error when troubleshooting.
- Resource locking to lock a subscription, resource group, or resource. Locking prevents other users in your organization from accidentally deleting or modifying critical resources.
### Ease of use
Azure DNS can manage DNS records for your Azure services and provide DNS for your external resources as well. Azure DNS is integrated in the Azure portal and uses the same credentials, support contract, and billing as your other Azure services.
Because Azure DNS is running on Azure, it means you can manage your domains and records with the Azure portal, Azure PowerShell cmdlets, and the cross-platform Azure CLI. Applications that require automated DNS management can integrate with the service by using the REST API and SDKs.
### Customizable virtual networks with private domains
Azure DNS also supports private DNS domains. This feature allows you to use your own custom domain names in your private virtual networks, rather than being stuck with the Azure-provided names.
### Alias records
Azure DNS also supports alias record sets. You can use an alias record set to refer to an Azure resource, such as an Azure public IP address, an Azure Traffic Manager profile, or an Azure Content Delivery Network (CDN) endpoint. If the IP address of the underlying resource changes, the alias record set seamlessly updates itself during DNS resolution. The alias record set points to the service instance, and the service instance is associated with an IP address.
Important
You can't use Azure DNS to buy a domain name. For an annual fee, you can buy a domain name by using App Service domains or a third-party domain name registrar. Once purchased, your domains can be hosted in Azure DNS for record management.

## 2.14 Summary

# Summary
, you learned about some of the compute and networking services that are part of Azure. You learned about virtual machines, and the different options associated with them (such as virtual machine scale sets and virtual machine availability sets). You were also introduced to some of the networking capabilities, including virtual networking, ExpressRoute, and virtual private networks.
## Learning objectives
You should now be able to:
- Compare compute types, including container instances, virtual machines, and functions.
- Describe virtual machine options, including virtual machines (VMs), virtual machine scale sets, virtual machine availability sets, and Azure Virtual Desktop.
- Describe resources required for virtual machines.
- Describe application hosting options, including Azure Web Apps, containers, and virtual machines.
- Describe virtual networking, including the purpose of Azure Virtual Networks, Azure virtual subnets, peering, Azure DNS, VPN Gateway, and ExpressRoute.
- Define public and private endpoints.
## Additional resources
The following additional resources are intended to provide more information on topics or on additional topics related to this module.
- Host a web application with Azure App Service is a Microsoft Learn module that explores the process of hosting a web application in Azure.
- Introduction to Azure network foundation services is a Microsoft Learn course that provides greater insight and information on networking with Azure.

---

# Module 3: Describe Azure storage services

Azure storage services, tiers, redundancy options, and migration options and tools.

## 3.1 Introduction

# Introduction
, you’ll be introduced to the Azure storage services. You’ll learn about the Azure Storage Account and how that relates to the different storage services that are available. You’ll also learn about blob storage tiers, data redundancy options, and ways to move data or even entire infrastructures to Azure.
## Learning objectives
After completing this module, you’ll be able to:
- Compare Azure storage services.
- Describe storage tiers.
- Describe redundancy options.
- Describe storage account options and storage types.
- Identify options for moving files, including AzCopy, Azure Storage Explorer, and Azure File Sync.
- Describe migration options, including Azure Migrate and Azure Data Box.

## 3.2 Describe Azure storage accounts

# Describe Azure storage accounts
The following video introduces the different services that should be available with Azure Storage.
A storage account provides a unique namespace for your Azure Storage data that's accessible from anywhere in the world over HTTP or HTTPS. Data in this account is secure, highly available, durable, and massively scalable.
When you create your storage account, you’ll start by picking the storage account type. The type of account determines the storage services and redundancy options and has an impact on the use cases. Below is a list of redundancy options that will be covered later :
- Locally redundant storage (LRS)
- Geo-redundant storage (GRS)
- Read-access geo-redundant storage (RA-GRS)
- Zone-redundant storage (ZRS)
- Geo-zone-redundant storage (GZRS)
- Read-access geo-zone-redundant storage (RA-GZRS)
Type 
Supported services 
Redundancy Options 
Usage 
Standard general-purpose v2 
Blob Storage (including Data Lake Storage), Queue Storage, Table Storage, and Azure Files 
LRS, GRS, RA-GRS, ZRS, GZRS, RA-GZRS 
Standard storage account type for blobs, file shares, queues, and tables. Recommended for most scenarios using Azure Storage. If you want support for network file system (NFS) in Azure Files, use the premium file shares account type. 
Premium block blobs 
Blob Storage (including Data Lake Storage) 
LRS, ZRS 
Premium storage account type for block blobs and append blobs. Recommended for scenarios with high transaction rates or that use smaller objects or require consistently low storage latency. 
Premium file shares 
Azure Files 
LRS, ZRS 
Premium storage account type for file shares only. Recommended for enterprise or high-performance scale applications. Use this account type if you want a storage account that supports both Server Message Block (SMB) and NFS file shares. 
Premium page blobs 
Page blobs only 
LRS 
Premium storage account type for page blobs only. 
## Storage account endpoints
One of the benefits of using an Azure Storage Account is having a unique namespace in Azure for your data. In order to do this, every storage account in Azure must have a unique-in-Azure account name. The combination of the account name and the Azure Storage service endpoint forms the endpoints for your storage account.
When naming your storage account, keep these rules in mind:
- Storage account names must be between 3 and 24 characters in length and may contain numbers and lowercase letters only.
- Your storage account name must be unique within Azure. No two storage accounts can have the same name. This supports the ability to have a unique, accessible namespace in Azure.
The following table shows the endpoint format for Azure Storage services.
Storage service 
Endpoint 
Blob Storage 
https://&lt;storage-account-name&gt;.blob.core.windows.net 
Data Lake Storage Gen2 
https://&lt;storage-account-name&gt;.dfs.core.windows.net 
Azure Files 
https://&lt;storage-account-name&gt;.file.core.windows.net 
Queue Storage 
https://&lt;storage-account-name&gt;.queue.core.windows.net 
Table Storage 
https://&lt;storage-account-name&gt;.table.core.windows.net

## 3.3 Describe Azure storage redundancy

# Describe Azure storage redundancy
Azure Storage always stores multiple copies of your data so that it's protected from planned and unplanned events such as transient hardware failures, network or power outages, and natural disasters. Redundancy ensures that your storage account meets its availability and durability targets even in the face of failures.
When deciding which redundancy option is best for your scenario, consider the tradeoffs between lower costs and higher availability. The factors that help determine which redundancy option you should choose include:
- How your data is replicated in the primary region.
- Whether your data is replicated to a second region that is geographically distant to the primary region, to protect against regional disasters.
- Whether your application requires read access to the replicated data in the secondary region if the primary region becomes unavailable.
## Redundancy in the primary region
Data in an Azure Storage account is always replicated three times in the primary region. Azure Storage offers two options for how your data is replicated in the primary region, locally redundant storage (LRS) and zone-redundant storage (ZRS).
### Locally redundant storage
Locally redundant storage (LRS) replicates your data three times within a single data center in the primary region. LRS provides at least 11 nines of durability (99.999999999%) of objects over a given year.
LRS is the lowest-cost redundancy option and offers the least durability compared to other options. LRS protects your data against server rack and drive failures. However, if a disaster such as fire or flooding occurs within the data center, all replicas of a storage account using LRS may be lost or unrecoverable. To mitigate this risk, Microsoft recommends using zone-redundant storage (ZRS), geo-redundant storage (GRS), or geo-zone-redundant storage (GZRS).
### Zone-redundant storage
For Availability Zone-enabled Regions, zone-redundant storage (ZRS) replicates your Azure Storage data synchronously across three Azure availability zones in the primary region. ZRS offers durability for Azure Storage data objects of at least 12 nines (99.9999999999%) over a given year.
With ZRS, your data is still accessible for both read and write operations even if a zone becomes unavailable. No remounting of Azure file shares from the connected clients is required. If a zone becomes unavailable, Azure undertakes networking updates, such as DNS repointing. These updates may affect your application if you access data before the updates have .
Microsoft recommends using ZRS in the primary region for scenarios that require high availability. ZRS is also recommended for restricting replication of data within a country or region to meet data governance requirements.
## Redundancy in a secondary region
For applications requiring high durability, you can choose to additionally copy the data in your storage account to a secondary region that is hundreds of miles away from the primary region. If the data in your storage account is copied to a secondary region, then your data is durable even in the event of a catastrophic failure that prevents the data in the primary region from being recovered.
When you create a storage account, you select the primary region for the account. The paired secondary region is based on Azure Region Pairs, and can't be changed.
Azure Storage offers two options for copying your data to a secondary region: geo-redundant storage (GRS) and geo-zone-redundant storage (GZRS). GRS is similar to running LRS in two regions, and GZRS is similar to running ZRS in the primary region and LRS in the secondary region.
By default, data in the secondary region isn't available for read or write access unless there's a failover to the secondary region. If the primary region becomes unavailable, you can choose to fail over to the secondary region. After the failover has , the secondary region becomes the primary region, and you can again read and write data.
Important
Because data is replicated to the secondary region asynchronously, a failure that affects the primary region may result in data loss if the primary region can't be recovered. The interval between the most recent writes to the primary region and the last write to the secondary region is known as the recovery point objective (RPO). The RPO indicates the point in time to which data can be recovered. Azure Storage typically has an RPO of less than 15 minutes, although there's currently no SLA on how long it takes to replicate data to the secondary region.
### Geo-redundant storage
GRS copies your data synchronously three times within a single physical location in the primary region using LRS. It then copies your data asynchronously to a single physical location in the secondary region (the region pair) using LRS. GRS offers durability for Azure Storage data objects of at least 16 nines (99.99999999999999%) over a given year.
### Geo-zone-redundant storage
GZRS combin

## 3.4 Describe Azure storage services

# Describe Azure storage services
The Azure Storage platform includes the following data services:
- Azure Blobs : A massively scalable object store for text and binary data. Also includes support for big data analytics through Data Lake Storage Gen2.
- Azure Files : Managed file shares for cloud or on-premises deployments.
- Azure Queues : A messaging store for reliable messaging between application components.
- Azure Disks : Block-level storage volumes for Azure VMs.
- Azure Tables: NoSQL table option for structured, non-relational data.
## Benefits of Azure Storage
Azure Storage services offer the following benefits for application developers and IT professionals:
- Durable and highly available . Redundancy ensures that your data is safe if transient hardware failures occur. You can also opt to replicate data across data centers or geographical regions for additional protection from local catastrophes or natural disasters. Data replicated in this way remains highly available if an unexpected outage occurs.
- Secure . All data written to an Azure storage account is encrypted by the service. Azure Storage provides you with fine-grained control over who has access to your data.
- Scalable . Azure Storage is designed to be massively scalable to meet the data storage and performance needs of today's applications.
- Managed . Azure handles hardware maintenance, updates, and critical issues for you.
- Accessible . Data in Azure Storage is accessible from anywhere in the world over HTTP or HTTPS. Microsoft provides client libraries for Azure Storage in a variety of languages, including .NET, Java, Node.js, Python, PHP, Ruby, Go, and others, as well as a mature REST API. Azure Storage supports scripting in Azure PowerShell or Azure CLI. And the Azure portal and Azure Storage Explorer offer easy visual solutions for working with your data.
## Azure Blobs
Azure Blob storage is an object storage solution for the cloud. It can store massive amounts of data, such as text or binary data. Azure Blob storage is unstructured, meaning that there are no restrictions on the kinds of data it can hold. Blob storage can manage thousands of simultaneous uploads, massive amounts of video data, constantly growing log files, and can be reached from anywhere with an internet connection.
Blobs aren't limited to common file formats. A blob could contain gigabytes of binary data streamed from a scientific instrument, an encrypted message for another application, or data in a custom format for an app you're developing. One advantage of blob storage over disk storage is that it doesn't require developers to think about or manage disks. Data is uploaded as blobs, and Azure takes care of the physical storage needs.
Blob storage is ideal for:
- Serving images or documents directly to a browser.
- Storing files for distributed access.
- Streaming video and audio.
- Storing data for backup and restore, disaster recovery, and archiving.
- Storing data for analysis by an on-premises or Azure-hosted service.
### Accessing blob storage
Objects in blob storage can be accessed from anywhere in the world via HTTP or HTTPS. Users or client applications can access blobs via URLs, the Azure Storage REST API, Azure PowerShell, Azure CLI, or an Azure Storage client library. The storage client libraries are available for multiple languages, including .NET, Java, Node.js, Python, PHP, and Ruby.
### Blob storage tiers
Data stored in the cloud can grow at an exponential pace. To manage costs for your expanding storage needs, it's helpful to organize your data based on attributes like frequency of access and planned retention period. Data stored in the cloud can be handled differently based on how it's generated, processed, and accessed over its lifetime. Some data is actively accessed and modified throughout its lifetime. Some data is accessed frequently early in its lifetime, with access dropping drastically as the data ages. Some data remains idle in the cloud and is rarely, if ever, accessed after it's stored. To accommodate these different access needs, Azure provides several access tiers, which you can use to balance your storage costs with your access needs.
Azure Storage offers different access tiers for your blob storage, helping you store object data in the most cost-effective manner. The available access tiers include:
- Hot access tier : Optimized for storing data that is accessed frequently (for example, images for your website).
- Cool access tier : Optimized for data that is infrequently accessed and stored for at least 30 days (for example, invoices for your customers).
- Cold access tier : Optimized for storing data that is infrequently accessed and stored for at least 90 days.
- Archive access tier : Appropriate for data that is rarely accessed and stored for at least 180 days, with flexible latency requirements (for example, long-term backups).
The following considerations apply to the different access tiers:
- Hot, cool, and cold access t

## 3.5 Exercise - Create a storage blob

# Exercise - Create a storage blob
## Create a storage account
In this task, you'll create a new storage account.
- to the Azure portal at https://portal.azure.com 
- Select Create a resource .
- Under Categories, select Storage .
- Under Storage account, select Create .
- On the Basics tab of the Create a storage account blade, fill in the following information. Leave the defaults for everything else.
Setting 
Value 
Subscription 
Select the subscription you want to use for the exercise. 
Resource group 
Select Create new and enter IntroAzureRG and select OK 
Storage account name 
Create a unique storage account name 
Region 
Leave default 
Performance 
Standard 
Redundancy 
Locally redundant storage (LRS) 
- On the Advanced tab of the Create a storage account blade, fill in the following information. Leave the defaults for everything else.
Setting 
Value 
Allow enabling anonymous access on individual containers 
Checked 
- Select Review to review your storage account settings and allow Azure to validate the configuration.
- Once validated, select Create . Wait for the notification that the account was successfully created.
- Select Go to resource .
## Work with blob storage
In this section, you'll create a Blob container and upload a picture.
- Under Data storage , select Containers .
- Select + Container and complete the information.
Setting 
Value 
Name 
Enter a name for the container 
Anonymous access level 
Private (no anonymous access) 
- Select Create.
Note
Step 4 will need an image. If you want to upload an image you already have on your computer, continue to Step 4. Otherwise, open a new browser window and search Bing for an image of a flower. Save the image to your computer.
- Back in the Azure portal, select the container you created, then select Upload.
- Browse for the image file you want to upload. Select it and then select upload.
Note
You can upload as many blobs as you like in this way. New blobs will be listed within the container.
- Select the Blob (file) you just uploaded. You should be on the properties tab.
- Copy the URL from the URL field and paste it into a new tab. You should receive an error message similar to the following.
&lt;Error&gt;
&lt;Code&gt;ResourceNotFound&lt;/Code&gt;
&lt;Message&gt;The specified resource does not exist. RequestId:4a4bd3d9-101e-005a-1a3e-84bd42000000&lt;/Message&gt;
&lt;/Error&gt; 
## Change the access level of your blob
- Go back to the Azure portal.
- Select Change access level.
- Set the Anonymous access level to Blob (anonymous read access for blobs only).
- Select OK.
- Refresh the tab where you attempted to access the file earlier.
Congratulations - you've this exercise. You created a storage account, added a container to the storage account, and then uploaded blobs (files) to your container. Then you changed the access level so you could access your file from the internet.
## Clean up
To clean up the assets created in this exercise and avoid unnecessary costs, delete the resource group (and all associated resources).
- From the Azure home page, under Azure services, select Resource groups .
- Select the IntroAzureRG resource group.
- Select Delete resource group .
- Enter IntroAzureRG to confirm deletion of the resource group and select delete.

## 3.6 Identify Azure data migration options

# Identify Azure data migration options
Now that you understand the different storage options within Azure, it’s important to also understand how to get your data and information into Azure. Azure supports both real-time migration of infrastructure, applications, and data using Azure Migrate as well as asynchronous migration of data using Azure Data Box.
## Azure Migrate
Azure Migrate is a service that helps you migrate from an on-premises environment to the cloud. Azure Migrate functions as a hub to help you manage the assessment and migration of your on-premises datacenter to Azure. It provides the following:
- Unified migration platform : A single portal to start, run, and track your migration to Azure.
- Range of tools : A range of tools for assessment and migration. Azure Migrate tools include Azure Migrate: Discovery and assessment and Azure Migrate: Server Migration. Azure Migrate also integrates with other Azure services and tools, and with independent software vendor (ISV) offerings.
- Assessment and migration : In the Azure Migrate hub, you can assess and migrate your on-premises infrastructure to Azure.
### Integrated tools
In addition to working with tools from ISVs, the Azure Migrate hub also includes the following tools to help with migration:
- Azure Migrate: Discovery and assessment . Discover and assess on-premises servers running on VMware, Hyper-V, and physical servers in preparation for migration to Azure.
- Azure Migrate: Server Migration . Migrate VMware VMs, Hyper-V VMs, physical servers, other virtualized servers, and public cloud VMs to Azure.
- Data Migration Assistant . Data Migration Assistant is a stand-alone tool to assess SQL Servers. It helps pinpoint potential problems blocking migration. It identifies unsupported features, new features that can benefit you after migration, and the right path for database migration.
- Azure Database Migration Service . Migrate on-premises databases to Azure VMs running SQL Server, Azure SQL Database, or SQL Managed Instances.
- Azure App Service migration assistant . Azure App Service migration assistant is a standalone tool to assess on-premises websites for migration to Azure App Service. Use Migration Assistant to migrate .NET and PHP web apps to Azure.
- Azure Data Box . Use Azure Data Box products to move large amounts of offline data to Azure.
## Azure Data Box
Azure Data Box is a physical migration service that helps transfer large amounts of data in a quick, inexpensive, and reliable way. The secure data transfer is accelerated by shipping you a proprietary Data Box storage device that has a maximum usable storage capacity of 80 terabytes. The Data Box is transported to and from your datacenter via a regional carrier. A rugged case protects and secures the Data Box from damage during transit.
You can order the Data Box device via the Azure portal to import or export data from Azure. Once the device is received, you can quickly set it up using the local web UI and connect it to your network. Once you’re finished transferring the data (either into or out of Azure), simply return the Data Box. If you’re transferring data into Azure, the data is automatically uploaded once Microsoft receives the Data Box back. The entire process is tracked end-to-end by the Data Box service in the Azure portal.
### Use cases
Data Box is ideally suited to transfer data sizes larger than 40 TBs in scenarios with no to limited network connectivity. The data movement can be one-time, periodic, or an initial bulk data transfer followed by periodic transfers.
Here are the various scenarios where Data Box can be used to import data to Azure.
- Onetime migration - when a large amount of on-premises data is moved to Azure.
- Moving a media library from offline tapes into Azure to create an online media library.
- Migrating your VM farm, SQL server, and applications to Azure.
- Moving historical data to Azure for in-depth analysis and reporting using HDInsight.
- Initial bulk transfer - when an initial bulk transfer is done using Data Box (seed) followed by incremental transfers over the network.
- Periodic uploads - when large amount of data is generated periodically and needs to be moved to Azure.
Here are the various scenarios where Data Box can be used to export data from Azure.
- Disaster recovery - when a copy of the data from Azure is restored to an on-premises network. In a typical disaster recovery scenario, a large amount of Azure data is exported to a Data Box. Microsoft then ships this Data Box, and the data is restored on your premises in a short time.
- Security requirements - when you need to be able to export data out of Azure due to government or security requirements.
- Migrate back to on-premises or to another cloud service provider - when you want to move all the data back to on-premises, or to another cloud service provider, export data via Data Box to migrate the workloads.
Once the data from your import order is uploaded to Azure, the disks 

## 3.7 Identify Azure file movement options

# Identify Azure file movement options
In addition to large scale migration using services like Azure Migrate and Azure Data Box, Azure also has tools designed to help you move or interact with individual files or small file groups. Among those tools are AzCopy, Azure Storage Explorer, and Azure File Sync.
## AzCopy
AzCopy is a command-line utility that you can use to copy blobs or files to or from your storage account. With AzCopy, you can upload files, download files, copy files between storage accounts, and even synchronize files. AzCopy can even be configured to work with other cloud providers to help move files back and forth between clouds.
Important
Synchronizing blobs or files with AzCopy is one-direction synchronization. When you synchronize, you designate the source and destination, and AzCopy will copy files or blobs in that direction. It doesn't synchronize bi-directionally based on timestamps or other metadata.
## Azure Storage Explorer
Azure Storage Explorer is a standalone app that provides a graphical interface to manage files and blobs in your Azure Storage Account. It works on Windows, macOS, and Linux operating systems and uses AzCopy on the backend to perform all of the file and blob management tasks. With Storage Explorer, you can upload to Azure, download from Azure, or move between storage accounts.
## Azure File Sync
Azure File Sync is a tool that lets you centralize your file shares in Azure Files and keep the flexibility, performance, and compatibility of a Windows file server. It’s almost like turning your Windows file server into a miniature content delivery network. Once you install Azure File Sync on your local Windows server, it will automatically stay bi-directionally synced with your files in Azure.
With Azure File Sync, you can:
- Use any protocol that's available on Windows Server to access your data locally, including SMB, NFS, and FTPS.
- Have as many caches as you need across the world.
- Replace a failed local server by installing Azure File Sync on a new server in the same datacenter.
- Configure cloud tiering so the most frequently accessed files are replicated locally, while infrequently accessed files are kept in the cloud until requested.

## 3.9 Summary

# Summary
, you learned about the Azure storage services. You learned about the Azure Storage Account and how they relate to different storage services. You were introduced to storage blobs and redundancy options, and ways to migrate and move your data both into and within Azure.
## Learning objectives
You should now be able to:
- Compare Azure storage services.
- Describe storage tiers.
- Describe redundancy options.
- Describe storage account options and storage types.
- Identify options for moving files, including AzCopy, Azure Storage Explorer, and Azure File Sync.
- Describe migration options, including Azure Migrate and Azure Data Box.
## Additional resources
The following resources provide more information on topics or related to this module.
- Store data in Azure is a Microsoft Learn course that covers more information about storing data in Azure.
- Microsoft Certified: Azure Data Fundamentals is an entire certification, with associated training that dives deeper into data fundamentals on Azure.

---

# Module 4: Describe Azure identity, access, and security

Describe Azure identity, access, and security

## 4.1 Introduction

# Introduction
, you’ll be introduced to the Azure identity, access, and security services and tools. You’ll learn about directory services in Azure, authentication methods, and access control. You’ll also cover things like Zero Trust and defense in depth, and how they keep your cloud safer. You’ll wrap up with an introduction to Microsoft Defender for Cloud.
## Learning objectives
After completing this module, you’ll be able to:
- Describe directory services in Azure, including Microsoft Entra ID and Microsoft Entra Domain Services.
- Describe authentication methods in Azure, including single sign-on (SSO), multifactor authentication (MFA), and passwordless.
- Describe external identities and guest access in Azure.
- Describe Microsoft Entra Conditional Access.
- Describe Azure Role Based Access Control (RBAC).
- Describe the concept of Zero Trust.
- Describe the purpose of the defense in depth model.
- Describe the purpose of Microsoft Defender for Cloud.

## 4.2 Describe Azure directory services

# Describe Azure directory services
Microsoft Entra ID is a directory service that enables you to and access both Microsoft cloud applications and cloud applications that you develop. Microsoft Entra ID can also help you maintain your on-premises Active Directory deployment.
For on-premises environments, Active Directory running on Windows Server provides an identity and access management service that's managed by your organization. Microsoft Entra ID is Microsoft's cloud-based identity and access management service. With Microsoft Entra ID, you control the identity accounts, but Microsoft ensures that the service is available globally. If you've worked with Active Directory, Microsoft Entra ID will be familiar to you.
When you secure identities on-premises with Active Directory, Microsoft doesn't monitor sign-in attempts. When you connect Active Directory with Microsoft Entra ID, Microsoft can help protect you by detecting suspicious sign-in attempts at no extra cost. For example, Microsoft Entra ID can detect sign-in attempts from unexpected locations or unknown devices.
## Who uses Microsoft Entra ID?
Microsoft Entra ID is for:
- IT administrators . Administrators can use Microsoft Entra ID to control access to applications and resources based on their business requirements.
- App developers . Developers can use Microsoft Entra ID to provide a standards-based approach for adding functionality to applications that they build, such as adding SSO functionality to an app or enabling an app to work with a user's existing credentials.
- Users . Users can manage their identities and take maintenance actions like self-service password reset.
- Online service subscribers . Microsoft 365, Microsoft Office 365, Azure, and Microsoft Dynamics CRM Online subscribers are already using Microsoft Entra ID to authenticate into their account.
## What does Microsoft Entra ID do?
Microsoft Entra ID provides services such as:
- Authentication : This includes verifying identity to access applications and resources. It also includes providing functionality such as self-service password reset, multifactor authentication, a custom list of banned passwords, and smart lockout services.
- Single sign-on : Single sign-on (SSO) enables you to remember only one username and one password to access multiple applications. A single identity is tied to a user, which simplifies the security model. As users change roles or leave an organization, access modifications are tied to that identity, which greatly reduces the effort needed to change or disable accounts.
- Application management : You can manage your cloud and on-premises apps by using Microsoft Entra ID. Features like Application Proxy, SaaS apps, the My Apps portal, and single sign-on provide a better user experience.
- Device management : Along with accounts for individual people, Microsoft Entra ID supports the registration of devices. Registration enables devices to be managed through tools like Microsoft Intune. It also allows for device-based Conditional Access policies to restrict access attempts to only those coming from known devices, regardless of the requesting user account.
## Can I connect my on-premises AD with Microsoft Entra ID?
If you had an on-premises environment running Active Directory and a cloud deployment using Microsoft Entra ID, you would need to maintain two identity sets. However, you can connect Active Directory with Microsoft Entra ID, enabling a consistent identity experience between cloud and on-premises.
One method of connecting Microsoft Entra ID with your on-premises AD is using Microsoft Entra Connect. Microsoft Entra Connect synchronizes user identities between on-premises Active Directory and Microsoft Entra ID. Microsoft Entra Connect synchronizes changes between both identity systems, so you can use features like SSO, multifactor authentication, and self-service password reset under both systems.
## What is Microsoft Entra Domain Services?
Microsoft Entra Domain Services is a service that provides managed domain services such as domain join, group policy, lightweight directory access protocol (LDAP), and Kerberos/NTLM authentication. Just like Microsoft Entra ID lets you use directory services without having to maintain the infrastructure supporting it, with Microsoft Entra Domain Services, you get the benefit of domain services without the need to deploy, manage, and patch domain controllers (DCs) in the cloud.
A Microsoft Entra Domain Services managed domain lets you run legacy applications in the cloud that can't use modern authentication methods, or where you don't want directory lookups to always go back to an on-premises AD DS environment. You can lift and shift those legacy applications from your on-premises environment into a managed domain, without needing to manage the AD DS environment in the cloud.
Microsoft Entra Domain Services integrates with your existing Microsoft Entra tenant. This integration lets users to services and applic

## 4.3 Describe Azure authentication methods

# Describe Azure authentication methods
Authentication is the process of establishing the identity of a person, service, or device. It requires the person, service, or device to provide some type of credential to prove who they are. Authentication is like presenting ID when you’re traveling. It doesn’t confirm that you’re ticketed, it just proves that you're who you say you are. Azure supports multiple authentication methods, including standard passwords, single sign-on (SSO), multifactor authentication (MFA), and passwordless.
For the longest time, security and convenience seemed to be at odds with each other. Thankfully, new authentication solutions provide both security and convenience.
The following diagram shows the security level compared to the convenience. Notice Passwordless authentication is high security and high convenience while passwords on their own are low security but high convenience.
## What's single sign-on?
Single sign-on (SSO) enables a user to one time and use that credential to access multiple resources and applications from different providers. For SSO to work, the different applications and providers must trust the initial authenticator.
More identities mean more passwords to remember and change. Password policies can vary among applications. As complexity requirements increase, it becomes increasingly difficult for users to remember them. The more passwords a user has to manage, the greater the risk of a credential-related security incident.
Consider the process of managing all those identities. More strain is placed on help desks as they deal with account lockouts and password reset requests. If a user leaves an organization, tracking down all those identities and ensuring they're disabled can be challenging. If an identity is overlooked, this might allow access when it should have been eliminated.
With SSO, you need to remember only one ID and one password. Access across applications is granted to a single identity that's tied to the user, which simplifies the security model. As users change roles or leave an organization, access is tied to a single identity. This change greatly reduces the effort needed to change or disable accounts. Using SSO for accounts makes it easier for users to manage their identities and for IT to manage users.
Important
Single sign-on is only as secure as the initial authenticator because the subsequent connections are all based on the security of the initial authenticator.
## What’s multifactor authentication?
Multifactor authentication is the process of prompting a user for an extra form (or factor) of identification during the sign-in process. MFA helps protect against a password compromise in situations where the password was compromised but the second factor wasn't.
Think about how you to websites, email, or online services. After entering your username and password, have you ever needed to enter a code that was sent to your phone? If so, you've used multifactor authentication to .
Multifactor authentication provides additional security for your identities by requiring two or more elements to fully authenticate. These elements fall into three categories:
- Something the user knows – this might be a challenge question.
- Something the user has – this might be a code that's sent to the user's mobile phone.
- Something the user is – this is typically some sort of biometric property, such as a fingerprint or face scan.
Multifactor authentication increases identity security by limiting the impact of credential exposure (for example, stolen usernames and passwords). With multifactor authentication enabled, an attacker who has a user's password would also need to have possession of their phone or their fingerprint to fully authenticate.
Compare multifactor authentication with single-factor authentication. Under single-factor authentication, an attacker would need only a username and password to authenticate. Multifactor authentication should be enabled wherever possible because it adds enormous benefits to security.
### What's Microsoft Entra multifactor authentication?
Microsoft Entra multifactor authentication is a Microsoft service that provides multifactor authentication capabilities. Microsoft Entra multifactor authentication enables users to choose an additional form of authentication during sign-in, such as a phone call or mobile app notification.
## What’s passwordless authentication?
Features like MFA are a great way to secure your organization, but users often get frustrated with the additional security layer on top of having to remember their passwords. People are more likely to comply when it's easy and convenient to do so. Passwordless authentication methods are more convenient because the password is removed and replaced with something you have, plus something you are, or something you know.
Passwordless authentication needs to be set up on a device before it can work. For example, your computer is something you have. Once it’s been registe

## 4.4 Describe Azure external identities

# Describe Azure external identities
An external identity is a person, device, service, etc. that is outside your organization. Microsoft Entra External ID refers to all the ways you can securely interact with users outside of your organization. If you want to collaborate with partners, distributors, suppliers, or vendors, you can share your resources and define how your internal users can access external organizations. If you're a developer creating consumer-facing apps, you can manage your customers' identity experiences.
External identities may sound similar to single sign-on. With External Identities, external users can "bring their own identities." Whether they have a corporate or government-issued digital identity, or an unmanaged social identity like Google or , they can use their own credentials to . The external user’s identity provider manages their identity, and you manage access to your apps with Microsoft Entra ID or Azure AD B2C to keep your resources protected.
The following capabilities make up External Identities:
- Business to business (B2B) collaboration - Collaborate with external users by letting them use their preferred identity to sign-in to your Microsoft applications or other enterprise applications (SaaS apps, custom-developed apps, etc.). B2B collaboration users are represented in your directory, typically as guest users.
- B2B direct connect - Establish a mutual, two-way trust with another Microsoft Entra organization for seamless collaboration. B2B direct connect currently supports Teams shared channels, enabling external users to access your resources from within their home instances of Teams. B2B direct connect users aren't represented in your directory, but they're visible from within the Teams shared channel and can be monitored in Teams admin center reports.
- Microsoft Azure Active Directory business to customer (B2C) - Publish modern SaaS apps or custom-developed apps (excluding Microsoft apps) to consumers and customers, while using Azure AD B2C for identity and access management.
Depending on how you want to interact with external organizations and the types of resources you need to share, you can use a combination of these capabilities.
With Microsoft Entra ID, you can easily enable collaboration across organizational boundaries by using the Microsoft Entra B2B feature. Guest users from other tenants can be invited by administrators or by other users. This capability also applies to social identities such as Microsoft accounts.
You also can easily ensure that guest users have appropriate access. You can ask the guests themselves or a decision maker to participate in an access review and recertify (or attest) to the guests' access. The reviewers can give their input on each user's need for continued access, based on suggestions from Microsoft Entra ID. When an access review is finished, you can then make changes and remove access for guests who no longer need it.

## 4.5 Describe Azure conditional access

# Describe Azure conditional access
Conditional Access is a tool that Microsoft Entra ID uses to allow (or deny) access to resources based on identity signals. These signals include who the user is, where the user is, and what device the user is requesting access from.
Conditional Access helps IT administrators:
- Empower users to be productive wherever and whenever.
- Protect the organization's assets.
Conditional Access also provides a more granular multifactor authentication experience for users. For example, a user might not be challenged for second authentication factor if they're at a known location. However, they might be challenged for a second authentication factor if their sign-in signals are unusual or they're at an unexpected location.
During sign-in, Conditional Access collects signals from the user, makes decisions based on those signals, and then enforces that decision by allowing or denying the access request or challenging for a multifactor authentication response.
The following diagram illustrates this flow:
Here, the signal might be the user's location, the user's device, or the application that the user is trying to access.
Based on these signals, the decision might be to allow full access if the user is signing in from their usual location. If the user is signing in from an unusual location or a location that's marked as high risk, then access might be blocked entirely or possibly granted after the user provides a second form of authentication.
Enforcement is the action that carries out the decision. For example, the action is to allow access or require the user to provide a second form of authentication.
## When can I use Conditional Access?
Conditional Access is useful when you need to:
- Require multifactor authentication (MFA) to access an application depending on the requester’s role, location, or network. For example, you could require MFA for administrators but not regular users or for people connecting from outside your corporate network.
- Require access to services only through approved client applications. For example, you could limit which email applications are able to connect to your email service.
- Require users to access your application only from managed devices. A managed device is a device that meets your standards for security and compliance.
- Block access from untrusted sources, such as access from unknown or unexpected locations.

## 4.6 Describe Azure role-based access control

# Describe Azure role-based access control
When you have multiple IT and engineering teams, how can you control what access they have to the resources in your cloud environment? The principle of least privilege says you should only grant access up to the level needed to complete a task. If you only need read access to a storage blob, then you should only be granted read access to that storage blob. Write access to that blob shouldn’t be granted, nor should read access to other storage blobs. It’s a good security practice to follow.
However, managing that level of permissions for an entire team would become tedious. Instead of defining the detailed access requirements for each individual, and then updating access requirements when new resources are created or new people join the team, Azure enables you to control access through Azure role-based access control (Azure RBAC).
Azure provides built-in roles that describe common access rules for cloud resources. You can also define your own roles. Each role has an associated set of access permissions that relate to that role. When you asdividuals or groups to one or more roles, they receive all the associated access permissions.
So, if you hire a new engineer and add them to the Azure RBAC group for engineers, they automatically get the same access as the other engineers in the same Azure RBAC group. Similarly, if you itional resources and point Azure RBAC at them, everyone in that Azure RBAC group will now have those permissions on the new resources as well as the existing resources.
## How is role-based access control applied to resources?
Role-based access control is applied to a scope, which is a resource or set of resources that this access applies to.
The following diagram shows the relationship between roles and scopes. A management group, subscription, or resource group might be given the role of owner, so they have increased control and authority. An observer, who isn't expected to make any updates, might be given a role of Reader for the same scope, enabling them to review or observe the management group, subscription, or resource group.
Scopes include:
- A management group (a collection of multiple subscriptions).
- A single subscription.
- A resource group.
- A single resource.
Observers, users managing resources, admins, and automated processes illustrate the kinds of users or accounts that would typically be assigned each of the various roles.
Azure RBAC is hierarchical, in that when you grant access at a parent scope, those permissions are inherited by all child scopes. For example:
- When you assign the Owner role to a user at the management group scope, that user can manage everything in all subscriptions within the management group.
- When you assign the Reader role to a group at the subscription scope, the members of that group can view every resource group and resource within the subscription.
## How is Azure RBAC enforced?
Azure RBAC is enforced on any action that's initiated against an Azure resource that passes through Azure Resource Manager. Resource Manager is a management service that provides a way to organize and secure your cloud resources.
You typically access Resource Manager from the Azure portal, Azure Cloud Shell, Azure PowerShell, and the Azure CLI. Azure RBAC doesn't enforce access permissions at the application or data level. Application security must be handled by your application.
Azure RBAC uses an allow model. When you're assigned a role, Azure RBAC allows you to perform actions within the scope of that role. If one role assignment grants you read permissions to a resource group and a different role assignment grants you write permissions to the same resource group, you have both read and write permissions on that resource group.

## 4.7 Describe Zero Trust model

# Describe Zero Trust model
Zero Trust is a security model that assumes the worst case scenario and protects resources with that expectation. Zero Trust assumes breach at the outset, and then verifies each request as though it originated from an uncontrolled network.
Today, organizations need a new security model that effectively adapts to the complexity of the modern environment; embraces the mobile workforce; and protects people, devices, applications, and data wherever they're located.
To address this new world of computing, Microsoft highly recommends the Zero Trust security model, which is based on these guiding principles:
- Verify explicitly - Always authenticate and authorize based on all available data points.
- Use least privilege access - Limit user access with Just-In-Time and Just-Enough-Access (JIT/JEA), risk-based adaptive policies, and data protection.
- Assume breach - Minimize blast radius and segment access. Verify end-to-end encryption. Use analytics to get visibility, drive threat detection, and improve defenses.
## Adjusting to Zero Trust
Traditionally, corporate networks were restricted, protected, and generally assumed safe. Only managed computers could join the network, VPN access was tightly controlled, and personal devices were frequently restricted or blocked.
The Zero Trust model flips that scenario. Instead of assuming that a device is safe because it’s within the corporate network, it requires everyone to authenticate. Then grants access based on authentication rather than location.

## 4.8 Describe defense-in-depth

# Describe defense-in-depth
The objective of defense-in-depth is to protect information and prevent it from being stolen by those who aren't authorized to access it.
A defense-in-depth strategy uses a series of mechanisms to slow the advance of an attack that aims at acquiring unauthorized access to data.
## Layers of defense-in-depth
You can visualize defense-in-depth as a set of layers, with the data to be secured at the center and all the other layers functioning to protect that central data layer.
Each layer provides protection so that if one layer is breached, a subsequent layer is already in place to prevent further exposure. This approach removes reliance on any single layer of protection. It slows down an attack and provides alert information that security teams can act upon, either automatically or manually.
Here's a brief overview of the role of each layer:
- The physical security layer is the first line of defense to protect computing hardware in the datacenter.
- The identity and access layer controls access to infrastructure and change control.
- The perimeter layer uses distributed denial of service (DDoS) protection to filter large-scale attacks before they can cause a denial of service for users.
- The network layer limits communication between resources through segmentation and access controls.
- The compute layer secures access to virtual machines.
- The application layer helps ensure that applications are secure and free of security vulnerabilities.
- The data layer controls access to business and customer data that you need to protect.
These layers provide a guideline for you to help make security configuration decisions in all of the layers of your applications.
Azure provides security tools and features at every level of the defense-in-depth concept. Let's take a closer look at each layer:
### Physical security
Physically securing access to buildings and controlling access to computing hardware within the datacenter are the first line of defense.
With physical security, the intent is to provide physical safeguards against access to assets. These safeguards ensure that other layers can't be bypassed, and loss or theft is handled appropriately. Microsoft uses various physical security mechanisms in its cloud datacenters.
### Identity and access
The identity and access layer is all about ensuring that identities are secure, that access is granted only to what's needed, and that sign-in events and changes are logged.
At this layer, it's important to:
- Control access to infrastructure and change control.
- Use single sign-on (SSO) and multifactor authentication.
- Audit events and changes.
### Perimeter
The network perimeter protects from network-based attacks against your resources. Identifying these attacks, eliminating their impact, and alerting you when they happen are important ways to keep your network secure.
At this layer, it's important to:
- Use DDoS protection to filter large-scale attacks before they can affect the availability of a system for users.
- Use perimeter firewalls to identify and alert on malicious attacks against your network.
### Network
At this layer, the focus is on limiting the network connectivity across all your resources to allow only what's required. By limiting this communication, you reduce the risk of an attack spreading to other systems in your network.
At this layer, it's important to:
- Limit communication between resources.
- Deny by default.
- Restrict inbound internet access and limit outbound access where appropriate.
- Implement secure connectivity to on-premises networks.
### Compute
Malware, unpatched systems, and improperly secured systems open your environment to attacks. The focus in this layer is on making sure that your compute resources are secure and that you have the proper controls in place to minimize security issues.
At this layer, it's important to:
- Secure access to virtual machines.
- Implement endpoint protection on devices and keep systems patched and current.
### Application
Integrating security into the application development lifecycle helps reduce the number of vulnerabilities introduced in code. Every development team should ensure that its applications are secure by default.
At this layer, it's important to:
- Ensure that applications are secure and free of vulnerabilities.
- Store sensitive application secrets in a secure storage medium.
- Make security a design requirement for all application development.
### Data
Those who store and control access to data are responsible for ensuring that it's properly secured. Often, regulatory requirements dictate the controls and processes that must be in place to ensure the confidentiality, integrity, and availability of the data.
In almost all cases, attackers are after data:
- Stored in a database.
- Stored on disk inside virtual machines.
- Stored in software as a service (SaaS) applications, such as Office 365.
- Managed through cloud storage.

## 4.9 Describe Microsoft Defender for Cloud

# Describe Microsoft Defender for Cloud
Defender for Cloud is a monitoring tool for security posture management and threat protection. It monitors your cloud, on-premises, hybrid, and multicloud environments to provide guidance and notifications aimed at strengthening your security posture.
Defender for Cloud provides the tools needed to harden your resources, track your security posture, protect against cyber attacks, and streamline security management. Deployment of Defender for Cloud is easy, it’s already natively integrated to Azure.
## Protection everywhere you’re deployed
Because Defender for Cloud is an Azure-native service, many Azure services are monitored and protected without needing any deployment. However, if you also have an on-premises datacenter or are also operating in another cloud environment, monitoring of Azure services may not give you a complete picture of your security situation.
When necessary, Defender for Cloud can automatically deploy a Log Analytics agent to gather security-related data. For Azure machines, deployment is handled directly. For hybrid and multicloud environments, Microsoft Defender plans are extended to non-Azure machines with the help of Azure Arc. Cloud security posture management (CSPM) features are extended to multicloud machines without the need for any agents.
### Azure-native protections
Defender for Cloud helps you detect threats across:
- Azure PaaS services – Detect threats targeting Azure services including Azure App Service, Azure SQL, Azure Storage Account, and more data services. You can also perform anomaly detection on your Azure activity logs using the native integration with Microsoft Defender for Cloud Apps (formerly known as Microsoft Cloud App Security).
- Azure data services – Defender for Cloud includes capabilities that help you automatically classify your data in Azure SQL. You can also get assessments for potential vulnerabilities across Azure SQL and Storage services, and recommendations for how to mitigate them.
- Networks – Defender for Cloud helps you limit exposure to brute force attacks. By reducing access to virtual machine ports, using the just-in-time VM access, you can harden your network by preventing unnecessary access. You can set secure access policies on selected ports, for only authorized users, allowed source IP address ranges or IP addresses, and for a limited amount of time.
### Defend your hybrid resources
In addition to defending your Azure environment, you can add Defender for Cloud capabilities to your hybrid cloud environment to protect your non-Azure servers. To help you focus on what matters the most, you'll get customized threat intelligence and prioritized alerts according to your specific environment.
To extend protection to on-premises machines, deploy Azure Arc and enable Defender for Cloud's enhanced security features.
### Defend resources running on other clouds
Defender for Cloud can also protect resources in other clouds (such as AWS and GCP).
For example, if you've connected an Amazon Web Services (AWS) account to an Azure subscription, you can enable any of these protections:
- Defender for Cloud's CSPM features extend to your AWS resources. This agentless plan assesses your AWS resources according to AWS-specific security recommendations, and includes the results in the secure score. The resources will also be assessed for compliance with built-in standards specific to AWS (AWS CIS, AWS PCI DSS, and AWS Foundational Security Best Practices). Defender for Cloud's asset inventory page is a multicloud enabled feature helping you manage your AWS resources alongside your Azure resources.
- Microsoft Defender for Containers extends its container threat detection and advanced defenses to your Amazon EKS Linux clusters.
- Microsoft Defender for Servers brings threat detection and advanced defenses to your Windows and Linux EC2 instances.
## Assess, Secure, and Defend
Defender for Cloud fills three vital needs as you manage the security of your resources and workloads in the cloud and on-premises:
- Continuously assess – Know your security posture. Identify and track vulnerabilities.
- Secure – Harden resources and services with Azure Security Benchmark.
- Defend – Detect and resolve threats to resources, workloads, and services.
### Continuously assess
Defender for cloud helps you continuously assess your environment. Defender for Cloud includes vulnerability assessment solutions for your virtual machines, container registries, and SQL servers.
Microsoft Defender for servers includes automatic, native integration with Microsoft Defender for Endpoint. With this integration enabled, you'll have access to the vulnerability findings from Microsoft threat and vulnerability management.
Between these assessment tools you’ll have regular, detailed vulnerability scans that cover your compute, data, and infrastructure. You can review and respond to the results of these scans all from within Defender for Cloud.
### Secu

## 4.11 Summary

# Summary
, you learned about Azure identity, access, and security services and tools. You covered authentication methods, including which ones are more secure. You learned about restricting access based on a role to help create a more secure environment. And, you learned about the Defense In Depth and Zero Trust models.
## Learning objectives
You should now be able to:
- Describe directory services in Azure, including Microsoft Entra ID and Microsoft Entra Domain Services.
- Describe authentication methods in Azure, including single sign-on (SSO), multifactor authentication (MFA), and passwordless.
- Describe external identities and guest access in Azure.
- Describe Microsoft Entra Conditional Access.
- Describe Azure Role Based Access Control (RBAC).
- Describe the concept of Zero Trust.
- Describe the purpose of the defense in depth model.
- Describe the purpose of Microsoft Defender for Cloud.
## Additional resources
The following resources provide more information on topics or related to this module.
Microsoft Certified: Security, Compliance, and Identity Fundamentals is an entire certification, with associated training, dedicated to helping you better understand and manage Security, Compliance, and identity.

---

# Key Concepts Index

- + Container
- Access control boundary
- Accessible
- Advanced
- Allow
- App developers
- Application management
- Archive access tier
- Assessment and migration
- Assume breach
- Authentication
- Azure App Service migration assistant
- Azure Blobs
- Azure Data Box
- Azure Database Migration Service
- Azure Disks
- Azure Files
- Azure Migrate: Discovery and assessment
- Azure Migrate: Server Migration
- Azure Queues
- Azure Tables:
- B2B direct connect
- Basics
- Basics tab
- Billing
- Billing boundary
- Bring ideas to life:
- Business to business (B2B) collaboration
- Cold access tier
- Containers
- Cool access tier
- Create
- Create a hierarchy that applies a policy
- Create a resource
- Data Migration Assistant
- Data storage
- Delete resource group
- Deny
- Device management
- Durable and highly available
- During disaster recovery
- During testing and development
- Endpoint
- Environments
- Exercise - Create an Azure virtual machine
- Familiar programmability
- Fault domain
- Fully managed
- Go to resource
- Hot access tier

# Code Samples

### Sample 1
```
az version
```

### Sample 2
```
az group create --name IntroAzureRG --location eastus
```

### Sample 3
```
az vm create \
  --resource-group "IntroAzureRG" \
  --name my-vm \
  --size Standard_D2s_v5 \
  --public-ip-sku Standard \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys
```

### Sample 4
```
az vm extension set \
  --resource-group "IntroAzureRG" \
  --vm-name my-vm \
  --name customScript \
  --publisher Microsoft.Azure.Extensions \
  --version 2.1 \
  --settings '{"fileUris":["https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-nginx.sh"]}' \
  --protected-settings '{"commandToExecute": "./configure-nginx.sh"}'
```

### Sample 5
```
IPADDRESS="$(az vm list-ip-addresses \
  --resource-group "IntroAzureRG" \
  --name my-vm \
  --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
  --output tsv)"
```

### Sample 6
```
curl --connect-timeout 5 http://$IPADDRESS
```

### Sample 7
```
curl: (28) Connection timed out after 5001 milliseconds
```

### Sample 8
```
echo $IPADDRESS
```

### Sample 9
```
az network nsg list \
  --resource-group "IntroAzureRG" \
  --query '[].name' \
  --output tsv
```

### Sample 10
```
my-vmNSG
```

### Sample 11
```
az network nsg rule list \
  --resource-group "IntroAzureRG" \
  --nsg-name my-vmNSG
```

### Sample 12
```
az network nsg rule list \
  --resource-group "IntroAzureRG" \
  --nsg-name my-vmNSG \
  --query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' \
  --output table
```

### Sample 13
```
Name              Priority    Port    Access
-----------------  ----------  ------  --------
default-allow-ssh  1000        22      Allow
```

### Sample 14
```
az network nsg rule create \
  --resource-group "IntroAzureRG" \
  --nsg-name my-vmNSG \
  --name allow-http \
  --protocol tcp \
  --priority 100 \
  --destination-port-range 80 \
  --access Allow
```

### Sample 15
```
az network nsg rule list \
  --resource-group "IntroAzureRG" \
  --nsg-name my-vmNSG \
  --query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' \
  --output table
```

### Sample 16
```
Name              Priority    Port    Access
-----------------  ----------  ------  --------
default-allow-ssh  1000        22      Allow
allow-http          100        80      Allow
```

### Sample 17
```
curl --connect-timeout 5 http://$IPADDRESS
```

### Sample 18
```
<html><body><h2>Welcome to Azure! My name is my-vm.</h2></body></html>
```

### Sample 19
```
<Error>
<Code>ResourceNotFound</Code>
  <Message>The specified resource does not exist. RequestId:4a4bd3d9-101e-005a-1a3e-84bd42000000</Message>
</Error>
```
