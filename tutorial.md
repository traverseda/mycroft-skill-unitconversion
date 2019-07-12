I've found mycroft's documentation to be less then ideal, so here I'll document
how I made the `skill-unitconversion` skill, which can do things like tell you
how many meters a second 88 miles per hour is.

The first step was installing mycroft. I didn't install the version from the
archlinux package repo as it has some permissions issues. Instead I followed the
guide [here](https://mycroft.ai/documentation/linux/). If you do run into
issues, try running `chown -R :$USER /opt/mycroft/skills /var/log/mycroft` to
make it so that your user can edit those two locations.

(It would be better if mycroft ran on a per-user basis without involving any
system level logging. Perhaps a systemd user service?)

Then you need to download the mycroft-skills repository using
`git clone https://github.com/MycroftAI/mycroft-skills.git`.

Then create a new skill and register it with mycroft.

```
cd mycroft-skills
cp 00__skill_template skill-name-of-my-skill #Create a new skill from template
ln -s $(pwd)/skill-name-of-my-skill /opt/mycroft/skills #Make your skill findable by mycroft
```

You can now start working on your skill in the `skill-name-of-my-skill` folder.
In my example the skill is `skill-unit-conversions`.

Thankfully we don't need to do the actual unit conversions ourselves, we can
load in a python library to do it for us. Unfortunatly since we're not really
installing the skill we're not able to automatically install our python
dependencies.

From your `mycroft-core` directory (as per the installation guide I linked to)
activate the microft virtual env and install
[python-pint](https://pint.readthedocs.io/en/0.9/). We'll also install sympy to
eliminate floating point errors and work with fractions like `1/3rd`.

```
source ./venv-activate.sh
pip install pint sympy
deactivate
```

For deployment you'll need to add your dependencies to `manifest.yaml`, but
we're not going to worry about that until we actually have something production
ready.

We're going to use the [padatious](https://mycroft.ai/documentation/padatious/)
intent parser instead of adapt, it seems to be what people are moving towards
anyway.

First, make sure padatious is available available. In
`skill-yourskill/__init__.py` import the `intent_file_handler`.
`from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler`.

Next we need to create some `.entity` files for our units. Thankfully pint already
has a big list of units, and we're just going to put those in some voc files
without worrying too much if they're actually pronouncable or what.

```
import pint
ureg = pint.UnitRegistry()
ureg._units.keys() #Goes in vocab/en_us/unit.entity
ureg._prefixes.keys() #Goes in vocab/en_us/prefix.entity
```

We only need to run this once since pint units don't change very often. We might
even want to manuelly edit those lists to remove un-pronouncable units, but it's
a good starting point.

Prefixes are words like `kilo` or `mili` and units are words like `meter` or
`gram`.


