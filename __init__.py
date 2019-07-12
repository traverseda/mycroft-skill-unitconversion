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
        try:
            result = round((count*ureg(source)).to(target),2)
            self.speak_dialog("conversion", {'statement': source, 'result':result})
        except pint.errors.DimensionalityError as e:
            sourceDimensions = {i.strip("[]") for i in ureg(source).dimensionality.keys()}
            targetDimensions = {i.strip("[]") for i in ureg(target).dimensionality.keys()}
            common = sourceDimensions.intersection(targetDimensions)
            uncommon = (sourceDimensions|targetDimensions).difference(common)
            self.speak_dialog("dimensionalityError", {'dimensions': ", ".join(uncommon),
                                                      "source": source,
                                                      "target": target})
        except pint.errors.UndefinedUnitError as e:
            self.speak_dialog("unknownUnitError",{"units":e.unit_names})



def create_skill():
    return UnitConversionSkill()
