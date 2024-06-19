from faker import Faker


fake = Faker("en_GB")


def generate_data(*generate, num_records=3):
    data_structures = {data_structure: [] for data_structure in generate}

    for _ in range(num_records):
        record = {
            "name": fake.name(),
            "age": str(fake.random_int(min=18, max=66)),
            "city": fake.city(),
            "email": fake.email(),
            "phone": fake.phone_number(),
        }

        for data_structure in generate:
            entry = entry_generators[data_structure](record)
            data_structures[data_structure].append(entry)

    for data_structure in data_structures:
        if "xml_str" in data_structure:
            xml_entries = "".join(data_structures[data_structure])
            data_structures[data_structure] = f"<root>{xml_entries}</root>"

    return data_structures


entry_generators = {
    "shallow_list_based": lambda data: {
        "name": data["name"],
        "age": data["age"],
        "city": data["city"],
    },
    "shallow_list_based_obfuscated": lambda data: {
        "name": "***",
        "age": data["age"],
        "city": data["city"],
    },
    "shallow_dict_based": lambda data: {
        "person": {
            "name": data["name"],
            "age": data["age"],
            "city": data["city"],
        }
    },
    "shallow_dict_based_obfuscated": lambda data: {
        "person": {"name": "***", "age": data["age"], "city": data["city"]}
    },
    "deep_list_based": lambda data: {
        "name": data["name"],
        "age": data["age"],
        "city": data["city"],
        "contact": [{"email": data["email"]}, {"phone": data["phone"]}],
    },
    "deep_list_based_obfuscated": lambda data: {
        "name": "***",
        "age": data["age"],
        "city": data["city"],
        "contact": [{"email": "***"}, {"phone": "***"}],
    },
    "deep_dict_based": lambda data: {
        "person": {
            "name": data["name"],
            "age": data["age"],
            "city": data["city"],
            "contact": {"email": data["email"], "phone": data["phone"]},
        }
    },
    "deep_dict_based_obfuscated": lambda data: {
        "person": {
            "name": "***",
            "age": data["age"],
            "city": data["city"],
            "contact": {"email": "***", "phone": "***"},
        }
    },
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
    ),
    "shallow_xml_data": lambda data: {
        "root": {
            "person": {
                "name": data["name"],
                "age": data["age"],
                "city": data["city"],
            }
        }
    },
    "deep_xml_data": lambda data: {
        "root": {
            "person": {
                "name": data["name"],
                "age": data["age"],
                "city": data["city"],
                "contact": {"email": data["email"], "phone": data["phone"]},
            }
        }
    },
    "shallow_xml_str_obfuscated": lambda data: (
        f"<person>"
        f"<name>***</name>"
        f"<age>{data['age']}</age>"
        f"<city>{data['city']}</city>"
        f"</person>"
    ),
}
