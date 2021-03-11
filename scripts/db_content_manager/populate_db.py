import json
import string
import random
import traceback
import pandas as pd
import pytz

from decimal import Decimal
from dataclasses import asdict

from typing import Tuple, List, Callable
from dateutil import tz

from django.utils import timezone
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.db import models

from app_zero.models import *


from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.domain.trader.models import Trader, TraderLicense

from mtrade.domain.market.order_group.models import OrderGroup, OrderGroupFactory
from mtrade.domain.security.models import SecurityIssuer, Security, SecurityFactory, SecurityIssuerFactory


from mtrade.settings import TIME_ZONE
pd.options.display.max_columns = 500

# timezone aware datetime iso format
tz_aware_datetime_iso_format = "%Y-%m-%dT%H:%M:%S%z"

User = get_user_model()


def create_data_template() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = ''
    data = dict()
    return data


def random_date(start, end):
    """
    Returns a random datetime between two datetime objects. Precision is in seconds
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def create_random_string(n=12, only_numbers=False):
    """
    Creates a random string
    """
    if only_numbers:
        return ''.join(random.choice([str(i) for i in range(9)]) for i in range(n))

    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))


def create_random_datetime(start: str, end: str, format: str = '%d/%m/%Y %I:%M %p'):
    """
    Description
    ----------
    Creates a random datetime between provided start and end datetimes. Precision is in seconds.

    Arguments
    ---------
    start: str
        Start datetime with format '%d/%m/%Y %I:%M %p' -- example: '20/1/2008 1:30 PM'
    end: str
        End datetime with format '%d/%m/%Y %I:%M %p' -- example: '20/1/2008 1:30 PM'
    format: str
        Format for string-parsing datetimes. Has default value
    """
    start = datetime.strptime(start, format)
    # localize naive start datetime object
    start = pytz.utc.localize(start)
    end = datetime.strptime(end, format)
    # localize naive end datetime object
    end = pytz.utc.localize(end)
    delta = end - start
    # get number of seconds in interval
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def create_random_price(return_type='str'):
    """
    Returns a random price between reasonable boundaries
    @args:
        return_type: 'str' | 'number'
    """
    value = round(random.random()*10 + 95, 4)
    if return_type == 'str':
        return str(value)
    if return_type == 'number':
        return value


def create_random_spread(return_type='str'):
    """
    Returns a random price between reasonable boundaries
    @args:
        return_type: 'str' | 'number'
    """
    value = round(150 + random.random()*100, 4)
    if return_type == 'str':
        return str(value)
    if return_type == 'number':
        return value


def create_random_dm():
    """Creates a random discount margin"""
    return str(round(random.random(), 4))


def create_random_yield(return_type='str'):
    """
    Returns a random yield between reasonable boundaries
    @args:
        return_type: 'str' | 'number'
    """
    value = round(0.08 + random.random()*0.03, 4)
    if return_type == 'str':
        return str(value)
    if return_type == 'number':
        return value


def create_random_number_of_securities():
    return random.randint(0, 10000000)


def select_random_fk_reference(Model: models.Model, return_type='model_instance'):
    """
    Description
    -----
    Creates a reference to an instance of provided model

    Arguments
    ----
    Model:
        a model class from which selection is to be performed
    return_type: str
        model_instance -> if return value is a models.Model instance
        uuid -> if return value is a uuid.uuid4 instance



    """
    count = Model.objects.all().count()
    random_index = random.randint(0, count-1)
    instance = Model.objects.all()[random_index]

    if return_type == 'model_instance':
        return instance
    elif return_type == 'uuid':
        return instance.id
    else:
        print('Provided return_type is incorrect')


def select_random_model_choice(choices: List[Tuple], many=False):
    if many:
        num_returned = random.randint(1, len(choices))
        return [i[0] for i in random.choices(choices, k=num_returned)]
    return random.choice(choices)[0]


def create_instances(n: int, create_new_instance: Callable, Model: models.Model, manage_validation_and_saving=True) -> int:
    """
    A loop for automatizing entity creation

    Arguments
    ----
    n:
        number of iterations for loop

    create_new_instance:
        a function in charge of creating a new instance. If it does not manage model saving and validation, it must return the instance to be validated

    Model:
        models.Model instance

    manage_validation_and_saving:
        if True, model data validation and saving is handled in this function. if False, it is assumed that these processes are handled in create_new_instance callable
    """
    num_created = 0
    for _ in range(n):
        try:

            if manage_validation_and_saving:
                new_instance = create_new_instance()
                new_instance.full_clean()
                new_instance.save()
            else:
                # don't manage validation and saving (this is already handles in provided create_new_instance) function
                create_validate_and_save_new_instance = create_new_instance
                create_validate_and_save_new_instance()

            num_created += 1
        except Exception as e:
            print(
                f'There was a problem while trying to create a {Model.__name__} instance -- {e.args}')
            traceback.print_exc()

    print(
        f'{num_created} of {n} {Model.__name__} instances were created')


"""             MAIN MODEL INSTANCE GENERATORS     """


def create_adress_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = Address

    random_str = create_random_string()
    data = dict(
        address=f"Street {random_str}",
        country=f"Country {random_str}",
        state=f"State {random_str}",
        municipality=f"Municipality {random_str}",
        zip_code=create_random_string(n=6, only_numbers=True)
    )

    return data


def create_addresses(n: int = 5):
    """
    Creates sprecified instances 

    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = Address

    def create_new_instance():

        data = create_adress_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_file_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = File

    random_str = create_random_string()
    data = dict(
        location=f"https://www.files.com/{random_str}"
    )

    return data


def create_files(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = File

    def create_new_instance():
        data = create_file_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_user_settings_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = UserSettings

    random_str = create_random_string()
    data = dict(
        timezone='Test time zone',
        date_format='Test date format',
        language='Test language',
        theme_preferences={'key': 'this is a theme preference'}
    )

    return data


def create_user_settings(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = UserSettings

    def create_new_instance():
        data = create_user_settings_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


# def create_user_data() -> dict:
#     """
#     Returns a dict to be used in instance creation or for testing purposes
#     """
#     Model = User

#     random_str = create_random_string()
#     data = dict(
#         first_name=f'Name {random_str}',
#         second_name=f'Second Name {random_str}',
#         last_name=f'Last Name {random_str}',
#         password=make_password(f'password'),
#         email=f"email_{random_str}" + "@mail.com",
#         image=select_random_fk_reference(File),
#         telephone='55555555',
#         cell_phone='55555555',
#         rfc=f'RFC {random_str}',
#         curp=f'CURP {random_str}',
#         address=select_random_fk_reference(Address),
#         status=select_random_model_choice(Model.STATUS_CHOICES),
#         mfa_method=select_random_model_choice(Model.MFA_METHOD_CHOICES),
#         settings=select_random_fk_reference(UserSettings)
#     )

#     return data

# we defined a large number of possible users. Must be sufficient
_users_gen = (i for i in range(1000))


def create_user_data(test_word=None):
    """
    Returns a dict to be used in instance creation or for testing purposes

    If test_word (str) is provided. It will create a user with credentials `username_<test_word>`
    ans password `password_<test_word>`

    Note: provide test_word argument is recommended in case where a single instance is being created for testing purposes
    """
    num_user = next(_users_gen) + 1
    personal_data = asdict(UserPersonalData(
        username=f"username_{num_user}",
        first_name=f"Name {num_user}",
        last_name=f"Last Name {num_user}",
        email=f"email_{num_user}@example.com"
    ))
    base_permissions = asdict(UserBasePermissions(
        is_staff=False,
        is_active=False
    ))

    password = make_password(f'password_{num_user}')

    additional_data = dict(id=uuid.uuid4(), password=password,

                           )
    data = dict()
    data.update(personal_data)
    data.update(base_permissions)
    data.update(additional_data)

    return data


def create_users(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = User

    def create_new_instance():
        data = create_user_data()
        user = User.objects.create_user(**data)
        user.save()

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model, manage_validation_and_saving=False)


def create_instituion_manager_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = InstitutionManager
    data = dict(user=select_random_fk_reference(User, return_type='uuid'))
    return data


def create_institution_managers(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = InstitutionManager

    def create_new_instance():
        data = create_instituion_manager_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_controller_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = Controller
    data = dict(user=select_random_fk_reference(User, return_type='uuid'))
    return data


def create_controllers(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = Controller

    def create_new_instance():
        data = create_controller_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_compliance_officer_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = ComplianceOfficer
    random_str = create_random_string()
    data = dict(first_name=f"Name {random_str}",
                last_name=f"Last Name {random_str}",
                telephone=f"{create_random_string(n=10, only_numbers=True)}",
                email=f"{random_str}@mail.com")
    return data


def create_compliance_officers(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = ComplianceOfficer

    def create_new_instance():
        data = create_compliance_officer_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_institution_leads_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = InstitutionLead
    random_str = create_random_string()
    data = dict(contract=select_random_fk_reference(File),
                rfc=f"RFC {random_str}",
                logo=select_random_fk_reference(File),
                contact_user=select_random_fk_reference(
                    User, return_type='uuid'),
                status=select_random_model_choice(Model.STATUS_CHOICES),
                compliance_officer=select_random_fk_reference(
                    ComplianceOfficer),
                address=select_random_fk_reference(Address))
    return data


def create_institution_leads(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = InstitutionLead

    def create_new_instance():

        data = create_institution_leads_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_institution_data():
    """
    No test data here yet.
    """
    pass


def create_institutions():
    """
    Creates institutions
    """
    Model = Institution

    # NOTE: the following data will be externally provided
    institution_data = [
        {"name": "BBVA"},
        {"name": "Scotiabank"},
        {"name": "Actinver"},
        {"name": "Banamex"},
        {"name": "HSBC"},
        {"name": "Santancer"}
    ]

    institution_gen = (i for i in institution_data)

    n = len(institution_data)

    def create_new_instance():
        random_str = create_random_string()
        inst_data = next(institution_gen)

        new_instance = Model(
            name=inst_data["name"],
            contract=select_random_fk_reference(File),
            rfc=f"RFC {random_str}",
            logo=select_random_fk_reference(File),
            manager=select_random_fk_reference(InstitutionManager),
            status=select_random_model_choice(Model.STATUS_CHOICES),
            license_type=select_random_model_choice(
                Model.LICENSE_TYPE_CHOICES, many=True),
            demo_licenses=random.randint(0, 5),
            trade_licenses=random.randint(0, 5),
            data_licenses=random.randint(0, 5),
            curp=f"CURP {random_str}",
            compliance_officer=select_random_fk_reference(ComplianceOfficer),
            address=select_random_fk_reference(Address)
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_trader_licenses():
    """
    Creates trader licenses
    """

    Model = TraderLicense

    licenses = [
        dict(
            id=uuid.uuid4(),
            name='analyst',
            short_description='Analyst license. May only view'
        ),
        dict(
            id=uuid.uuid4(),
            name='trading',
            short_description='Trading license. May trade.'
        ),
        dict(
            id=uuid.uuid4(),
            name='demo',
            short_description='Demo license. May only view'
        )
    ]

    license_gen = (i for i in licenses)

    n = len(licenses)

    def create_new_instance():
        data = next(license_gen)
        new_instance = Model(**data)
        return new_instance

    create_instances(n=n, create_new_instance=create_new_instance, Model=Model)


# def create_trader_data() -> dict:
#     """
#     Returns a dict to be used in instance creation or for testing purposes
#     """
#     # user = next(_trader_gen)
#     # data = dict(
#     #     id=user.id,
#     #     license=select_random_fk_reference(TraderLicense),
#     #     institution=select_random_fk_reference(
#     #         Institution, return_type='uuid')
#     # )
#     return data


def create_traders():
    """
    Creates traders. One per user. 
    TODO: (optional) update so not all users have a trader profile associated
    """
    Model = Trader
    users_for_trader_gen = User.objects.all()
    trader_gen = (i for i in users_for_trader_gen)

    def create_new_instance():
        user = next(trader_gen)
        data = dict(
            id=user.id,
            license=select_random_fk_reference(TraderLicense),
            institution_id=select_random_fk_reference(
                Institution, return_type='uuid')
        )

        new_instance = Model(**data)

        return new_instance

    n = len(users_for_trader_gen)

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_contact_person_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = ContactPerson
    random_str = create_random_string()
    data = dict(first_name=f"Name {random_str}",
                last_name=f"Last Name {random_str}",
                telephone=f"{create_random_string(n=10, only_numbers=True)}",
                email=f"{random_str}@mail.com")
    return data


def create_contact_persons(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = ContactPerson

    def create_new_instance():
        data = create_contact_person_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_lead_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = Lead
    random_str = create_random_string()
    data = dict(institution_lead=select_random_fk_reference(InstitutionLead),
                institution=select_random_fk_reference(Institution),
                contact_person=select_random_fk_reference(ContactPerson),
                comments='This is a comment.')
    return data


def create_leads(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = Lead

    def create_new_instance():
        data = create_lead_data()
        new_instance = Model(**data)

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_concierges(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = Concierge

    def create_new_instance():
        random_str = create_random_string()
        new_instance = Model(
            user=select_random_fk_reference(User, return_type='uuid'),
        )
        new_instance.full_clean()
        new_instance.save()
        # add a random number of institutions to concierge
        for i in range(random.randint(0, 6)):
            new_instance.institutions.add(
                select_random_fk_reference(Institution))

        # add a random number of institution leads to concierge
        for i in range(random.randint(0, 6)):
            new_instance.leads.add(select_random_fk_reference(Lead))

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model, manage_validation_and_saving=False)


def create_security_issuers():
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = SecurityIssuer

    security_issuers_data = [
        dict(name='Issuer 1'),
        dict(name='Issuer 2'),
        dict(name='Issuer 3')

    ]

    security_issuers_gen = (i for i in security_issuers_data)

    n = len(security_issuers_data)

    def create_new_instance():
        random_str = create_random_string()
        security_issuer_data = next(security_issuers_gen)

        security_issuer = SecurityIssuerFactory.build_entity(
            **security_issuer_data)
        security_issuer.save()

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model, manage_validation_and_saving=False)


def create_securities():

    Model = Security

    PATH_TO_INPUT_DATA = "scripts/db_content_manager/db_input_data"
    # path to file with security info (except amortization schemes, that will be in a separate file)
    path_to_general_info = f'{PATH_TO_INPUT_DATA}/securities_structural_data.csv'
    # path to excel with amortization schemes info for each security
    path_to_amort_scheme = f'{PATH_TO_INPUT_DATA}/amortization_schemes.xlsx'

    def format_column_to_iso(column):
        """
        given a date string with format "%m/%d/%Y", this method returns a time aware iso format string
        """
        return column.map(lambda x: datetime.
                          strptime(x, "%m/%d/%Y")
                          .replace(tzinfo=tz.gettz(TIME_ZONE))
                          .isoformat())

    try:
        # get general security info
        _data = pd.read_csv(path_to_general_info, index_col='isin')
        # convert data structuress
        _data.issue_date = format_column_to_iso(_data.issue_date)
        _data.first_coupon_date = format_column_to_iso(_data.first_coupon_date)
        _data.final_maturity_date = format_column_to_iso(
            _data.final_maturity_date)

        # print('Resulting dataframe for security:')
        # print(_data)

        data = _data.T.to_dict()

        # assign amortization structures for each security (from amort_schemes excel)
        for isin, content in data.items():
            amort_scheme = pd.read_excel(path_to_amort_scheme, sheet_name=isin)
            amort_scheme.date = amort_scheme.date.map(
                lambda x: datetime.strftime(x, '%d/%m/%Y'))
            amort_scheme_dict = amort_scheme.T.to_dict()
            content['amortization_scheme'] = amort_scheme_dict

    except Exception:
        logger.error('There was a problem importing security data')
        raise Exception

    security_gen = (i for i in data.items())

    def create_new_instance():
        isin, content = next(security_gen)

        def create_security_name():
            ticker = f"{content['ticker']}"
            coupon = f"{round(content['coupon_rate']*100, 2)}%"
            maturity_date = datetime.strptime(
                content['final_maturity_date'], tz_aware_datetime_iso_format)
            maturity_year = maturity_date.year
            # string format month (short name)
            maturity_month = maturity_date.strftime("%b")
            maturity_day = f"{maturity_date.day:02d}"
            return f"{ticker}  {coupon}  {maturity_day}/{maturity_month}/{maturity_year}"

        random_str = create_random_string(n=12)

        security_data = dict(
            isin=isin,
            name=create_security_name(),
            ticker=str(content["ticker"]),
            series=f'Series {random_str}',
            issuer=select_random_fk_reference(SecurityIssuer),
            registration=select_random_model_choice(
                Model.REGISTRATION_CHOICES),
            classification_mx='Classification mx',
            amortization_scheme=content['amortization_scheme'],
            coupon_rate=str(content['coupon_rate']),
            initial_margin=str(round(200 + random.random()*150, 4)),
            issue_date=content['issue_date'],
            first_coupon_date=content['first_coupon_date'],
            final_maturity_date=content['final_maturity_date'],
            nominal_value=str(content['nominal_value']),
            year_day_count=str(content['year_day_count']),
            redemption_price='100',
            redemption_type=select_random_model_choice(
                Model.REDEMPTION_TYPE_CHOICES),
            security_notes='TEST Issued Int. under 144a/RegS',
            number_of_payments=str(random.randint(0, 50)),
            issued_amount=str(content['issued_amount']),
            outstanding=str(content['outstanding']),
            category=select_random_model_choice(Model.CATEGORY_CHOICES),
            listing=select_random_model_choice(
                Model.LISTING_CHOICES, many=True),
            clearing=select_random_model_choice(
                Model.CLEARING_CHOICES, many=True),
            amortization_structure=content['amortization_structure'],
            coupon_period=content['coupon_period'],
            day_count_convention=Model.DAY_COUNT_CONVENTION_MX_ACT_360,
            currency_risk=content['currency_risk'],
            currency_of_payments=content['currency_of_payments'],
            security_type=Model.TYPE_M_BONO,
            seniority=Model.SENIOR_SENIORITY,
            guarantee=Model.GUARANTEE_SECURED

        )

        security = SecurityFactory.build_entity(**security_data)
        security.save()

    n = len(data)

    create_instances(n=n, create_new_instance=create_new_instance, Model=Model,
                     manage_validation_and_saving=False)


def create_settlement_instructions(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = SettlementInstruction

    def create_new_instance():
        random_str = create_random_string()
        new_instance = Model(
            name=f'Settlement {random_str}',
            document=select_random_fk_reference(File),
            clearing_house=select_random_model_choice(Model.CLEARING_CHOICES),
            account=f'Account {random_str}',
            bic_code=f'Bic Code {random_str}',
            custodian=f'Custodian {random_str}',
            institution=select_random_fk_reference(Institution),
            trader=select_random_fk_reference(Trader, return_type='uuid'),
            status=select_random_model_choice(Model.STATUS_CHOICES)
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_alarms(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = Alarm

    def create_new_instance():
        random_str = create_random_string()
        new_instance = Model(
            alarm_type=select_random_model_choice(Model.TYPE_CHOICES),
            value='100',
            security=select_random_fk_reference(Security, return_type='uuid')
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_order_group_data() -> dict:
    """
    Returns a dict to be used in instance creation or for testing purposes
    """
    Model = OrderGroup

    volume = create_random_number_of_securities()
    price = create_random_price(return_type='number')
    yield_value = create_random_yield()
    notional = str(volume * price)
    spread = create_random_spread()
    submission = create_random_datetime(
        '20/1/2020 1:30 PM', '20/5/2020 1:30 PM')
    expiration = create_random_datetime(
        '20/5/2021 1:30 PM', '20/6/2021 1:30 PM')
    data = dict(
        security=select_random_fk_reference(
            Security, return_type='uuid'),
        orderbook=select_random_model_choice(Model.ORDERBOOK_CHOICES),
        order_type=select_random_model_choice(Model.ORDER_TYPE_CHOICES),
        direction=select_random_model_choice(Model.DIRECTION_CHOICES),
        volume=volume,
        notional=notional,
        weighted_avg_price=Decimal(str(price)),
        weighted_avg_yield=Decimal(str(yield_value)),
        weighted_avg_spread=Decimal(spread),
        fx=Decimal(str(random.random()*10 + 15)),
        status=select_random_model_choice(Model.STATUS_CHOICES),
        submission=submission,
        expiration=expiration,
        allocation_pct=Decimal(str(random.random())),
        responded_by=select_random_model_choice(
            Model.RESPONDED_BY_CHOICES),
        settlement_currency=select_random_model_choice(
            Model.CURRENCY_CHOICES),
        requestor_type=select_random_model_choice(
            Model.REQUESTOR_TYPE_CHOICES),
        requestor=select_random_fk_reference(
            Institution, return_type='uuid'),
        resp_received=random.randint(0, 10),
        trader=select_random_fk_reference(Trader, return_type='uuid'),
        priority=create_random_datetime(
            '20/1/2021 1:30 PM', '20/4/2021 1:30 PM')
    )

    return data


def create_order_groups(n: int = 5):
    """
    Creates sprecified instances 

    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = OrderGroup

    def create_new_instance():
        data = create_order_group_data()
        order_group = OrderGroupFactory.build_entity(**data)
        order_group.save()

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model, manage_validation_and_saving=False)


def create_cob_orders(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of cob orders to be created
    """
    Model = CobOrder

    def create_new_instance():
        submission = create_random_datetime(
            '20/1/2015 1:30 PM', '20/1/2020 1:30 PM')
        volume = create_random_number_of_securities()
        price = create_random_price()
        dirty_price = float(price) + 1.1

        new_instance = Model(
            trader=select_random_fk_reference(Trader, return_type='uuid'),
            security=select_random_fk_reference(Security, return_type='uuid'),
            submission=submission,
            expiration=create_random_datetime(
                '20/1/2020 1:30 PM', '20/3/2021 1:30 PM'),
            volume=volume,
            status=select_random_model_choice(Model.STATUS_CHOICES),
            dirty_price=Decimal(str(dirty_price)),
            notional=Decimal(str(float(volume) * float(dirty_price))),
            price=price,
            spread=create_random_spread(),
            discount_margin=create_random_dm(),
            yield_value=create_random_yield(),
            direction=select_random_model_choice(Model.DIRECTION_CHOICES),
            order_group=select_random_fk_reference(
                OrderGroup, return_type='uuid')
        )
        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_cob_auto_refreshers(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = CobAutoRefresher

    def create_new_instance():
        new_instance = Model(
            cob_order=select_random_fk_reference(CobOrder),
            autorefresh_type=select_random_model_choice(Model.TYPE_CHOICES),
            interval=2400
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_cob_streams(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = CobStream

    def create_new_instance():
        random_str = create_random_string()
        new_instance = Model(
            cob_order=select_random_fk_reference(CobOrder),
            status=select_random_model_choice(Model.STATUS_CHOICES),
            order_group=select_random_fk_reference(
                OrderGroup, return_type='uuid')
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_rfqs(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = Rfq

    def create_new_instance():
        submission = create_random_datetime(
            '20/1/2021 1:30 PM', '20/3/2021 1:30 PM')
        new_instance = Model(
            security=select_random_fk_reference(Security, return_type='uuid'),
            trader=select_random_fk_reference(Trader, return_type='uuid'),
            anonymous=random.choice([True, False]),
            public=random.choice([True, False]),
            submission=submission,
            expiration=create_random_datetime(
                '20/3/2021 1:30 PM', '20/4/2021 1:30 PM'),
            status=select_random_model_choice(Model.STATUS_CHOICES),
            direction=select_random_model_choice(Model.DIRECTION_CHOICES),
            volume=create_random_number_of_securities(),
            settlement_currency=Model.MXN_CURRENCY,
            order_group=select_random_fk_reference(
                OrderGroup, return_type='uuid')
        )
        new_instance.full_clean()
        new_instance.save()
        for _ in range(random.randint(0, 4)):
            new_instance.counterparties.add(
                select_random_fk_reference(Institution))
        new_instance.save()

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model, manage_validation_and_saving=False)


def create_rfq_responses(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of cob orders to be created
    """
    Model = RfqResponse

    def create_new_instance():
        price = create_random_price(return_type='number')
        _yield = create_random_yield(return_type='number')
        spread = create_random_spread(return_type='number')
        dm = create_random_dm()
        submission_datetime = create_random_datetime(
            '20/1/2015 1:30 PM', '20/1/2020 1:30 PM')
        bid_price = price
        ask_price = price + random.random()*2
        ask_volume = create_random_number_of_securities()
        bid_volume = create_random_number_of_securities()

        new_instance = Model(
            trader=select_random_fk_reference(Trader, return_type='uuid'),
            submission=submission_datetime,
            rfq=select_random_fk_reference(Rfq),
            status=select_random_model_choice(Model.STATUS_CHOICES),
            bid_price=Decimal(str(bid_price)),
            bid_yield=Decimal(str(_yield)),
            bid_spread=Decimal(str(spread)),
            bid_notional=Decimal(str(bid_price*bid_volume)),
            bid_discount_margin=Decimal(str(dm)),
            bid_volume=bid_volume,
            bid_fx='1',
            ask_price=Decimal(str(ask_price)),
            ask_yield=Decimal(str(_yield + random.random()*0.01)),
            ask_spread=Decimal(str(spread + random.random()*30)),
            ask_notional=Decimal(str(ask_price*ask_volume)),
            ask_discount_margin=Decimal(str(dm)),
            ask_fx='1',
            ask_volume=ask_volume,
            autoresponded=random.choice([False, True])
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_rfq_auto_responders(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = RfqAutoResponder

    def create_new_instance():
        min_volume = create_random_number_of_securities()
        random_str = create_random_string()
        ask_price = create_random_price(return_type='number')
        ask_spread = create_random_spread(return_type='number')
        ask_fx = 1
        ask_notional = ask_price*min_volume

        new_instance = Model(
            security=select_random_fk_reference(Security, return_type='uuid'),
            trader=select_random_fk_reference(Trader, return_type='uuid'),
            min_volume=min_volume,
            max_volume=min_volume + random.randint(100, 1000000),
            public=random.choice([False, True]),
            settlement_currency=Model.MXN_CURRENCY,
            ask_price=Decimal(str(ask_price)),
            ask_spread=Decimal(str(ask_spread)),
            ask_fx=Decimal(str(ask_fx)),
            ask_notional=Decimal(str(ask_notional)),
            bid_price=Decimal(str(ask_price+random.random())),
            bid_spread=Decimal(str(ask_spread - random.random()*0.002)),
            bid_fx=Decimal(str(ask_fx)),
            bid_notional=Decimal(str(ask_notional)),
            status=select_random_model_choice(Model.STATUS_CHOICES),
            priority=create_random_datetime(
                '20/1/2021 1:30 PM', '20/4/2021 1:30 PM')
        )

        new_instance.full_clean()
        new_instance.save()
        for _ in range(random.randint(1, 5)):
            new_instance.counterparties.add(
                select_random_fk_reference(Institution))
        new_instance.save()

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model, manage_validation_and_saving=False)


def create_rfq_locks(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of cob orders to be created
    """
    Model = RfqLock

    def create_new_instance():
        trader = select_random_fk_reference(Trader)
        new_instance = Model(
            status=select_random_model_choice(Model.STATUS_CHOICES),
            trader=trader.id,
            institution=Institution.objects.get(id=trader.institution_id)
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_cob_transactions(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of cob orders to be created
    """
    Model = CobTransaction

    def create_new_instance():
        execution_datetime = create_random_datetime(
            '20/1/2021 1:30 PM', '20/4/2021 1:30 PM')
        price = create_random_price(return_type='number')
        dirty_price = price * (1 + random.random() * 0.1)
        volume = random.randint(1, 10000)
        notional = volume * 100
        cash_amount = volume * dirty_price
        vat = notional * 0.007
        yield_value = create_random_yield()

        new_instance = Model(
            buyer=select_random_fk_reference(Trader, return_type='uuid'),
            seller=select_random_fk_reference(Trader, return_type='uuid'),
            security=select_random_fk_reference(Security, return_type='uuid'),
            volume=Decimal(str(volume)),
            notional=Decimal(str(notional)),
            accrued_interest='0.002',
            price=Decimal(str(price)),
            all_in_price=Decimal(str(price)),
            all_in_yield=yield_value,
            discount_margin=create_random_dm(),
            yield_value=yield_value,
            dirty_price=Decimal(str(dirty_price)),
            status=select_random_model_choice(Model.STATUS_CHOICES),
            fee_buyer='100',
            fee_seller='100',
            vat=Decimal(str(vat)),
            cash_amount=Decimal(str(cash_amount)),
            total_cash=Decimal(str(cash_amount + vat)),
            settlement_date=create_random_datetime(
                '20/4/2021 1:30 PM', '20/5/2021 1:30 PM'),
            settlement_currency=Model.MXN_CURRENCY,

            spread=create_random_spread(),
            buy_order=random.choice(
                CobOrder.objects.filter(direction='buy')),
            sell_order=random.choice(
                CobOrder.objects.filter(direction='sell')),
            created_at=execution_datetime,
            fx='1'
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_rfq_transactions(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of cob orders to be created
    """
    Model = RfqTransaction

    def create_new_instance():
        execution_datetime = create_random_datetime(
            '20/1/2021 1:30 PM', '20/4/2021 1:30 PM')
        price = create_random_price(return_type='number')
        dirty_price = price * (1 + random.random() * 0.1)
        volume = random.randint(1, 10000)
        cash_amount = volume * dirty_price
        notional = volume * 100

        vat = notional * 0.007
        yield_value = create_random_yield()

        new_instance = Model(
            buyer=select_random_fk_reference(Trader, return_type='uuid'),
            seller=select_random_fk_reference(Trader, return_type='uuid'),
            security=select_random_fk_reference(Security, return_type='uuid'),
            volume=Decimal((volume)),
            notional=Decimal(str(notional)),
            accrued_interest='0.002',
            price=Decimal(str(price)),
            all_in_price=Decimal(str(price)),
            all_in_yield=yield_value,
            discount_margin=create_random_dm(),
            yield_value=yield_value,
            dirty_price=Decimal(str(dirty_price)),
            status=select_random_model_choice(Model.STATUS_CHOICES),
            fee_buyer='100',
            fee_seller='100',
            vat=Decimal(str(vat)),
            cash_amount=Decimal(str(cash_amount)),
            total_cash=Decimal(str(cash_amount + vat)),
            settlement_date=create_random_datetime(
                '20/4/2021 1:30 PM', '20/5/2021 1:30 PM'),
            settlement_currency=Model.MXN_CURRENCY,
            rfq=select_random_fk_reference(Rfq),
            rfq_response=select_random_fk_reference(RfqResponse),
            created_at=execution_datetime,
            fx='1'
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_watchlists(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of instances to be created
    """
    Model = Watchlist
    random_str = create_random_string()

    def create_new_instance():
        random_str = create_random_string()
        new_instance = Model(
            trader=select_random_fk_reference(Trader, return_type='uuid'),
            name=f'Watchlist {random_str}',
            description='This is a watchlist',
            status=select_random_model_choice(Model.STATUS_CHOICES),
            securities=[
                select_random_fk_reference(Security, return_type='uuid'),
                select_random_fk_reference(Security, return_type='uuid'),
                select_random_fk_reference(Security, return_type='uuid')]
        )
        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def create_notifications(n: int = 5):
    """
    Arguments
    ----------
    n : int
        Number of cob orders to be created
    """
    Model = Notification

    def create_new_instance():
        trader = select_random_fk_reference(Trader, return_type='uuid'),
        new_instance = Model(
            notification_type=select_random_model_choice(Model.TYPE_CHOICES),
            body={"key": "this is a body"},
            status=select_random_model_choice(Model.STATUS_CHOICES),
            user=select_random_fk_reference(User, return_type='uuid')
        )

        return new_instance

    create_instances(
        n=n, create_new_instance=create_new_instance, Model=Model)


def run(interactive: bool = True):

    selected_option = 0

    while(selected_option != '9'):
        if interactive == True:
            print('\nWELCOME TO MTRADE SIMULATOR')
            selected_option = input('\nThe following processes will be executed:\
                                \n1. Create core models \
                                \n\nIf you want to abort execution and go back press 0 (zero); press any other key to execute described processes...')

            if (selected_option == '0'):
                break
        else:
            selected_option = '9'

        try:
            print('CREATING CORE MODELS')
            create_addresses(100)
            create_files(50)
            create_user_settings(50)
            create_users(2)
            create_institution_managers(10)
            create_controllers(10)

            create_compliance_officers(10)
            create_institution_leads(10)
            create_institutions()

            create_trader_licenses()
            create_traders()

            create_contact_persons(10)
            create_leads(10)
            create_concierges(10)
            create_security_issuers()
            create_securities()
            create_settlement_instructions(10)
            create_alarms(10)
            create_order_groups(20)
            create_cob_orders(20)
            create_cob_auto_refreshers(20)
            create_cob_streams(20)
            create_rfqs(20)
            create_rfq_responses(20)
            create_rfq_auto_responders(20)
            create_rfq_locks(20)
            create_cob_transactions(20)
            create_rfq_transactions(20)
            create_watchlists(20)
            create_notifications(20)
            break
        except Exception as e:
            traceback.print_exc()
            logger.error(f'ERR! -- {e}')

    print('Exiting dummy data generator...')
