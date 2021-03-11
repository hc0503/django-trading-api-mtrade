import typing

from django.utils.crypto import get_random_string

from .models import (
    TraderLicense,
    TraderLicenseFactory,
    TraderLicenseMetadata,
)

def gen_rand_license_metadata() -> TraderLicenseMetadata:
    return TraderLicenseMetadata(
            name = 'license'+get_random_string(36),
            short_description = 'description'+get_random_string(100)
            )

def gen_rand_license() -> TraderLicense:
    return TraderLicenseFactory.build_entity_with_id(gen_rand_license_metadata())

def gen_rand_licenses(num_of_licenses: int) -> typing.List[TraderLicense]:
    licenses = []
    for _ in range(num_of_licenses):
        licenses.append(gen_rand_license())
    return licenses
