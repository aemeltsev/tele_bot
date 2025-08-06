from typing import Union, List
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

class ContainsWord(Filter):
    '''
    A filter to check if a message or callback query contains specific word(s).

    Attributes:
        words (List[str]): List of words to check for.
        ignore_case (bool): Whether to ignore case when checking for words.
        partial_match (bool): Whether to allow partial matching of words.
    '''
    def __init__(self, words: Union[str, List[str]], ignore_case: bool = True, partial_match: bool = False):
        '''
        Initialize the ContainsWord filter.

        Args:
            words (Union[str, List[str]]): Word or list of words to check for.
            ignore_case (bool): Whether to ignore case when checking for words.
            partial_match (bool): Whether to allow partial matching of words.
        '''
        self.words = [words] if isinstance(words, str) else words
        self.ignore_case = ignore_case
        self.partial_match = partial_match

    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        '''
        Check if the message or callback query contains the specified word(s).

        Args:
            message (Union[Message, CallbackQuery]): The message or callback query to check.

        Returns:
            bool: True if the message or callback query contains the word(s), False otherwise.
        '''
        try:
            text = message.text if isinstance(message, Message) else message.data
            if text is None:
                return False

            if self.ignore_case:
                text = text.lower()

            for word in self.words:
                word_to_check = word.lower() if self.ignore_case else word
                if self.partial_match:
                    if word_to_check in text:
                        return True
                else:
                    if text == word_to_check:
                        return True
            return False
        except AttributeError:
            return False
        

'''
    # Using the ContainsWord filter with a single word
    @dp.message(ContainsWord("example"))
    async def example_message(message: types.Message):
        await message.reply("You mentioned the word 'example'!")

    # Using the ContainsWord filter with multiple words
    @dp.message(ContainsWord(["hello", "hi"], ignore_case=True, partial_match=True))
    async def hello_message(message: types.Message):
        await message.reply("You mentioned a greeting word!")
'''