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
from mtrade.infrastructure.emailer.services import Mail

mail = Mail(
	'Here is the subject',
	'Here is the body.',
	'from@mtrade.mx',
	['to@mtrade.mx'],
)

mail.send(fail_silently=False)
```
#### Dynamic Template with JSON Data
First, create a [dynamic template](https://mc.sendgrid.com/dynamic-templates) and copy the ID.

```python
from mtrade.infrastructure.emailer.services import Mail

mail = Mail(
	'Here is the subject',
	from_email = 'from@mtrade.mx',
	to = ['to@mtrade.mx'],
	bcc = ['bcc@mtrade.mx'],
)

mail.template_id = 'sendgrid_template_id'
# Dynamic SendGrid template data
mail.dynamic_template_data = {
	'title': 'testTitle',
	'name': 'testName'
}
mail.reply_to = 'reply-to@mtrade.mx'

mail.send(fail_silently=False)
```

#### The kitchen sink Mail (all of the supported SendGrid specific properties)
```python
from mtrade.infrastructure.emailer.services import Mail

mail = Mail(
  from_email='from@mtrade.mx',
  to=['to@mtrade.mx'],
  cc=['cc@mtrade.mx'],
  bcc=['bcc@mtrade.mx'],
)

# Personalization custom args
# https://sendgrid.com/docs/for-developers/sending-email/personalizations/
mail.custom_args = {'arg1': 'value1', 'arg2': 'value2'}

# Reply to email address (sendgrid only supports 1 reply-to email address)
mail.reply_to = 'reply-to@mtrade.mx'

# Send at (accepts an integer per the sendgrid docs)
# https://sendgrid.com/docs/API_Reference/SMTP_API/scheduling_parameters.html#-Send-At
mail.send_at = 1600188812

# Transactional templates
# https://sendgrid.com/docs/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates/
mail.template_id = "your-dynamic-template-id"
mail.dynamic_template_data = {  # Sendgrid v6+ only
  "title": foo
}
mail.substitutions = {
  "title": bar
}

# Unsubscribe groups
# https://sendgrid.com/docs/ui/sending-email/unsubscribe-groups/
mail.asm = {'group_id': 123, 'groups_to_display': ['group1', 'group2']}

# Categories
# https://sendgrid.com/docs/glossary/categories/
mail.categories = ['category1', 'category2']

# IP Pools
# https://sendgrid.com/docs/ui/account-and-settings/ip-pools/
mail.ip_pool_name = 'my-ip-pool'


mail.send(fail_silently=False)
```