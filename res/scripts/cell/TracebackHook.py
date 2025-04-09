# -*- coding: utf-8 -*-
import sys
def handle_exception(exc_type, exc_value, exc_traceback):
    import sys
    from CoreObject import MonsterObject
    import NPC
    from ConfigObject.Skill.SkillBase import Skill
    from CoreObject.SpaceObject import SpaceObject
    tb = exc_traceback
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

    infos = []
    while tb is not None:
        f = tb.tb_frame
        if "self" in f.f_locals:
            info = ""
            if isinstance(f.f_locals['self'], MonsterObject.MonsterObject):
                info =  "----(Monster," + f.f_locals["self"].scriptID + " id:" + str(f.f_locals["self"].id) + ")"
            elif isinstance(f.f_locals['self'], NPC.NPC):
                info =  "----(NPC," + f.f_locals["self"].scriptID +" id:" + str(f.f_locals["self"].id )+ ")"
            elif str(f.f_locals['self']).find("Role") != -1:
                info = "----(Role," + f.f_locals["self"].playerName +" id:" + str(f.f_locals["self"].id) + ")"
            elif isinstance(f.f_locals['self'],SpaceObject):
                info = "----(Space," + f.f_locals["self"].scriptID + " spaceID:" + str(f.f_locals["self"].spaceID) + ")"
            elif isinstance(f.f_locals['self'],Skill.Skill):
                info = "----(Skill," +  str(f.f_locals["self"].getID()) + ")"
            if info != "":
                infos.append(info)
        tb = tb.tb_next
    infos = list(set(infos))
    if len(infos) != 0:
        print ("Traceback (most recent call last):")
    for v in infos:
        print( v )
    if len(infos) != 0:
        print ("TypeError: " + str(exc_value))


sys.excepthook = handle_exception
