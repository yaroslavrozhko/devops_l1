def parity_generator():
    """Генератор, який поперемінно повертає 'Парне' і 'Непарне'."""
    while True:
        yield "Парне"
        yield "Непарне"