def create_signed_dockerfile(image: str, signature_label: str, signature: str) -> str:
    dockerfile_template = """
        FROM {image_name}
        LABEL {signature_label}={signature}
        """.format(
            image_name=image, signature_label=signature_label, signature=signature
        )

    return dockerfile_template
