# Generated by Django 2.1.5 on 2022-04-26 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='salesDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item_Code', models.IntegerField()),
                ('session_id', models.CharField(max_length=150)),
                ('Item_Name', models.CharField(max_length=500)),
                ('Item_Catogory', models.CharField(max_length=150)),
                ('HSN_Code', models.CharField(max_length=30)),
                ('Quatity_Sold', models.FloatField()),
                ('Unit', models.CharField(max_length=60)),
                ('Rate_Of_Sale', models.FloatField()),
                ('IGST_Percent', models.FloatField()),
                ('CGST_Percent', models.FloatField()),
                ('SGST_Percent', models.FloatField()),
                ('Total', models.FloatField(null=True)),
                ('Gross_Total', models.FloatField(null=True)),
                ('Total_CGST', models.FloatField(null=True)),
                ('Total_SGST', models.FloatField(null=True)),
                ('Total_IGST', models.FloatField(null=True)),
                ('GST_Type', models.CharField(max_length=6)),
                ('Rate_Of_Purchase', models.FloatField()),
                ('insert_date', models.DateTimeField(auto_now=True)),
                ('FinalSP', models.FloatField(null=True)),
                ('FinalGST', models.FloatField(null=True)),
            ],
        ),
    ]
