import random
import re

from faker import Faker

from src.utils.obfuscation_methods.tokenise import tokenise

fake = Faker("en_GB")


pii_fields = {
    "name": fake.name(),
    "firstname": fake.first_name(),
    "lastname": fake.last_name(),
    "surname": fake.last_name(),
    "email": fake.email(),
    "emailaddress": fake.email(),
    "workemail": fake.email(),
    "gender": random.choices(
        ["F", "M", "T", "N"], [0.45, 0.45, 0.05, 0.05], k=1
    )[0],
    "age": lambda: random.randint(18, 66),
    "birthday": fake.date_of_birth(),
    "dateofbirth": fake.date_of_birth(),
    "dob": fake.date_of_birth(),
    "phone": fake.phone_number(),
    "mobile": fake.phone_number(),
    "landline": fake.phone_number(),
    "workphone": fake.phone_number(),
    "hometelephone": fake.phone_number(),
    "worktelephone": fake.phone_number(),
    "mobilephone": fake.phone_number(),
    "homephone": fake.phone_number(),
    "phonenumber": fake.phone_number(),
    "address": fake.address(),
    "housenumber": fake.building_number(),
    "homeaddress": fake.address(),
    "workaddress": fake.address(),
    "buildingnumber": fake.building_number(),
    "street": fake.street_address(),
    "streetaddress": fake.address(),
    "town": fake.city(),
    "city": fake.city(),
    "county": fake.county(),
    "postcode": fake.postcode(),
    "nin": fake.ssn(),
    "ssn": fake.ssn(),
    "ninumber": fake.ssn(),
    "nationalinsurancenumber": fake.ssn(),
    "socialsecuritynumber": fake.ssn(),
    "cardnumber": fake.credit_card_number(),
    "debitcard": fake.credit_card_number(),
    "creditcard": fake.credit_card_number(),
    "creditcardnumber": fake.credit_card_number(),
    "debitcardnumber": fake.credit_card_number(),
    "ip": fake.ipv4(),
    "ipaddress": fake.ipv4(),
    "cookieid": fake.uuid4(),
    "advertisingidentifier": fake.uuid4(),
    "mobilelocationdata": fake.location_on_land(),
    "locationdata": fake.location_on_land(),
}


def anonymise(field, options):
    """
    Returns an randomly generated value intended to be used as an obfuscation
    for a field in a data set.

    Args:
        field (string): The field to be obfuscated, used to look up an
            appropriate value in pii_fields.
        options (dict): A dictionary containing obfuscation options. If the key
            "token" is in options, then the value will be returned in the
            event that field is not found in pii_fields.

    Returns:
        str: A randomly generated value from pii_fields, or a token if a value
            is not found in pii_fields.
    """
    cleaned_field = re.sub(r"[ \-_]", "", field).lower()
    value = pii_fields.get(cleaned_field, tokenise(field, options))
    return value
