from collections import namedtuple
import pickle

SpellListData = namedtuple('SpellListData', ['spell_name',
                                             'spell_type',
                                             'spell_school',
                                             'spell_range',
                                             'spell_incant',
                                             'spell_materials',
                                             'spell_effects',
                                             'spell_limitations',
                                             'spell_notes',
                                             'is_archetype',
                                             'is_equipment'])

PurchaseListData = namedtuple('PurchaseListData', ['class_name',
                                                   'spell_level',
                                                   'spell_name',
                                                   'spell_cost',
                                                   'spell_max',
                                                   'spell_frequency_number',
                                                   'spell_frequency_type',
                                                   'spell_type',
                                                   'spell_school',
                                                   'spell_range'])


class DisplaySpell:
    def __init__(self, list_data, purchase_data, is_visible=True):
        self.class_name = purchase_data.class_name
        self.spell_level = purchase_data.spell_level
        self.spell_name = purchase_data.spell_name
        self.spell_cost = purchase_data.spell_cost
        self.spell_max = purchase_data.spell_max
        self.spell_frequency_number = purchase_data.spell_frequency_number
        self.spell_freq_type = purchase_data.spell_frequency_type

        self.spell_type = purchase_data.spell_type if purchase_data.spell_type \
            else list_data.spell_type
        self.spell_school = purchase_data.spell_school if purchase_data.spell_school \
            else list_data.spell_school
        self.spell_range = purchase_data.spell_range if purchase_data.spell_range \
            else list_data.spell_range

        self.spell_incant = list_data.spell_incant
        self.spell_materials = list_data.spell_materials  # List of tuples, (number,color,type)
        self.spell_effects = list_data.spell_effects
        self.spell_limitations = list_data.spell_limitations
        self.spell_notes = list_data.spell_notes

        self.is_archetype = list_data.is_archetype
        self.is_equipment = list_data.is_equipment
        self.is_visible = is_visible


class SpellList:
    def __init__(self, spell_list, list_name, player_class, player_level):
        self.spell_list = spell_list
        self.list_name = list_name
        self.player_class = player_class
        self.player_level = player_level

    # TODO make into an iterable using spell_list


class DisplayList:
    def __init__(self, spell_list=None, player_class='', player_level=''):
        self.player_class = player_class
        self.player_level = player_level
        self.look_the_part = True
        self.spell_list = spell_list if spell_list \
            else self.new_list(player_class=player_class, player_level=player_level)
        self.spell_list_data = None  # dict, key=spell name
        self.purchase_list_data = None  # dict, key=(class,level,name)
        self.points_available = {str(level): 0 for level in range(1, 6)}
        self.spells_purchased = {key: 0 for key in self.spell_list.keys()}
        self.load_data()

    def reset_points(self):
        int_player_level = int(self.player_level)
        for level in range(6, 0, -1):
            self.points_available[(str(level))] = 0 if level > int_player_level else \
                5 + self.points_available[str(level + 1)]
            self.points_available[self.player_level] += 1 if self.look_the_part else 0
            for k, v in self.spells_purchased.items():
                self.spells_purchased[k] = 0

    def add_remove_spell(self, spell, buy=True):
        if buy:
            if self.spells_purchased[(spell.spell_level, spell.spell_name)] >= spell.spell_max:
                return f'{spell.spell_name} already at max'
        else:
            if self.spells_purchased[(spell.spell_level, spell.spell_name)] <= 0:
                return
        try:
            if spell.is_archetype:
                self.points_available, self.spells_purchased = self.process_archetypes(spell)
            else:
                self.points_available = self.adjust_points(spell, buy)
        except ValueError:
            return 'Insufficient points available'
        else:
            self.spells_purchased[(spell.spell_level, spell.spell_name)] += 1 if buy else -1

    def process_archetypes(self, spell, buy=True):
        arch_calls = {
            'Combat Caster': self.combat_caster,
            'Derish': self.dervish,
            'Legend': self.legend,
            'Avatar of Nature': self.aon,
            'Ranger': self.ranger,
            'Summoner': self.summoner,
            'Necromancer': self.necro,
            'Priest': self.priest,
            'Warder': self.warder,
            'Battlemage': self.battlemage,
            'Evoker': self.evoker,
            'Warlock': self.warlock
        }
        return arch_calls[spell.spell_name](spell, buy)

    def combat_caster(self, spell, buy=True):
        """"""
        # Does not require an empty hand to cast Magic.
        return self.adjust_points(spell=spell, buy=buy)

    def dervish(self, spell, buy=True):
        temp_points = self.adjust_points(spell, buy)
        temp_purchases = {}
        for temp_spell in self.spell_list:
            if temp_spell.is_equipment:
                if self.spells_purchased[(temp_spell.spell_level, temp_spell.spell_name)] > 0:
                    try:
                        temp_points = self.adjust_points(temp_spell, buy)
                    except ValueError:
                        raise ValueError

        """Equipment costs are doubled. Each Verbal purchased
        gives double the uses. Example: 1/Life Charge x3
        becomes 2/life Charge x3, 2/life becomes 4/life, 1/Refresh
        becomes 2/Refresh."""
        pass

    def legend(self, spell, buy=True):
        pass

    def aon(self, spell, buy=True):
        pass

    def ranger(self, spell, buy=True):
        pass

    def summoner(self, spell, buy=True):
        pass

    def necro(self, spell, buy=True):
        pass

    def priest(self, spell, buy=True):
        pass

    def warder(self, spell, buy=True):
        pass

    def battlemage(self, spell, buy=True):
        pass

    def evoker(self, spell, buy=True):
        pass

    def warlock(self, spell, buy=True):
        pass

    def adjust_points(self, spell, buy=True):
        spent = {k: v for k, v in self.points_available.items()}
        for level in range(0, int(spell.spell_level)):
            if buy:
                spent[str(level)] -= spell.spell_cost
                if spent[str(level)] < 0:
                    raise ValueError
                else:
                    spent[str(level)] += spell.spell_cost
        return spent

    def load_spell_list(self, list_name):
        with open(list_name, 'rb') as list_file:
            self.spell_list = pickle.load(list_file)

    def save_spell_list(self):
        file_name = f'{self.spell_list.player_class}.{self.spell_list.player_level}.{self.spell_list.list_name}.spells'
        with open(file_name, 'wb') as list_file:
            pickle.dump(self.spell_list, list_file)

    def load_data(self):
        with open('data.spells', 'rb') as data_file:
            self.spell_list_data, self.purchase_list_data = pickle.load(data_file)

    def new_list(self, player_class, player_level):
        auto_name_number = 1
        list_name = f'{player_class} List {auto_name_number}'
        spell_list = {(spell.spell_level, spell.spell_name):
                      DisplaySpell(self.spell_list_data[spell.spell_name], spell, int(spell.spell_level)
                      <= int(player_level)) for spell in self.purchase_list_data.values()
                      if spell.class_name == player_class}
        return SpellList(spell_list, list_name, player_class, player_level)
