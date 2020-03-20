"""
Banner object

--

Author : DrLarck

Last update : 20/03/20 by DrLarck
"""

import asyncio
import random

# util
from utility.database import Database
from utility.entity.character import CharacterGetter


class Banner:

    def __init__(self):
        # Public
        self.name = ""
        self.image = ""
        self.characters = []
        self.sorted = False
        self.multi = 10

        # Private
        self.__lr = []
        self.__ur = []
        self.__ssr = []
        self.__sr = []
        self.__r = []
        self.__n = []

        # Droprate as %
        self.__lr_droprate = 0.01
        self.__ur_droprate = 3
        self.__ssr_droprate = 15
        self.__sr_droprate = 33
        self.__r_droprate = 50
        self.__n_droprate = 100

    # Public
    async def sort(self):
        """
        Sort the banner

        --

        :return: `None`
        """

        if self.sorted is False:
            # Sort the characters
            for character in self.characters:
                await asyncio.sleep(0)

                # Put the character in the LR list
                if character.rarity.value == 5:
                    self.__lr.append(character)

                # Put the character in the UR list
                elif character.rarity.value == 4:
                    self.__ur.append(character)

                elif character.rarity.value == 3:
                    self.__ssr.append(character)

                elif character.rarity.value == 2:
                    self.__sr.append(character)

                elif character.rarity.value == 1:
                    self.__r.append(character)

                elif character.rarity.value == 0:
                    self.__n.append(character)

                self.sorted = True

        return

    async def summon(self):
        """
        Summon a random character

        --

        :return: `Character` or `None` in case of problem
        """

        # Init
        roll = random.uniform(0, 100)

        # Get a character according to the player's roll right above
        # Check if the list is not empty
        if len(self.__lr) > 0 and roll <= self.__lr_droprate:
            # If the player get a LR character
            # Get a random LR character form the LR list
            character = random.choice(self.__lr)

            return character

        elif len(self.__ur) > 0 and roll <= self.__ur_droprate:
            character = random.choice(self.__ur)

            return character

        elif len(self.__ssr) > 0 and roll <= self.__ssr_droprate:
            character = random.choice(self.__ssr)

            return character

        elif len(self.__sr) > 0 and roll <= self.__sr_droprate:
            character = random.choice(self.__sr)

            return character

        elif len(self.__r) > 0 and roll <= self.__r_droprate:
            character = random.choice(self.__r)

            return character

        elif len(self.__n) > 0 and roll <= self.__n_droprate:
            character = random.choice(self.__n)

            return character

        return

    async def multi_summon(self):
        """
        Proceed to a multi summon

        --

        :return: `list` of `Character`
        """

        # Init
        characters = []

        for i in range(self.multi):
            summoned = await self.summon()

            if summoned is not None:
                characters.append(summoned)

            else:
                i -= 1

        return characters

    async def generate(self, name="",
                       image="", characters=""):
        """
        Generate a banner object

        :param name: (`str`)
        :param image: (`str`) Valid url
        :param characters: (`str`)

        --

        :return: `Banner`
        """

        # Init
        getter = CharacterGetter

        # Set the attributes
        self.name = name
        self.image = image
        self.characters = characters

        # Get the character instances
        self.characters = self.characters.split()

        # The character are stored as reference id in the characters[] attribute
        for reference in self.characters:
            await asyncio.sleep(0)

            # Convert the str reference to int
            reference = int(reference)
            character = await getter.get_reference_character(reference)

            # Add the character into the list
            self.characters.append(character)

        # Sort the banner
        await self.sort()

        return self


class BannerGetter:

    # Private
    __database = Database()
    __cache = []
    __cache_ok = False

    # Public
    async def set_cache(self):
        """
        Set the banner cache

        --

        :return: `None`
        """

        if self.__cache_ok is False:
            data = await self.__database.fetch_row("""
                                                   SELECT * 
                                                   FROM portal
                                                   ORDER BY portal_num;
                                                   """)

            if len(data) > 0:
                for banner in data:
                    await asyncio.sleep(0)

                    # Generate the banner object
                    banner_ = Banner()

                    await banner_.generate(name=banner[1], image=banner[3], characters=banner[4])

                    self.__cache.append(banner)

                self.__cache_ok = True
                print("Banner Cache : DONE")

        else:
            print("Banner Cache : The cache has already been filled.")

        return

    async def get_banner(self, reference):
        """
        Return a banner object from the cache

        :param reference: (`int`)

        --

        :return: `Banner` or `None` if not found
        """

        # Get the banner object from the cache
        if reference > 0 and reference < len(self.__cache):
            return self.__cache[reference - 1]

        else:
            print(f"Banner {reference} not found.")
            return None