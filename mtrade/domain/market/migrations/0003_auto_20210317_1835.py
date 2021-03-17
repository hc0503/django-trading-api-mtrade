# Generated by Django 3.1.7 on 2021-03-17 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_auto_20210317_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordergroup',
            name='status',
        ),
        migrations.AddField(
            model_name='ordergroup',
            name='allocation_status',
            field=models.CharField(choices=[('full', 'Full'), ('partial', 'Partial'), ('none', 'None')], default='none', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordergroup',
            name='group_status',
            field=models.CharField(choices=[('active', 'Active'), ('expired', 'Expired'), ('cancelled', 'Cancelled')], default='inactive', max_length=150),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='COBOrder',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('trader_id', models.UUIDField()),
                ('institution_id', models.UUIDField()),
                ('security_id', models.UUIDField()),
                ('priority', models.DateTimeField()),
                ('expiration', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=20, max_digits=40)),
                ('size', models.IntegerField()),
                ('direction', models.CharField(choices=[('bid', 'Bid'), ('ask', 'Ask')], max_length=150)),
                ('status', models.CharField(choices=[('new', 'New'), ('active', 'Active'), ('cancelled', 'Cancelled'), ('expired', 'Expired'), ('queued', 'Queued'), ('replaced', 'Replaced'), ('fully-allocated', 'Fully Allocated')], max_length=150)),
                ('dirty_price', models.DecimalField(decimal_places=20, max_digits=40)),
                ('notional', models.DecimalField(decimal_places=20, max_digits=40)),
                ('spread', models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True)),
                ('discount_margin', models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True)),
                ('yield_value', models.DecimalField(decimal_places=20, max_digits=40)),
                ('order_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='market.ordergroup')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
