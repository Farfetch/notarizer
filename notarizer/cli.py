import sys
from typing import Sequence

import click
import notarizer.image_verifier as image_verifier
import notarizer.image_signer as image_signer
import notarizer.exceptions


@click.group()
def main():
    """
    Simple CLI for Verifying and Signing Images
    """


@main.command()
@click.option("--image", "-i", required=True, multiple=True)
@click.option("--public-key", "-p", required=True)
@click.option("--signature-label", "-s", required=False, default="signature")
def verify(image, public_key, signature_label):
    for img in image:
        image_verifier.verify(img, public_key, signature_label)
        print("{img} Verification OK".format(img=img))


@main.command()
@click.option("--image", "-i", required=True, multiple=True)
@click.option("--private-key", "-p", required=True)
@click.option("--signature-label", "-s", required=False, default="signature")
def sign(image: Sequence[str], private_key: str, signature_label: str):
    for img in image:
        image_signer.sign(img, private_key, signature_label)
        print("{img} Signature OK".format(img=img))


if __name__ == "__main__":
    try:
        main()
    except notarizer.exceptions.NotarizerException as nte:
        print(str(nte), file=sys.stderr)
        sys.exit(nte.error_code)
