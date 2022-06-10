# Azure EventHub OAuth samples
[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?https://github.com/rajkalemsft/event-hub-ouath-samples)

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
