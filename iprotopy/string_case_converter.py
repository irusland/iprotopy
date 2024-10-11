import re

from iprotopy.package_generator_settings import StringCase


class StringCaseConverter:
    def convert(self, string: str, string_case: StringCase) -> str:
        words = re.findall(r'[A-Z][a-z]*', string)
        if string_case == StringCase.ORIGINAL:
            return string
        elif string_case == StringCase.CAMEL:
            # Lowercase the first word and capitalize the rest
            return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

        elif string_case == StringCase.SNAKE:
            # Lowercase all words and join with underscores
            return '_'.join(word.lower() for word in words)

        elif string_case == StringCase.KEBAB:
            # Lowercase all words and join with hyphens
            return '-'.join(word.lower() for word in words)

        elif string_case == StringCase.PASCAL:
            # Capitalize all words
            return ''.join(word.capitalize() for word in words)
        else:
            raise ValueError(f'Unknown string case: {string_case}')


if __name__ == '__main__':
    print(StringCaseConverter().convert('HelloWorld', StringCase.SNAKE))
