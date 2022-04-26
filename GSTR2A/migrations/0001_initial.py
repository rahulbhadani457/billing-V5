# Generated by Django 2.1.5 on 2022-04-26 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GSRT2A',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Supplier_name', models.CharField(max_length=100)),
                ('GSTIN_of_Supplier', models.CharField(max_length=15)),
                ('Invoice_number', models.CharField(max_length=20)),
                ('Invoice_date', models.DateField()),
                ('Received_date', models.DateField(blank=True, null=True)),
                ('Amount_No_Tax', models.FloatField()),
                ('SGST_Tax', models.FloatField(blank=True, null=True)),
                ('CGST_Tax', models.FloatField(blank=True, null=True)),
                ('IGST_Tax', models.FloatField(blank=True, null=True)),
                ('supplier_id', models.PositiveIntegerField()),
                ('Total_Amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GSRT2A_payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('GSTIN_of_Supplier', models.CharField(max_length=15)),
                ('Supplier_name', models.CharField(max_length=100)),
                ('Invoice_number', models.CharField(max_length=20)),
                ('payment_Amount', models.FloatField()),
                ('payment_left', models.FloatField()),
                ('current_payment_Date', models.DateField()),
                ('supplier_id', models.PositiveIntegerField()),
                ('Comment', models.CharField(max_length=200)),
                ('is_last', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='GSRT2A_supplier_id',
            fields=[
                ('supplier_id', models.AutoField(primary_key=True, serialize=False)),
                ('GSTIN_of_Supplier', models.CharField(max_length=15)),
            ],
        ),
    ]
