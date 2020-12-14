import notarizer.credentials_repository as credentials_repository
import notarizer.cryptography_wrapper as crypto_wrapper
import notarizer.docker_gateway as docker_gateway
import notarizer.templates as templating

client = docker_gateway.get_client()


def sign(image: str, private_key_file_name: str, signature_label: str):
    private_key = credentials_repository.load_private_key(private_key_file_name)

    _sign_image(image, private_key, signature_label)


def _sign_image(image: str, private_key: bytes, signature_label: str):
    column_to_filter = "CreatedBy"
    history = docker_gateway.get_history(client, image, column_to_filter)
    image_history = "\n".join(history)
    signature = crypto_wrapper.create_signature(private_key, image_history)
    dockerfile_template = templating.create_signed_dockerfile(image, signature_label, signature)
    docker_gateway.build_image(client, dockerfile_template, image)
