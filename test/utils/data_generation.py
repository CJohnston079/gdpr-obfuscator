from faker import Faker

fake = Faker("en_GB")


def generate_data(*generate, num_records=3):
    data = {key: [] for key in generate}

    for _ in range(num_records):
        name = fake.name()
        age = str(fake.random_int(min=18, max=66))
        city = fake.city()
        email_address = fake.email()
        phone_number = fake.phone_number()

        for key in generate:
            if key == "shallow_list_based":
                entry = {"name": name, "age": age, "city": city}
            elif key == "shallow_list_based_obfuscated":
                entry = {"name": "***", "age": age, "city": city}
            elif key == "shallow_object_based":
                entry = {"person": {"name": name, "age": age, "city": city}}
            elif key == "shallow_object_based_obfuscated":
                entry = {"person": {"name": "***", "age": age, "city": city}}
            elif key == "deep_list_based":
                entry = {
                    "name": name,
                    "age": age,
                    "city": city,
                    "contact": [{"email": email_address}, {"phone": phone_number}]
                }
            elif key == "deep_list_based_obfuscated":
                entry = {
                    "name": "***",
                    "age": age,
                    "city": city,
                    "contact": [{"email": "***"}, {"phone": "***"}]
                }
            elif key == "deep_object_based":
                entry = {"person": {
                    "name": name,
                    "age": age,
                    "city": city,
                    "contact": {
                        "email": email_address,
                        "phone": phone_number
                    }
                }}
            elif key == "deep_object_based_obfuscated":
                entry = {"person": {
                    "name": "***",
                    "age": age,
                    "city": city,
                    "contact": {
                        "email": "***",
                        "phone": "***"
                    }
                }}
            elif key == "shallow_xml_str":
                entry = (
                    f"<person>"
                    f"<name>{name}</name><age>{age}</age><city>{city}</city>"
                    f"</person>")
            elif key == "deep_xml_str":
                entry = (
                    f"<person>"
                    f"<name>{name}</name><age>{age}</age><city>{city}</city>"
                    f"<contact><email>{email_address}</email>"
                    f"<phone>{phone_number}</phone></contact>"
                    f"</person>")

            data[key].append(entry)

    return data


def generate_shallow_data_old(num_records=3):
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


def generate_deep_array_based_data(num_records=3):
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


def generate_deep_object_based_data(num_records=3):
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
            "contact": {"email": email_address, "phone": phone_number}
        })

        obfuscated_deep_data.append({
            "name": "***",
            "age": age,
            "city": city,
            "contact": {"email": "***", "phone": "***"}
        })

    return deep_data, obfuscated_deep_data
