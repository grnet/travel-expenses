# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
import texpenses.models.common
import texpenses.validators
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('iban', models.CharField(max_length=27, null=True, validators=[django.core.validators.RegexValidator(b'^^GR\\d{9}[0-9A-Z]{16}$', b'IBAN number is not valid.')])),
                ('specialty', models.CharField(max_length=5, null=True, choices=[['CE', '\u0397\u03bb\u03b5\u03ba\u03c4\u03c1\u03bf\u03bb\u03cc\u03b3\u03bf\u03c2 \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03cc\u03c2 \u03ba\u03b1\u03b9 \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03cc\u03c2 \u03a5\u03c0\u03bf\u03bb\u03bf\u03b3\u03b9\u03c3\u03c4\u03ce\u03bd'], ['INF', '\u0395\u03c0\u03b9\u03c3\u03c4\u03ae\u03bc\u03b7 \u03a0\u03bb\u03b7\u03c1\u03bf\u03c6\u03bf\u03c1\u03b9\u03ba\u03ae\u03c2 \u03ba\u03b1\u03b9 \u03a4\u03b7\u03bb\u03b5\u03c0\u03b9\u03ba\u03bf\u03b9\u03bd\u03c9\u03bd\u03b9\u03ce\u03bd'], ['SCIE', '\u0398\u03b5\u03c4\u03b9\u03ba\u03ad\u03c2 \u0395\u03c0\u03b9\u03c3\u03c4\u03ae\u03bc\u03b5\u03c2 (\u03c6\u03c5\u03c3\u03b9\u03ba\u03ae, \u03c7\u03b7\u03bc\u03b5\u03af\u03b1, \u03bc\u03b1\u03b8\u03b7\u03bc\u03b1\u03c4\u03b9\u03ba\u03ac)'], ['ECON', '\u0394\u03b9\u03bf\u03af\u03ba\u03b7\u03c3\u03b7 \u03ba\u03b1\u03b9 \u039f\u03b9\u03ba\u03bf\u03bd\u03bf\u03bc\u03af\u03b1'], ['JOU', '\u0394\u03b7\u03bc\u03bf\u03c3\u03b9\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1 - \u0395\u03c0\u03b9\u03ba\u03bf\u03b9\u03bd\u03c9\u03bd\u03af\u03b1'], ['LAW', '\u039d\u03bf\u03bc\u03b9\u03ba\u03ae'], ['PHI', '\u03a6\u03b9\u03bb\u03bf\u03c3\u03bf\u03c6\u03af\u03b1 - \u03a0\u03b1\u03b9\u03b4\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae - \u03a6\u03b9\u03bb\u03bf\u03bb\u03bf\u03b3\u03af\u03b1'], ['OTHER', '\u0386\u03bb\u03bb\u03b5\u03c2 \u03b5\u03b9\u03b4\u03b9\u03ba\u03cc\u03c4\u03b7\u03c4\u03b5\u03c2 \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03ce\u03bd (\u03c0\u03bb\u03b7\u03bd \u0397\u03bb\u03b5\u03ba\u03c4\u03c1\u03bf\u03bb\u03cc\u03b3\u03c9\u03bd \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03ce\u03bd)']])),
                ('tax_reg_num', models.CharField(max_length=9, unique=True, null=True, validators=[texpenses.validators.afm_validator])),
                ('kind', models.CharField(max_length=5, null=True, choices=[['PRE', '\u03a0\u03c1\u03cc\u03b5\u03b4\u03c1\u03bf\u03c2 \u0394\u03a3'], ['MEM', '\u039c\u03ad\u03bb\u03bf\u03c2 \u0394\u03a3'], ['LEAD', '\u0395\u03c0\u03b9\u03ba\u03b5\u03c6\u03b1\u03bb\u03ae\u03c2 \u039f\u03bc\u03ac\u03b4\u03b1\u03c2 \u03a3\u03c4\u03c1\u03b1\u03c4\u03b7\u03b3\u03b9\u03ba\u03ae\u03c2'], ['PM', '\u0394\u03b9\u03b1\u03c7\u03b5\u03b9\u03c1\u03b9\u03c3\u03c4\u03ae\u03c2 \u0388\u03c1\u03b3\u03c9\u03bd'], ['TECH', '\u03a3\u03c4\u03ad\u03bb\u03b5\u03c7\u03bf\u03c2 \u03a4\u03b5\u03c7\u03bd\u03b9\u03ba\u03bf\u03cd \u03a4\u03bc\u03ae\u03bc\u03b1\u03c4\u03bf\u03c2'], ['PRO', '\u0391\u03bd\u03b1\u03bb\u03c5\u03c4\u03ae\u03c2/\u03a0\u03c1\u03bf\u03b3\u03c1\u03b1\u03bc\u03bc\u03b1\u03c4\u03b9\u03c3\u03c4\u03ae\u03c2'], ['LAW', '\u039d\u03bf\u03bc\u03b9\u03ba\u03ae \u03a5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7'], ['ECON', '\u0394\u03b9\u03bf\u03b9\u03ba\u03b7\u03c4\u03b9\u03ba\u03ae \u03ba\u03b1\u03b9 \u039f\u03b9\u03ba\u03bf\u03bd\u03bf\u03bc\u03b9\u03ba\u03ae \u03a5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7'], ['EXT', '\u0395\u03be\u03c9\u03c4\u03b5\u03c1\u03b9\u03ba\u03cc\u03c2 \u03c3\u03c5\u03bd\u03b5\u03c1\u03b3\u03ac\u03c4\u03b7\u03c2']])),
                ('user_category', models.CharField(default=b'B', max_length=1, choices=[['A', 'A'], ['B', 'B']])),
                ('trip_days_left', models.IntegerField(default=60, validators=[django.core.validators.MaxValueValidator(60), django.core.validators.MinValueValidator(0)])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('category', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('currency', models.CharField(default=b'EUR', max_length=3, choices=[['AFN', 'Afghani'], ['EUR', 'Euro'], ['ALL', 'Lek'], ['DZD', 'Algerian Dinar'], ['USD', 'US Dollar'], ['AOA', 'Kwanza'], ['XCD', 'East Caribbean Dollar'], ['ARS', 'Argentine Peso'], ['AMD', 'Armenian Dram'], ['AWG', 'Aruban Florin'], ['AUD', 'Australian Dollar'], ['AZN', 'Azerbaijanian Manat'], ['BSD', 'Bahamian Dollar'], ['BHD', 'Bahraini Dinar'], ['BDT', 'Taka'], ['BBD', 'Barbados Dollar'], ['BYN', 'Belarusian Ruble'], ['BYR', 'Belarusian Ruble'], ['BZD', 'Belize Dollar'], ['XOF', 'CFA Franc BCEAO'], ['BMD', 'Bermudian Dollar'], ['INR', 'Indian Rupee'], ['BTN', 'Ngultrum'], ['BOB', 'Boliviano'], ['BOV', 'Mvdol'], ['BAM', 'Convertible Mark'], ['BWP', 'Pula'], ['NOK', 'Norwegian Krone'], ['BRL', 'Brazilian Real'], ['BND', 'Brunei Dollar'], ['BGN', 'Bulgarian Lev'], ['BIF', 'Burundi Franc'], ['CVE', 'Cabo Verde Escudo'], ['KHR', 'Riel'], ['XAF', 'CFA Franc BEAC'], ['CAD', 'Canadian Dollar'], ['KYD', 'Cayman Islands Dollar'], ['CLP', 'Chilean Peso'], ['CLF', 'Unidad de Fomento'], ['CNY', 'Yuan Renminbi'], ['COP', 'Colombian Peso'], ['COU', 'Unidad de Valor Real'], ['KMF', 'Comoro Franc'], ['CDF', 'Congolese Franc'], ['NZD', 'New Zealand Dollar'], ['CRC', 'Costa Rican Colon'], ['HRK', 'Kuna'], ['CUP', 'Cuban Peso'], ['CUC', 'Peso Convertible'], ['ANG', 'Netherlands Antillean Guilder'], ['CZK', 'Czech Koruna'], ['DKK', 'Danish Krone'], ['DJF', 'Djibouti Franc'], ['DOP', 'Dominican Peso'], ['EGP', 'Egyptian Pound'], ['SVC', 'El Salvador Colon'], ['ERN', 'Nakfa'], ['ETB', 'Ethiopian Birr'], ['FKP', 'Falkland Islands Pound'], ['FJD', 'Fiji Dollar'], ['XPF', 'CFP Franc'], ['GMD', 'Dalasi'], ['GEL', 'Lari'], ['GHS', 'Ghana Cedi'], ['GIP', 'Gibraltar Pound'], ['GTQ', 'Quetzal'], ['GBP', 'Pound Sterling'], ['GNF', 'Guinea Franc'], ['GYD', 'Guyana Dollar'], ['HTG', 'Gourde'], ['HNL', 'Lempira'], ['HKD', 'Hong Kong Dollar'], ['HUF', 'Forint'], ['ISK', 'Iceland Krona'], ['IDR', 'Rupiah'], ['XDR', 'SDR (Special Drawing Right)'], ['IRR', 'Iranian Rial'], ['IQD', 'Iraqi Dinar'], ['ILS', 'New Israeli Sheqel'], ['JMD', 'Jamaican Dollar'], ['JPY', 'Yen'], ['JOD', 'Jordanian Dinar'], ['KZT', 'Tenge'], ['KES', 'Kenyan Shilling'], ['KPW', 'North Korean Won'], ['KRW', 'Won'], ['KWD', 'Kuwaiti Dinar'], ['KGS', 'Som'], ['LAK', 'Kip'], ['LBP', 'Lebanese Pound'], ['LSL', 'Loti'], ['ZAR', 'Rand'], ['LRD', 'Liberian Dollar'], ['LYD', 'Libyan Dinar'], ['CHF', 'Swiss Franc'], ['MOP', 'Pataca'], ['MKD', 'Denar'], ['MGA', 'Malagasy Ariary'], ['MWK', 'Malawi Kwacha'], ['MYR', 'Malaysian Ringgit'], ['MVR', 'Rufiyaa'], ['MRO', 'Ouguiya'], ['MUR', 'Mauritius Rupee'], ['XUA', 'ADB Unit of Account'], ['MXN', 'Mexican Peso'], ['MXV', 'Mexican Unidad de Inversion (UDI)'], ['MDL', 'Moldovan Leu'], ['MNT', 'Tugrik'], ['MAD', 'Moroccan Dirham'], ['MZN', 'Mozambique Metical'], ['MMK', 'Kyat'], ['NAD', 'Namibia Dollar'], ['NPR', 'Nepalese Rupee'], ['NIO', 'Cordoba Oro'], ['NGN', 'Naira'], ['OMR', 'Rial Omani'], ['PKR', 'Pakistan Rupee'], ['PAB', 'Balboa'], ['PGK', 'Kina'], ['PYG', 'Guarani'], ['PEN', 'Sol'], ['PHP', 'Philippine Peso'], ['PLN', 'Zloty'], ['QAR', 'Qatari Rial'], ['RON', 'Romanian Leu'], ['RUB', 'Russian Ruble'], ['RWF', 'Rwanda Franc'], ['SHP', 'Saint Helena Pound'], ['WST', 'Tala'], ['STD', 'Dobra'], ['SAR', 'Saudi Riyal'], ['RSD', 'Serbian Dinar'], ['SCR', 'Seychelles Rupee'], ['SLL', 'Leone'], ['SGD', 'Singapore Dollar'], ['XSU', 'Sucre'], ['SBD', 'Solomon Islands Dollar'], ['SOS', 'Somali Shilling'], ['SSP', 'South Sudanese Pound'], ['LKR', 'Sri Lanka Rupee'], ['SDG', 'Sudanese Pound'], ['SRD', 'Surinam Dollar'], ['SZL', 'Lilangeni'], ['SEK', 'Swedish Krona'], ['CHE', 'WIR Euro'], ['CHW', 'WIR Franc'], ['SYP', 'Syrian Pound'], ['TWD', 'New Taiwan Dollar'], ['TJS', 'Somoni'], ['TZS', 'Tanzanian Shilling'], ['THB', 'Baht'], ['TOP', 'Pa\u2019anga'], ['TTD', 'Trinidad and Tobago Dollar'], ['TND', 'Tunisian Dinar'], ['TRY', 'Turkish Lira'], ['TMT', 'Turkmenistan New Manat'], ['UGX', 'Uganda Shilling'], ['UAH', 'Hryvnia'], ['AED', 'UAE Dirham'], ['USN', 'US Dollar (Next day)'], ['UYU', 'Peso Uruguayo'], ['UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'], ['UZS', 'Uzbekistan Sum'], ['VUV', 'Vatu'], ['VEF', 'Bol\xedvar'], ['VND', 'Dong'], ['YER', 'Yemeni Rial'], ['ZMW', 'Zambian Kwacha'], ['ZWL', 'Zimbabwe Dollar'], ['XBA', 'Bond Markets Unit European Composite Unit (EURCO)'], ['XBB', 'Bond Markets Unit European Monetary Unit (E.M.U.-6)'], ['XBC', 'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'], ['XBD,', 'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'], ['XTS', 'Codes specifically reserved for testing purposes'], ['XXX', 'The codes assigned for transactions where no currency is involved'], ['XAU', 'Gold'], ['XPD', 'Palladium'], ['XPT', 'Platinum'], ['XAG', 'Silver']])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('non_grnet_quota', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('movement_id', models.CharField(max_length=200, null=True, blank=True)),
                ('expenditure_protocol', models.CharField(max_length=30, null=True, blank=True)),
                ('expenditure_date_protocol', models.DateField(blank=True, null=True, validators=[texpenses.validators.date_validator])),
                ('movement_protocol', models.CharField(max_length=30, null=True, blank=True)),
                ('movement_date_protocol', models.DateField(blank=True, null=True, validators=[texpenses.validators.date_validator])),
                ('compensation_petition_protocol', models.CharField(max_length=30, null=True, blank=True)),
                ('compensation_petition_date', models.DateField(blank=True, null=True, validators=[texpenses.validators.date_validator])),
                ('compensation_decision_protocol', models.CharField(max_length=30, null=True, blank=True)),
                ('compensation_decision_date', models.DateField(blank=True, null=True, validators=[texpenses.validators.date_validator])),
                ('manager_travel_approval', models.CharField(max_length=200, null=True, blank=True)),
                ('manager_final_approval', models.CharField(max_length=200, null=True, blank=True)),
                ('participation_cost', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('participation_default_currency', models.CharField(default=b'EUR', max_length=3)),
                ('participation_local_cost', models.FloatField(default=0.0, blank=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('participation_local_currency', models.CharField(blank=True, max_length=3, choices=[['AFN', 'Afghani'], ['EUR', 'Euro'], ['ALL', 'Lek'], ['DZD', 'Algerian Dinar'], ['USD', 'US Dollar'], ['AOA', 'Kwanza'], ['XCD', 'East Caribbean Dollar'], ['ARS', 'Argentine Peso'], ['AMD', 'Armenian Dram'], ['AWG', 'Aruban Florin'], ['AUD', 'Australian Dollar'], ['AZN', 'Azerbaijanian Manat'], ['BSD', 'Bahamian Dollar'], ['BHD', 'Bahraini Dinar'], ['BDT', 'Taka'], ['BBD', 'Barbados Dollar'], ['BYN', 'Belarusian Ruble'], ['BYR', 'Belarusian Ruble'], ['BZD', 'Belize Dollar'], ['XOF', 'CFA Franc BCEAO'], ['BMD', 'Bermudian Dollar'], ['INR', 'Indian Rupee'], ['BTN', 'Ngultrum'], ['BOB', 'Boliviano'], ['BOV', 'Mvdol'], ['BAM', 'Convertible Mark'], ['BWP', 'Pula'], ['NOK', 'Norwegian Krone'], ['BRL', 'Brazilian Real'], ['BND', 'Brunei Dollar'], ['BGN', 'Bulgarian Lev'], ['BIF', 'Burundi Franc'], ['CVE', 'Cabo Verde Escudo'], ['KHR', 'Riel'], ['XAF', 'CFA Franc BEAC'], ['CAD', 'Canadian Dollar'], ['KYD', 'Cayman Islands Dollar'], ['CLP', 'Chilean Peso'], ['CLF', 'Unidad de Fomento'], ['CNY', 'Yuan Renminbi'], ['COP', 'Colombian Peso'], ['COU', 'Unidad de Valor Real'], ['KMF', 'Comoro Franc'], ['CDF', 'Congolese Franc'], ['NZD', 'New Zealand Dollar'], ['CRC', 'Costa Rican Colon'], ['HRK', 'Kuna'], ['CUP', 'Cuban Peso'], ['CUC', 'Peso Convertible'], ['ANG', 'Netherlands Antillean Guilder'], ['CZK', 'Czech Koruna'], ['DKK', 'Danish Krone'], ['DJF', 'Djibouti Franc'], ['DOP', 'Dominican Peso'], ['EGP', 'Egyptian Pound'], ['SVC', 'El Salvador Colon'], ['ERN', 'Nakfa'], ['ETB', 'Ethiopian Birr'], ['FKP', 'Falkland Islands Pound'], ['FJD', 'Fiji Dollar'], ['XPF', 'CFP Franc'], ['GMD', 'Dalasi'], ['GEL', 'Lari'], ['GHS', 'Ghana Cedi'], ['GIP', 'Gibraltar Pound'], ['GTQ', 'Quetzal'], ['GBP', 'Pound Sterling'], ['GNF', 'Guinea Franc'], ['GYD', 'Guyana Dollar'], ['HTG', 'Gourde'], ['HNL', 'Lempira'], ['HKD', 'Hong Kong Dollar'], ['HUF', 'Forint'], ['ISK', 'Iceland Krona'], ['IDR', 'Rupiah'], ['XDR', 'SDR (Special Drawing Right)'], ['IRR', 'Iranian Rial'], ['IQD', 'Iraqi Dinar'], ['ILS', 'New Israeli Sheqel'], ['JMD', 'Jamaican Dollar'], ['JPY', 'Yen'], ['JOD', 'Jordanian Dinar'], ['KZT', 'Tenge'], ['KES', 'Kenyan Shilling'], ['KPW', 'North Korean Won'], ['KRW', 'Won'], ['KWD', 'Kuwaiti Dinar'], ['KGS', 'Som'], ['LAK', 'Kip'], ['LBP', 'Lebanese Pound'], ['LSL', 'Loti'], ['ZAR', 'Rand'], ['LRD', 'Liberian Dollar'], ['LYD', 'Libyan Dinar'], ['CHF', 'Swiss Franc'], ['MOP', 'Pataca'], ['MKD', 'Denar'], ['MGA', 'Malagasy Ariary'], ['MWK', 'Malawi Kwacha'], ['MYR', 'Malaysian Ringgit'], ['MVR', 'Rufiyaa'], ['MRO', 'Ouguiya'], ['MUR', 'Mauritius Rupee'], ['XUA', 'ADB Unit of Account'], ['MXN', 'Mexican Peso'], ['MXV', 'Mexican Unidad de Inversion (UDI)'], ['MDL', 'Moldovan Leu'], ['MNT', 'Tugrik'], ['MAD', 'Moroccan Dirham'], ['MZN', 'Mozambique Metical'], ['MMK', 'Kyat'], ['NAD', 'Namibia Dollar'], ['NPR', 'Nepalese Rupee'], ['NIO', 'Cordoba Oro'], ['NGN', 'Naira'], ['OMR', 'Rial Omani'], ['PKR', 'Pakistan Rupee'], ['PAB', 'Balboa'], ['PGK', 'Kina'], ['PYG', 'Guarani'], ['PEN', 'Sol'], ['PHP', 'Philippine Peso'], ['PLN', 'Zloty'], ['QAR', 'Qatari Rial'], ['RON', 'Romanian Leu'], ['RUB', 'Russian Ruble'], ['RWF', 'Rwanda Franc'], ['SHP', 'Saint Helena Pound'], ['WST', 'Tala'], ['STD', 'Dobra'], ['SAR', 'Saudi Riyal'], ['RSD', 'Serbian Dinar'], ['SCR', 'Seychelles Rupee'], ['SLL', 'Leone'], ['SGD', 'Singapore Dollar'], ['XSU', 'Sucre'], ['SBD', 'Solomon Islands Dollar'], ['SOS', 'Somali Shilling'], ['SSP', 'South Sudanese Pound'], ['LKR', 'Sri Lanka Rupee'], ['SDG', 'Sudanese Pound'], ['SRD', 'Surinam Dollar'], ['SZL', 'Lilangeni'], ['SEK', 'Swedish Krona'], ['CHE', 'WIR Euro'], ['CHW', 'WIR Franc'], ['SYP', 'Syrian Pound'], ['TWD', 'New Taiwan Dollar'], ['TJS', 'Somoni'], ['TZS', 'Tanzanian Shilling'], ['THB', 'Baht'], ['TOP', 'Pa\u2019anga'], ['TTD', 'Trinidad and Tobago Dollar'], ['TND', 'Tunisian Dinar'], ['TRY', 'Turkish Lira'], ['TMT', 'Turkmenistan New Manat'], ['UGX', 'Uganda Shilling'], ['UAH', 'Hryvnia'], ['AED', 'UAE Dirham'], ['USN', 'US Dollar (Next day)'], ['UYU', 'Peso Uruguayo'], ['UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'], ['UZS', 'Uzbekistan Sum'], ['VUV', 'Vatu'], ['VEF', 'Bol\xedvar'], ['VND', 'Dong'], ['YER', 'Yemeni Rial'], ['ZMW', 'Zambian Kwacha'], ['ZWL', 'Zimbabwe Dollar'], ['XBA', 'Bond Markets Unit European Composite Unit (EURCO)'], ['XBB', 'Bond Markets Unit European Monetary Unit (E.M.U.-6)'], ['XBC', 'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'], ['XBD,', 'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'], ['XTS', 'Codes specifically reserved for testing purposes'], ['XXX', 'The codes assigned for transactions where no currency is involved'], ['XAU', 'Gold'], ['XPD', 'Palladium'], ['XPT', 'Platinum'], ['XAG', 'Silver']])),
                ('participation_payment_way', models.CharField(default=b'NON', max_length=10, choices=[['NON', '\u038c\u03c7\u03b9 \u03b1\u03ba\u03cc\u03bc\u03b7'], ['AGNT', '\u03a0\u03c1\u03b1\u03ba\u03c4\u03bf\u03c1\u03b5\u03af\u03bf'], ['GRNET', 'VISA \u0395\u0394\u0395\u03a4'], ['VISA', '\u03a0\u03b9\u03c3\u03c4\u03c9\u03c4\u03b9\u03ba\u03ae \u039c\u03b5\u03c4/\u03bd\u03bf\u03c5']])),
                ('participation_payment_description', models.CharField(max_length=200, null=True, blank=True)),
                ('additional_expenses_initial', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('additional_expenses_default_currency', models.CharField(default=b'EUR', max_length=3)),
                ('additional_expenses_initial_description', models.CharField(max_length=400, null=True, blank=True)),
                ('additional_expenses', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('additional_expenses_local_currency', models.CharField(default=b'EUR', max_length=3)),
                ('additional_expenses_description', models.CharField(max_length=400, null=True, blank=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('iban', models.CharField(max_length=27, validators=[django.core.validators.RegexValidator(b'^^GR\\d{9}[0-9A-Z]{16}$', b'IBAN number is not valid.')])),
                ('specialty', models.CharField(max_length=5, choices=[['CE', '\u0397\u03bb\u03b5\u03ba\u03c4\u03c1\u03bf\u03bb\u03cc\u03b3\u03bf\u03c2 \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03cc\u03c2 \u03ba\u03b1\u03b9 \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03cc\u03c2 \u03a5\u03c0\u03bf\u03bb\u03bf\u03b3\u03b9\u03c3\u03c4\u03ce\u03bd'], ['INF', '\u0395\u03c0\u03b9\u03c3\u03c4\u03ae\u03bc\u03b7 \u03a0\u03bb\u03b7\u03c1\u03bf\u03c6\u03bf\u03c1\u03b9\u03ba\u03ae\u03c2 \u03ba\u03b1\u03b9 \u03a4\u03b7\u03bb\u03b5\u03c0\u03b9\u03ba\u03bf\u03b9\u03bd\u03c9\u03bd\u03b9\u03ce\u03bd'], ['SCIE', '\u0398\u03b5\u03c4\u03b9\u03ba\u03ad\u03c2 \u0395\u03c0\u03b9\u03c3\u03c4\u03ae\u03bc\u03b5\u03c2 (\u03c6\u03c5\u03c3\u03b9\u03ba\u03ae, \u03c7\u03b7\u03bc\u03b5\u03af\u03b1, \u03bc\u03b1\u03b8\u03b7\u03bc\u03b1\u03c4\u03b9\u03ba\u03ac)'], ['ECON', '\u0394\u03b9\u03bf\u03af\u03ba\u03b7\u03c3\u03b7 \u03ba\u03b1\u03b9 \u039f\u03b9\u03ba\u03bf\u03bd\u03bf\u03bc\u03af\u03b1'], ['JOU', '\u0394\u03b7\u03bc\u03bf\u03c3\u03b9\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1 - \u0395\u03c0\u03b9\u03ba\u03bf\u03b9\u03bd\u03c9\u03bd\u03af\u03b1'], ['LAW', '\u039d\u03bf\u03bc\u03b9\u03ba\u03ae'], ['PHI', '\u03a6\u03b9\u03bb\u03bf\u03c3\u03bf\u03c6\u03af\u03b1 - \u03a0\u03b1\u03b9\u03b4\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae - \u03a6\u03b9\u03bb\u03bf\u03bb\u03bf\u03b3\u03af\u03b1'], ['OTHER', '\u0386\u03bb\u03bb\u03b5\u03c2 \u03b5\u03b9\u03b4\u03b9\u03ba\u03cc\u03c4\u03b7\u03c4\u03b5\u03c2 \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03ce\u03bd (\u03c0\u03bb\u03b7\u03bd \u0397\u03bb\u03b5\u03ba\u03c4\u03c1\u03bf\u03bb\u03cc\u03b3\u03c9\u03bd \u039c\u03b7\u03c7\u03b1\u03bd\u03b9\u03ba\u03ce\u03bd)']])),
                ('tax_reg_num', models.CharField(max_length=9, validators=[texpenses.validators.afm_validator])),
                ('kind', models.CharField(max_length=5, choices=[['PRE', '\u03a0\u03c1\u03cc\u03b5\u03b4\u03c1\u03bf\u03c2 \u0394\u03a3'], ['MEM', '\u039c\u03ad\u03bb\u03bf\u03c2 \u0394\u03a3'], ['LEAD', '\u0395\u03c0\u03b9\u03ba\u03b5\u03c6\u03b1\u03bb\u03ae\u03c2 \u039f\u03bc\u03ac\u03b4\u03b1\u03c2 \u03a3\u03c4\u03c1\u03b1\u03c4\u03b7\u03b3\u03b9\u03ba\u03ae\u03c2'], ['PM', '\u0394\u03b9\u03b1\u03c7\u03b5\u03b9\u03c1\u03b9\u03c3\u03c4\u03ae\u03c2 \u0388\u03c1\u03b3\u03c9\u03bd'], ['TECH', '\u03a3\u03c4\u03ad\u03bb\u03b5\u03c7\u03bf\u03c2 \u03a4\u03b5\u03c7\u03bd\u03b9\u03ba\u03bf\u03cd \u03a4\u03bc\u03ae\u03bc\u03b1\u03c4\u03bf\u03c2'], ['PRO', '\u0391\u03bd\u03b1\u03bb\u03c5\u03c4\u03ae\u03c2/\u03a0\u03c1\u03bf\u03b3\u03c1\u03b1\u03bc\u03bc\u03b1\u03c4\u03b9\u03c3\u03c4\u03ae\u03c2'], ['LAW', '\u039d\u03bf\u03bc\u03b9\u03ba\u03ae \u03a5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7'], ['ECON', '\u0394\u03b9\u03bf\u03b9\u03ba\u03b7\u03c4\u03b9\u03ba\u03ae \u03ba\u03b1\u03b9 \u039f\u03b9\u03ba\u03bf\u03bd\u03bf\u03bc\u03b9\u03ba\u03ae \u03a5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7'], ['EXT', '\u0395\u03be\u03c9\u03c4\u03b5\u03c1\u03b9\u03ba\u03cc\u03c2 \u03c3\u03c5\u03bd\u03b5\u03c1\u03b3\u03ac\u03c4\u03b7\u03c2']])),
                ('user_category', models.CharField(default=b'B', max_length=1, choices=[['A', 'A'], ['B', 'B']])),
                ('dse', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('task_start_date', models.DateTimeField(blank=True, null=True, validators=[texpenses.validators.date_validator])),
                ('task_end_date', models.DateTimeField(blank=True, null=True, validators=[texpenses.validators.date_validator])),
                ('created', models.DateTimeField(default=datetime.datetime(2016, 10, 5, 15, 4, 53, 665491))),
                ('updated', models.DateTimeField(default=datetime.datetime(2016, 10, 5, 15, 4, 53, 665521))),
                ('deleted', models.BooleanField(default=False)),
                ('reason', models.CharField(max_length=500, null=True, blank=True)),
                ('user_recommendation', models.CharField(max_length=500, null=True, blank=True)),
                ('secretary_recommendation', models.CharField(max_length=500, null=True, blank=True)),
                ('status', models.IntegerField()),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('travel_report', models.CharField(max_length=1000, null=True, blank=True)),
                ('travel_files', models.FileField(null=True, upload_to=texpenses.models.common.user_directory_path, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=500)),
                ('accounting_code', models.CharField(max_length=20)),
                ('manager_name', models.CharField(max_length=40)),
                ('manager_surname', models.CharField(max_length=40)),
                ('manager_email', models.EmailField(max_length=256, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaxOffice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('description', models.CharField(max_length=300, blank=True)),
                ('address', models.CharField(max_length=20, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('phone', models.CharField(max_length=20, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TravelInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accommodation_cost', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('accommodation_default_currency', models.CharField(default=b'EUR', max_length=3)),
                ('accommodation_local_cost', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('accommodation_local_currency', models.CharField(blank=True, max_length=3, choices=[['AFN', 'Afghani'], ['EUR', 'Euro'], ['ALL', 'Lek'], ['DZD', 'Algerian Dinar'], ['USD', 'US Dollar'], ['AOA', 'Kwanza'], ['XCD', 'East Caribbean Dollar'], ['ARS', 'Argentine Peso'], ['AMD', 'Armenian Dram'], ['AWG', 'Aruban Florin'], ['AUD', 'Australian Dollar'], ['AZN', 'Azerbaijanian Manat'], ['BSD', 'Bahamian Dollar'], ['BHD', 'Bahraini Dinar'], ['BDT', 'Taka'], ['BBD', 'Barbados Dollar'], ['BYN', 'Belarusian Ruble'], ['BYR', 'Belarusian Ruble'], ['BZD', 'Belize Dollar'], ['XOF', 'CFA Franc BCEAO'], ['BMD', 'Bermudian Dollar'], ['INR', 'Indian Rupee'], ['BTN', 'Ngultrum'], ['BOB', 'Boliviano'], ['BOV', 'Mvdol'], ['BAM', 'Convertible Mark'], ['BWP', 'Pula'], ['NOK', 'Norwegian Krone'], ['BRL', 'Brazilian Real'], ['BND', 'Brunei Dollar'], ['BGN', 'Bulgarian Lev'], ['BIF', 'Burundi Franc'], ['CVE', 'Cabo Verde Escudo'], ['KHR', 'Riel'], ['XAF', 'CFA Franc BEAC'], ['CAD', 'Canadian Dollar'], ['KYD', 'Cayman Islands Dollar'], ['CLP', 'Chilean Peso'], ['CLF', 'Unidad de Fomento'], ['CNY', 'Yuan Renminbi'], ['COP', 'Colombian Peso'], ['COU', 'Unidad de Valor Real'], ['KMF', 'Comoro Franc'], ['CDF', 'Congolese Franc'], ['NZD', 'New Zealand Dollar'], ['CRC', 'Costa Rican Colon'], ['HRK', 'Kuna'], ['CUP', 'Cuban Peso'], ['CUC', 'Peso Convertible'], ['ANG', 'Netherlands Antillean Guilder'], ['CZK', 'Czech Koruna'], ['DKK', 'Danish Krone'], ['DJF', 'Djibouti Franc'], ['DOP', 'Dominican Peso'], ['EGP', 'Egyptian Pound'], ['SVC', 'El Salvador Colon'], ['ERN', 'Nakfa'], ['ETB', 'Ethiopian Birr'], ['FKP', 'Falkland Islands Pound'], ['FJD', 'Fiji Dollar'], ['XPF', 'CFP Franc'], ['GMD', 'Dalasi'], ['GEL', 'Lari'], ['GHS', 'Ghana Cedi'], ['GIP', 'Gibraltar Pound'], ['GTQ', 'Quetzal'], ['GBP', 'Pound Sterling'], ['GNF', 'Guinea Franc'], ['GYD', 'Guyana Dollar'], ['HTG', 'Gourde'], ['HNL', 'Lempira'], ['HKD', 'Hong Kong Dollar'], ['HUF', 'Forint'], ['ISK', 'Iceland Krona'], ['IDR', 'Rupiah'], ['XDR', 'SDR (Special Drawing Right)'], ['IRR', 'Iranian Rial'], ['IQD', 'Iraqi Dinar'], ['ILS', 'New Israeli Sheqel'], ['JMD', 'Jamaican Dollar'], ['JPY', 'Yen'], ['JOD', 'Jordanian Dinar'], ['KZT', 'Tenge'], ['KES', 'Kenyan Shilling'], ['KPW', 'North Korean Won'], ['KRW', 'Won'], ['KWD', 'Kuwaiti Dinar'], ['KGS', 'Som'], ['LAK', 'Kip'], ['LBP', 'Lebanese Pound'], ['LSL', 'Loti'], ['ZAR', 'Rand'], ['LRD', 'Liberian Dollar'], ['LYD', 'Libyan Dinar'], ['CHF', 'Swiss Franc'], ['MOP', 'Pataca'], ['MKD', 'Denar'], ['MGA', 'Malagasy Ariary'], ['MWK', 'Malawi Kwacha'], ['MYR', 'Malaysian Ringgit'], ['MVR', 'Rufiyaa'], ['MRO', 'Ouguiya'], ['MUR', 'Mauritius Rupee'], ['XUA', 'ADB Unit of Account'], ['MXN', 'Mexican Peso'], ['MXV', 'Mexican Unidad de Inversion (UDI)'], ['MDL', 'Moldovan Leu'], ['MNT', 'Tugrik'], ['MAD', 'Moroccan Dirham'], ['MZN', 'Mozambique Metical'], ['MMK', 'Kyat'], ['NAD', 'Namibia Dollar'], ['NPR', 'Nepalese Rupee'], ['NIO', 'Cordoba Oro'], ['NGN', 'Naira'], ['OMR', 'Rial Omani'], ['PKR', 'Pakistan Rupee'], ['PAB', 'Balboa'], ['PGK', 'Kina'], ['PYG', 'Guarani'], ['PEN', 'Sol'], ['PHP', 'Philippine Peso'], ['PLN', 'Zloty'], ['QAR', 'Qatari Rial'], ['RON', 'Romanian Leu'], ['RUB', 'Russian Ruble'], ['RWF', 'Rwanda Franc'], ['SHP', 'Saint Helena Pound'], ['WST', 'Tala'], ['STD', 'Dobra'], ['SAR', 'Saudi Riyal'], ['RSD', 'Serbian Dinar'], ['SCR', 'Seychelles Rupee'], ['SLL', 'Leone'], ['SGD', 'Singapore Dollar'], ['XSU', 'Sucre'], ['SBD', 'Solomon Islands Dollar'], ['SOS', 'Somali Shilling'], ['SSP', 'South Sudanese Pound'], ['LKR', 'Sri Lanka Rupee'], ['SDG', 'Sudanese Pound'], ['SRD', 'Surinam Dollar'], ['SZL', 'Lilangeni'], ['SEK', 'Swedish Krona'], ['CHE', 'WIR Euro'], ['CHW', 'WIR Franc'], ['SYP', 'Syrian Pound'], ['TWD', 'New Taiwan Dollar'], ['TJS', 'Somoni'], ['TZS', 'Tanzanian Shilling'], ['THB', 'Baht'], ['TOP', 'Pa\u2019anga'], ['TTD', 'Trinidad and Tobago Dollar'], ['TND', 'Tunisian Dinar'], ['TRY', 'Turkish Lira'], ['TMT', 'Turkmenistan New Manat'], ['UGX', 'Uganda Shilling'], ['UAH', 'Hryvnia'], ['AED', 'UAE Dirham'], ['USN', 'US Dollar (Next day)'], ['UYU', 'Peso Uruguayo'], ['UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'], ['UZS', 'Uzbekistan Sum'], ['VUV', 'Vatu'], ['VEF', 'Bol\xedvar'], ['VND', 'Dong'], ['YER', 'Yemeni Rial'], ['ZMW', 'Zambian Kwacha'], ['ZWL', 'Zimbabwe Dollar'], ['XBA', 'Bond Markets Unit European Composite Unit (EURCO)'], ['XBB', 'Bond Markets Unit European Monetary Unit (E.M.U.-6)'], ['XBC', 'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'], ['XBD,', 'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'], ['XTS', 'Codes specifically reserved for testing purposes'], ['XXX', 'The codes assigned for transactions where no currency is involved'], ['XAU', 'Gold'], ['XPD', 'Palladium'], ['XPT', 'Platinum'], ['XAG', 'Silver']])),
                ('accommodation_payment_way', models.CharField(default=b'NON', max_length=5, choices=[['NON', '\u038c\u03c7\u03b9 \u03b1\u03ba\u03cc\u03bc\u03b7'], ['AGNT', '\u03a0\u03c1\u03b1\u03ba\u03c4\u03bf\u03c1\u03b5\u03af\u03bf'], ['GRNET', 'VISA \u0395\u0394\u0395\u03a4'], ['VISA', '\u03a0\u03b9\u03c3\u03c4\u03c9\u03c4\u03b9\u03ba\u03ae \u039c\u03b5\u03c4/\u03bd\u03bf\u03c5']])),
                ('accommodation_payment_description', models.CharField(max_length=200, null=True)),
                ('transportation_cost', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('transportation_default_currency', models.CharField(default=b'EUR', max_length=3)),
                ('transportation_payment_way', models.CharField(default=b'NON', max_length=5, choices=[['NON', '\u038c\u03c7\u03b9 \u03b1\u03ba\u03cc\u03bc\u03b7'], ['AGNT', '\u03a0\u03c1\u03b1\u03ba\u03c4\u03bf\u03c1\u03b5\u03af\u03bf'], ['GRNET', 'VISA \u0395\u0394\u0395\u03a4'], ['VISA', '\u03a0\u03b9\u03c3\u03c4\u03c9\u03c4\u03b9\u03ba\u03ae \u039c\u03b5\u03c4/\u03bd\u03bf\u03c5']])),
                ('transportation_payment_description', models.CharField(max_length=200, null=True)),
                ('depart_date', models.DateTimeField(null=True, validators=[texpenses.validators.date_validator])),
                ('return_date', models.DateTimeField(null=True, validators=[texpenses.validators.date_validator])),
                ('means_of_transport', models.CharField(default=b'AIR', max_length=10, choices=[['B\u0399\u039a\u0395', '\u039c\u03b7\u03c7\u03b1\u03bd\u03ae'], ['TR\u0391\u0399\u039d', '\u03a4\u03c1\u03b1\u03af\u03bd\u03bf'], ['SHIP', '\u039a\u03b1\u03c1\u03ac\u03b2\u03b9'], ['AIR', '\u0391\u03b5\u03c1\u03bf\u03c0\u03bb\u03ac\u03bd\u03bf'], ['CAR', '\u0391\u03c5\u03c4\u03bf\u03ba\u03af\u03bd\u03b7\u03c4\u03bf']])),
                ('transport_days_manual', models.PositiveSmallIntegerField(default=0)),
                ('overnights_num_manual', models.PositiveSmallIntegerField(default=0)),
                ('compensation_days_manual', models.PositiveSmallIntegerField(default=0)),
                ('meals', models.CharField(default=b'NON', max_length=10, choices=[['FULL', '\u03a0\u03bb\u03ae\u03c1\u03b7\u03c2 \u03b4\u03b9\u03b1\u03c4\u03c1\u03bf\u03c6\u03ae'], ['SEMI', '\u0397\u03bc\u03b9\u03b4\u03b9\u03b1\u03c4\u03c1\u03cc\u03c6\u03b7'], ['NON', '\u039a\u03b1\u03b8\u03cc\u03bb\u03bf\u03c5'], ['BRKF', 'Breakfast']])),
                ('arrival_point', models.ForeignKey(related_name=b'travel_arrival_point', blank=True, to='texpenses.City', null=True)),
                ('departure_point', models.ForeignKey(related_name=b'travel_departure_point', blank=True, to='texpenses.City', null=True)),
                ('travel_petition', models.ForeignKey(to='texpenses.Petition')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='petition',
            name='project',
            field=models.ForeignKey(to='texpenses.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='petition',
            name='tax_office',
            field=models.ForeignKey(to='texpenses.TaxOffice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='petition',
            name='travel_info',
            field=models.ManyToManyField(to='texpenses.TravelInfo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='petition',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='texpenses.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tax_office',
            field=models.ForeignKey(to='texpenses.TaxOffice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SecretaryCompensation',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.petition',),
        ),
        migrations.CreateModel(
            name='SecretaryPetition',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.petition',),
        ),
        migrations.CreateModel(
            name='SecretaryPetitionSubmission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.petition',),
        ),
        migrations.CreateModel(
            name='TravelInfoCompensation',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.travelinfo',),
        ),
        migrations.CreateModel(
            name='TravelInfoSecretarySubmission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.travelinfo',),
        ),
        migrations.CreateModel(
            name='TravelInfoUserSubmission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.travelinfo',),
        ),
        migrations.CreateModel(
            name='UserCompensation',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.petition',),
        ),
        migrations.CreateModel(
            name='UserPetition',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.petition',),
        ),
        migrations.CreateModel(
            name='UserPetitionSubmission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.petition',),
        ),
    ]
