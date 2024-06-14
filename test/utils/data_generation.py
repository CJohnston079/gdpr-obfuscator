from faker import Faker

fake = Faker("en_GB")


def generate_data(*generate, num_records=3):
    data = {key: [] for key in generate}

    for _ in range(num_records):
        record = {
            "name": fake.name(),
            "age": str(fake.random_int(min=18, max=66)),
            "city": fake.city(),
            "email": fake.email(),
            "phone": fake.phone_number()
        }

        for key in generate:
            entry = entry_generators[key](record)
            data[key].append(entry)

    return data


entry_generators = {
    "shallow_list_based": lambda data: {
        "name": data["name"],
        "age": data["age"],
        "city": data["city"]
    },
    "shallow_list_based_obfuscated": lambda data: {
        "name": "***",
        "age": data["age"],
        "city": data["city"]
    },
    "shallow_dict_based": lambda data: {
        "person": {
            "name": data["name"],
            "age": data["age"],
            "city": data["city"]
        }
    },
    "shallow_dict_based_obfuscated": lambda data: {
        "person": {
            "name": "***",
            "age": data["age"],
            "city": data["city"]
        }
    },
    "deep_list_based": lambda data: {
        "name": data["name"],
        "age": data["age"],
        "city": data["city"],
        "contact": [{"email": data["email"]}, {"phone": data["phone"]}]
    },
    "deep_list_based_obfuscated": lambda data: {
        "name": "***",
        "age": data["age"],
        "city": data["city"],
        "contact": [{"email": "***"}, {"phone": "***"}]
    },
    "deep_dict_based": lambda data: {"person": {
        "name": data["name"],
        "age": data["age"],
        "city": data["city"],
        "contact": {
            "email": data["email"],
            "phone": data["phone"]
        }
    }},
    "deep_dict_based_obfuscated": lambda data: {"person": {
        "name": "***",
        "age": data["age"],
        "city": data["city"],
        "contact": {
            "email": "***",
            "phone": "***"
        }
    }},
    "shallow_xml_str": lambda data: (
        f"<person>"
        f"<name>{data['name']}</name>"
        f"<age>{data['age']}</age>"
        f"<city>{data['city']}</city>"
        f"</person>"
    ),
    "deep_xml_str": lambda data: (
        f"<person>"
        f"<name>{data['name']}</name>"
        f"<age>{data['age']}</age>"
        f"<city>{data['city']}</city>"
        f"<contact>"
        f"<email>{data['email']}</email>"
        f"<phone>{data['phone']}</phone>"
        f"</contact>"
        f"</person>"
    ), }
