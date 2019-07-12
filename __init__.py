from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import LOG
import pint
import sympy
ureg = pint.UnitRegistry()

class UnitConversionSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(UnitConversionSkill, self).__init__(name="UnitConversionSkill")

    @intent_file_handler("convert.units.intent")
    def handle_unit_conversion(self, message):
        source=(message.data.get('prefixfrom',"")+message.data['unitfrom']).lstrip("a ")
        target=(message.data.get('prefixto',"")+message.data['unitto']).lstrip("a ")

        count =sympy.S(message.data.get('number',1)) #Convert number to sympy representation
        result = round((count*ureg(source)).to(target),2)
        self.speak_dialog("conversion", {'statement': source, 'result':result})


def create_skill():
    return UnitConversionSkill()
