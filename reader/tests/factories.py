# author: goodalg0s@gmail.com
from factory import (
    Faker,
    SubFactory,
    Sequence
)

from factory.django import DjangoModelFactory
from reader.models import (
    ReaderError,
    ReaderRun,
    NemFile,
    Record100,
    Record250,
    Record550
)


class ReaderError_Factory(DjangoModelFactory):
    class Meta:
        model = ReaderError


class ReaderRun_Factory(DjangoModelFactory):
    class Meta:
        model = ReaderRun


class NemFile_Factory(DjangoModelFactory):
    class Meta:
        model = NemFile

    name = Sequence(lambda n: f"{Faker('word')}{n}")
    description = Faker('sentence')
    path = Faker('file_path', depth=2)
