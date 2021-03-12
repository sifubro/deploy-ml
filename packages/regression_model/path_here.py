import pathlib


print(__name__)

print(pathlib.Path(__file__))

print(pathlib.Path(__file__).resolve())

print(pathlib.Path(__file__).resolve().parent)

print(pathlib.Path(__file__).resolve().parent.parent)