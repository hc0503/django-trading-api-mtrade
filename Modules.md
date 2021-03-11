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
	subject = 'Here is the subject',
	body = 'Here is the body.',
	from_email = 'from@mtrade.mx',
	to = ['to@mtrade.mx'],
	bcc = ['bcc@mtrade.mx'],
	connection = 'Here is connection',
	attachments = 'Here is attachments',
	headers = 'headers',
	cc = ['cc@mtrade.mx'],
	reply_to = 'reply-to@mtrade.mx',
	# Transactional templates
	# https://sendgrid.com/docs/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates/
	template_id = 'sendgrid_template_id',
	dynamic_template_data = {
		'title': 'testTitle',
		'name': 'testName'
	},
)

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

# Send at (accepts an integer per the sendgrid docs)
# https://sendgrid.com/docs/API_Reference/SMTP_API/scheduling_parameters.html#-Send-At
mail.send_at = 1600188812

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

## Logger module
### Usage
```python
import logging

logger = logging.getLogger(__name__)

logger.info('Here is the message.', extra={'key1': 'value1', 'key2': 'value2'})
# output logs/log.json > {"key1":"value1","key2":"value2",level":"INFO","msg":"Here is the message.","module":"mtrade.infrastructure.logger.views.infoLogger","time":"2021-03-09T23:39:08.748015"}

logger.debug('Here is the message.')
# output logs/log.json > {level":"DEBUG","msg":"Here is the message.","module":"mtrade.infrastructure.logger.views.infoLogger","time":"2021-03-09T23:39:08.748015"}
```

### Logger levels
- debug
- info
- warning
- error
- fatal