"""
BACON = Building Autama's Core Overall Nature

This file contains a class to handle generating an Autama's personality.
"""

from itertools import chain
from random import choice, randint, seed
from Nucleus.utils import get_dataset
from Nucleus.tools import read_pickle


class Bacon:
    def __init__(self):
        self.__nucleus = read_pickle("nucleus.pickle")
        self.__args = self.__nucleus.get_args()
        self.__tokenizer = self.__nucleus.get_tokenizer()
        self.__required_amount = 6 # The required amount of traits per personality

    # A method to generate a random personality with exactly the required amount of traits
    def generate_full_personality(self):
        personality = self.__generate_personality()
        return self.__fill_up(personality)

    # A method to generate a personality with half of a new user's personality and half random
    def make_hybrid_freak(self, user_personality: list):
        personality = self.__format_personality(user_personality)
        personality = self.__remove_name_trait(personality)
        personality = self.__choose_some(personality)
        return self.__fill_up(personality)

    # A method to check and remove name traits from user's personality when copying the personality to a new Autama
    def check_personality(self, user_personality: list):
        personality = self.__format_personality(user_personality)
        personality = self.__remove_name_trait(personality)
        return self.__fill_up(personality)

    # A method to generate a random personality. It returns a list of personality trait strings.
    def __generate_personality(self):
        encoded_personality = self.__generate_encoded_personality()
        decoded_personality = self.__decode_personality(encoded_personality)
        return self.__remove_name_trait(decoded_personality)

    # A method for generating one encoded personality
    # https://github.com/huggingface/transfer-learning-conv-ai/blob/master/interact.py
    def __generate_encoded_personality(self):
        dataset = get_dataset(self.__tokenizer, self.__args.dataset_path, self.__args.dataset_cache)
        personalities = [dialog["personality"] for dataset in dataset.values() for dialog in dataset]
        personality = choice(personalities)
        return personality

    # A method for decoding an encoded personality
    def __decode_personality(self, encoded_personality: list):
        encoded_personality_string = self.__tokenizer.decode(chain(*encoded_personality))
        decoded_personality_list = [i + "." for i in encoded_personality_string.split(".")]
        decoded_personality_list.pop()
        return decoded_personality_list

    # A method that takes an existing personality and fills it up until it has the required amount of traits
    def __fill_up(self, personality: list):
        required = self.__required_amount
        copy_personality = personality[:]
        amount = len(copy_personality)

        # Loop until personality has the required amount or more
        while amount < required:
            new_personality = self.__generate_personality()
            new_amount = len(new_personality)

            # Determine if new personality has required amount
            if new_amount == required:
                copy_personality = new_personality
                amount = new_amount
            else:
                copy_personality = copy_personality + new_personality
                amount = len(copy_personality)

        difference = amount - required

        # Loop until personality is equal to required amount
        for i in range(difference):
            copy_personality.pop()
            amount = amount - 1

        return copy_personality

    # A method that chooses some of the user's traits
    def __choose_some(self, user_personality: list):
        personality = user_personality[:]
        amount = len(personality)
        half = int(amount / 2)
        seed()

        for i in range(half):
            amount = amount - 1
            index = randint(0, amount)
            personality.pop(index)

        return personality

    # A method to format a user's personality for copying
    def __format_personality(self, user_personality: list):
        personality = user_personality[:]
        personality = [trait.lower() for trait in personality]
        return personality

    # A method to check and remove Convai generated names (any traits with "my name is")
    def __remove_name_trait(self, personality: list):
        revised_personality = []

        # Loop and keep traits that do not contain "my name is"
        for trait in personality:
            if "my name is" not in trait:
                revised_personality.append(trait)

        return revised_personality
