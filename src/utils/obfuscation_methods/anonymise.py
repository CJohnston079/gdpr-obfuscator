import random

from faker import Faker

faker = Faker("en_GB")


pii_fields = {
    "name": faker.name(),
    "firstname": faker.first_name(),
    "lastname": faker.last_name(),
    "surname": faker.last_name(),
    "email": faker.email(),
    "emailaddress": faker.email(),
    "gender": random.choice(["M", "F", "TG", "NB", "AG", "BI"]),
    "age": lambda: random.randint(18, 66),
    "birthday": faker.date_of_birth(),
    "dateofbirth": faker.date_of_birth(),
    "dob": faker.date_of_birth(),
    "phone": faker.phone_number(),
    "mobile": faker.phone_number(),
    "landline": faker.phone_number(),
    "workphone": faker.phone_number(),
    "hometelephone": faker.phone_number(),
    "worktelephone": faker.phone_number(),
    "mobilephone": faker.phone_number(),
    "homephone": faker.phone_number(),
    "phonenumber": faker.phone_number(),
    "address": faker.address(),
    "housenumber": faker.building_number(),
    "homeaddress": faker.address(),
    "workaddress": faker.address(),
    "buildingnumber": faker.building_number(),
    "street": faker.street_address(),
    "streetaddress": faker.address(),
    "town": faker.city(),
    "city": faker.city(),
    "county": faker.county(),
    "postcode": faker.postcode(),
    "nin": faker.ssn(),
    "ssn": faker.ssn(),
    "ninumber": faker.ssn(),
    "nationalinsurancenumber": faker.ssn(),
    "socialsecuritynumber": faker.ssn(),
    "cardnumber": faker.credit_card_number(),
    "debitcard": faker.credit_card_number(),
    "creditcard": faker.credit_card_number(),
    "creditcardnumber": faker.credit_card_number(),
    "debitcardnumber": faker.credit_card_number(),
    "ip": faker.ipv4(),
    "ipaddress": faker.ipv4(),
    "cookieid": faker.uuid4(),
    "advertisingidentifier": faker.uuid4(),
    "mobilelocationdata": faker.location_on_land(),
    "locationdata": faker.location_on_land(),
}


def anonymise(field, options):
    pass
