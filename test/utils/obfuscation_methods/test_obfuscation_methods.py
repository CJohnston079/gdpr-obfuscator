from src.utils.obfuscation_methods.tokenise import tokenise


class TestTokenise:
    def test_returns_triple_star_by_default(self):
        assert tokenise("name", {}) == "***"

    def test_returns_custom_token_if_token_in_options_dict(self):
        assert tokenise("name", {"token": "custom-token"}) == "custom-token"
