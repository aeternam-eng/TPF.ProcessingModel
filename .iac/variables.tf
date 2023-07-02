variable "resource_config" {
  type = object({
    environment = string
    name        = string
    location    = string
    namespace   = string
  })
}

variable "appserviceplan_config" {
  type = object({
    os_type  = string
    sku_name = string
  })
}
