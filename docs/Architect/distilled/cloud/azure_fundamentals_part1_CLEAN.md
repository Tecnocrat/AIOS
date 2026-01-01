# Introduction to Cloud Infrastructure: Describe Cloud Concepts

**Source**: https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/
**Level**: Beginner
**Modules**: 3
**Total Units**: 21

## Overview

Introductory learning path that is part of the Azure Infrastructure fundamentals content.

---

# Module 1: Describe Cloud Computing

Introduction to concepts surrounding cloud computing. Mostly platform agnostic, focused instead on general concepts.

## 1.1 Introduction to Microsoft Azure Fundamentals

# Introduction to Microsoft Azure Fundamentals
Microsoft Azure is a cloud computing platform with an ever-expanding set of services to help you build solutions to meet your business goals. Azure services support everything from simple to complex. Azure has simple web services for hosting your business presence in the cloud. Azure also supports running fully virtualized computers managing your custom software solutions. Azure provides a wealth of cloud-based services like remote storage, database hosting, and centralized account management. Azure also offers new capabilities like artificial intelligence (AI) and Internet of Things (IoT) focused services.
In this series, you’ll cover cloud computing basics, be introduced to some of the core services provided by Microsoft Azure, and will learn more about the governance and compliance services that you can use.
## What is Azure Fundamentals?
Azure Fundamentals is a series of three learning paths that familiarize you with Azure and its many services and features.
Whether you're interested in compute, networking, or storage services; learning about cloud security best practices; or exploring governance and management options, think of Azure Fundamentals as your curated guide to Azure.
Azure Fundamentals includes interactive exercises that give you hands-on experience with Azure. Many exercises provide a temporary Azure portal environment called the sandbox, which allows you to practice creating cloud resources for free at your own pace.
Technical IT experience isn't required; however, having general IT knowledge will help you get the most from your learning experience.
## Why should I take Azure Fundamentals?
If you're just beginning to work with the cloud, or if you already have cloud experience, Azure Fundamentals provides you with everything you need to get started.
No matter your goals, Azure Fundamentals has something for you. You should take this course if you:
- Have general interest in Azure or in cloud computing
- Want to earn official certification from Microsoft (AZ-900)
The Azure Fundamentals learning path series can help you prepare for Exam AZ-900: Microsoft Azure Fundamentals. This exam includes three knowledge domain areas:
AZ-900 Domain Area 
Weight 
Describe cloud concepts 
25-30% 
Describe Azure architecture and services 
35-40% 
Describe Azure management and governance 
30-35% 
Each domain area maps to a learning path in Azure Fundamentals. The percentages shown indicate the relative weight of each area on the exam. The higher the percentage, the more questions that part of the exam will contain. Be sure to read the exam page for specifics about what skills are covered in each area.
This training helps you develop a broad understanding of Azure.

## 1.2 Introduction to cloud computing

# Introduction to cloud computing
, you’ll be introduced to general cloud concepts. You’ll start with an introduction to the cloud in general. Then you'll dive into concepts like shared responsibility, different cloud models, and explore the unique pricing method for the cloud.
If you’re already familiar with cloud computing, this module may be largely review for you.
## Learning objectives
After completing this module, you’ll be able to:
- Define cloud computing.
- Describe the shared responsibility model.
- Define cloud models, including public, private, and hybrid.
- Identify appropriate use cases for each cloud model.
- Describe the consumption-based model.
- Compare cloud pricing models.

## 1.3 What is cloud computing

# What is cloud computing
Cloud computing is the delivery of computing services over the internet. Computing services include common IT infrastructure such as virtual machines, storage, databases, and networking. Cloud services also expand the traditional IT offerings to include things like Internet of Things (IoT), machine learning (ML), and artificial intelligence (AI).
Because cloud computing uses the internet to deliver these services, it doesn’t have to be constrained by physical infrastructure the same way that a traditional datacenter is. That means if you need to increase your IT infrastructure rapidly, you don’t have to wait to build a new datacenter—you can use the cloud to rapidly expand your IT footprint.
This short video provides a quick introduction to cloud computing.

## 1.4 Describe the shared responsibility model

# Describe the shared responsibility model
You may have heard of the shared responsibility model, but you may not understand what it means or how it impacts cloud computing.
Start with a traditional corporate datacenter. The company is responsible for maintaining the physical space, ensuring security, and maintaining or replacing the servers if anything happens. The IT department is responsible for maintaining all the infrastructure and software needed to keep the datacenter up and running. They’re also likely to be responsible for keeping all systems patched and on the correct version.
With the shared responsibility model, these responsibilities get shared between the cloud provider and the consumer. Physical security, power, cooling, and network connectivity are the responsibility of the cloud provider. The consumer isn’t collocated with the datacenter, so it wouldn’t make sense for the consumer to have any of those responsibilities.
At the same time, the consumer is responsible for the data and information stored in the cloud. (You wouldn’t want the cloud provider to be able to read your information.) The consumer is also responsible for access security, meaning you only give access to those who need it.
Then, for some things, the responsibility depends on the situation. If you’re using a cloud SQL database, the cloud provider would be responsible for maintaining the actual database. However, you’re still responsible for the data that gets ingested into the database. If you deployed a virtual machine and installed an SQL database on it, you’d be responsible for database patches and updates, as well as maintaining the data and information stored in the database.
With an on-premises datacenter, you’re responsible for everything. With cloud computing, those responsibilities shift. The shared responsibility model is heavily tied into the cloud service types (covered later in this learning path): infrastructure as a service (IaaS), platform as a service (PaaS), and software as a service (SaaS). IaaS places the most responsibility on the consumer, with the cloud provider being responsible for the basics of physical security, power, and connectivity. On the other end of the spectrum, SaaS places most of the responsibility with the cloud provider. PaaS, being a middle ground between IaaS and SaaS, rests somewhere in the middle and evenly distributes responsibility between the cloud provider and the consumer.
The following diagram highlights how the Shared Responsibility Model informs who is responsible for what, depending on the cloud service type.
When using a cloud provider, you’ll always be responsible for:
- The information and data stored in the cloud
- Devices that are allowed to connect to your cloud (cell phones, computers, and so on)
- The accounts and identities of the people, services, and devices within your organization
The cloud provider is always responsible for:
- The physical datacenter
- The physical network
- The physical hosts
Your service model will determine responsibility for things like:
- Operating systems
- Network controls
- Applications
- Identity and infrastructure

## 1.5 Define cloud models

# Define cloud models
What are cloud models? The cloud models define the deployment type of cloud resources. The three main cloud models are: private, public, and hybrid.
## Private cloud
Let’s start with a private cloud. A private cloud is, in some ways, the natural evolution from a corporate datacenter. It’s a cloud (delivering IT services over the internet) that’s used by a single entity. Private cloud provides much greater control for the company and its IT department. However, it also comes with greater cost and fewer of the benefits of a public cloud deployment. Finally, a private cloud may be hosted from your on site datacenter. It may also be hosted in a dedicated datacenter offsite, potentially even by a third party that has dedicated that datacenter to your company.
## Public cloud
A public cloud is built, controlled, and maintained by a third-party cloud provider. With a public cloud, anyone that wants to purchase cloud services can access and use resources. The general public availability is a key difference between public and private clouds.
## Hybrid cloud
A hybrid cloud is a computing environment that uses both public and private clouds in an inter-connected environment. A hybrid cloud environment can be used to allow a private cloud to surge for increased, temporary demand by deploying public cloud resources. Hybrid cloud can be used to provide an extra layer of security. For example, users can flexibly choose which services to keep in public cloud and which to deploy to their private cloud infrastructure.
The following table highlights a few key comparative aspects between the cloud models.
Public cloud 
Private cloud 
Hybrid cloud 
No capital expenditures to scale up 
Organizations have complete control over resources and security 
Provides the most flexibility 
Applications can be quickly provisioned and deprovisioned 
Data is not collocated with other organizations’ data 
Organizations determine where to run their applications 
Organizations pay only for what they use 
Hardware must be purchased for startup and maintenance 
Organizations control security, compliance, or legal requirements 
Organizations don’t have complete control over resources and security 
Organizations are responsible for hardware maintenance and updates 
## Multi-cloud
A fourth, and increasingly likely scenario is a multi-cloud scenario. In a multi-cloud scenario, you use multiple public cloud providers. Maybe you use different features from different cloud providers. Or maybe you started your cloud journey with one provider and are in the process of migrating to a different provider. Regardless, in a multi-cloud environment you deal with two (or more) public cloud providers and manage resources and security in both environments.
## Azure Arc
Azure Arc is a set of technologies that helps manage your cloud environment. Azure Arc can help manage your cloud environment whether it's a public cloud solely on Azure, a private cloud in your datacenter, a hybrid configuration, or even a multi-cloud environment running on multiple cloud providers at once.
## Azure VMware Solution
What if you’re already established with VMware in a private cloud environment but want to migrate to a public or hybrid cloud? Azure VMware Solution lets you run your VMware workloads in Azure with seamless integration and scalability.

## 1.6 Describe the consumption-based model

# Describe the consumption-based model
When comparing IT infrastructure models, there are two types of expenses to consider. Capital expenditure (CapEx) and operational expenditure (OpEx).
CapEx is typically a one-time, up-front expenditure to purchase or secure tangible resources. A new building, repaving the parking lot, building a datacenter, or buying a company vehicle are examples of CapEx.
In contrast, OpEx is spending money on services or products over time. Renting a convention center, leasing a company vehicle, or signing up for cloud services are all examples of OpEx.
Cloud computing falls under OpEx because cloud computing operates on a consumption-based model. With cloud computing, you don’t pay for the physical infrastructure, the electricity, the security, or anything else associated with maintaining a datacenter. Instead, you pay for the IT resources you use. If you don’t use any IT resources this month, you don’t pay for any IT resources.
This consumption-based model has many benefits, including:
- No upfront costs.
- No need to purchase and manage costly infrastructure that users might not use to its fullest potential.
- The ability to pay for more resources when they're needed.
- The ability to stop paying for resources that are no longer needed.
With a traditional datacenter, you try to estimate the future resource needs. If you overestimate, you spend more on your datacenter than you need to and potentially waste money. If you underestimate, your datacenter will quickly reach capacity and your applications and services may suffer from decreased performance. Fixing an under-provisioned datacenter can take a long time. You may need to order, receive, and install more hardware. You'll also need to add power, cooling, and networking for the extra hardware.
In a cloud-based model, you don’t have to worry about getting the resource needs just right. If you find that you need more virtual machines, you add more. If the demand drops and you don’t need as many virtual machines, you remove machines as needed. Either way, you’re only paying for the virtual machines that you use, not the “extra capacity” that the cloud provider has on hand.
## Compare cloud pricing models
Cloud computing is the delivery of computing services over the internet by using a pay-as-you-go pricing model. You typically pay only for the cloud services you use, which helps you:
- Plan and manage your operating costs.
- Run your infrastructure more efficiently.
- Scale as your business needs change.
To put it another way, cloud computing is a way to rent compute power and storage from someone else’s datacenter. You can treat cloud resources like you would resources in your own datacenter. However, unlike in your own datacenter, when you're done using cloud resources, you give them back. You’re billed only for what you use.
Instead of maintaining CPUs and storage in your datacenter, you rent them for the time that you need them. The cloud provider takes care of maintaining the underlying infrastructure for you. The cloud enables you to quickly solve your toughest business challenges and bring cutting-edge solutions to your users.

## 1.8 Summary

# Summary
, you learned about general cloud concepts. You started with things like just understanding what cloud computing is. You also learned about the shared responsibility model and how you and your cloud provider share the responsibility of keeping your information in the cloud secure. You briefly covered the differences between the cloud models (public, private, hybrid, and multicloud). Then, you wrapped up with a unit on how the cloud shifts IT spend from a capital expense to an operational expense.
## Learning objectives
You should now be able to:
- Define cloud computing.
- Describe the shared responsibility model.
- Define cloud models, including public, private, and hybrid.
- Identify appropriate use cases for each cloud model.
- Describe the consumption-based model.
- Compare cloud pricing models.
## Additional resources
The following resources provide more information on topics or related to this module.
- Shared responsibility model The shared responsibility model is the sharing of responsibilities for the cloud between you and your cloud provider.
- Introduction to Azure VMware Solution is a Microsoft Learn course that dives deeper into Azure VMware Solution.
- Introduction to Azure hybrid cloud services is a Microsoft Learn course that explains hybrid cloud in greater detail.

---

# Module 2: Describe the benefits of using cloud services

Introduction to concepts surrounding cloud computing. Mostly platform agnostic, focused instead on general concepts.

## 2.1 Introduction

# Introduction
, you’ll be introduced to some of the benefits that cloud computing offers. You’ll learn how cloud computing can help you meet variable demand while providing a good experience for your customer. You’ll also learn about security, governance, and overall manageability in the cloud.
## Learning objectives
After completing this module, you’ll be able to:
- Describe the benefits of high availability and scalability in the cloud.
- Describe the benefits of reliability and predictability in the cloud.
- Describe the benefits of security and governance in the cloud.
- Describe the benefits of manageability in the cloud.

## 2.2 Describe the benefits of high availability and scalability in the cloud

# Describe the benefits of high availability and scalability in the cloud
When building or deploying a cloud application, two of the biggest considerations are uptime (or availability) and the ability to handle demand (or scale).
## High availability
When you’re deploying an application, a service, or any IT resources, it’s important the resources are available when needed. High availability focuses on ensuring maximum availability, regardless of disruptions or events that may occur.
When you’re architecting your solution, you’ll need to account for service availability guarantees. Azure is a highly available cloud environment with uptime guarantees depending on the service. These guarantees are part of the service-level agreements (SLAs).
This short video describes Azure SLAs in more detail.
## Scalability
Another major benefit of cloud computing is the scalability of cloud resources. Scalability refers to the ability to adjust resources to meet demand. If you suddenly experience peak traffic and your systems are overwhelmed, the ability to scale means you can add more resources to better handle the increased demand.
The other benefit of scalability is that you aren't overpaying for services. Because the cloud is a consumption-based model, you only pay for what you use. If demand drops off, you can reduce your resources and thereby reduce your costs.
Scaling generally comes in two varieties: vertical and horizontal. Vertical scaling is focused on increasing or decreasing the capabilities of resources. Horizontal scaling is adding or subtracting the number of resources.
### Vertical scaling
With vertical scaling, if you were developing an app and you needed more processing power, you could vertically scale up to add more CPUs or RAM to the virtual machine. Conversely, if you realized you had over-specified the needs, you could vertically scale down by lowering the CPU or RAM specifications.
### Horizontal scaling
With horizontal scaling, if you suddenly experienced a steep jump in demand, your deployed resources could be scaled out (either automatically or manually). For example, you could itional virtual machines or containers, scaling out. In the same manner, if there was a significant drop in demand, deployed resources could be scaled in (either automatically or manually), scaling in.

## 2.3 Describe the benefits of reliability and predictability in the cloud

# Describe the benefits of reliability and predictability in the cloud
Reliability and predictability are two crucial cloud benefits that help you develop solutions with confidence.
## Reliability
Reliability is the ability of a system to recover from failures and continue to function. It's also one of the pillars of the Microsoft Azure Well-Architected Framework.
The cloud, by virtue of its decentralized design, naturally supports a reliable and resilient infrastructure. With a decentralized design, the cloud enables you to have resources deployed in regions around the world. With this global scale, even if one region has a catastrophic event other regions are still up and running. You can design your applications to automatically take advantage of this increased reliability. In some cases, your cloud environment itself will automatically shift to a different region for you, with no action needed on your part. You’ll learn more about how Azure leverages global scale to provide reliability later in this series.
## Predictability
Predictability in the cloud lets you move forward with confidence. Predictability can be focused on performance predictability or cost predictability. Both performance and cost predictability are heavily influenced by the Microsoft Azure Well-Architected Framework. Deploy a solution built around this framework and you have a solution whose cost and performance are predictable.
### Performance
Performance predictability focuses on predicting the resources needed to deliver a positive experience for your customers. Autoscaling, load balancing, and high availability are just some of the cloud concepts that support performance predictability. If you suddenly need more resources, autoscaling can deploy additional resources to meet the demand, and then scale back when the demand drops. Or if the traffic is heavily focused on one area, load balancing will help redirect some of the overload to less stressed areas.
### Cost
Cost predictability is focused on predicting or forecasting the cost of the cloud spend. With the cloud, you can track your resource use in real time, monitor resources to ensure that you’re using them in the most efficient way, and apply data analytics to find patterns and trends that help better plan resource deployments. By operating in the cloud and using cloud analytics and information, you can predict future costs and adjust your resources as needed. You can even use tools like the Total Cost of Ownership (TCO) or Pricing Calculator to get an estimate of potential cloud spend.

## 2.4 Describe the benefits of security and governance in the cloud

# Describe the benefits of security and governance in the cloud
Whether you’re deploying infrastructure as a service or software as a service, cloud features support governance and compliance. Things like set templates help ensure that all your deployed resources meet corporate standards and government regulatory requirements. Plus, you can update all your deployed resources to new standards as standards change. Cloud-based auditing helps flag any resource that’s out of compliance with your corporate standards and provides mitigation strategies. Depending on your operating model, software patches and updates may also automatically be applied, which helps with both governance and security.
On the security side, you can find a cloud solution that matches your security needs. If you want maximum control of security, infrastructure as a service provides you with physical resources but lets you manage the operating systems and installed software, including patches and maintenance. If you want patches and maintenance taken care of automatically, platform as a service or software as a service deployments may be the best cloud strategies for you.
And because the cloud is intended as an over-the-internet delivery of IT resources, cloud providers are typically well suited to handle things like distributed denial of service (DDoS) attacks, making your network more robust and secure.
By establishing a good governance footprint early, you can keep your cloud footprint updated, secure, and well managed.

## 2.5 Describe the benefits of manageability in the cloud

# Describe the benefits of manageability in the cloud
A major benefit of cloud computing is the manageability options. There are two types of manageability for cloud computing that you’ll learn about in this series, and both are excellent benefits.
## Management of the cloud
Management of the cloud speaks to managing your cloud resources. In the cloud, you can:
- Automatically scale resource deployment based on need.
- Deploy resources based on a preconfigured template, removing the need for manual configuration.
- Monitor the health of resources and automatically replace failing resources.
- Receive automatic alerts based on configured metrics, so you’re aware of performance in real time.
## Management in the cloud
Management in the cloud speaks to how you’re able to manage your cloud environment and resources. You can manage these:
- Through a web portal.
- Using a command line interface.
- Using APIs.
- Using PowerShell.

## 2.7 Summary

# Summary
, you learned about some of the benefits of operating in the cloud. You learned about high availability and reliability, and how those work to keep your applications running. You also learned about how the cloud can provide a more secure environment. Finally, you learned that the cloud provides a highly manageable environment for your resources.
## Learning objectives
You should now be able to:
- Describe the benefits of high availability and scalability in the cloud.
- Describe the benefits of reliability and predictability in the cloud.
- Describe the benefits of security and governance in the cloud.
- Describe the benefits of manageability in the cloud.
## Additional resources
The following resources provide more information on topics or related to this module.
- Build great solutions with the Microsoft Azure Well-Architected Framework is a Microsoft Learn course that introduces you to the Microsoft Azure Well-Architected Framework.

---

# Module 3: Describe Cloud Service Types

Introduction to cloud service types (Infrastructure, Platform, and Software as a Service models) and associated use cases for each.

## 3.1 Introduction

# Introduction
, you’ll be introduced to cloud service types. You’ll learn how each cloud service type determines the flexibility you’ll have with managing and configuring resources. You'll understand how the shared responsibility model applies to each cloud service type, and about various use cases for each cloud service type.
## Learning objectives
After completing this module, you’ll be able to:
- Describe infrastructure as a service (IaaS).
- Describe platform as a service (PaaS).
- Describe software as a service (SaaS).
- Identify appropriate use cases for each cloud service (IaaS, PaaS, SaaS).

## 3.2 Describe Infrastructure as a Service

# Describe Infrastructure as a Service
Infrastructure as a service (IaaS) is the most flexible category of cloud services, as it provides you the maximum amount of control for your cloud resources. In an IaaS model, the cloud provider is responsible for maintaining the hardware, network connectivity (to the internet), and physical security. You’re responsible for everything else: operating system installation, configuration, and maintenance; network configuration; database and storage configuration; and so on. With IaaS, you’re essentially renting the hardware in a cloud datacenter, but what you do with that hardware is up to you.
## Shared responsibility model
The shared responsibility model applies to all the cloud service types. IaaS places the largest share of responsibility with you. The cloud provider is responsible for maintaining the physical infrastructure and its access to the internet. You’re responsible for installation and configuration, patching and updates, and security.
## Scenarios
Some common scenarios where IaaS might make sense include:
- Lift-and-shift migration: You’re setting up cloud resources similar to your on-prem datacenter, and then simply moving the things running on-prem to running on the IaaS infrastructure.
- Testing and development: You have established configurations for development and test environments that you need to rapidly replicate. You can start up or shut down the different environments rapidly with an IaaS structure, while maintaining complete control.

## 3.3 Describe Platform as a Service

# Describe Platform as a Service
Platform as a service (PaaS) is a middle ground between renting space in a datacenter (infrastructure as a service) and paying for a complete and deployed solution (software as a service). In a PaaS environment, the cloud provider maintains the physical infrastructure, physical security, and connection to the internet. They also maintain the operating systems, middleware, development tools, and business intelligence services that make up a cloud solution. In a PaaS scenario, you don't have to worry about the licensing or patching for operating systems and databases.
PaaS is well suited to provide a complete development environment without the headache of maintaining all the development infrastructure.
## Shared responsibility model
The shared responsibility model applies to all the cloud service types. PaaS splits the responsibility between you and the cloud provider. The cloud provider is responsible for maintaining the physical infrastructure and its access to the internet, just like in IaaS. In the PaaS model, the cloud provider will also maintain the operating systems, databases, and development tools. Think of PaaS like using a domain joined machine: IT maintains the device with regular updates, patches, and refreshes.
Depending on the configuration, you or the cloud provider may be responsible for networking settings and connectivity within your cloud environment, network and application security, and the directory infrastructure.
## Scenarios
Some common scenarios where PaaS might make sense include:
- Development framework: PaaS provides a framework that developers can build upon to develop or customize cloud-based applications. Similar to the way you create an Excel macro, PaaS lets developers create applications using built-in software components. Cloud features such as scalability, high-availability, and multi-tenant capability are included, reducing the amount of coding that developers must do.
- Analytics or business intelligence: Tools provided as a service with PaaS allow organizations to analyze and mine their data, finding insights and patterns and predicting outcomes to improve forecasting, product design decisions, investment returns, and other business decisions.

## 3.4 Describe Software as a Service

# Describe Software as a Service
Software as a service (SaaS) is the most complete cloud service model from a product perspective. With SaaS, you’re essentially renting or using a fully developed application. Email, financial software, messaging applications, and connectivity software are all common examples of a SaaS implementation.
While the SaaS model may be the least flexible, it’s also the easiest to get up and running. It requires the least amount of technical knowledge or expertise to fully employ.
## Shared responsibility model
The shared responsibility model applies to all the cloud service types. SaaS is the model that places the most responsibility with the cloud provider and the least responsibility with the user. In a SaaS environment you’re responsible for the data that you put into the system, the devices that you allow to connect to the system, and the users that have access. Nearly everything else falls to the cloud provider. The cloud provider is responsible for physical security of the datacenters, power, network connectivity, and application development and patching.
## Scenarios
Some common scenarios for SaaS are:
- Email and messaging.
- Business productivity applications.
- Finance and expense tracking.

## 3.6 Summary

# Summary
, you learned about the cloud service types and some common scenarios for each type. You also reinforced how the shared responsibility model determines your responsibilities with different cloud service types.
## Learning objectives
You should now be able to:
- Describe infrastructure as a service (IaaS).
- Describe platform as a service (PaaS).
- Describe software as a service (SaaS).
- Identify appropriate use cases for each cloud service (IaaS, PaaS, SaaS).

---

# Key Concepts Index

- AZ-900 Domain Area
- Hybrid cloud
- Private cloud
- Public cloud
- Weight
