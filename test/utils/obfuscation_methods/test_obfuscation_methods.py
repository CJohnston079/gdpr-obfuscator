import pytest

from src.utils.obfuscation_methods.anonymise import anonymise
from src.utils.obfuscation_methods.tokenise import tokenise


class TestTokenise:
    def test_returns_triple_star_by_default(self):
        assert tokenise("name", {}) == "***"

    def test_returns_custom_token_if_token_in_options_dict(self):
        assert tokenise("name", {"token": "custom-token"}) == "custom-token"


class TestAnonymise:
    @pytest.fixture(scope="function")
    def pii_fields(self):
        return {
            "anonymous_pii_fields": {
                "firstname": "Aaron",
                "lastname": "Baker",
                "email": "aaron480@yahoo.co.uk",
            }
        }

    @pytest.mark.parametrize(
        "field",
        [("first-name"), ("first_name"), ("firstName")],
    )
    def test_works_for_camel_snake_and_kebab_case(self, field, pii_fields):
        result = anonymise(field, pii_fields)
        assert result == "Aaron"

    def test_returns_token_if_pii_field_not_found(self):
        assert (
            anonymise("unexpected_field", {"anonymous_pii_fields": {}})
            == "***"
        )
