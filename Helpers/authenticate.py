def keyvault(tenant):
    """
    Authenticate the end-user using device auth on Azure Keyvault
    """
    import adal, uuid, time
    authority_host_uri = 'https://login.microsoftonline.com'
    
    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://vault.azure.net'
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46' #this identifies this request

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials

def management(tenant):
    """
    Authenticate the end-user using device auth.
    """
    import adal, uuid, time
    authority_host_uri = 'https://login.microsoftonline.com'

    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://management.core.windows.net/'
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46' #this identifies this request

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials