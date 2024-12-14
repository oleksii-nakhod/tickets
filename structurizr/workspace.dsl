workspace "Train Ticketing System" "System context diagram for the train ticketing system" {

    !identifiers hierarchical

    model {
        customer = person "Train Ticket Buyer" "A customer of the train ticketing company."
        
        ticketingSystem = softwareSystem "Train Ticketing System" "Allows customers to search and buy tickets for trains." {
            orderApp = container "Order Application" "Handles order processing and ticket management" "Python/Flask" {
                tags "App"
            }
            
            authApp = container "Auth Application" "Handles user authentication and authorization" "Python/Flask" {
                tags "App"
            }
            
            searchApp = container "Search Application" "Handles train and seat search functionality" "Python/Flask" {
                tags "App"
            }

            webApp = container "Web Application" "Delivers the static content and single page application." "Python/Flask" {
                authComponent = component "Auth Component" "Handles user authentication and authorization UI" "Python/Flask"
                searchComponent = component "Search Component" "Handles train and seat search UI" "Python/Flask"
                orderComponent = component "Order Component" "Handles order processing and ticket management UI" "Python/Flask"
                
                # Component relationships
                authComponent -> authApp "Makes API calls to" "JSON/HTTPS"
                searchComponent -> searchApp "Makes API calls to" "JSON/HTTPS"
                orderComponent -> orderApp "Makes API calls to" "JSON/HTTPS"
            }

            messageBus = container "Message Bus" "Handles asynchronous communication between services" "RabbitMQ" {
                tags "Queue"
            }

            authDB = container "Auth Database" "Stores user accounts and authentication data" "MySQL" {
                tags "Database"
            }

            orderDB = container "Order Database" "Stores order and ticket information" "MySQL" {
                tags "Database"
            }

            searchDB = container "Search Database" "Stores train and seat availability data" "MySQL" {
                tags "Database"
            }

            authApp -> authDB "Reads from and writes to"
            orderApp -> orderDB "Reads from and writes to"
            searchApp -> searchDB "Reads from and writes to"

            orderApp -> messageBus "Publishes order events to"
            searchApp -> messageBus "Subscribes to order events from"
            authApp -> messageBus "Publishes user events to"
        }
        
        emailSystem = softwareSystem "Email System (SendGrid)" "Sends out emails to customers." {
            tags "External System"
        }
        
        paymentSystem = softwareSystem "Payment System (Stripe)" "Handles payments for tickets." {
            tags "External System"
        }

        # relationships
        customer -> ticketingSystem.webApp.searchComponent "Searches trains and seats, buys tickets using" "HTTPS"
        customer -> ticketingSystem.webApp.orderComponent "Manages orders and tickets using" "HTTPS"
        customer -> ticketingSystem.webApp.authComponent "Logs in and manages account using" "HTTPS"
        ticketingSystem.orderApp -> emailSystem "Sends emails using"
        ticketingSystem.orderApp -> paymentSystem "Processes payments using"
        emailSystem -> customer "Sends emails to"

        production = deploymentEnvironment "Production" {
            awsDeployment = deploymentNode "AWS Cloud" {
                tags "Cloud"
                
                loadBalancerDeployment = deploymentNode "Load Balancer" "AWS ELB" {
                    loadBalancerInfrastructure = infrastructureNode "Load Balancer" "AWS Elastic Load Balancer" {
                        tags "Load Balancer"
                    }
                }

                apiGatewayDeployment = deploymentNode "API Gateway" "Kong" {
                    apiGatewayInfrastructure = infrastructureNode "Kong API Gateway" "API Gateway and Rate Limiting"
                }

                webAppDeploymentCluster = deploymentNode "Web Server Cluster" "AWS EC2" {
                    webAppDeployment = deploymentNode "Docker Container - Web" {
                        webAppInstance = containerInstance ticketingSystem.webApp
                    }
                }

                appDeploymentCluster = deploymentNode "Application Server Cluster" "AWS EC2" {
                    authAppDeployment = deploymentNode "Docker Container - Auth" {
                        authAppInstance = containerInstance ticketingSystem.authApp
                    }

                    orderAppDeployment = deploymentNode "Docker Container - Order" {
                        orderAppInstance = containerInstance ticketingSystem.orderApp
                    }

                    searchAppDeployment = deploymentNode "Docker Container - Search" {
                        searchAppInstance = containerInstance ticketingSystem.searchApp
                    }
                }

                deploymentNode "Message Queue Cluster" "AWS EC2" {
                    deploymentNode "Docker Container - RabbitMQ" {
                        messageBusInstance = containerInstance ticketingSystem.messageBus
                    }
                }

                deploymentNode "Database Cluster" "AWS RDS" {
                    deploymentNode "Auth Database Primary" "MySQL RDS" {
                        authDBInstance = containerInstance ticketingSystem.authDB
                    }

                    deploymentNode "Order Database Primary" "MySQL RDS" {
                        orderDBInstance = containerInstance ticketingSystem.orderDB
                    }

                    deploymentNode "Search Database Primary" "MySQL RDS" {
                        searchDBInstance = containerInstance ticketingSystem.searchDB
                    }
                }
                loadBalancerDeployment.loadBalancerInfrastructure -> webAppDeploymentCluster.webAppDeployment.webAppInstance "Routes traffic to" "HTTPS"
                loadBalancerDeployment.loadBalancerInfrastructure -> apiGatewayDeployment.apiGatewayInfrastructure "Routes traffic to" "HTTPS"
                apiGatewayDeployment.apiGatewayInfrastructure -> appDeploymentCluster.authAppDeployment.authAppInstance "For authentication API calls"
                apiGatewayDeployment.apiGatewayInfrastructure -> appDeploymentCluster.orderAppDeployment.orderAppInstance "For order API calls"
                apiGatewayDeployment.apiGatewayInfrastructure -> appDeploymentCluster.searchAppDeployment.searchAppInstance "For search API calls"
            }
            
        }
    }

    

    views {
        systemContext ticketingSystem "SystemContext" {
            include *
            autolayout tb
        }

        container ticketingSystem "Containers" {
            include *
            autolayout tb
        }

        component ticketingSystem.webApp "Components" {
            include *
            autolayout tb
        }

        deployment ticketingSystem "Production" "ProductionDeployment" {
            include *
            autolayout tb
        }

        styles {
            element "Person" {
                shape person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "External System" {
                background #999999
                color #ffffff
            }
            element "Web App" {
                shape WebBrowser
                background #438dd5
                color #ffffff
            }
            element "App" {
                background #438dd5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
                background #438dd5
                color #ffffff
            }
            element "Queue" {
                shape Pipe
                background #438dd5
                color #ffffff
            }
            element "Component" {
                background #85bbf0
                color #000000
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}