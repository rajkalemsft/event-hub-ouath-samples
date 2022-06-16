import base64
import os

from azure.identity import CertificateCredential, DefaultAzureCredential
from azure.keyvault.certificates import CertificateClient, CertificateContentType, CertificatePolicy
from azure.keyvault.secrets import SecretClient
import time
from confluent_kafka import Producer
from azure.identity import ClientSecretCredential 
from dotenv import load_dotenv

load_dotenv()

FULLY_QUALIFIED_NAMESPACE= os.environ['EVENT_HUB_HOSTNAME']
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']
CONSUMER_GROUP='$Default'
AUTH_SCOPE= "https://" + FULLY_QUALIFIED_NAMESPACE +"/.default"


def get_cred(self):
    VAULT_URL = os.environ["VAULT_URL"]

    credential = ClientSecretCredential(os.environ['AZURE_TENANT_ID'], os.environ['AZURE_KV_CLIENT_ID'],
     os.environ['AZURE_KV_CLIENT_SECRET'])

    # a CertificateClient to create self-signed certs to work with
    CERT_CLIENT = CertificateClient(VAULT_URL, credential)

    # Key Vault stores certificate private keys as secrets, so we use a SecretClient to retrieve them
    SECRET_CLIENT = SecretClient(VAULT_URL, credential)

    ## Creating a self-signed cert to work with
    #create_cert_poller = CERT_CLIENT.begin_create_certificate("azure-identity-sample", CertificatePolicy.get_default())
    #cert = create_cert_poller.result()
    #
    ## The certificate as returned by begin_create_certificate() or get_certificate() contains
    ## only the public portion of the certificate. Key Vault will release the private key only
    ## if the certificate's policy indicates it's exportable (certs are exportable by default).
    #policy = CERT_CLIENT.get_certificate_policy(cert.name)
    #assert policy.exportable, "Expected an exportable certificate because that's Key Vault's default"
    #
    ## The policy's content_type indicates whether the certificate is stored in PEM or PKCS12 format
    #assert policy.content_type == CertificateContentType.pkcs12, "Expected PKCS12 because that's Key Vault's default"
    #
    # Key Vault stores the complete certificate, with its private key, as a secret sharing the certificate's name
    # Because this certificate is stored in PKCS12 format, the secret's value is base64 encoded bytes
    encoded_cert = SECRET_CLIENT.get_secret("eventhub-kafka").value
    pkcs12_bytes = base64.b64decode(encoded_cert)

    # This credential will load the certificate but can't actually authenticate. Authentication requires real
    # tenant and client IDs for a service principal configured to accept the certificate.
    return CertificateCredential(os.environ["AZURE_TENANT_ID"], os.environ["AZURE_CLIENT_ID"], certificate_data=pkcs12_bytes)

def _get_token(self):
    """Note here value of config comes from sasl.oauthbearer.config below.
    It is not used in this example but you can put arbitrary values to
    configure how you can get the token (e.g. which token URL to use)
    """
    cred = get_cred(self)
    access_token = cred.get_token(AUTH_SCOPE)
    return access_token.token, time.time() + access_token.expires_on

producer = Producer({
    "bootstrap.servers": FULLY_QUALIFIED_NAMESPACE + ":9093",
    "sasl.mechanism": "OAUTHBEARER",
    "security.protocol": "SASL_SSL",
    "oauth_cb": _get_token,
    "enable.idempotence": True,
    "acks": "all",
    # "debug": "broker,topic,msg"
})


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


some_data_source = [str(i) for i in range(1000)]
for data in some_data_source:
    # Trigger any available delivery report callbacks from previous produce() calls
    producer.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    producer.produce(EVENTHUB_NAME, data.encode("utf-8"), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
producer.flush()
