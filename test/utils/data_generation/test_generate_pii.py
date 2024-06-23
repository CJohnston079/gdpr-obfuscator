import pytest

from src.utils.data_generation.generate_pii import generate_email
from src.utils.data_generation.generate_pii import generate_gender
from src.utils.data_generation.generate_pii import generate_name
from src.utils.data_generation.generate_pii import generate_person
from src.utils.data_generation.generate_pii import generate_pii


class TestGenerateGender:
    @pytest.mark.parametrize(
        "random_gender, expected_gender",
        [
            (["F"], "F"),
            (["M"], "M"),
            (["T"], "T"),
            (["FTM"], "FTM"),
            (["MTF"], "MTF"),
            (["N"], "N"),
        ],
    )
    def test_generate_gender(self, mocker, random_gender, expected_gender):
        mocker.patch("random.choices", return_value=random_gender)
        assert generate_gender() == expected_gender


class TestGenerateName:
    @pytest.fixture(
        scope="function",
    )
    def fake(self, mocker):
        return mocker.patch("src.utils.data_generation.generate_pii.fake")

    @pytest.mark.parametrize(
        "gender, expected_first_name",
        [
            ("F", "Mary"),
            ("MTF", "Mary"),
            ("M", "Joseph"),
            ("FTM", "Joseph"),
            ("N", "Aaron"),
        ],
    )
    def test_generates_name(self, fake, gender, expected_first_name):
        if gender in ["F", "MTF"]:
            fake.first_name_female.return_value = expected_first_name
        elif gender in ["M", "FTM"]:
            fake.first_name_male.return_value = expected_first_name
        else:
            fake.first_name_nonbinary.return_value = expected_first_name

        fake.last_name.return_value = "Doe"
        result = generate_name(gender)

        assert result["first"] == expected_first_name
        assert result["last"] == "Doe"


class TestGenerateEmail:
    @pytest.fixture(scope="function", autouse=True)
    def set_up_fake_and_random(self, mocker):
        mocker.patch("random.randint", return_value=123)
        mocker.patch("src.utils.data_generation.generate_pii.fake")
        fake = mocker.patch("src.utils.data_generation.generate_pii.fake")
        fake.domain_word.return_value = "example"
        fake.free_email_domain.return_value = "example.com"

    def test_generates_personal_email(self, mocker):
        result = generate_email("Aaron", "Baker")
        personal_email = result["personal"]

        assert personal_email.startswith("aaron123@")
        assert personal_email.endswith("@example.com")

    def test_generates_work_email(self, mocker):
        result = generate_email("Aaron", "Baker")
        work_email = result["work"]

        assert work_email.startswith("a.baker@")
        assert work_email.endswith("@example.org.uk") or work_email.endswith(
            "@example.com"
        )


class TestGeneratePerson:
    @pytest.fixture(scope="function")
    def mock_generators(self, mocker):
        generate_gender = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_gender"
        )
        generate_name = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_name"
        )
        generate_email = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_email"
        )
        generate_gender.return_value = "N"
        generate_name.return_value = {
            "first": "Aaron",
            "middle": "Shirley",
            "last": "Baker",
        }
        generate_email.return_value = {
            "personal": "aaron480@yahoo.co.uk",
            "work": "a.baker@company.org.uk",
        }

    def test_generate_person_calls_generate_generators(self, mocker):
        generate_gender = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_gender"
        )
        generate_name = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_name"
        )
        generate_email = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_email"
        )
        generate_gender.return_value = "N"
        generate_name.return_value = {
            "first": "Aaron",
            "middle": "Shirley",
            "last": "Baker",
        }

        generate_person()

        generate_gender.assert_called_once_with()
        generate_name.assert_called_once_with("N")
        generate_email.assert_called_once_with("Aaron", "Baker")

    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ("gender", "N"),
            ("name", "Aaron Baker"),
            ("first_name", "Aaron"),
            ("middle_name", "Shirley"),
            ("last_name", "Baker"),
            ("email_personal", "aaron480@yahoo.co.uk"),
            ("email_work", "a.baker@company.org.uk"),
        ],
    )
    def test_uses_generated_data(self, mock_generators, key, expected_value):
        person = generate_person()
        assert person[key] == expected_value


class TestGeneratePII:
    @pytest.fixture(scope="function")
    def generate_person(self, mocker):
        generate_person = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_person"
        )
        test_person = {
            "gender": "N",
            "name": "Aaron Baker",
            "first_name": "Aaron",
            "middle_name": "Shirley",
            "last_name": "Baker",
            "email_personal": "aaron480@yahoo.co.uk",
            "email_work": "a.baker@company.org.uk",
        }
        generate_person.return_value = test_person

    def test_generate_pii_calls_generate_person(self, mocker):
        generate_person = mocker.patch(
            "src.utils.data_generation.generate_pii.generate_person"
        )
        generate_pii()
        generate_person.assert_called_once_with()

    @pytest.mark.parametrize(
        "field, expected_value",
        [
            ("gender", "N"),
            ("name", "Aaron Baker"),
            ("fullname", "Aaron Baker"),
            ("firstname", "Aaron"),
            ("middlename", "Shirley"),
            ("lastname", "Baker"),
            ("surname", "Baker"),
            ("email", "aaron480@yahoo.co.uk"),
            ("emailaddress", "aaron480@yahoo.co.uk"),
            ("emailaddresswork", "a.baker@company.org.uk"),
            ("workemailaddress", "a.baker@company.org.uk"),
            ("workemail", "a.baker@company.org.uk"),
        ],
    )
    def test_uses_generated_data(self, generate_person, field, expected_value):
        pii_fields = generate_pii()
        assert pii_fields[field] == expected_value
