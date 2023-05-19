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
    click.echo(f"{calculate_difficulty(party, monsters)}")


if __name__ == '__main__':
    difficulty()
