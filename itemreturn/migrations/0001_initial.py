# Generated by Django 2.1.5 on 2022-04-21 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='returnitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Return_Date', models.DateField(auto_now=True)),
                ('Item_Code', models.CharField(max_length=30)),
                ('Quatity_return', models.PositiveIntegerField()),
                ('Unit_Price', models.FloatField(blank=True, null=True)),
                ('Igst_Percent', models.FloatField(blank=True, null=True)),
                ('Cgst_Percent', models.FloatField(blank=True, null=True)),
                ('Sgst_Percent', models.FloatField(blank=True, null=True)),
                ('Igst_Tot', models.FloatField(blank=True, null=True)),
                ('Cgst_Tot', models.FloatField(blank=True, null=True)),
                ('Sgst_Tot', models.FloatField(blank=True, null=True)),
                ('Total_No_Tax', models.FloatField()),
                ('Total', models.FloatField()),
                ('customer_name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]