# Azure EventHub OAuth samples
Repository includes python samples using Azure AD OUATH for eventhub resource.

**/eventhub** --> Includes producer and consumer sample with azure sdk for EventHub

**/eventhub-kafka** --> Includes producer and consumer sample with confluent-kafka and Azure.Identity package

**Setup**
Edit the .env file for below values before open the repo in .devcontainer.

AZURE_AUTHORITY_HOST=login.microsoftonline.com
AZURE_CLIENT_ID=<<AppClientId>>
AZURE_CLIENT_SECRET=<<AppSecret>>
AZURE_TENANT_ID=<<TenantID>>
EVENT_HUB_HOSTNAME=<<EventHubNameSpace>>
EVENT_HUB_NAME=<<EvemtHubName>>
CONSUMER_GROUP=<<ConsumerGroupName>>
