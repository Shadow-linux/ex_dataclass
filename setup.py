import typing
import setuptools

PROJECT_NAME = "ex_dataclass"
VERSION = "1.0.2"
AUTHOR = "ShadowYD"
E_MAIL = "972367265@qq.com"
GIT_URL= "https://github.com/Shadow-linux/ex_dataclass"

READ_ME = "README.md"


def description() -> str:
    return "A more powerful data model management than DataClass that reduces maintenance costs and improves coding efficiency."


def long_description() -> str:
    with open(READ_ME, "r") as fd:
        content = fd.read()
        return content


def package_data() -> typing.Dict:
    return {
        "example": [
            "example/*"
        ]
    }


def main():

    setuptools.setup(
            name=PROJECT_NAME,
            version=VERSION,
            author=AUTHOR,
            author_email=E_MAIL,
            description=description(),
            long_description=long_description(),
            url=GIT_URL,
            include_package_data=True,
            package_data=package_data(),
            packages=setuptools.find_packages(),
            python_requires=">=3.7",

    )

if __name__ == '__main__':
    main()