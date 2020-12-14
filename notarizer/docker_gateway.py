from io import BytesIO

import docker.errors
from docker import DockerClient, from_env

import notarizer.exceptions


def get_client() -> DockerClient:
    return from_env()


def get_history(client: DockerClient, image: str, column_to_filter="") -> str:
    try:
        full_history = client.api.history(image)
    except docker.errors.ImageNotFound:
        raise notarizer.exceptions.ImageNotFound("The image: {image} was not found".format(image=image))

    if column_to_filter != "":
        history = [hline[column_to_filter] for hline in full_history]
        return history

    return full_history


def build_image(client: DockerClient, dockerfile: str, image: str):
    dockerfile_in_bytes = BytesIO(bytes(dockerfile, "utf-8"))
    try:
        client.images.build(fileobj=dockerfile_in_bytes, tag=image)
    except docker.errors.BuildError as build_error:
        raise notarizer.exceptions.SigningError(str(build_error))
