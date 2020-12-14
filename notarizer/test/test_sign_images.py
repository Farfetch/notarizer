import unittest
from unittest.mock import patch

import notarizer.image_signer as image_signer
import notarizer.credentials_repository as credentials_repository
import notarizer.docker_gateway as docker_gateway
import notarizer.cryptography_wrapper as crypto_wrapper

from notarizer.exceptions import (
    InvalidLabelSignature,
    PrivateKeyNotFound,
    ImageNotFound,
    NotarizerException,
    SigningError
)
from notarizer.test.mocked_data import MockedData


class TestImageSigner(unittest.TestCase):
    def setUp(self):
        self.func = image_signer.sign
        self.priv_key_fake = MockedData.get_private_key_bytes()
        self.valid_history = MockedData.get_fake_valid_history_content("sign")

    def test_private_key_does_not_exist_raises_private_key_not_found(self,):
        # Arrange
        with patch.object(
                credentials_repository,
                "load_private_key",
                side_effect=PrivateKeyNotFound()
            ), self.assertRaises(
                PrivateKeyNotFound
                ) as exp:
            # Act
            self.func("test:1", "path/not_exists.pem", "dummy")

            # Assert
            self.assertEqual(exp.exception.error_code, 15)

    def test_sign__docker_image_does_not_raises_image_not_found(self):
        # Arrange
        with patch.object(credentials_repository, "load_private_key", return_value=self.priv_key_fake,), patch.object(
                docker_gateway, "get_history", side_effect=ImageNotFound("not_exists:1"),
            ), self.assertRaises(
                ImageNotFound
                ) as exp:
            # Act
            self.func("not_exists:1", "path/private.pem", "dummy")

            # Assert
            self.assertEqual(exp.exception.error_code, 14)

    def test_error_creating_signature_raises_invalid_label_signature(self):
        # Arrange
        with patch.object(credentials_repository, "load_private_key", return_value=self.priv_key_fake,), patch.object(
                docker_gateway, "get_history", side_effect=self.valid_history,
            ), patch.object(
                crypto_wrapper, "create_signature", side_effect=InvalidLabelSignature("error_msg")
            ), self.assertRaises(
                InvalidLabelSignature
                ) as exp:
            # Act
            self.func("exists:1", "path/private.pem", "dummy")

            # Assert
            self.assertEqual(exp.exception.code, 11)

    def test_sign_build_error_raises_error_creating_signed_image(self):
        # Arrange
        with patch.object(credentials_repository, "load_private_key", return_value=self.priv_key_fake,), patch.object(
                docker_gateway, "get_history", side_effect=self.valid_history,
            ), patch.object(crypto_wrapper, "create_signature", return_value="abc"), patch.object(
                docker_gateway, "build_image", side_effect=SigningError("forced error reason"),
            ), self.assertRaises(
                SigningError
                ) as exp:
            # Act
            self.func("exists:1", "path/private.pem", "dummy")

            # Assert
            self.assertEqual(exp.exception.code, 16)

    def test_sign_success_signing_image(self):
        # Arrange
        with patch.object(credentials_repository, "load_private_key", return_value=self.priv_key_fake,), patch.object(
                docker_gateway, "get_history", side_effect=self.valid_history,
            ), patch.object(
                crypto_wrapper, "create_signature", return_value="abc"
            ), patch.object(
                docker_gateway, "build_image"
                ):
            try:
                # Act
                self.func("exists:1", "path/private.pem", "dummy")
            except NotarizerException:
                self.fail("Should not raise an exception")
