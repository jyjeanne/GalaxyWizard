"""
Security tests for GalaxyWizard.
Tests input validation to prevent directory traversal and other attacks.
"""
import unittest
import re


def validate_name(name, name_type):
    """
    Validate campaign/scenario names to prevent directory traversal attacks.
    (Copy of the validation logic for testing without circular imports)
    """
    if not name:
        raise ValueError(f"{name_type} name cannot be empty")

    # Check for reserved names first (before regex check)
    if name in ['.', '..', 'CON', 'PRN', 'AUX', 'NUL']:
        raise ValueError(f"Reserved {name_type} name '{name}' is not allowed")

    # Only allow alphanumeric characters, hyphens, and underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        raise ValueError(
            f"Invalid {name_type} name '{name}'. "
            f"Only alphanumeric characters, hyphens, and underscores are allowed."
        )

    return name


class TestScenarioValidation(unittest.TestCase):
    """Test scenario/campaign name validation for security vulnerabilities."""

    def test_valid_campaign_names(self):
        """Test that valid campaign names are accepted."""
        valid_names = [
            'demo',
            'campaign1',
            'my-campaign',
            'test_scenario',
            'Campaign-2024',
            'a',  # single character
            'ABC123',
        ]

        for name in valid_names:
            # Should not raise exception
            validated = validate_name(name, 'campaign')
            self.assertEqual(validated, name)

    def test_valid_scenario_names(self):
        """Test that valid scenario names are accepted."""
        valid_names = [
            'castle',
            'scenario-1',
            'test_map',
            'battle_01',
        ]

        for name in valid_names:
            # Should not raise exception
            validated = validate_name(name, 'scenario')
            self.assertEqual(validated, name)

    def test_directory_traversal_attacks(self):
        """Test that directory traversal attempts are blocked."""
        malicious_names = [
            '../etc/passwd',
            '../../secret',
            '../../../system32',
            './hidden',
            '..',
            '.',
            '/etc/shadow',
            'C:/Windows/System32',
            '..\\..\\windows',
            'demo/../../../etc',
        ]

        for name in malicious_names:
            with self.assertRaises(ValueError) as context:
                validate_name(name, 'campaign')

            # Should be rejected with either "Invalid" or "Reserved" error
            error_msg = str(context.exception)
            self.assertTrue(
                'Invalid' in error_msg or 'Reserved' in error_msg,
                f"Expected 'Invalid' or 'Reserved' in error message, got: {error_msg}"
            )

    def test_special_characters_blocked(self):
        """Test that special characters are blocked."""
        invalid_names = [
            'test/scenario',
            'test\\scenario',
            'test?scenario',
            'test*scenario',
            'test|scenario',
            'test<scenario',
            'test>scenario',
            'test:scenario',
            'test"scenario',
            "test'scenario",
            'test scenario',  # space
            'test;scenario',
            'test&scenario',
            'test$scenario',
            'test@scenario',
            'test!scenario',
            'test%scenario',
            'test^scenario',
            'test(scenario)',
            'test[scenario]',
            'test{scenario}',
        ]

        for name in invalid_names:
            with self.assertRaises(ValueError) as context:
                validate_name(name, 'scenario')

            self.assertIn('Invalid', str(context.exception))

    def test_empty_name_rejected(self):
        """Test that empty names are rejected."""
        with self.assertRaises(ValueError) as context:
            validate_name('', 'campaign')

        self.assertIn('cannot be empty', str(context.exception))

    def test_none_name_rejected(self):
        """Test that None is rejected."""
        with self.assertRaises(ValueError):
            validate_name(None, 'campaign')

    def test_reserved_names_blocked(self):
        """Test that reserved system names are blocked."""
        reserved_names = [
            '.',
            '..',
            'CON',
            'PRN',
            'AUX',
            'NUL',
        ]

        for name in reserved_names:
            with self.assertRaises(ValueError) as context:
                validate_name(name, 'campaign')

            self.assertIn('Reserved', str(context.exception))

    def test_error_messages_descriptive(self):
        """Test that error messages are clear and helpful."""
        # Test with directory traversal
        with self.assertRaises(ValueError) as context:
            validate_name('../secret', 'campaign')

        error_msg = str(context.exception)
        self.assertIn('Invalid', error_msg)
        self.assertIn('campaign', error_msg)
        self.assertIn('alphanumeric', error_msg.lower())

    def test_case_sensitive(self):
        """Test that validation is case-sensitive."""
        # Both uppercase and lowercase should work
        validate_name('Demo', 'campaign')
        validate_name('demo', 'campaign')
        validate_name('DEMO', 'campaign')

    def test_unicode_characters_blocked(self):
        """Test that unicode/international characters are blocked."""
        unicode_names = [
            'café',
            '日本語',
            'тест',
            'مرحبا',
            'test™',
            'test©',
            'test®',
        ]

        for name in unicode_names:
            with self.assertRaises(ValueError):
                validate_name(name, 'scenario')


if __name__ == '__main__':
    unittest.main()
