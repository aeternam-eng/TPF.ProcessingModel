resource_group_config = {
  location = "brazilsouth"
  name     = "rg-stronzo-tapegandofogo-#{SHORT_ENV}#"
}

appserviceplan_config = {
  os_type  = "Linux"
  sku_name = "F1"
}
