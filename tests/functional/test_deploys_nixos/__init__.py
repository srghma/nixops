from nixops.util import root_dir
from itertools import product
from parameterized import parameterized

from tests.functional.shared.deployment_run_command import deployment_run_command
from tests.functional.shared.create_deployment import create_deployment
from tests.functional.shared.using_state_file import using_state_file

@parameterized(product(
    ['json', 'nixops'],
    [
        # vbox
        [
            '{}/tests/functional/shared/nix_expressions/logical_base.nix'.format(root_dir),
            '{}/tests/functional/shared/nix_expressions/vbox_base.nix'.format(root_dir),
        ],
        # ec2
        [
            '{}/tests/functional/shared/nix_expressions/logical_base.nix'.format(root_dir),
            '{}/tests/functional/shared/nix_expressions/ec2_base.nix'.format(root_dir),
        ],
        # gce
        [
            '{}/tests/functional/shared/nix_expressions/logical_base.nix'.format(root_dir),
            '{}/tests/functional/shared/nix_expressions/gce_base.nix'.format(root_dir),
        ],
        # azure
        [
            '{}/tests/functional/shared/nix_expressions/logical_base.nix'.format(root_dir),
            '{}/tests/functional/shared/nix_expressions/azure_base.nix'.format(root_dir),
        ],
        # libvirtd
        [
            '{}/tests/functional/shared/nix_expressions/logical_base.nix'.format(root_dir),
            '{}/tests/functional/shared/nix_expressions/libvirtd_base.nix'.format(root_dir),
        ]
    ],
))

def test_deploys_nixos(state_extension, nix_expressions):
    with using_state_file(
            unique_name='test_deploys_nixos',
            state_extension=state_extension) as state:
        deployment = create_deployment(state, nix_expressions)
        deployment_run_command(deployment, "test -f /etc/NIXOS")
