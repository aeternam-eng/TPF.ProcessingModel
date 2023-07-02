// Should come from token replacement
variable "azurerm_provider_config" {
  type = object({
    subscription_id = string
    client_id       = string
    client_secret   = string
    tenant_id       = string
  })
}

variable "resource_group_config" {
  type = object({
    name     = string
    location = string
  })
}

variable "service_config" {
  type = object({
    name      = string
    short_env = string
  })
}

variable "appserviceplan_config" {
  type = object({
    os_type  = string
    sku_name = string
  })
}
