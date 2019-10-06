#%%
tenantID='a87101d0-71e5-40d5-829e-cf14f5cbe9dd'
clientID='8a018b8d-62f4-4ecd-b028-b146d301c332'
clientSecret='NZpw8m:4PLD9Nh]QxIOvxj7mygPVcL-]'
workspaceID='88e4dd19-caa6-4a38-a2e2-506488c113de'
ip='85.146.253.12'

#%%
!pip install Kqlmagic --no-cache-dir --upgrade
!pip install msticpy --upgrade --no-cache-dir
!pip install pandas --upgrade --no-cache-dir

#%%
# you can try it within the notebook, by setting the environment variable using %env magic
%env KQLMAGIC_NOTEBOOK_APP=jupyterlab
%env KQLMAGIC_LOAD_MODE=silent
%env KQLMAGIC_CONFIGURATION="show_query_time=False;plot_package='plotly';display_limit=100"
#%env KQLMAGIC_CONFIGURATION="show_init_banner=True;check_magic_version=False;show_what_new=False"

%env KQLMAGIC_CONNECTION_STR=loganalytics://username='maurice@mcpforlifecom';workspace='88e4dd19-caa6-4a38-a2e2-506488c113de'
#%env KQLMAGIC_CONNECTION_STR=AzureDataExplorer://code;cluster='help';database='Samples'

#%env KQLMAGIC_LOG_LEVEL=DEBUG
#%env KQLMAGIC_LOG_FILE_MODE=Append
# %env KQLMAGIC_LOG_FILE=michael.log
#%env KQLMAGIC_LOG_FILE_PREFIX=myLog
#%env KQLMAGIC_DEVICE_CODE_NOTIFICATION_EMAIL=SMTPEndPoint='endpoint';SMTPPort='port';sendFrom='from';sendFromPassword='password';sendTo='to';context='text'



#%%
%reload_ext Kqlmagic
#%%
%reload_ext msticpy

#%%
import sys
from IPython.display import display
import pandas as pd
import msticpy.sectools as sectools
import msticpy.nbtools as mas
from msticpy.nbtools.entityschema import IpAddress, GeoLocation
from msticpy.sectools.geoip import GeoLiteLookup, IPStackLookup

#%%
#%kql loganalytics://tenant=tenantID;clientid=clientID;clientsecret=clientSecret;workspace=workspaceID
%kql loganalytics://tenant=tenantID;workspace=workspaceID

#%%
kql AzureActivity | where Caller contains "maurice" | where TimeGenerated > ago(12h) | project TimeGenerated, OperationName, ActivityStatus, CallerIpAddress
#%%
result = GeoLiteLookup().lookup_ip(ip)

#%%
print('Location')
print('City: '+result[0][0]['city']['names']['en'])
print('Country: '+result[0][0]['country']['names']['en'])
print('Continent: '+result[0][0]['continent']['names']['en'])
print('Accuracy radius: '+str(result[0][0]['location']['accuracy_radius']))
print('Latitude, Longitude: '+str(result[0][0]['location']['latitude'])+', '+str(result[0][0]['location']['longitude']))



# http://192.168.74.146:8888/?token=dbbb896af9c603684a0311b446b3c6f05b5259fb4e4e7cb4


#%%
kql ipAddresses << ActivityIpAddresses | project Address=CallerIpAddress

#%%
IpAddress.ip_address
results = GeoLiteLookup().lookup_ip(ip_addr_list=address)

#%%
print(ipAddresses['Address'])

#%%
from azure.keyvault import KeyVaultClient


#%%
pip install azure --no-cache-dir --upgrade
!pip install azure-keyvault --no-cache-dir --upgrade

#%%
from msrestazure.azure_active_directory import MSIAuthentication
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient

# Create MSI Authentication
credentials = MSIAuthentication()


# Create a Subscription Client
subscription_client = SubscriptionClient(credentials)
subscription = next(subscription_client.subscriptions.list())
subscription_id = subscription.subscription_id

# Create a Resource Management client
resource_client = ResourceManagementClient(credentials, subscription_id)


# List resource groups as an example. The only limit is what role and policy are assigned to this MSI token.
for resource_group in resource_client.resource_groups.list():
    print(resource_group.name)


#%%
def authenticate_device_code_management():
    """
    Authenticate the end-user using device auth.
    """
    authority_host_uri = 'https://login.microsoftonline.com'
    tenant = 'a87101d0-71e5-40d5-829e-cf14f5cbe9dd'
    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://management.core.windows.net/'
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials



#%%
def authenticate_device_code_azure_keyvault():
    """
    Authenticate the end-user using device auth.
    """
    authority_host_uri = 'https://login.microsoftonline.com'
    tenant = 'a87101d0-71e5-40d5-829e-cf14f5cbe9dd'
    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://vault.azure.net'
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials



#%%
credentials = authenticate_device_code_vault()


# Create a Subscription Client
# subscription_client = SubscriptionClient(credentials)
# subscription = next(subscription_client.subscriptions.list())
# subscription_id = subscription.subscription_id

# # Create a Resource Management client
# resource_client = ResourceManagementClient(credentials, subscription_id)


# # List resource groups as an example. The only limit is what role and policy are assigned to this MSI token.
# for resource_group in resource_client.resource_groups.list():
#     print(resource_group.name)



keyVaultClient = KeyVaultClient(credentials)

# VAULT_URL must be in the format 'https://<vaultname>.vault.azure.net'
VAULT_URL = 'https://keyvault-mcpforlife.vault.azure.net/'
SECRET_ID = 'kql-magic'
# SECRET_VERSION is required, and can be obtained with the KeyVaultClient.get_secret_versions(self, vault_url, secret_id) API
#SECRET_VERSION = keyVaultClient.get_secret_versions(self, VAULT_URL, SECRET_ID)
secret_bundle = keyVaultClient.get_secret(VAULT_URL, SECRET_ID, '')
secret = secret_bundle.value
print(secret)

#%%
