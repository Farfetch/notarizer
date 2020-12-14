from notarizer.exceptions import NoSignatureFound
import notarizer.converter as converter
import notarizer.credentials_repository as credentials_repository
import notarizer.cryptography_wrapper as crypto_wrapper
import notarizer.docker_gateway as docker_gateway

client = docker_gateway.get_client()


def verify(image: str, public_key_file_name: str, signature_label: str):
    signature_line_pattern = "/bin/sh -c #(nop)  LABEL {label}=".format(label=signature_label)
    public_key = credentials_repository.load_public_key(public_key_file_name)

    column_to_filter = "CreatedBy"
    history = docker_gateway.get_history(client, image, column_to_filter)

    (signature, parent_history_start) = _extract_signature_from_history(history, signature_line_pattern, image)

    parent_image_history = "\n".join(history[i] for i in range(parent_history_start, len(history)))

    decoded_signature = converter.decode_from_base64(signature)
    crypto_wrapper.verify(public_key, decoded_signature, parent_image_history)


def _extract_signature_from_history(image_history: str, signature_line_pattern: str, image: str):
    parent_image_history_starting_line = -1
    signature = None
    for hline in image_history:
        if hline.startswith(signature_line_pattern):
            signature = hline.replace(signature_line_pattern, "")
            parent_image_history_starting_line = image_history.index(hline) + 1
            break

    if signature is None or len(signature) == 0 or parent_image_history_starting_line == -1:
        raise NoSignatureFound("No Signature Found for image: {img}. \n\
Please make sure you are using the signed parent image in your Dockerfile.".format(img=image))

    return (signature, parent_image_history_starting_line)
