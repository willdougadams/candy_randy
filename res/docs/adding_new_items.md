# Adding a new item

Add a anew item by creating a new .item file in res/items, then add it to the Game class as the config file for the item.

# Aruments

* location: should probably be removed

* gear_slot: defines which gear slot it will occupy when equppipped
    - head
    - face
    - hand (euipped)
    - hand (wearing)
    - feet
    - torso
    - legs

* damage_*: defines the damage added to a characters base attack damage.
            * _must_ be substituted with a type of damage, for example "damage_normal"
            (the game will generate damage maps for whatever kinds of damage it is given???)

* uses: will be a positive integer for limited use items, or -1 for infinite use items

* weight: the item's weight

* value: the item's value

* length: defined the reach of the weapon in unscaled pixels 

* spritesheet: name of the png file to use for drawing the weapon relative to res/DawnLike

* spritesheet_location: A tuple defining the sprite size offset to grab the image from.
for example if you have a spritesheet with nine weapons on it
laid out 3x3 and you want the one in the center this value would be 
(1, 1).  For a 3x3 sritesheet, the values would be as follows:

          0 1 2
        0 X X X
        1 X X X
        2 X X X 
The size of the srite is defined in the Items class, should probably be moved here.

* attack_type: defines if attacking with this weapon will swing or jab the weapon
    - swing
    - jab