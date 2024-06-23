import random

from faker import Faker

fake = Faker("en_GB")


def generate_gender():
    genders = ["F", "M", "T", "FTM", "MTF", "N"]
    weights = [0.4, 0.4, 0.05, 0.05, 0.05, 0.05]
    gender = random.choices(genders, weights, k=1)[0]
    return gender


def generate_name(gender):
    if gender in ["F", "MTF"]:
        first_name = fake.first_name_female()
        middle_name = fake.first_name_female()
    elif gender in ["M", "FTM"]:
        first_name = fake.first_name_male()
        middle_name = fake.first_name_male()
    else:
        first_name = fake.first_name_nonbinary()
        middle_name = fake.first_name_nonbinary()

    return {
        "first": first_name,
        "middle": middle_name,
        "last": fake.last_name(),
    }


def generate_email(first_name, last_name):
    personal_user = f"{first_name}{random.randint(1, 999)}"
    work_user = f"{first_name[0]}.{last_name}"
    work_domain = fake.domain_word() + random.choice([".org.uk", ".com"])

    personal_email = f"{personal_user}@{fake.free_email_domain()}".lower()
    work_email = f"{work_user}@{work_domain}".lower()

    return {"personal": personal_email, "work": work_email}


def generate_person():
    gender = generate_gender()
    name = generate_name(gender)
    email = generate_email(name["first"], name["last"])
    person = {
        "gender": gender,
        "name": f'{name["first"]} {name["last"]}',
        "first_name": name["first"],
        "middle_name": name["middle"],
        "last_name": name["last"],
        "email_personal": email["personal"],
        "email_work": email["work"],
    }
    return person


def generate_pii():
    """
    Randomly generates a dictionary of PII (Personally Identifiable
    Information) fields.

    Returns:
        dict: a dictionary of PII fields containing random data.
    """
    person = generate_person()
    pii_fields = {
        "gender": person["gender"],
        "name": person["name"],
        "fullname": person["name"],
        "firstname": person["first_name"],
        "middlename": person["middle_name"],
        "lastname": person["last_name"],
        "surname": person["last_name"],
        "email": person["email_personal"],
        "emailaddress": person["email_personal"],
        "emailaddresswork": person["email_work"],
        "workemailaddress": person["email_work"],
        "workemail": person["email_work"],
        "age": random.randint(18, 66),
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
    return pii_fields
