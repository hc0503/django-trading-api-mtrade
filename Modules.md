# MTrade Infrastructure modules

## Emailer module
### How to install
In your project's in .env
```shell
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your_sendgrid_api
SENDGRID_SANDBOX_MODE_IN_DEBUG=True/False
```

### Usage
#### Simple
```python
from django.core.mail import send_mail

send_mail(
	'Subject here',
	'Here is the message.',
	'from@example.com',
	['to@example.com'],
	fail_silently=False,
)
```
#### Dynamic Template with JSON Data
First, create a [dynamic template](https://mc.sendgrid.com/dynamic-templates) and copy the ID.

```python
from mtrade.infrastructure.emailer.services import EmailerServices

emailer = EmailerServices(
	'sendgrid_template_id',
	# SendGrid template data
	{
		'title': 'testTitle',
		'name': 'testName',
	},
	# Reply email, the default is None
	'reply@example.com',
)

# Email send with to
emailer.sendTo([
	'to1@example.com',
	'to2@example.com',
])

# Email send with cc
emailer.sendCC([
	'to1@example.com',
	'to2@example.com',
])

# Email send with bcc
emailer.sendBCC([
	'to1@example.com',
	'to2@example.com',
])
```

