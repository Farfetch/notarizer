import unittest
from unittest.mock import patch

import notarizer.converter as converter
import notarizer.credentials_repository as credentials_repository
import notarizer.cryptography_wrapper as crypto_wrapper
import notarizer.docker_gateway as docker_gateway
import notarizer.image_verifier as image_verifier
from notarizer.exceptions import (ImageNotFound, InvalidLabelSignature,
                                  NoSignatureFound, NotarizerException,
                                  PublicKeyNotFound, VerificationFailure)
from notarizer.test.mocked_data import MockedData


class TestVerifySignature(unittest.TestCase):
    def setUp(self):
        self.func = image_verifier.verify
        self.key_fake = MockedData.get_public_key_bytes()
        self.signature_name = "signature"
        self.valid_history_fake = MockedData.get_fake_valid_history_content(self.signature_name)
        self.invalid_history = MockedData.get_fake_invalid_history_content(self.signature_name)

    def test_no_signature_found_raises_no_signature_found(self):
        # Arrange
        with patch.object(
                credentials_repository,
                "load_public_key",
                return_value=self.key_fake
            ), patch.object(
                docker_gateway,
                "get_history"
            ), self.assertRaises(
                NoSignatureFound
                ) as ex:
            # Act
            self.func(["image:tag"], "key", self.signature_name)
            # Assert
            exception = ex.exception
            self.assertEqual(exception.error_code, 10)

    def test_invalid_signature_raises_invalid_image_signature(self):
        # Arrange
        with patch.object(
                credentials_repository, "load_public_key", return_value=self.key_fake
            ), patch.object(
                docker_gateway, "get_history", return_value=self.invalid_history,
            ), patch.object(
                converter, "decode_from_base64", side_effect=InvalidLabelSignature("error")
            ), self.assertRaises(
                InvalidLabelSignature
                ) as ex:
            # Act
            self.func(["image:tag"], "key", self.signature_name)
            # Assert
            exception = ex.exception
            self.assertEqual(exception.error_code, 11)

    def test_invalid_signature_raises_verification_failure(self):
        # Arrange
        with patch.object(
                credentials_repository, "load_public_key", return_value=self.key_fake
            ), patch.object(
                docker_gateway, "get_history", return_value=self.invalid_history
            ), patch.object(
                crypto_wrapper, "verify", side_effect=VerificationFailure("error")
            ), self.assertRaises(
                VerificationFailure
                ) as ex:
            # Act
            self.func(["image:tag"], "key", self.signature_name)
            # Assert
            exception = ex.exception
            self.assertEqual(exception.error_code, 12)

    def test_no_public_key_provided_raises_no_public_key_found(self):
        # Arrange
        with patch.object(
                credentials_repository, "load_public_key", side_effect=PublicKeyNotFound(),
        ), self.assertRaises(PublicKeyNotFound) as ex:
            # Act
            self.func(None, None, self.signature_name)
            # Assert
            exception = ex.exception
            self.assertEqual(exception.error_code, 13)

    def test_image_not_found_image_not_found(self):
        # Arrange
        with patch.object(
                credentials_repository, "load_public_key", return_value=self.key_fake
            ), patch.object(
                docker_gateway, "get_history", side_effect=ImageNotFound("error message"),
            ), self.assertRaises(
                ImageNotFound
                ) as ex:
            # Act
            self.func(["image:tag"], "key", self.signature_name)
            # Assert
            exception = ex.exception
            self.assertEqual(exception.error_code, 14)

    def test_valid_public_key_and_valid_history_does_not_raise_exception(self):
        # Arrange
        with patch.object(
                credentials_repository, "load_public_key", return_value=self.key_fake
            ), patch.object(
                docker_gateway, "get_history", return_value=self.valid_history_fake
                ), patch.object(crypto_wrapper, "verify"):
            # Act
            try:
                self.func(["image:tag"], "key", self.signature_name)
            except NotarizerException:
                self.fail("Should not raise an exception.")


if __name__ == "__main__":
    unittest.main()
