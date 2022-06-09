import os
import asyncio
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubConsumerClient
from azure.identity.aio import EnvironmentCredential
#aiohttp

fully_qualified_namespace = "rklabeventhub.servicebus.windows.net" #os.environ['EVENT_HUB_HOSTNAME']
eventhub_name = "topic3" #os.environ['EVENT_HUB_NAME']
consumer_group='$default'

async def on_event(partition_context, event):
    # Put your code here.
    # If the operation is i/o intensive, async will have better performance.
    print("Received event from partition: {}.".format(partition_context.partition_id))
    await partition_context.update_checkpoint(event)

async def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))

async def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))

async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


async def run():
    credential = EnvironmentCredential()
    async with credential:
        consumer = EventHubConsumerClient(fully_qualified_namespace=fully_qualified_namespace,
                                          eventhub_name=eventhub_name,
                                          consumer_group= consumer_group,
                                          credential=credential)

        async with consumer:
             await consumer.receive(
            on_event=on_event,
            on_error=on_error,
            on_partition_close=on_partition_close,
            on_partition_initialize=on_partition_initialize,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )


asyncio.run(run())
print('Finished receiving.')