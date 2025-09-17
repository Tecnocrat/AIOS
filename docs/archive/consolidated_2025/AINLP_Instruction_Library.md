# AINLP Instruction Library

## Artificial Intelligence Natural Language Programming

**AINLP** (Artificial Intelligence Natural Language Programming) is a system of reusable natural language instructions designed to streamline AI-human collaboration. This document serves as a quick reference library for frequently used instruction patterns that can be copy-pasted to improve working speed.

## Quick Reference Table

| Category | Instruction | Use Case |
|----------|-------------|----------|
| [Code Analysis](#code-analysis--review) | [Analyze Codebase](#analyze-entire-codebase) | Get comprehensive code overview |
| [Implementation](#implementation-tasks) | [Implement Feature](#implement-new-feature) | Add new functionality |
| [Testing](#testing--validation) | [Create Tests](#create-comprehensive-tests) | Generate test suites |
| [Documentation](#documentation) | [Generate Docs](#generate-comprehensive-documentation) | Create documentation |
| [Refactoring](#refactoring) | [Refactor Code](#refactor-code-for-improved-maintainability) | Improve code quality |
| [Debugging](#debugging) | [Debug Issue](#debug-application-issue) | Troubleshoot problems |
| [Architecture](#architecture-design) | [Design System](#design-system-architecture) | Plan system structure |
| [File Operations](#file-operations) | [Process Files](#process-multiple-files) | Handle file operations |
| [Build & Deploy](#build--deployment) | [Setup CI/CD](#setup-cicd-pipeline) | Configure deployment |
| [Collaboration](#collaboration-patterns) | [Code Review](#conduct-code-review) | Review and improve code |

## How to Use This Document

1. **Find** the instruction you need using the Quick Reference Table
2. **Copy** the instruction text from the detailed section
3. **Customize** any variables/parameters in `[brackets]`
4. **Paste** into your AI interaction
5. **Execute** and iterate as needed

## Code Analysis & Review

### Analyze Entire Codebase
**Purpose:** Get a comprehensive overview of the entire codebase structure and functionality.

```
Please analyze the entire codebase in the workspace. Provide a detailed overview including:

1. **Architecture Overview**
   - Main components and their relationships
   - Technology stack and frameworks used
   - Entry points and main workflows

2. **Code Quality Assessment**
   - Strengths and areas for improvement
   - Code patterns and conventions
   - Potential technical debt

3. **Functionality Summary**
   - Key features and capabilities
   - Business logic overview
   - Integration points

4. **Recommendations**
   - Immediate improvements needed
   - Long-term architectural suggestions
   - Best practices to implement

Focus on actionable insights that will help improve the codebase quality and maintainability.
```

### Analyze Specific File
**Purpose:** Deep dive into a particular file's functionality and structure.

```
Analyze the file `[FILE_PATH]` in detail. Provide:

1. **File Overview**
   - Purpose and responsibility
   - Key classes/functions/methods
   - Dependencies and imports

2. **Code Structure**
   - Main components and their relationships
   - Design patterns used
   - Code organization quality

3. **Functionality Analysis**
   - What the code does
   - Key algorithms or logic
   - Edge cases handled

4. **Quality Assessment**
   - Code readability and maintainability
   - Potential improvements
   - Security considerations

5. **Integration Points**
   - How it interacts with other components
   - API contracts
   - Data flow

Provide specific, actionable recommendations for improvement.
```

## Implementation Tasks

### Implement New Feature
**Purpose:** Add new functionality following best practices.

```
Implement a new feature for `[FEATURE_NAME]` with the following requirements:

**Requirements:**
- [List specific requirements]
- [Technical specifications]
- [Acceptance criteria]

**Implementation Approach:**
1. **Analysis Phase**
   - Review existing codebase for similar patterns
   - Identify integration points
   - Plan the implementation strategy

2. **Design Phase**
   - Define the component structure
   - Plan error handling and edge cases
   - Consider testing requirements

3. **Implementation Phase**
   - Write clean, maintainable code
   - Follow existing code conventions
   - Include comprehensive error handling
   - Add appropriate logging

4. **Testing Phase**
   - Write unit tests
   - Integration testing
   - Edge case validation

**Deliverables:**
- Production-ready code
- Unit tests with good coverage
- Updated documentation
- Migration guide if needed

Ensure the implementation follows SOLID principles and is easily maintainable.
```

### Create API Endpoint
**Purpose:** Implement REST API endpoints with proper structure.

```
Create a REST API endpoint for `[ENDPOINT_PURPOSE]` with the following specifications:

**Endpoint Details:**
- **URL:** `[API_PATH]`
- **Method:** `[GET/POST/PUT/DELETE]`
- **Authentication:** `[AUTH_METHOD]`

**Request/Response:**
- **Request Body:** `[SCHEMA/DESCRIPTION]`
- **Response Body:** `[SCHEMA/DESCRIPTION]`
- **Status Codes:** `[SUCCESS/ERROR_CODES]`

**Implementation Requirements:**
1. **Input Validation**
   - Request parameter validation
   - Data type checking
   - Business rule validation

2. **Business Logic**
   - Core functionality implementation
   - Error handling
   - Logging and monitoring

3. **Response Formatting**
   - Consistent response structure
   - Proper HTTP status codes
   - Meaningful error messages

4. **Security Considerations**
   - Input sanitization
   - Rate limiting if needed
   - Authentication/authorization

5. **Testing**
   - Unit tests for business logic
   - Integration tests for the endpoint
   - Error scenario testing

Ensure the endpoint follows RESTful conventions and includes comprehensive error handling.
```

## Testing & Validation

### Create Comprehensive Tests
**Purpose:** Generate complete test suites for code components.

```
Create comprehensive tests for `[COMPONENT_NAME]` including:

**Test Categories:**
1. **Unit Tests**
   - Test individual functions/methods
   - Mock external dependencies
   - Cover edge cases and error conditions

2. **Integration Tests**
   - Test component interactions
   - End-to-end workflows
   - Database operations if applicable

3. **Performance Tests**
   - Load testing scenarios
   - Memory usage validation
   - Response time benchmarks

**Test Structure:**
- **Setup/Teardown:** Proper test isolation
- **Test Data:** Realistic test data generation
- **Assertions:** Clear, meaningful assertions
- **Coverage:** Aim for >80% code coverage

**Best Practices:**
- Use descriptive test names
- Test both positive and negative scenarios
- Include boundary value testing
- Document test scenarios clearly

**Deliverables:**
- Test files with comprehensive coverage
- Test data fixtures if needed
- Test documentation
- CI/CD integration setup
```

### Validate Code Changes
**Purpose:** Ensure code changes meet quality standards.

```
Validate the following code changes for quality and correctness:

**Changes Made:**
- [List of files modified]
- [Key functionality added/changed]

**Validation Checklist:**
1. **Code Quality**
   - Follows coding standards and conventions
   - Proper error handling implemented
   - Code is readable and maintainable
   - No hardcoded values or magic numbers

2. **Functionality**
   - Meets all requirements
   - Handles edge cases properly
   - Backward compatibility maintained
   - Performance impact assessed

3. **Testing**
   - Unit tests added/updated
   - Integration tests pass
   - No regressions introduced
   - Test coverage maintained

4. **Security**
   - Input validation implemented
   - No security vulnerabilities introduced
   - Authentication/authorization handled
   - Data sanitization applied

5. **Documentation**
   - Code comments added where needed
   - API documentation updated
   - README changes if required

**Review Results:**
- [ ] Passes all validation criteria
- [ ] Ready for production deployment
- [ ] Requires additional work

Provide specific recommendations for any issues found.
```

## Documentation

### Generate Comprehensive Documentation
**Purpose:** Create thorough documentation for code components.

```
Generate comprehensive documentation for `[COMPONENT_NAME]` including:

**Documentation Types:**
1. **Code Documentation**
   - Inline code comments
   - Function/method documentation
   - Class and interface documentation

2. **API Documentation**
   - Endpoint documentation
   - Request/response schemas
   - Authentication requirements

3. **User Documentation**
   - Usage examples
   - Configuration instructions
   - Troubleshooting guide

**Documentation Structure:**
- **Overview:** What the component does
- **Architecture:** How it's structured
- **Usage:** How to use it
- **Configuration:** Setup and configuration
- **Examples:** Code examples and use cases
- **Troubleshooting:** Common issues and solutions

**Quality Standards:**
- Clear, concise language
- Consistent formatting
- Up-to-date information
- Easy to navigate structure
- Searchable content

**Maintenance:**
- Update documentation with code changes
- Review documentation periodically
- Keep examples current and working

Deliver documentation that enables developers to understand and use the component effectively.
```

### Create README File
**Purpose:** Generate project README with essential information.

```
Create a comprehensive README.md file for the project with the following sections:

**Project Information:**
- Project name and description
- Key features and capabilities
- Technology stack used

**Getting Started:**
- Prerequisites and requirements
- Installation instructions
- Quick start guide
- Configuration options

**Usage:**
- Basic usage examples
- Advanced features
- API documentation links
- Configuration examples

**Development:**
- Development setup
- Testing instructions
- Contributing guidelines
- Code standards

**Deployment:**
- Build instructions
- Deployment procedures
- Environment configurations
- Monitoring and logging

**Support:**
- Troubleshooting common issues
- FAQ section
- Contact information
- License information

**Quality Standards:**
- Use clear, concise language
- Include code examples where helpful
- Keep information up-to-date
- Use consistent formatting
- Make it easy to scan and navigate

Ensure the README serves as the primary entry point for developers working with the project.
```

## Refactoring

### Refactor Code for Improved Maintainability
**Purpose:** Improve code quality and maintainability through refactoring.

```
Refactor the code in `[FILE_PATH/COMPONENT]` to improve maintainability. Focus on:

**Refactoring Goals:**
1. **Code Organization**
   - Break down large functions into smaller ones
   - Extract common functionality into shared methods
   - Organize code into logical modules

2. **Readability Improvements**
   - Use descriptive variable and method names
   - Add meaningful comments where needed
   - Simplify complex conditional logic

3. **Performance Optimizations**
   - Remove unnecessary computations
   - Optimize database queries if applicable
   - Improve memory usage patterns

4. **Error Handling**
   - Implement proper exception handling
   - Add input validation
   - Provide meaningful error messages

**Refactoring Principles:**
- **Single Responsibility:** Each function/method should do one thing
- **DRY (Don't Repeat Yourself):** Eliminate code duplication
- **SOLID Principles:** Follow object-oriented design principles
- **Clean Code:** Write code that is easy to read and understand

**Quality Assurance:**
- Ensure all existing functionality is preserved
- Update tests to reflect refactored code
- Verify performance is not degraded
- Maintain backward compatibility

**Deliverables:**
- Refactored code with improved structure
- Updated tests if needed
- Documentation of changes made
- Performance comparison if applicable

Provide a summary of improvements made and their impact on code quality.
```

### Optimize Performance
**Purpose:** Improve application performance through code optimization.

```
Optimize the performance of `[COMPONENT/FUNCTION]` by implementing the following improvements:

**Performance Analysis:**
1. **Identify Bottlenecks**
   - Profile the current implementation
   - Identify slow-running functions
   - Analyze resource usage patterns

2. **Optimization Strategies**
   - Algorithm improvements
   - Data structure optimization
   - Caching implementation
   - Database query optimization

**Implementation Plan:**
1. **Code Optimizations**
   - Remove unnecessary computations
   - Implement efficient algorithms
   - Optimize loop structures
   - Reduce memory allocations

2. **Caching Strategy**
   - Identify cacheable data
   - Implement appropriate caching mechanism
   - Set proper cache expiration policies

3. **Database Optimizations**
   - Optimize query performance
   - Implement proper indexing
   - Reduce N+1 query problems
   - Use connection pooling

4. **Resource Management**
   - Optimize memory usage
   - Implement proper resource disposal
   - Reduce network calls where possible

**Quality Assurance:**
- Maintain functional correctness
- Preserve code readability
- Update performance tests
- Monitor for regressions

**Success Metrics:**
- [Specific performance targets]
- [Measurable improvements expected]

Document the optimizations made and their performance impact.
```

## Debugging

### Debug Application Issue
**Purpose:** Systematically troubleshoot and resolve application issues.

```
Debug the following issue in the application:

**Issue Description:**
- **Problem:** [Brief description of the issue]
- **Expected Behavior:** [What should happen]
- **Actual Behavior:** [What actually happens]
- **Environment:** [Where the issue occurs]
- **Frequency:** [How often it happens]

**Debugging Approach:**
1. **Reproduce the Issue**
   - Steps to reproduce
   - Environment setup
   - Test data required

2. **Gather Information**
   - Error messages and stack traces
   - Log files analysis
   - System state when issue occurs
   - Recent changes that might be related

3. **Root Cause Analysis**
   - Code path analysis
   - Data flow examination
   - Dependency analysis
   - Configuration review

4. **Hypothesis Testing**
   - Formulate hypotheses about the cause
   - Test each hypothesis systematically
   - Eliminate false hypotheses

5. **Solution Implementation**
   - Implement the fix
   - Test the solution thoroughly
   - Verify no regressions introduced

**Debugging Best Practices:**
- Use systematic debugging techniques
- Log relevant information
- Test assumptions
- Document findings
- Implement proper error handling

**Deliverables:**
- Root cause identified
- Solution implemented and tested
- Documentation of the debugging process
- Preventive measures if applicable
```

### Analyze Error Logs
**Purpose:** Extract insights from application error logs.

```
Analyze the error logs from `[TIME_PERIOD/SYSTEM]` and provide insights:

**Log Analysis Scope:**
- **Time Period:** [Date range]
- **Systems/Components:** [Specific areas to focus on]
- **Error Types:** [Categories of errors to analyze]

**Analysis Framework:**
1. **Error Classification**
   - Categorize errors by type and severity
   - Identify patterns and trends
   - Group related errors together

2. **Root Cause Identification**
   - Analyze error messages and stack traces
   - Identify common failure points
   - Determine underlying causes

3. **Impact Assessment**
   - Evaluate user impact
   - Assess system stability
   - Identify critical vs. minor issues

4. **Frequency Analysis**
   - Most common errors
   - Peak error periods
   - Error rate trends

**Recommendations:**
1. **Immediate Actions**
   - Critical issues requiring immediate attention
   - Quick fixes for high-impact problems

2. **Short-term Improvements**
   - Code fixes and patches
   - Configuration changes
   - Monitoring enhancements

3. **Long-term Solutions**
   - Architectural improvements
   - Process changes
   - Preventive measures

**Deliverables:**
- Error analysis report
- Prioritized list of issues
- Actionable recommendations
- Monitoring improvements
```

## Architecture Design

### Design System Architecture
**Purpose:** Plan and design system architecture for new or existing systems.

```
Design the system architecture for `[SYSTEM_NAME]` with the following requirements:

**System Overview:**
- **Purpose:** [What the system does]
- **Scale:** [Expected user load, data volume]
- **Constraints:** [Technical and business constraints]

**Architecture Components:**
1. **High-Level Design**
   - System boundaries and interfaces
   - Major components and their responsibilities
   - Data flow and integration points

2. **Technology Stack**
   - Programming languages and frameworks
   - Database and storage solutions
   - Infrastructure and deployment platforms

3. **Component Design**
   - Service boundaries and APIs
   - Data models and relationships
   - Security and authentication mechanisms

**Quality Attributes:**
- **Scalability:** How the system will handle growth
- **Reliability:** Uptime and error handling requirements
- **Performance:** Response time and throughput targets
- **Security:** Authentication, authorization, and data protection
- **Maintainability:** Code organization and documentation standards

**Implementation Roadmap:**
1. **Phase 1:** Core functionality and MVP
2. **Phase 2:** Advanced features and optimizations
3. **Phase 3:** Scaling and performance improvements

**Risk Assessment:**
- Technical risks and mitigation strategies
- Dependencies and external factors
- Timeline and resource considerations

Deliver a comprehensive architecture document that guides implementation and ensures system success.
```

### Design Database Schema
**Purpose:** Design efficient and scalable database structures.

```
Design the database schema for `[APPLICATION/SYSTEM]` with the following requirements:

**Database Requirements:**
- **Data Types:** [Types of data to be stored]
- **Relationships:** [Entity relationships and cardinalities]
- **Performance:** [Query patterns and performance requirements]
- **Scalability:** [Growth expectations and scaling strategy]

**Schema Design:**
1. **Entity Analysis**
   - Identify all entities and their attributes
   - Define relationships between entities
   - Determine cardinality and constraints

2. **Table Design**
   - Normalize tables appropriately
   - Define primary and foreign keys
   - Create indexes for performance
   - Plan for data integrity

3. **Performance Optimization**
   - Index strategy for common queries
   - Partitioning strategy if needed
   - Caching considerations

**Implementation Plan:**
1. **DDL Scripts**
   - Table creation scripts
   - Index creation scripts
   - Constraint definitions

2. **Data Migration**
   - Migration scripts if upgrading
   - Data transformation requirements
   - Rollback procedures

3. **Documentation**
   - Entity relationship diagrams
   - Field descriptions and constraints
   - Usage examples

**Quality Assurance:**
- Review for normalization issues
- Performance testing of key queries
- Data integrity validation
- Backup and recovery procedures

Deliver a complete database schema design with all necessary scripts and documentation.
```

## File Operations

### Process Multiple Files
**Purpose:** Handle operations on multiple files systematically.

```
Process the following files in the `[DIRECTORY_PATH]` directory:

**Operation Type:** [BATCH_OPERATION_TYPE]
**Files to Process:** [FILE_PATTERNS_OR_LIST]
**Operation Parameters:** [SPECIFIC_PARAMETERS]

**Processing Requirements:**
1. **File Selection**
   - Include/exclude patterns
   - File type filtering
   - Size or date filters

2. **Operation Execution**
   - Process files in correct order
   - Handle errors gracefully
   - Maintain operation log

3. **Validation**
   - Verify operation success
   - Check file integrity
   - Validate results

**Error Handling:**
- Skip problematic files and continue
- Log all errors and warnings
- Provide summary of operations

**Performance Considerations:**
- Process files efficiently
- Handle large file sets
- Memory usage optimization

Deliver a comprehensive processing solution with proper error handling and logging.
```

### Organize Project Structure
**Purpose:** Reorganize project files for better maintainability.

```
Reorganize the project structure in `[PROJECT_PATH]` to improve maintainability:

**Current Issues:**
- [List current structural problems]
- [Organization issues identified]

**Reorganization Plan:**
1. **Directory Structure**
   - Create logical folder hierarchy
   - Group related files together
   - Separate concerns appropriately

2. **File Naming**
   - Consistent naming conventions
   - Descriptive file names
   - Version control friendly names

3. **Configuration Files**
   - Centralize configuration
   - Environment-specific configs
   - Documentation of settings

**Migration Strategy:**
1. **Planning Phase**
   - Document current structure
   - Plan new organization
   - Identify dependencies

2. **Implementation Phase**
   - Create new directory structure
   - Move files systematically
   - Update import statements

3. **Testing Phase**
   - Verify all references work
   - Test build process
   - Validate functionality

**Quality Standards:**
- Follow industry best practices
- Maintain clean separation of concerns
- Ensure easy navigation
- Support future growth

Deliver a well-organized project structure that improves developer productivity and code maintainability.
```

## Build & Deployment

### Setup CI/CD Pipeline
**Purpose:** Configure automated build and deployment processes.

```
Set up a CI/CD pipeline for `[PROJECT_NAME]` with the following requirements:

**Pipeline Stages:**
1. **Build Stage**
   - Code compilation
   - Dependency management
   - Static code analysis
   - Unit test execution

2. **Test Stage**
   - Integration testing
   - Performance testing
   - Security scanning
   - Code quality checks

3. **Deploy Stage**
   - Artifact creation
   - Environment-specific deployment
   - Configuration management
   - Rollback procedures

**Tools and Technologies:**
- **CI Platform:** [GitHub Actions/Jenkins/GitLab CI/etc.]
- **Containerization:** [Docker/Kubernetes]
- **Cloud Platform:** [AWS/Azure/GCP]
- **Monitoring:** [Application monitoring tools]

**Quality Gates:**
- Code coverage requirements
- Performance benchmarks
- Security scan results
- Manual approval for production

**Environment Configuration:**
- Development environment
- Staging environment
- Production environment
- Rollback capabilities

**Monitoring and Alerting:**
- Pipeline status monitoring
- Deployment success/failure alerts
- Performance monitoring
- Error tracking

Deliver a robust CI/CD pipeline that ensures reliable and automated deployments.
```

### Configure Build System
**Purpose:** Set up proper build configuration and scripts.

```
Configure the build system for `[PROJECT_NAME]` with the following components:

**Build Configuration:**
1. **Build Scripts**
   - Clean build process
   - Dependency management
   - Compilation settings
   - Output organization

2. **Development Environment**
   - Local development setup
   - IDE configuration
   - Debugging setup
   - Hot reload capabilities

3. **Testing Framework**
   - Unit testing setup
   - Integration testing
   - Test coverage reporting
   - Test automation

**Build Optimization:**
1. **Performance**
   - Parallel build processes
   - Incremental builds
   - Build caching
   - Resource optimization

2. **Quality Assurance**
   - Code linting
   - Static analysis
   - Security scanning
   - Documentation generation

**Deployment Preparation:**
1. **Artifact Creation**
   - Build artifacts
   - Container images
   - Deployment packages
   - Configuration files

2. **Environment Setup**
   - Development environment
   - Staging environment
   - Production environment

**Documentation:**
- Build instructions
- Configuration options
- Troubleshooting guide
- Maintenance procedures

Deliver a comprehensive build system that supports efficient development and reliable deployments.
```

## Collaboration Patterns

### Conduct Code Review
**Purpose:** Perform thorough code review following best practices.

```
Conduct a comprehensive code review for the following changes:

**Review Context:**
- **Changes:** [Files/PR/Commit references]
- **Author:** [Developer name]
- **Purpose:** [What the changes accomplish]

**Review Checklist:**
1. **Code Quality**
   - [ ] Follows coding standards and conventions
   - [ ] Code is readable and maintainable
   - [ ] Proper error handling implemented
   - [ ] No hardcoded values or security issues

2. **Functionality**
   - [ ] Meets all requirements and acceptance criteria
   - [ ] Handles edge cases appropriately
   - [ ] Backward compatibility maintained
   - [ ] Performance impact assessed

3. **Testing**
   - [ ] Unit tests added/updated with good coverage
   - [ ] Integration tests included if needed
   - [ ] No existing tests broken
   - [ ] Test edge cases covered

4. **Documentation**
   - [ ] Code comments added where needed
   - [ ] API documentation updated
   - [ ] README changes if required
   - [ ] Breaking changes documented

5. **Architecture**
   - [ ] Follows established patterns
   - [ ] No unnecessary complexity added
   - [ ] Scalability considerations addressed
   - [ ] Security best practices followed

**Review Results:**
- **Approval Status:** [Approved/Changes Requested/Rejected]
- **Severity:** [Blocking/Major/Minor]
- **Comments:** [Detailed feedback and suggestions]

**Recommendations:**
- [Specific improvement suggestions]
- [Best practices to implement]
- [Follow-up actions needed]

Provide constructive feedback that helps improve code quality and developer skills.
```

### Plan Sprint/Iteration
**Purpose:** Plan development work for upcoming iteration.

```
Plan the development work for iteration `[SPRINT_NUMBER]` with the following context:

**Sprint Goals:**
- [Primary objectives for this iteration]
- [Key results expected]
- [Business value to be delivered]

**Team Capacity:**
- **Team Members:** [List of team members]
- **Availability:** [Working hours/days]
- **Velocity:** [Historical velocity data]

**Backlog Items:**
1. **High Priority**
   - [Critical features and fixes]
   - [Dependencies and blockers]

2. **Medium Priority**
   - [Important but not critical items]
   - [Technical debt items]

3. **Low Priority**
   - [Nice-to-have features]
   - [Research and investigation tasks]

**Sprint Planning:**
1. **Capacity Planning**
   - Estimate story points for each item
   - Consider team capacity and availability
   - Plan for meetings and overhead

2. **Risk Assessment**
   - Technical risks identified
   - Dependencies on external teams
   - Potential blockers

3. **Definition of Done**
   - Code complete and reviewed
   - Tests written and passing
   - Documentation updated
   - Acceptance criteria met

**Success Metrics:**
- Sprint goal achievement
- Story point completion
- Quality metrics (bug rates, etc.)
- Team satisfaction

Deliver a realistic sprint plan that sets the team up for success while managing expectations appropriately.
```

---

## Maintenance Guidelines

### Adding New Instructions

1. **Categorization:** Place new instructions in the most appropriate category
2. **Consistency:** Follow the established format and structure
3. **Clarity:** Use clear, descriptive titles and descriptions
4. **Completeness:** Include all necessary components (purpose, requirements, deliverables)
5. **Testing:** Verify the instruction works as intended

### Updating Instructions

1. **Regular Review:** Review instructions periodically for relevance
2. **Version Control:** Track changes to instruction effectiveness
3. **User Feedback:** Incorporate feedback from team members
4. **Best Practices:** Update based on new tools and methodologies

### Usage Tracking

1. **Effectiveness:** Track which instructions are most valuable
2. **Improvements:** Identify areas for instruction enhancement
3. **Metrics:** Measure time savings and quality improvements
4. **Evolution:** Adapt instructions based on changing needs

---

## Quick Copy-Paste Templates

### Standard Code Review Template
```
Please review the code changes in [PR_LINK/FILE_LIST]. Focus on:
- Code quality and readability
- Security implications
- Performance considerations
- Test coverage
- Documentation updates

Provide specific, actionable feedback.
```

### Bug Investigation Template
```
Investigate the bug reported in [ISSUE_LINK]. Steps to reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected: [Expected behavior]
Actual: [Actual behavior]

Please identify root cause and provide fix.
```

### Feature Implementation Template
```
Implement [FEATURE_NAME] with the following requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Include:
- Unit tests
- Documentation
- Error handling
- Edge case coverage
```

Remember: This document should remain focused and actionable. Avoid feature creep by regularly reviewing and pruning less-used instructions.
