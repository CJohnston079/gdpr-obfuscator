from faker import Faker

fake = Faker("en_GB")


def generate_shallow_data(num_records=3):
    shallow_data = []
    obfuscated_shallow_data = []

    for _ in range(num_records):
        name = fake.name()
        age = str(fake.random_int(min=18, max=66))
        city = fake.city()

        shallow_data.append({"name": name, "age": age, "city": city})
        obfuscated_shallow_data.append(
            {"name": "***", "age": str(age), "city": city})

    return shallow_data, obfuscated_shallow_data


def generate_deep_data(num_records=3):
    deep_data = []
    obfuscated_deep_data = []

    for _ in range(num_records):
        name = fake.name()
        age = str(fake.random_int(min=18, max=66))
        city = fake.city()
        email_address = fake.email()
        phone_number = fake.phone_number()

        deep_data.append({
            "name": name,
            "age": age,
            "city": city,
            "contact": [{"email": email_address}, {"phone": phone_number}]
        })

        obfuscated_deep_data.append({
            "name": "***",
            "age": age,
            "city": city,
            "contact": [{"email": "***"}, {"phone": "***"}]
        })

    return deep_data, obfuscated_deep_data
