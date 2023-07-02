azurerm_provider_config = {
  subscription_id = "#{AzureSubscriptionId}#"
  client_id       = "#{AzureSvcAccountClientId}#"
  client_secret   = "#{AzureSvcAccountClientSecret}#"
  tenant_id       = "#{AzureTenantId}#"
}

service_config = {
  name      = "#{SERVICE_NAME}#"
  short_env = "#{SHORT_ENV}#"
}
