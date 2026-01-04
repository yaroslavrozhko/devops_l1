import click

# Створюємо групу команд (основний клієнт)
@click.group()
def cli():
    """Мій CLI інструмент на Click."""
    pass

# Створюємо команду 'say'
@click.command()
@click.option('--name', required=True, help='Ім\'я користувача для привітання.')
def say(name):
    """Виводить ім'я, якщо воно не починається на 'p'."""
    if name.lower().startswith('p'):
        click.echo("Ім’я не підходить")
    else:
        click.echo(name)

# Додаємо команду say до групи
cli.add_command(say)

if __name__ == '__main__':
    cli()