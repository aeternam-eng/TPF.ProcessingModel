// All values are injected through pipeline
provider "azurerm" {
  features {}
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.0"
    }
  }

  // All values are injected through pipeline
  backend "azurerm" {}
}

module "conventions" {
  source      = "https://sastronzo.blob.core.windows.net/terraform-modules/naming-conventions.zip"
  environment = var.resource_config.environment
  namespace   = var.resource_config.namespace
  appName     = var.resource_config.name
}

resource "azurerm_service_plan" "appserviceplan" {
  name                = module.conventions.app_config.app_service_plan_name
  location            = var.resource_config.location
  resource_group_name = module.conventions.resource_group_name
  os_type             = var.appserviceplan_config.os_type
  sku_name            = var.appserviceplan_config.sku_name
}

resource "azurerm_linux_web_app" "webapp" {
  name                = module.conventions.app_config.web_app_name
  location            = azurerm_service_plan.appserviceplan.location
  resource_group_name = module.conventions.resource_group_name
  service_plan_id     = azurerm_service_plan.appserviceplan.id
  https_only          = true

  site_config {
    minimum_tls_version = "1.2"
    always_on           = false
    application_stack {
      python_version = "3.9"
    }
  }
}
