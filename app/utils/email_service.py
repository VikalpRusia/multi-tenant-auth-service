# Import SendinBlue library
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from config.constants import EMAIL_API_KEY

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = EMAIL_API_KEY

# Initialize the SendingBlue API instance
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)


# Define the email sender function
def send_email(
    subject: str, html: str, to_address: dict[str, str] | list[dict[str, str]]
):
    subject = subject
    sender = {"name": "Vikalp Rusia", "email": "rusiavikalp@gmail.com"}
    html_content = html

    # Define the recipient(s)
    if isinstance(to_address, dict):
        to = [to_address]
    else:
        to = to_address

    # Create a SendSmtpEmail object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, sender=sender, subject=subject
    )

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        return {"message": "Email sent successfully!"}
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s" % e)
        raise e


# if __name__ == "__main__":
#     send_email("hi", "hi", {"email": "rusiavikalp@gmail.com"})
