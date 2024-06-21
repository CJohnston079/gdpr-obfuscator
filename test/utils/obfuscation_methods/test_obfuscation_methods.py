import pytest

from src.utils.obfuscation_methods.anonymise import anonymise
from src.utils.obfuscation_methods.anonymise import pii_fields
from src.utils.obfuscation_methods.tokenise import tokenise


class TestTokenise:
    def test_returns_triple_star_by_default(self):
        assert tokenise("name", {}) == "***"

    def test_returns_custom_token_if_token_in_options_dict(self):
        assert tokenise("name", {"token": "custom-token"}) == "custom-token"


class TestAnonymise:
    @pytest.mark.parametrize(
        "field, expected",
        [
            ("name", pii_fields["name"]),
            ("birthday", pii_fields["birthday"]),
            ("homephone", pii_fields["homephone"]),
            ("address", pii_fields["address"]),
            ("postcode", pii_fields["postcode"]),
            ("email", pii_fields["email"]),
        ],
    )
    def test_generates_data(self, field, expected):
        assert anonymise(field, {}) == expected

    @pytest.mark.parametrize(
        "field, expected",
        [
            ("first name", pii_fields["firstname"]),
            ("first-name", pii_fields["firstname"]),
            ("first_name", pii_fields["firstname"]),
            ("firstName", pii_fields["firstname"]),
            ("FirstName", pii_fields["firstname"]),
        ],
    )
    def test_works_for_camel_snake_and_kebab_case(self, field, expected):
        assert anonymise(field, {}) == expected

    def test_returns_token_if_pii_field_not_found(self):
        assert anonymise("unexpected_field", {}) == "***"
        assert anonymise("unexpected_field", {"token": "---"}) == "---"
