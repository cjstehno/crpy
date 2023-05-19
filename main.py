"""Module to provide a CLI for the encounter difficulty calculation."""
import click

from difficulty import calculate_difficulty


@click.command()
@click.option(
    '--party',
    prompt='What are the party levels? ',
    help='The level of each party member, comma-separated.'
)
@click.option(
    '--monsters',
    prompt='What are the monster CRs? ',
    help='The count and CR values for each monster, as n@CR.'
)
def difficulty(party: str, monsters: str):
    """Command line interface wrapper around the `calculate_difficulty` function."""
    click.echo(f"{calculate_difficulty(party, monsters)}")


if __name__ == '__main__':
    difficulty()  # pylint: disable=no-value-for-parameter
