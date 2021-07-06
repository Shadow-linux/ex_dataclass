import typing
import requests
import setuptools

PROJECT_NAME = "ex_dataclass"
VERSION = "1.1.0"
AUTHOR = "ShadowYD"
E_MAIL = "972367265@qq.com"
GIT_URL= "https://github.com/Shadow-linux/ex_dataclass"

READ_ME = "README_PYPI.md"
READ_ME_RST = "README.rst"


def md_to_rst(from_file, to_file):
    """
    将markdown格式转换为rst格式
    @param from_file: {str} markdown文件的路径
    @param to_file: {str} rst文件的路径
    """
    response = requests.post(
        url='http://c.docverter.com/convert',
        data={'to': 'rst', 'from': 'markdown'},
        files={'input_files[]': open(from_file, 'rb')}
    )

    if response.ok:
        with open(to_file, "wb") as f:
            f.write(response.content)


def description() -> str:
    return "A more powerful data model management than DataClass that reduces maintenance costs and improves coding efficiency."


def long_description() -> str:
    # md_to_rst(READ_ME, READ_ME_RST)
    with open(READ_ME_RST, "r") as fd:
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