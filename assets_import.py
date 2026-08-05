# Auto-generated asset import for an R1 → R2 mod, produced by R1Importer.
#
# Run via:   unrealtool run <this file>
#
# What it does:
#   1. Imports each <name>_stripN.png from R1's sprites/ as a UTexture2D.
#   2. Slices it into N UPaperSprites with per-frame custom pivots derived
#      from R1's sprite_change_offset (see PIVOTS dict). Pivot is offset by
#      source_uv to make it absolute in source-texture space.
#   3. Builds UPaperFlipbook assets per animation at 12 fps default — modder
#      tunes after import.
#   4. Stamps CD_<CHAR> as a Blueprint of URivalsLua2DCharacterData and
#      Char_<CHAR> as URivalsLuaCharacterDefinition pointing at it.
#
# Gaps that need a follow-up pass:
#   * Sound import (USoundWave from sounds/<name>.wav). R1 mods occasionally
#     reference base-game sound names; those resolve via R2 SoundEffectContainer.
#   * State / attack key mapping — the script wires a sensible default based
#     on R1 anim naming; modder edits CD_<CHAR>'s StateFlipbookKeys /
#     AttackFlipbookKeys to refine.

import unreal, os, re

MOD_ID = "3752198977"
CHAR   = "Hodan2"
CHAR_SHORT = (CHAR[:1].upper() + CHAR[1:3].lower()) if CHAR else CHAR
R1_ROOT    = r"D:/SteamLibrary/steamapps/workshop/content/383980/2136440419"
R1_SPRITES = r"D:/SteamLibrary/steamapps/workshop/content/383980/2136440419/sprites"
R1_SOUNDS  = r"D:/SteamLibrary/steamapps/workshop/content/383980/2136440419/sounds"
OUTPUT_ROOT = r"L:/Rivals2/Rivals2SnapNet/Game/Content/ModContent/3752198977"
IMPORT_MODE = "basic"
_ADVANCED = (IMPORT_MODE == "advanced")
_CHAR_DATA_PARENT     = unreal.RivalsR1CharacterData if _ADVANCED else unreal.RivalsLua2DCharacterData
_ARTICLE_DATA_PARENT  = unreal.RivalsR1ArticleData  if _ADVANCED else unreal.RivalsLua2DArticleData
_ARTICLE_ENTITY_CLASS = unreal.RivalsR1ArticleEntity if _ADVANCED else unreal.RivalsLua2DArticleEntity
HUD_ICON_PADDED = r"L:/Rivals2/Rivals2SnapNet/Game/Content/ModContent/3752198977/hud_icon_padded.png"
FMOD_BUILD_GUIDS_DIR = r"L:/Rivals2/Rivals2SnapNet/Tools/R1Importer/FMODBuild/GUIDs"
R1_BASE_SPRITES = os.environ.get('R1_BASE_SPRITES_DIR') or r"L:/Rivals2/Rivals2SnapNet/Tools/R1Importer/Resources/R1BaseSprites"

# Per-sprite origins from R1 load.gml. Keys are case-folded (lower())
# and lookups must lower() too — sprite filenames and load.gml
# sprite_change_offset names can disagree in case.
PIVOTS = {
    "abyss_dattack_strong_flash": (38, 78),
    "abyss_dstrong_strong_flash": (62, 120),
    "abyss_fair_strong_flash": (40, 92),
    "abyss_fspecialflash": (70, 106),
    "abyss_fspecialflash2": (70, 106),
    "abyss_uspecialflash": (78, 124),
    "abyss_uspecialflash2": (78, 124),
    "airdodge": (38, 84),
    "airdodge_back": (46, 84),
    "airdodge_down": (46, 84),
    "airdodge_downback": (46, 84),
    "airdodge_downforward": (46, 84),
    "airdodge_forward": (46, 84),
    "airdodge_up": (46, 84),
    "airdodge_upback": (46, 84),
    "airdodge_upforward": (46, 84),
    "ambitaunt": (36, 120),
    "bair": (60, 92),
    "bighud1": (0, 256),
    "bighud2": (0, 256),
    "bighud3": (0, 256),
    "bighud4": (0, 256),
    "bighud5": (0, 256),
    "bighurt": (38, 66),
    "bouncehurt": (42, 72),
    "crouch": (40, 82),
    "dair": (70, 92),
    "dash": (52, 68),
    "dashstart": (52, 84),
    "dashstop": (42, 70),
    "dashturn": (38, 66),
    "dattack": (38, 78),
    "dattack_strong": (38, 78),
    "dattack_strong_flash": (38, 78),
    "doublejump": (52, 102),
    "downhurt": (42, 72),
    "dspecial": (78, 124),
    "dstrong": (62, 120),
    "dstrong_parry": (62, 120),
    "dstrong_strong_flash": (62, 120),
    "dtilt": (44, 82),
    "fair": (40, 92),
    "fair_strong": (40, 92),
    "fair_strong_flash": (40, 92),
    "fspecial": (70, 106),
    "fspecial_air": (70, 106),
    "fspecial_hitbox": (38, 32),
    "fspecialflash": (70, 106),
    "fspecialflash2": (70, 106),
    "fstrong": (62, 78),
    "ftilt": (56, 90),
    "gb_dattack_strong_flash": (38, 78),
    "gb_dstrong_strong_flash": (62, 120),
    "gb_fair_strong_flash": (40, 92),
    "gb_fspecialflash": (70, 106),
    "gb_fspecialflash2": (70, 106),
    "gb_uspecialflash": (78, 124),
    "gb_uspecialflash2": (78, 124),
    "gigasplash": (110, 148),
    "gold_shine": (7, 7),
    "hit_particle2": (92, 96),
    "hodan_crouch_box": (25, 36),
    "hodan_hurt_box": (25, 65),
    "hurt": (42, 72),
    "hurtground": (42, 72),
    "idle": (36, 76),
    "invishud1": (0, 256),
    "invishud2": (0, 256),
    "invishud3": (0, 256),
    "invishud4": (0, 256),
    "jab": (56, 98),
    "jump": (38, 84),
    "jumpstart": (36, 76),
    "kirby_sweatwhirl": (58, 70),
    "land": (36, 76),
    "landinglag": (36, 76),
    "nair": (52, 86),
    "nspecial": (70, 106),
    "nspecial_air": (70, 106),
    "nspecial_hitbox": (38, 32),
    "parry": (54, 92),
    "plat": (60, 44),
    "pratfall": (44, 80),
    "roll_backward": (60, 74),
    "roll_forward": (60, 74),
    "special_splash": (66, 78),
    "spinhurt": (42, 84),
    "splash": (90, 44),
    "sweatwhirl_charged": (70, 106),
    "sweatwhirl_proj": (38, 32),
    "sweatwhirl_proj_held": (42, 86),
    "sweatwhirl_proj_held_hitbox": (49, 80),
    "sweatwhirl_proj_held_hurt": (42, 76),
    "sweatwhirl_proj_hurt": (38, 32),
    "sweatwhirl_proj2": (42, 38),
    "sweatwhirl_proj2_held": (54, 94),
    "sweatwhirl_proj2_held_hitbox": (54, 90),
    "sweatwhirl_proj2_held_hurt": (54, 90),
    "sweatwhirl_proj2_hitbox": (42, 38),
    "sweatwhirl_proj2_hurt": (42, 38),
    "sweatwhirl_proj3": (72, 50),
    "sweatwhirl_proj3_held": (76, 122),
    "sweatwhirl_proj3_held_hitbox": (76, 114),
    "sweatwhirl_proj3_held_hurt": (76, 114),
    "sweatwhirl_proj3_hitbox": (72, 50),
    "sweatwhirl_proj3_hurt": (72, 50),
    "sweatwhirlhit": (64, 34),
    "taunt": (70, 84),
    "tech": (40, 82),
    "uair": (90, 162),
    "uspecial": (78, 124),
    "uspecialflash": (78, 124),
    "uspecialflash2": (78, 124),
    "ustrong": (88, 264),
    "utilt": (60, 134),
    "vapour_hurt": (126, 86),
    "vapour2_hurt": (126, 86),
    "vapour3_hurt": (126, 86),
    "vapour4_hurt": (126, 86),
    "walk": (36, 84),
    "walkturn": (36, 76),
    "walljump": (51, 102),
    "waveland": (36, 76),
}

# Sprite-mask opaque bboxes (w, h, ox, oy) relative to pivot, for ECB sizing.
BBOXES = {
    "abyss": (30, 30, 0, 0),
    "abyss_dattack_strong_flash": (82, 74, -36, -70),
    "abyss_dstrong_strong_flash": (112, 110, -50, -108),
    "abyss_fair_strong_flash": (104, 92, -36, -88),
    "abyss_fspecialflash": (130, 94, -63, -92),
    "abyss_fspecialflash2": (124, 98, -56, -96),
    "abyss_steamparticle1": (16, 2, 0, 0),
    "abyss_steamparticle2": (24, 2, 0, 0),
    "abyss_steamparticle3": (10, 2, 0, 0),
    "abyss_steamparticle4": (16, 2, 0, 0),
    "abyss_steamparticle5": (2, 16, 0, 0),
    "abyss_steamparticle6": (2, 24, 0, 0),
    "abyss_steamparticle7": (2, 10, 0, 0),
    "abyss_steamparticle8": (2, 16, 0, 0),
    "abyss_uspecialflash": (72, 74, -34, -74),
    "abyss_uspecialflash2": (72, 74, -34, -72),
    "abysssteamparticle3": (10, 2, 0, 0),
    "airdodge": (80, 78, -30, -76),
    "airdodge_back": (80, 78, -38, -76),
    "airdodge_down": (86, 86, -40, -78),
    "airdodge_downback": (78, 78, -36, -76),
    "airdodge_downforward": (78, 78, -38, -76),
    "airdodge_forward": (80, 78, -38, -76),
    "airdodge_up": (86, 86, -40, -78),
    "airdodge_upback": (80, 78, -38, -76),
    "airdodge_upforward": (80, 78, -38, -76),
    "ambitaunt": (78, 122, -36, -120),
    "bair": (106, 82, -58, -72),
    "bair_hurt": (106, 82, 2, 20),
    "bighud1": (224, 242, 0, -242),
    "bighud2": (224, 242, 0, -242),
    "bighud3": (224, 242, 0, -242),
    "bighud4": (224, 242, 0, -242),
    "bighud5": (224, 242, 0, -242),
    "bighurt": (78, 66, -38, -66),
    "bobblehead": (34, 36, 0, 0),
    "bouncehurt": (94, 70, -40, -68),
    "crouch": (72, 76, -32, -74),
    "cursor1": (10, 10, 0, 0),
    "cursor2": (10, 10, 0, 0),
    "cursor3": (10, 10, 0, 0),
    "cursor4": (10, 10, 0, 0),
    "dair": (112, 102, -58, -80),
    "dair_hurt": (110, 98, 14, 12),
    "dash": (90, 68, -48, -66),
    "dashstart": (98, 70, -46, -68),
    "dashstop": (72, 72, -42, -70),
    "dashturn": (74, 68, -38, -66),
    "dattack": (82, 74, -36, -70),
    "dattack_hurt": (82, 74, 2, 8),
    "dattack_strong": (84, 82, -38, -78),
    "dattack_strong_flash": (82, 74, -36, -70),
    "doublejump": (78, 84, -42, -80),
    "downhurt": (78, 72, -42, -72),
    "dspec_jump_mask": (400, 400, 0, 0),
    "dspecial": (104, 138, -40, -110),
    "dspecial_hurt": (82, 114, 40, 38),
    "dstrong": (112, 110, -50, -108),
    "dstrong_hurt": (112, 104, 12, 18),
    "dstrong_parry": (112, 110, -50, -108),
    "dstrong_parry_hurt": (112, 104, 12, 18),
    "dstrong_strong_flash": (112, 110, -50, -108),
    "dtilt": (146, 72, -38, -70),
    "dtilt_hurt": (118, 66, 6, 18),
    "earlyaccess": (26, 28, 0, 0),
    "empty": (0, 0, 0, 0),
    "event": (28, 30, 0, 0),
    "fair": (104, 92, -36, -88),
    "fair_hurt": (104, 92, 4, 4),
    "fair_strong": (106, 98, -36, -88),
    "fair_strong_flash": (104, 92, -36, -88),
    "fair_strong_hurt": (106, 92, 4, 4),
    "fspecial": (130, 94, -62, -92),
    "fspecial_air": (130, 94, -62, -92),
    "fspecial_air_hurt": (102, 94, 12, 14),
    "fspecial_hitbox": (36, 26, -18, -14),
    "fspecial_hurt": (102, 94, 12, 14),
    "fspecialflash": (130, 94, -63, -92),
    "fspecialflash2": (124, 98, -56, -96),
    "fstrong": (100, 76, -56, -74),
    "fstrong_hurt": (96, 76, 10, 4),
    "ftilt": (186, 92, -54, -90),
    "ftilt_hurt": (122, 92, 2, 0),
    "gb_dattack_strong_flash": (82, 74, -36, -70),
    "gb_dstrong_strong_flash": (112, 110, -50, -108),
    "gb_fair_strong_flash": (104, 92, -36, -88),
    "gb_fspecialflash": (130, 94, -63, -92),
    "gb_fspecialflash2": (124, 98, -56, -96),
    "gb_steamparticle1": (16, 2, 0, 0),
    "gb_steamparticle2": (24, 2, 0, 0),
    "gb_steamparticle3": (10, 2, 0, 0),
    "gb_steamparticle4": (16, 2, 0, 0),
    "gb_steamparticle5": (2, 16, 0, 0),
    "gb_steamparticle6": (2, 24, 0, 0),
    "gb_steamparticle7": (2, 10, 0, 0),
    "gb_steamparticle8": (2, 16, 0, 0),
    "gb_uspecialflash": (72, 74, -34, -74),
    "gb_uspecialflash2": (72, 74, -34, -72),
    "gigasplash": (236, 148, -110, -146),
    "gold_outlines": (204, 144, 0, 0),
    "gold_shine": (14, 14, -7, -7),
    "hit_particle1": (34, 8, 0, 12),
    "hit_particle2": (242, 232, -92, -96),
    "hodan_crouch_box": (50, 36, -25, -36),
    "hodan_hurt_box": (50, 65, -25, -65),
    "hodantcoart": (196, 266, 0, 0),
    "hurt": (84, 74, -42, -72),
    "hurtground": (68, 66, -36, -66),
    "idle": (68, 78, -36, -76),
    "invishud1": (224, 242, 0, -242),
    "invishud2": (224, 242, 0, -242),
    "invishud3": (224, 242, 0, -242),
    "invishud4": (224, 242, 0, -242),
    "jab": (118, 100, -56, -98),
    "jab_hurt": (84, 82, 24, 18),
    "jjjjj": (784, 82, 30, 16),
    "jump": (70, 88, -38, -84),
    "jumpstart": (68, 72, -36, -70),
    "kirby_sweatwhirl": (110, 74, -58, -70),
    "kirby_sweatwhirl_hurt": (58, 54, 24, 20),
    "kirbyicon": (22, 20, 0, 0),
    "land": (66, 76, -36, -74),
    "landinglag": (66, 76, -36, -74),
    "nair": (98, 86, -52, -86),
    "nair_hurt": (92, 76, 4, 10),
    "nspecial": (130, 94, -62, -92),
    "nspecial_air": (130, 94, -62, -92),
    "nspecial_air_hurt": (92, 94, 22, 14),
    "nspecial_hitbox": (64, 26, -32, -14),
    "nspecial_hurt": (92, 94, 22, 14),
    "parry": (86, 86, -46, -84),
    "plat": (126, 64, -60, -44),
    "portraitbb": (331, 293, 3, 8),
    "pratfall": (80, 78, -40, -80),
    "premium": (30, 30, 0, 0),
    "roll_backward": (100, 72, -56, -70),
    "roll_forward": (100, 72, -56, -70),
    "special_splash": (124, 48, -66, -48),
    "spinhurt": (84, 84, -42, -84),
    "splash": (158, 44, -80, -44),
    "steamparticle1": (16, 2, 0, 0),
    "steamparticle2": (24, 2, 0, 0),
    "steamparticle3": (10, 2, 0, 0),
    "steamparticle4": (16, 2, 0, 0),
    "steamparticle5": (2, 16, 0, 0),
    "steamparticle6": (2, 24, 0, 0),
    "steamparticle7": (2, 10, 0, 0),
    "steamparticle8": (2, 16, 0, 0),
    "sweatwhirl_charged": (130, 98, -62, -96),
    "sweatwhirl_charged_hurt": (92, 98, 22, 10),
    "sweatwhirl_proj": (72, 56, -38, -32),
    "sweatwhirl_proj2": (84, 66, -42, -38),
    "sweatwhirl_proj2_held": (80, 88, -38, -78),
    "sweatwhirl_proj2_held_hitbox": (6, 6, -1, -31),
    "sweatwhirl_proj2_held_hurt": (68, 68, -32, -61),
    "sweatwhirl_proj2_hitbox": (6, 6, -2, -4),
    "sweatwhirl_proj2_hurt": (70, 36, -34, -20),
    "sweatwhirl_proj3": (124, 88, -72, -50),
    "sweatwhirl_proj3_held": (102, 116, -48, -96),
    "sweatwhirl_proj3_held_hitbox": (4, 4, 3, -32),
    "sweatwhirl_proj3_held_hurt": (99, 99, -44, -78),
    "sweatwhirl_proj3_hitbox": (4, 4, -4, -8),
    "sweatwhirl_proj3_hurt": (88, 48, -42, -30),
    "sweatwhirl_proj_held": (68, 74, -30, -74),
    "sweatwhirl_proj_held_hitbox": (71, 70, -39, -66),
    "sweatwhirl_proj_held_hurt": (59, 59, -26, -57),
    "sweatwhirl_proj_hurt": (42, 24, -20, -14),
    "sweatwhirlhit": (142, 106, -62, -34),
    "taunt": (120, 80, -64, -76),
    "tech": (80, 84, -40, -82),
    "uair": (146, 132, -74, -132),
    "uair_hurt": (72, 96, 60, 66),
    "uspecial": (104, 138, -40, -110),
    "uspecial_hurt": (78, 114, 40, 38),
    "uspecialflash": (72, 74, -34, -74),
    "uspecialflash2": (72, 74, -34, -72),
    "ustrong": (264, 248, -88, -246),
    "ustrong_hurt": (106, 88, 28, 178),
    "utilt": (100, 122, -50, -120),
    "utilt_hurt": (86, 94, 20, 42),
    "vapour2_hurt": (174, 92, -84, -70),
    "vapour3_hurt": (174, 96, -84, -74),
    "vapour4_hurt": (174, 94, -84, -72),
    "vapour_hurt": (198, 114, -84, -78),
    "victory_bg": (480, 270, 0, 0),
    "walk": (68, 82, -30, -80),
    "walkturn": (68, 76, -36, -74),
    "walljump": (84, 82, -41, -88),
    "waveland": (68, 64, -28, -62),
}

# R1 character-physics literals from init.gml (walk_speed, gravity_speed,
# etc). Pre-population for CD_<CHAR>'s movement fields. Modder tunes in editor.
R1_PHYSICS = {
    "ab_hud_x": 0,
    "ab_hud_y": 0,
    "abyssEnabled": 0,
    "air_accel": 0.3,
    "air_dodge_active_frames": 3,
    "air_dodge_recovery_frames": 3,
    "air_dodge_speed": 7.5,
    "air_dodge_startup_frames": 1,
    "air_friction": 0.04,
    "air_hurtbox_spr": -1,
    "air_max_speed": 4,
    "attack_has_b_reversed": 0,
    "attacking": 0,
    "big_hit_length": 40,
    "bighud_frame": 0,
    "bubble_x": 0,
    "bubble_y": 8,
    "burning_bros": 0,
    "burning_bros_init": 0,
    "char_height": 52,
    "colour_hsv": 0,
    "colour_rgb": 0,
    "create_vapour": 0,
    "crouch_active_frames": 8,
    "crouch_anim_speed": 0.16,
    "crouch_recovery_frames": 3,
    "crouch_startup_frames": 3,
    "current_vapours": 0,
    "cursor_anim_speed": 20,
    "cursor_frame": 0,
    "cursor_line": 0,
    "dash_anim_speed": 0.2,
    "dash_speed": 5.75,
    "dash_stop_percent": 0.35,
    "dash_stop_time": 6,
    "dash_turn_accel": 0.65,
    "dash_turn_time": 16,
    "dattack_strong": 0,
    "default_height": 52,
    "displayed_steam_text": 0,
    "djump_speed": 11.75,
    "dodge_active_frames": 1,
    "dodge_recovery_frames": 3,
    "dodge_startup_frames": 1,
    "double_jump_time": 32,
    "dspecial_handspring": 0,
    "dspecial_jc": 0,
    "dspecial_jump_anim_speed": 0.25,
    "dspecial_jump_frames": 6,
    "dspecial_jump_index": 0,
    "dspecial_jump_steam": 0,
    "dspecial_jumped": -1,
    "dspecial_land": 0,
    "dspecial_landing_lag": 10,
    "dspecial_level_2_hit": 0,
    "dspecial_level_3_hit": 0,
    "dspecial_level_3_time": 2,
    "dspecial_throw_speed": 10,
    "dstrong_charged": 0,
    "dstrong_parry": 0,
    "dstrong_parry_frame": 12,
    "enemykirby": -1,
    "fair_strong": 0,
    "fake_dstrong_charge": 0,
    "fast_fall": 16,
    "flash_on": 0,
    "flash_sprite": 0,
    "flash_timing": 4,
    "flash_visible": 0,
    "frame_data": 0,
    "free_time": 0,
    "freeze_switched": 0,
    "fspecial_hspeed": 7,
    "fspecial_time": 30,
    "fspecial_vspeed": -5,
    "fstrong_parry": 0,
    "fstrong_parry_frame": 0,
    "giga_splash_length": 32,
    "god_mode": 0,
    "grabbed": -1,
    "grapple_x": 140,
    "grapple_y": 36,
    "grapple_y_2": 136,
    "grappled": 0,
    "grappled_block": 0,
    "grappled_platform": 0,
    "gravity_speed": 0.6,
    "ground_friction": 0.6,
    "hitbox_view": 0,
    "hitstun_grav": 0.52,
    "hitstun_hurtbox_spr": -1,
    "hud_buffer": 20,
    "hud_h": 236,
    "hud_w": 224,
    "hud_x": 0,
    "hud_y": 0,
    "hue": 0,
    "hue2": 0,
    "idle_anim_speed": 0.16,
    "inf_steam": 0,
    "inf_steam_checker": 0,
    "inf_steam_override": 0,
    "inf_steam_source": 0,
    "info_switched": 0,
    "initial_dash_speed": 6,
    "initial_dash_time": 14,
    "invis_hud": 0,
    "invis_hud_me": 0,
    "invis_hud_other": 0,
    "is_stinky_monke": 1,
    "jab_loop": 0,
    "jab_sound_ongoing": 0,
    "jump_change": 3,
    "jump_speed": 11.5,
    "jump_start_time": 5,
    "kill_steam": 0,
    "kirby_sweatwhirl_anim_speed": 6,
    "kirbyability": 16,
    "knockback_adj": 0.9,
    "land_time": 6,
    "last_nspecial_id": 0,
    "leave_ground_max": 6,
    "line_height": 16,
    "longest_vapour_lifetime": 0,
    "longest_vapour4_lifetime": 0,
    "max_djumps": 1,
    "max_fall": 11,
    "max_jump_hsp": 6,
    "max_vapours": 3,
    "menu_buffered": 0,
    "moonwalk_accel": 1.4,
    "moonwalking": 0,
    "moonwalking_buffer": 0,
    "nair_anim_frame": 0,
    "nair_parry": 0,
    "not_free_time": 0,
    "nspecial_full_time": 100,
    "nspecial_hold_time": 30,
    "nspecial_hspeed": 3,
    "nspecial_recorded": 0,
    "nspecial_thrown": 0,
    "nspecial_thrown_level_2_height": 90,
    "nspecial_thrown_level_2_width": 90,
    "nspecial_thrown_level_3_height": 130,
    "nspecial_thrown_level_3_width": 130,
    "nspecial_time": 40,
    "nspecial_vspeed": 30,
    "old_steam_dir": 0,
    "oldest_sprite_index": 0,
    "orig_air_max_speed": 4,
    "orig_dash_speed": 5.75,
    "orig_djump_speed": 11.75,
    "orig_dstrong_parry_frame": 12,
    "orig_initial_dash_speed": 6,
    "orig_initial_dash_time": 14,
    "orig_jump_change": 3,
    "orig_jump_speed": 11.5,
    "orig_jump_start_time": 5,
    "orig_leave_ground_max": 6,
    "orig_max_jump_hsp": 6,
    "orig_moonwalk_accel": 1.4,
    "orig_short_hop_speed": 7.4,
    "orig_steam_charge": 0.04,
    "orig_vapour_length": 10000,
    "orig_walk_accel": 0.2,
    "orig_walk_speed": 3,
    "parried_sweatwhirl_hitpause": 0,
    "parry_debug_view": 0,
    "parry_is_dstrong": 0,
    "parry_radius": 40,
    "parry_sweatwhirl_hit": 0,
    "parry_window_timer": 0,
    "parry_x_offset": 0,
    "parry_y_offset": 60,
    "paused": 0,
    "player_info": 0,
    "practice_mode": 0,
    "prat_fall_accel": 0.7,
    "prat_land_time": 26,
    "pratfall_anim_speed": 0.25,
    "proj_eat_timer": 0,
    "proj_eat_timer_max": 8,
    "rainbow": 0,
    "rainbow_window": 60,
    "roll_back_active_frames": 4,
    "roll_back_recovery_frames": 2,
    "roll_back_startup_frames": 2,
    "roll_backward_max": 9,
    "roll_forward_active_frames": 4,
    "roll_forward_max": 9,
    "roll_forward_recovery_frames": 1,
    "roll_forward_startup_frames": 1,
    "runeA": 0,
    "runeB": 0,
    "runeC": 0,
    "runeD": 0,
    "runeE": 0,
    "runeF": 0,
    "runeG": 0,
    "runeH": 0,
    "runeI": 0,
    "runeJ": 0,
    "runeK": 0,
    "runeL": 0,
    "runeM": 0,
    "runeN": 0,
    "runeO": 0,
    "runesUpdated": 0,
    "short_hop_speed": 7.4,
    "slam_hit": 0,
    "somersault_charged": 0,
    "somersault_easing": 1,
    "special_splash_length": 20,
    "splash_created": 0,
    "splash_length": 12,
    "starting_grapple_x": -10,
    "starting_grapple_y": 136,
    "starting_grapple_y_2": 236,
    "steam": 0,
    "steam_appearance_odds": 7,
    "steam_buffer": 0,
    "steam_buffer_max": 10,
    "steam_charge": 0.04,
    "steam_decay": 0.08,
    "steam_dir": 0,
    "steam_line_lifetime": 25,
    "steam_line_max_frames": 25,
    "steam_red_colour": 70,
    "steam_sfx_played": 0,
    "steam_sprites": 4,
    "steam_vis_per": 0.7,
    "swallowed": -1,
    "sweatwhirl_anim_speed": 6,
    "sweatwhirl_bashed": 0,
    "sweatwhirl_charged": 0,
    "sweatwhirl_charged_hit": 0,
    "sweatwhirl_charged_hspeed": 11,
    "sweatwhirl_charged_speed": 4,
    "sweatwhirl_charged_vspeed": 0,
    "sweatwhirl_cooldown_time": 0,
    "sweatwhirl_exists": 0,
    "sweatwhirl_float_speed": -3,
    "sweatwhirl_grabbed": 0,
    "sweatwhirl_gravity": 0.4,
    "sweatwhirl_held_frame": 0,
    "sweatwhirl_hitpause": 0,
    "sweatwhirl_hitpause_frames": -1,
    "sweatwhirl_length": 19,
    "sweatwhirl_level": 1,
    "sweatwhirl_level_2_width": 80,
    "sweatwhirl_level_3_timer": -1,
    "sweatwhirl_level_3_timing": 10,
    "sweatwhirl_level_3_width": 120,
    "sweatwhirl_leveled_hit": 0,
    "sweatwhirl_leveled_hit_reset": 20,
    "sweatwhirl_leveled_hit_time": 0,
    "sweatwhirl_looped": 0,
    "sweatwhirl_max_frames": 6,
    "sweatwhirl_max_hitpause": 10,
    "sweatwhirl_noncharged_speed": 6,
    "sweatwhirl_old_hsp": 0,
    "sweatwhirl_old_vsp": 0,
    "sweatwhirl_parry_player": 0,
    "sweatwhirl_starting_dir": 0,
    "sweatwhirl_startup_anim_frames": 3,
    "sweatwhirl_startup_frames": 10,
    "taunt_angle": 0,
    "taunt_buffered": 0,
    "taunt_direction": -1,
    "taunt_frozen": 1,
    "taunt_max": 4,
    "taunt_menu": 0,
    "taunt_speed": 0.1,
    "taunt_switched": 0,
    "tech_active_frames": 3,
    "tech_recovery_frames": 1,
    "techroll_active_frames": 2,
    "techroll_recovery_frames": 2,
    "techroll_speed": 10,
    "techroll_startup_frames": 2,
    "throw_frame": 12,
    "trail_frames": 6,
    "trummelcodecneeded": 0,
    "uair_count": 0,
    "uair_speed": -3,
    "uspecial_landing_lag": 17,
    "ustrong_parry": 0,
    "ustrong_parry_frame": 10,
    "utilt_height": 74,
    "v_steam": 0,
    "v_steam_buffer": 0,
    "v_steam_dir": 0,
    "vapour_down": 90,
    "vapour_left": -66,
    "vapour_length": 10000,
    "vapour_right": 78,
    "vapour_up": -64,
    "vapour1_exists": 0,
    "vapour2_exists": 0,
    "vapour3_exists": 0,
    "vapour4_count": 0,
    "vapour4_exists": 0,
    "vapour4_time": 0,
    "walk_accel": 0.2,
    "walk_anim_speed": 0.125,
    "walk_speed": 3,
    "walk_turn_time": 6,
    "wall_frames": 2,
    "walljump_hsp": 7,
    "walljump_time": 32,
    "walljump_vsp": 8,
    "wave_friction": 0.12,
    "wave_land_adj": 1.35,
    "wave_land_time": 8,
    "x_inc": 50,
    "y_inc": 50,
}

# R1 config.ini metadata.
R1_CONFIG = {
    "name": "Hodan",
    "description": "oo oo aa aa",
    "author": "team NeRVe",
    "url": "2136440419",
    "major version": "3",
    "minor version": "4",
    "bg color": "water",
}

# R1 per-attack data extracted at import time.
R1_ATTACKS = {
    "AT_BAIR": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 1,
            "AG_HAS_LANDING_LAG": 1,
            "AG_LANDING_LAG": 4,
            "AG_NUM_WINDOWS": 4,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "bair_hurt",
            "AG_SPRITE": "bair",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 5,
                    "AG_WINDOW_SFX_FRAME": 4,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 1,
                    "AG_WINDOW_ANIM_FRAMES": 4,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 12,
                    "AG_WINDOW_SFX_FRAME": 11,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium2",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 5,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_LENGTH": 3,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 6,
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 9,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 75,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 6,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 4,
                    "HG_HEIGHT": 50,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": -20,
                    "HG_HITBOX_Y": -20,
                    "HG_HITPAUSE_SCALING": 0.4,
                    "HG_KNOCKBACK_SCALING": 0.5,
                    "HG_LIFETIME": 3,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 84,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_weak1",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 70,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 5,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 6,
                    "HG_HEIGHT": 70,
                    "HG_HITBOX_GROUP": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": -32,
                    "HG_HITBOX_Y": -34,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.5,
                    "HG_LIFETIME": 3,
                    "HG_PRIORITY": 2,
                    "HG_VISUAL_EFFECT": 305,
                    "HG_WIDTH": 50,
                    "HG_WINDOW": 3,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium3",
                },
            },
        },
    },
    "AT_DAIR": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 1,
            "AG_HAS_LANDING_LAG": 1,
            "AG_LANDING_LAG": 8,
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "dair_hurt",
            "AG_SPRITE": "dair",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 16,
                    "AG_WINDOW_SFX_FRAME": 15,
                    "AG_WINDOW_VSPEED": -1,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium2",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 5,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_LENGTH": 4,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 6,
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 15,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 45,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 8,
                    "HG_DAMAGE": 8,
                    "HG_HEIGHT": 76,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 0,
                    "HG_HITBOX_Y": -24,
                    "HG_HITPAUSE_SCALING": 0.75,
                    "HG_KNOCKBACK_SCALING": 0.6,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 90,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 270,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 13,
                    "HG_HEIGHT": 10,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 0,
                    "HG_HITBOX_Y": 13,
                    "HG_HITPAUSE_SCALING": 0.65,
                    "HG_KNOCKBACK_SCALING": 0.65,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 2,
                    "HG_WIDTH": 10,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium3",
                },
            },
        },
    },
    "AT_DATTACK": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 2,
            "AG_NUM_WINDOWS": 3,
            "AG_OFF_LEDGE": 1,
            "AG_USES_CUSTOM_GRAVITY": 1,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "dattack_hurt",
            "AG_SPRITE": "dattack",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_HSPEED": 7,
                    "AG_WINDOW_HSPEED_TYPE": 1,
                    "AG_WINDOW_LENGTH": 9,
                    "AG_WINDOW_SFX_FRAME": 7,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 4,
                    "AG_WINDOW_CUSTOM_AIR_FRICTION": 0.2,
                    "AG_WINDOW_CUSTOM_GRAVITY": 0.4,
                    "AG_WINDOW_CUSTOM_GROUND_FRICTION": 0.2,
                    "AG_WINDOW_HAS_CUSTOM_FRICTION": 1,
                    "AG_WINDOW_LENGTH": 15,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 6,
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_CUSTOM_GRAVITY": 0.6,
                    "AG_WINDOW_CUSTOM_GROUND_FRICTION": 0.3,
                    "AG_WINDOW_HAS_CUSTOM_FRICTION": 1,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 10,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 55,
                    "HG_BASE_HITPAUSE": 7,
                    "HG_BASE_KNOCKBACK": 7,
                    "HG_DAMAGE": 8,
                    "HG_HEIGHT": 56,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 20,
                    "HG_HITBOX_Y": -30,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.45,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 56,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium2",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 45,
                    "HG_BASE_HITPAUSE": 5,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 6,
                    "HG_HEIGHT": 46,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 20,
                    "HG_HITBOX_Y": -30,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.6,
                    "HG_LIFETIME": 11,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 46,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 4,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
        },
    },
    "AT_DSPECIAL": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 2,
            "AG_NUM_WINDOWS": 3,
            "AG_OFF_LEDGE": 1,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "dspecial_hurt",
            "AG_SPRITE": "dspecial",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 3,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 7,
                    "AG_WINDOW_SFX_FRAME": 4,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 4,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HSPEED": 6,
                    "AG_WINDOW_HSPEED_TYPE": 2,
                    "AG_WINDOW_LENGTH": 16,
                    "AG_WINDOW_VSPEED": -8,
                    "AG_WINDOW_VSPEED_TYPE": 2,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 9,
                    "AG_WINDOW_ANIM_FRAMES": 7,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 13,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 16,
                    "AG_WINDOW_ANIM_FRAMES": 6,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 16,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 50,
                    "HG_BASE_HITPAUSE": 6,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 6,
                    "HG_HEIGHT": 84,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 2,
                    "HG_HITBOX_Y": -36,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.5,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 2,
                    "HG_VISUAL_EFFECT": 305,
                    "HG_WIDTH": 84,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 70,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 5,
                    "HG_DAMAGE": 4,
                    "HG_FINAL_BASE_KNOCKBACK": 3,
                    "HG_HEIGHT": 70,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 2,
                    "HG_HITBOX_Y": -36,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.4,
                    "HG_LIFETIME": 24,
                    "HG_PRIORITY": 2,
                    "HG_WIDTH": 70,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 4,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_weak2",
                },
            },
            3: {
                "num": {
                    "HG_ANGLE": 0,
                    "HG_ANGLE_FLIPPER": 9,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 3,
                    "HG_HEIGHT": 84,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_GROUP": -1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 2,
                    "HG_HITBOX_Y": -36,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 3,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WIDTH": 84,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam1",
                },
            },
            4: {
                "num": {
                    "HG_ANGLE": 0,
                    "HG_ANGLE_FLIPPER": 9,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 2,
                    "HG_HEIGHT": 120,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_GROUP": 2,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 2,
                    "HG_HITBOX_Y": -36,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 1,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WIDTH": 120,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam1",
                },
            },
            5: {
                "num": {
                    "HG_ANGLE": 270,
                    "HG_BASE_HITPAUSE": 6,
                    "HG_BASE_KNOCKBACK": 7,
                    "HG_DAMAGE": 4,
                    "HG_HEIGHT": 40,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 14,
                    "HG_HITBOX_Y": 6,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.4,
                    "HG_LIFETIME": 6,
                    "HG_PRIORITY": 2,
                    "HG_WIDTH": 40,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium2",
                },
            },
        },
    },
    "AT_DSTRONG": {
        "num_hitboxes": 3,
        "attr_num": {
            "AG_NUM_WINDOWS": 4,
            "AG_STRONG_CHARGE_WINDOW": 1,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "dstrong_hurt",
            "AG_SPRITE": "dstrong",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 4,
                },
                "str": {
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 1,
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 15,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_heavy2",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 4,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_LENGTH": 6,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 5,
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 18,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 45,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 10,
                    "HG_BASE_KNOCKBACK": 8.5,
                    "HG_DAMAGE": 16,
                    "HG_EXTRA_CAMERA_SHAKE": 1,
                    "HG_HEIGHT": 40,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 4,
                    "HG_HITBOX_Y": -12,
                    "HG_HITPAUSE_SCALING": 1,
                    "HG_KNOCKBACK_SCALING": 1.15,
                    "HG_LIFETIME": 6,
                    "HG_PRIORITY": 7,
                    "HG_SHAPE": 2,
                    "HG_VISUAL_EFFECT": 304,
                    "HG_WIDTH": 100,
                    "HG_WINDOW": 3,
                    "HG_WINDOW_CREATION_FRAME": 0,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy1",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 45,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 10,
                    "HG_BASE_KNOCKBACK": 8.5,
                    "HG_DAMAGE": 14,
                    "HG_HEIGHT": 120,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 8,
                    "HG_HITBOX_Y": -34,
                    "HG_HITPAUSE_SCALING": 1,
                    "HG_KNOCKBACK_SCALING": 1.05,
                    "HG_LIFETIME": 16,
                    "HG_PRIORITY": 6,
                    "HG_VISUAL_EFFECT": 304,
                    "HG_WIDTH": 120,
                    "HG_WINDOW_CREATION_FRAME": 1,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "HG_ANGLE": 45,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 8.5,
                    "HG_DAMAGE": 10,
                    "HG_HEIGHT": 180,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 8,
                    "HG_HITBOX_Y": -58,
                    "HG_HITPAUSE_SCALING": 1,
                    "HG_KNOCKBACK_SCALING": 0.95,
                    "HG_LIFETIME": 9,
                    "HG_PRIORITY": 5,
                    "HG_WIDTH": 180,
                    "HG_WINDOW_CREATION_FRAME": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_b_heavy2",
                },
            },
        },
    },
    "AT_DTILT": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "dtilt_hurt",
            "AG_SPRITE": "dtilt",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 5,
                    "AG_WINDOW_SFX_FRAME": 1,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_weak2",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_LENGTH": 4,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 4,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 8,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 2,
                    "HG_HEIGHT": 30,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 72,
                    "HG_HITBOX_Y": -12,
                    "HG_HITPAUSE_SCALING": 0,
                    "HG_HITSTUN_MULTIPLIER": 1.5,
                    "HG_KNOCKBACK_SCALING": 0,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 60,
                    "HG_WINDOW": 2,
                },
                "str": {
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 7,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 5,
                    "HG_HEIGHT": 30,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 54,
                    "HG_HITBOX_Y": -12,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.45,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 2,
                    "HG_WIDTH": 50,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_weak2",
                },
            },
        },
    },
    "AT_FAIR": {
        "num_hitboxes": 1,
        "attr_num": {
            "AG_CATEGORY": 1,
            "AG_HAS_LANDING_LAG": 1,
            "AG_LANDING_LAG": 4,
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "fair_hurt",
            "AG_SPRITE": "fair",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 6,
                    "AG_WINDOW_SFX_FRAME": 5,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium2",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_LENGTH": 2,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 3,
                    "AG_WINDOW_ANIM_FRAMES": 4,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 10,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 40,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 6,
                    "HG_HEIGHT": 64,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 40,
                    "HG_HITBOX_Y": -26,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.45,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 72,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium2",
                },
            },
        },
    },
    "AT_FSPECIAL": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 2,
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_AIR_SPRITE": "fspecial_air",
            "AG_HURTBOX_AIR_SPRITE": "fspecial_air_hurt",
            "AG_HURTBOX_SPRITE": "fspecial_hurt",
            "AG_SPRITE": "fspecial",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 20,
                    "AG_WINDOW_SFX_FRAME": 11,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_heavy1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 3,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 6,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_stinky_steam2",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 5,
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_LENGTH": 20,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 50,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 7,
                    "HG_DAMAGE": 3,
                    "HG_HITBOX_TYPE": 2,
                    "HG_HITBOX_X": 32,
                    "HG_HITBOX_Y": -38,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_HITSTUN_MULTIPLIER": 0.5,
                    "HG_KNOCKBACK_SCALING": 0.2,
                    "HG_LIFETIME": 200,
                    "HG_PRIORITY": 1,
                    "HG_PROJECTILE_ANIM_SPEED": 0,
                    "HG_PROJECTILE_DOES_NOT_REFLECT": 0,
                    "HG_PROJECTILE_ENEMY_BEHAVIOR": 0,
                    "HG_PROJECTILE_IS_TRANSCENDENT": 0,
                    "HG_PROJECTILE_PARRY_STUN": 0,
                    "HG_PROJECTILE_WALL_BEHAVIOR": 0,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam1",
                    "HG_PROJECTILE_MASK": "fspecial_hitbox",
                    "HG_PROJECTILE_SPRITE": "sweatwhirl_proj_hurt",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 55,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 1,
                    "HG_HEIGHT": 40,
                    "HG_HITBOX_TYPE": 2,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_HITSTUN_MULTIPLIER": 0.7,
                    "HG_KNOCKBACK_SCALING": 0.4,
                    "HG_LIFETIME": 3,
                    "HG_PRIORITY": 1,
                    "HG_PROJECTILE_ANIM_SPEED": 0.6,
                    "HG_PROJECTILE_DOES_NOT_REFLECT": 0,
                    "HG_PROJECTILE_ENEMY_BEHAVIOR": 0,
                    "HG_PROJECTILE_IS_TRANSCENDENT": 1,
                    "HG_PROJECTILE_MASK": -1,
                    "HG_PROJECTILE_PARRY_STUN": 0,
                    "HG_PROJECTILE_WALL_BEHAVIOR": 0,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_VISUAL_EFFECT_X_OFFSET": 15,
                    "HG_WIDTH": 40,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam2",
                    "HG_PROJECTILE_SPRITE": "empty",
                },
            },
        },
    },
    "AT_FSTRONG": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_NUM_WINDOWS": 4,
            "AG_STRONG_CHARGE_WINDOW": 1,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "fstrong_hurt",
            "AG_SPRITE": "fstrong",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 16,
                },
                "str": {
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 3,
                    "AG_WINDOW_SFX_FRAME": 2,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_heavy2",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 3,
                    "AG_WINDOW_ANIM_FRAMES": 4,
                    "AG_WINDOW_HSPEED": 10,
                    "AG_WINDOW_LENGTH": 10,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 6,
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 16,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 50,
                    "HG_BASE_HITPAUSE": 10,
                    "HG_BASE_KNOCKBACK": 9,
                    "HG_DAMAGE": 15,
                    "HG_HEIGHT": 62,
                    "HG_HIT_LOCKOUT": 10,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 20,
                    "HG_HITBOX_Y": -34,
                    "HG_HITPAUSE_SCALING": 0.5,
                    "HG_KNOCKBACK_SCALING": 1.15,
                    "HG_PRIORITY": 4,
                    "HG_VISUAL_EFFECT": 304,
                    "HG_WIDTH": 60,
                    "HG_WINDOW": 3,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy2",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 10,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 13,
                    "HG_FINAL_BASE_KNOCKBACK": 2,
                    "HG_HEIGHT": 46,
                    "HG_HIT_LOCKOUT": 10,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 28,
                    "HG_HITBOX_Y": -16,
                    "HG_HITPAUSE_SCALING": 0.75,
                    "HG_KNOCKBACK_SCALING": 1,
                    "HG_PRIORITY": 5,
                    "HG_SHAPE": 2,
                    "HG_WIDTH": 46,
                    "HG_WINDOW": 3,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy1",
                },
            },
        },
    },
    "AT_FTILT": {
        "num_hitboxes": 4,
        "attr_num": {
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "ftilt_hurt",
            "AG_SPRITE": "ftilt",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 6,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 17,
                    "AG_WINDOW_SFX_FRAME": 16,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_stinky_whip",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 6,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HITPAUSE_FRAME": 7,
                    "AG_WINDOW_LENGTH": 2,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 8,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 12,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 2,
                    "HG_HEIGHT": 50,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 52,
                    "HG_HITBOX_Y": -69,
                    "HG_HITSTUN_MULTIPLIER": 1.5,
                    "HG_KNOCKBACK_SCALING": 0,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 70,
                    "HG_WINDOW": 2,
                },
                "str": {
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 2,
                    "HG_HEIGHT": 100,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 88,
                    "HG_HITBOX_Y": -44,
                    "HG_HITSTUN_MULTIPLIER": 1.5,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 90,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 1,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "HG_ANGLE": 55,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 9,
                    "HG_DAMAGE": 7,
                    "HG_HEIGHT": 62,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 44,
                    "HG_HITBOX_Y": -32,
                    "HG_HITPAUSE_SCALING": 0.35,
                    "HG_KNOCKBACK_SCALING": 0.2,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 3,
                    "HG_WIDTH": 88,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
            4: {
                "num": {
                    "HG_ANGLE": 50,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 11,
                    "HG_DAMAGE": 9,
                    "HG_HEIGHT": 30,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 90,
                    "HG_HITBOX_Y": -38,
                    "HG_HITPAUSE_SCALING": 0.75,
                    "HG_KNOCKBACK_SCALING": 0.7,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 2,
                    "HG_VISUAL_EFFECT": 305,
                    "HG_WIDTH": 30,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 1,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy2",
                },
            },
        },
    },
    "AT_JAB": {
        "num_hitboxes": 3,
        "attr_num": {
            "AG_NUM_WINDOWS": 4,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "jab_hurt",
            "AG_SPRITE": "jab",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 5,
                    "AG_WINDOW_SFX_FRAME": 2,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium2",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 1,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_CANCEL_FRAME": 4,
                    "AG_WINDOW_CANCEL_TYPE": 1,
                    "AG_WINDOW_LENGTH": 4,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 6,
                    "AG_WINDOW_LENGTH": 16,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 8,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 7,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_ANGLE_FLIPPER": 5,
                    "HG_BASE_HITPAUSE": 6,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 4,
                    "HG_FORCE_FLINCH": 1,
                    "HG_HEIGHT": 70,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 20,
                    "HG_HITBOX_Y": -30,
                    "HG_HITPAUSE_SCALING": 0,
                    "HG_KNOCKBACK_SCALING": 0,
                    "HG_LIFETIME": 6,
                    "HG_PRIORITY": 3,
                    "HG_WIDTH": 56,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_weak2",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 2,
                    "HG_DAMAGE": 1,
                    "HG_EXTRA_HITPAUSE": 6,
                    "HG_HEIGHT": 80,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_GROUP": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": -10,
                    "HG_HITBOX_Y": -38,
                    "HG_HITPAUSE_SCALING": 0,
                    "HG_KNOCKBACK_SCALING": 0,
                    "HG_LIFETIME": 8,
                    "HG_PRIORITY": 3,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WIDTH": 80,
                    "HG_WINDOW": 3,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam1",
                },
            },
            3: {
                "num": {
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_GROUP": 2,
                    "HG_HITBOX_X": 24,
                    "HG_HITBOX_Y": -38,
                    "HG_LIFETIME": 8,
                    "HG_PARENT_HITBOX": 2,
                    "HG_WINDOW": 3,
                    "HG_WINDOW_CREATION_FRAME": 8,
                },
                "str": {
                },
            },
        },
    },
    "AT_NAIR": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 1,
            "AG_HAS_LANDING_LAG": 1,
            "AG_LANDING_LAG": 5,
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "nair_hurt",
            "AG_SPRITE": "nair",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 7,
                    "AG_WINDOW_SFX_FRAME": 6,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 3,
                    "AG_WINDOW_ANIM_FRAMES": 12,
                    "AG_WINDOW_LENGTH": 40,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 16,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 5,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 60,
                    "HG_BASE_HITPAUSE": 7,
                    "HG_BASE_KNOCKBACK": 8,
                    "HG_DAMAGE": 5,
                    "HG_HEIGHT": 66,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 0,
                    "HG_HITBOX_Y": -34,
                    "HG_HITPAUSE_SCALING": 0.5,
                    "HG_KNOCKBACK_SCALING": 0.5,
                    "HG_LIFETIME": 11,
                    "HG_PRIORITY": 1,
                    "HG_VISUAL_EFFECT": 304,
                    "HG_WIDTH": 66,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium2",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 60,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 3,
                    "HG_DAMAGE": 4,
                    "HG_HEIGHT": 66,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 0,
                    "HG_HITBOX_Y": -34,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.3,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 66,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 11,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
            3: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 1,
                    "HG_HEIGHT": 60,
                    "HG_HITBOX_GROUP": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 0,
                    "HG_HITBOX_Y": -20,
                    "HG_HITSTUN_MULTIPLIER": 1.5,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 1,
                    "HG_SHAPE": 2,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WIDTH": 120,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam1",
                },
            },
        },
    },
    "AT_NSPECIAL": {
        "num_hitboxes": 1,
        "attr_num": {
            "AG_CATEGORY": 2,
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_AIR_SPRITE": "nspecial_air",
            "AG_HURTBOX_AIR_SPRITE": "nspecial_air_hurt",
            "AG_HURTBOX_SPRITE": "nspecial_hurt",
            "AG_SPRITE": "nspecial",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 20,
                    "AG_WINDOW_SFX_FRAME": 11,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_heavy1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 3,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 6,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_stinky_steam1",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 5,
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_LENGTH": 20,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 60,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 5,
                    "HG_DAMAGE": 2,
                    "HG_HITBOX_TYPE": 2,
                    "HG_HITBOX_X": 32,
                    "HG_HITBOX_Y": -38,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_HITSTUN_MULTIPLIER": 0.5,
                    "HG_IGNORES_PROJECTILES": 1,
                    "HG_KNOCKBACK_SCALING": 0.1,
                    "HG_LIFETIME": 900,
                    "HG_PRIORITY": 1,
                    "HG_PROJECTILE_ANIM_SPEED": 0,
                    "HG_PROJECTILE_DOES_NOT_REFLECT": 0,
                    "HG_PROJECTILE_ENEMY_BEHAVIOR": 0,
                    "HG_PROJECTILE_IS_TRANSCENDENT": 1,
                    "HG_PROJECTILE_PARRY_STUN": 0,
                    "HG_PROJECTILE_WALL_BEHAVIOR": 0,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam2",
                    "HG_PROJECTILE_MASK": "nspecial_hitbox",
                    "HG_PROJECTILE_SPRITE": "sweatwhirl_proj_hurt",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 55,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 1,
                    "HG_HEIGHT": 40,
                    "HG_HITBOX_TYPE": 2,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_HITSTUN_MULTIPLIER": 0.7,
                    "HG_KNOCKBACK_SCALING": 0.4,
                    "HG_LIFETIME": 3,
                    "HG_PRIORITY": 1,
                    "HG_PROJECTILE_ANIM_SPEED": 0.6,
                    "HG_PROJECTILE_DOES_NOT_REFLECT": 1,
                    "HG_PROJECTILE_ENEMY_BEHAVIOR": 1,
                    "HG_PROJECTILE_IS_TRANSCENDENT": 1,
                    "HG_PROJECTILE_MASK": -1,
                    "HG_PROJECTILE_PARRY_STUN": 0,
                    "HG_PROJECTILE_WALL_BEHAVIOR": 1,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WIDTH": 40,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam2",
                    "HG_PROJECTILE_SPRITE": "empty",
                },
            },
            3: {
                "num": {
                    "HG_ANGLE": 90,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 1,
                    "HG_HEIGHT": 80,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_GROUP": -1,
                    "HG_HITBOX_TYPE": 2,
                    "HG_HITSTUN_MULTIPLIER": 3,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 1,
                    "HG_PROJECTILE_ANIM_SPEED": 0.6,
                    "HG_PROJECTILE_DOES_NOT_REFLECT": 1,
                    "HG_PROJECTILE_ENEMY_BEHAVIOR": 1,
                    "HG_PROJECTILE_IS_TRANSCENDENT": 1,
                    "HG_PROJECTILE_MASK": -1,
                    "HG_PROJECTILE_PARRY_STUN": 0,
                    "HG_PROJECTILE_WALL_BEHAVIOR": 1,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_WIDTH": 80,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam2",
                    "HG_PROJECTILE_SPRITE": "empty",
                },
            },
            4: {
                "num": {
                    "HG_ANGLE": 0,
                    "HG_ANGLE_FLIPPER": 9,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 1,
                    "HG_HEIGHT": 50,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_GROUP": -1,
                    "HG_HITBOX_TYPE": 2,
                    "HG_HITSTUN_MULTIPLIER": 1,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 1,
                    "HG_PROJECTILE_ANIM_SPEED": 0.6,
                    "HG_PROJECTILE_DOES_NOT_REFLECT": 1,
                    "HG_PROJECTILE_ENEMY_BEHAVIOR": 1,
                    "HG_PROJECTILE_IS_TRANSCENDENT": 1,
                    "HG_PROJECTILE_MASK": -1,
                    "HG_PROJECTILE_PARRY_STUN": 0,
                    "HG_PROJECTILE_WALL_BEHAVIOR": 1,
                    "HG_SDI_MULTIPLIER": 0.01,
                    "HG_TECHABLE": 1,
                    "HG_VISUAL_EFFECT": 6,
                    "HG_VISUAL_EFFECT_X_OFFSET": 15,
                    "HG_WIDTH": 80,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_stinky_steam2",
                    "HG_PROJECTILE_SPRITE": "empty",
                },
            },
        },
    },
    "AT_TAUNT": {
        "num_hitboxes": 0,
        "attr_num": {
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "hodan_hurt_box",
            "AG_SPRITE": "taunt",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 6,
                    "AG_WINDOW_SFX_FRAME": 5,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_weak2",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 12,
                    "AG_WINDOW_LENGTH": 48,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 14,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_LENGTH": 9,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
        },
    },
    "AT_TAUNT_2": {
        "num_hitboxes": 0,
        "attr_num": {
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "hodan_hurt_box",
            "AG_SPRITE": "ambitaunt",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 13,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 42,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_weak1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 13,
                    "AG_WINDOW_ANIM_FRAMES": 6,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 24,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_orca_bite",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 19,
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_LENGTH": 14,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
        },
    },
    "AT_UAIR": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 1,
            "AG_HAS_LANDING_LAG": 1,
            "AG_LANDING_LAG": 4,
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "uair_hurt",
            "AG_SPRITE": "uair",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 8,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_weak1",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 1,
                    "AG_WINDOW_ANIM_FRAMES": 4,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 16,
                    "AG_WINDOW_SFX_FRAME": 5,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_weak2",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 5,
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 15,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 140,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 3,
                    "HG_HEIGHT": 52,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 28,
                    "HG_HITBOX_Y": -108,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.4,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 82,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_weak1",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 40,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 3,
                    "HG_HEIGHT": 52,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_GROUP": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": -34,
                    "HG_HITBOX_Y": -108,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.4,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 82,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 8,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_weak2",
                },
            },
        },
    },
    "AT_USPECIAL": {
        "num_hitboxes": 2,
        "attr_num": {
            "AG_CATEGORY": 2,
            "AG_NUM_WINDOWS": 3,
            "AG_OFF_LEDGE": 1,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "uspecial_hurt",
            "AG_SPRITE": "uspecial",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 8,
                    "AG_WINDOW_SFX_FRAME": 7,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_heavy2",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 1,
                    "AG_WINDOW_ANIM_FRAMES": 1,
                    "AG_WINDOW_HSPEED": 7,
                    "AG_WINDOW_HSPEED_TYPE": 2,
                    "AG_WINDOW_LENGTH": 30,
                    "AG_WINDOW_VSPEED": -14,
                    "AG_WINDOW_VSPEED_TYPE": 2,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 6,
                    "AG_WINDOW_ANIM_FRAMES": 10,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 28,
                    "AG_WINDOW_TYPE": 7,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 16,
                    "AG_WINDOW_ANIM_FRAMES": 6,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 16,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 60,
                    "HG_BASE_HITPAUSE": 10,
                    "HG_BASE_KNOCKBACK": 9,
                    "HG_DAMAGE": 10,
                    "HG_HEIGHT": 84,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 2,
                    "HG_HITBOX_Y": -36,
                    "HG_HITPAUSE_SCALING": 0.6,
                    "HG_KNOCKBACK_SCALING": 0.7,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 8,
                    "HG_VISUAL_EFFECT": 304,
                    "HG_WIDTH": 84,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy1",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 50,
                    "HG_BASE_HITPAUSE": 4,
                    "HG_BASE_KNOCKBACK": 6,
                    "HG_DAMAGE": 8,
                    "HG_HEIGHT": 70,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 2,
                    "HG_HITBOX_Y": -36,
                    "HG_HITPAUSE_SCALING": 0.25,
                    "HG_KNOCKBACK_SCALING": 0.6,
                    "HG_LIFETIME": 16,
                    "HG_PRIORITY": 6,
                    "HG_WIDTH": 70,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 4,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
        },
    },
    "AT_USTRONG": {
        "num_hitboxes": 5,
        "attr_num": {
            "AG_NUM_WINDOWS": 4,
            "AG_STRONG_CHARGE_WINDOW": 1,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "ustrong_hurt",
            "AG_SPRITE": "ustrong",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 3,
                },
                "str": {
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 21,
                    "AG_WINDOW_SFX_FRAME": 14,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_heavy2",
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 6,
                    "AG_WINDOW_ANIM_FRAMES": 6,
                    "AG_WINDOW_LENGTH": 13,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 12,
                    "AG_WINDOW_ANIM_FRAMES": 5,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 16,
                },
                "str": {
                },
            },
            5: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 18,
                    "AG_WINDOW_ANIM_FRAMES": 6,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 28,
                    "AG_WINDOW_SFX_FRAME": 15,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_heavy1",
                },
            },
            6: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 24,
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_LENGTH": 19,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 10,
                    "HG_BASE_KNOCKBACK": 0.1,
                    "HG_DAMAGE": 6,
                    "HG_HEIGHT": 44,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 54,
                    "HG_HITBOX_Y": -150,
                    "HG_HITPAUSE_SCALING": 0.5,
                    "HG_HITSTUN_MULTIPLIER": 20,
                    "HG_LIFETIME": 6,
                    "HG_PRIORITY": 6,
                    "HG_TECHABLE": 1,
                    "HG_VISUAL_EFFECT": 305,
                    "HG_WIDTH": 90,
                    "HG_WINDOW": 3,
                    "HG_WINDOW_CREATION_FRAME": 3,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy1",
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_ANGLE_FLIPPER": 6,
                    "HG_BASE_HITPAUSE": 10,
                    "HG_BASE_KNOCKBACK": 0.1,
                    "HG_DAMAGE": 6,
                    "HG_HEIGHT": 70,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 50,
                    "HG_HITBOX_Y": -166,
                    "HG_HITPAUSE_SCALING": 0.5,
                    "HG_HITSTUN_MULTIPLIER": 20,
                    "HG_LIFETIME": 3,
                    "HG_PRIORITY": 8,
                    "HG_TECHABLE": 1,
                    "HG_VISUAL_EFFECT": 305,
                    "HG_WIDTH": 60,
                    "HG_WINDOW": 3,
                    "HG_WINDOW_CREATION_FRAME": 9,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy1",
                },
            },
            3: {
                "num": {
                    "HG_ANGLE": 60,
                    "HG_BASE_HITPAUSE": 7,
                    "HG_BASE_KNOCKBACK": 8,
                    "HG_DAMAGE": 7,
                    "HG_HEIGHT": 60,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": -50,
                    "HG_HITBOX_Y": -50,
                    "HG_HITPAUSE_SCALING": 0.75,
                    "HG_KNOCKBACK_SCALING": 0.8,
                    "HG_LIFETIME": 7,
                    "HG_PRIORITY": 4,
                    "HG_WIDTH": 30,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 17,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium2",
                },
            },
            4: {
                "num": {
                    "HG_ANGLE": 60,
                    "HG_BASE_HITPAUSE": 7,
                    "HG_BASE_KNOCKBACK": 3,
                    "HG_DAMAGE": 7,
                    "HG_HEIGHT": 72,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 34,
                    "HG_HITBOX_Y": -140,
                    "HG_HITPAUSE_SCALING": 0.75,
                    "HG_KNOCKBACK_SCALING": 1,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 4,
                    "HG_WIDTH": 148,
                    "HG_WINDOW": 3,
                    "HG_WINDOW_CREATION_FRAME": 3,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium2",
                },
            },
            5: {
                "num": {
                    "HG_ANGLE": 60,
                    "HG_BASE_HITPAUSE": 7,
                    "HG_BASE_KNOCKBACK": 3,
                    "HG_DAMAGE": 7,
                    "HG_HEIGHT": 106,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 54,
                    "HG_HITBOX_Y": -182,
                    "HG_HITPAUSE_SCALING": 0.75,
                    "HG_KNOCKBACK_SCALING": 1,
                    "HG_LIFETIME": 4,
                    "HG_PRIORITY": 4,
                    "HG_WIDTH": 70,
                    "HG_WINDOW": 3,
                    "HG_WINDOW_CREATION_FRAME": 9,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium2",
                },
            },
            6: {
                "num": {
                    "HG_ANGLE": 90,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 7,
                    "HG_DAMAGE": 10,
                    "HG_GROUNDEDNESS": 1,
                    "HG_HEIGHT": 130,
                    "HG_HITBOX_GROUP": 2,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 130,
                    "HG_HITBOX_Y": -40,
                    "HG_HITPAUSE_SCALING": 1,
                    "HG_HITSTUN_MULTIPLIER": 0.5,
                    "HG_KNOCKBACK_SCALING": 1.1,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 4,
                    "HG_VISUAL_EFFECT": 306,
                    "HG_WIDTH": 130,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy2",
                },
            },
            7: {
                "num": {
                    "HG_ANGLE": 270,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 8,
                    "HG_DAMAGE": 10,
                    "HG_GROUNDEDNESS": 2,
                    "HG_HEIGHT": 130,
                    "HG_HIT_LOCKOUT": 10,
                    "HG_HITBOX_GROUP": 2,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 130,
                    "HG_HITBOX_Y": -40,
                    "HG_HITPAUSE_SCALING": 1,
                    "HG_HITSTUN_MULTIPLIER": 0.5,
                    "HG_KNOCKBACK_SCALING": 1.35,
                    "HG_LIFETIME": 1,
                    "HG_PRIORITY": 4,
                    "HG_VISUAL_EFFECT": 306,
                    "HG_WIDTH": 130,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_heavy2",
                },
            },
        },
    },
    "AT_UTILT": {
        "num_hitboxes": 5,
        "attr_num": {
            "AG_CATEGORY": 2,
            "AG_NUM_WINDOWS": 3,
        },
        "attr_str": {
            "AG_HURTBOX_SPRITE": "utilt_hurt",
            "AG_SPRITE": "utilt",
        },
        "windows": {
            1: {
                "num": {
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_SFX": 1,
                    "AG_WINDOW_LENGTH": 13,
                    "AG_WINDOW_SFX_FRAME": 12,
                },
                "str": {
                    "AG_WINDOW_SFX": "sfx_swipe_medium2",
                },
            },
            2: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 2,
                    "AG_WINDOW_ANIM_FRAMES": 3,
                    "AG_WINDOW_LENGTH": 6,
                    "AG_WINDOW_VSPEED": -4.5,
                    "AG_WINDOW_VSPEED_TYPE": 2,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "AG_WINDOW_ANIM_FRAME_START": 5,
                    "AG_WINDOW_ANIM_FRAMES": 2,
                    "AG_WINDOW_HAS_WHIFFLAG": 1,
                    "AG_WINDOW_LENGTH": 12,
                },
                "str": {
                },
            },
        },
        "hitboxes": {
            1: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 2,
                    "HG_HEIGHT": 66,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 32,
                    "HG_HITBOX_Y": -44,
                    "HG_HITSTUN_MULTIPLIER": 1.5,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 40,
                    "HG_WINDOW": 2,
                },
                "str": {
                },
            },
            2: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 2,
                    "HG_HEIGHT": 60,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 8,
                    "HG_HITBOX_Y": -74,
                    "HG_HITSTUN_MULTIPLIER": 1.5,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 1,
                    "HG_WIDTH": 80,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 2,
                },
                "str": {
                },
            },
            3: {
                "num": {
                    "HG_ANGLE": 361,
                    "HG_BASE_HITPAUSE": 2,
                    "HG_BASE_KNOCKBACK": 4,
                    "HG_DAMAGE": 2,
                    "HG_HEIGHT": 70,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": -14,
                    "HG_HITBOX_Y": -86,
                    "HG_HITSTUN_MULTIPLIER": 1.5,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 1,
                    "HG_SHAPE": 2,
                    "HG_WIDTH": 56,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 4,
                },
                "str": {
                },
            },
            4: {
                "num": {
                    "HG_ANGLE": 85,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 8,
                    "HG_DAMAGE": 9,
                    "HG_HEIGHT": 44,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": 22,
                    "HG_HITBOX_Y": -69,
                    "HG_HITPAUSE_SCALING": 0.5,
                    "HG_KNOCKBACK_SCALING": 0.45,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 3,
                    "HG_SHAPE": 2,
                    "HG_WIDTH": 85,
                    "HG_WINDOW": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
            5: {
                "num": {
                    "HG_ANGLE": 100,
                    "HG_BASE_HITPAUSE": 8,
                    "HG_BASE_KNOCKBACK": 8,
                    "HG_DAMAGE": 9,
                    "HG_HEIGHT": 46,
                    "HG_HIT_PARTICLE_NUM": 1,
                    "HG_HITBOX_TYPE": 1,
                    "HG_HITBOX_X": -6,
                    "HG_HITBOX_Y": -74,
                    "HG_HITPAUSE_SCALING": 0.5,
                    "HG_KNOCKBACK_SCALING": 0.45,
                    "HG_LIFETIME": 2,
                    "HG_PRIORITY": 3,
                    "HG_WIDTH": 40,
                    "HG_WINDOW": 2,
                    "HG_WINDOW_CREATION_FRAME": 2,
                },
                "str": {
                    "HG_HIT_SFX": "sfx_blow_medium1",
                },
            },
        },
    },
}

R1_HIT_FX = {
    "gigasplash": 32,
    "hit_particle2": 40,
    "special_splash": 20,
    "splash": 12,
    "sweatwhirlhit": 19,
    "vapour": 10000,
    "vapour2": 10000,
    "vapour3": 10000,
}

R1_HIT_FX_PREFIX = {
}

ARTICLE_NUMBERS = [1, 3]


# Disable source-control prompts before bulk imports — Plastic / Perforce
# integrations otherwise pop modal 'check out from revision control' dialogs
# on every save and stall the script. We restore as the LAST step of the
# script (after the batched saves), so the re-enabled provider cannot pop
# checkout modals during the save passes.
_sc_orig_provider = None
try:
    _sc = unreal.SourceControl
    _sc_was_enabled = _sc.is_enabled() if hasattr(_sc, 'is_enabled') else False
    if _sc_was_enabled and hasattr(_sc, 'set_provider'):
        # Capture the ORIGINAL provider name BEFORE disabling. Reading it
        # at restore time just returns the current provider ('None'), which
        # made the old restore a silent no-op.
        for _getter in ('get_provider', 'get_provider_name'):
            if hasattr(_sc, _getter):
                try:
                    _sc_orig_provider = str(getattr(_sc, _getter)())
                except Exception:
                    pass
                break
        if not _sc_orig_provider or _sc_orig_provider == 'None':
            _sc_orig_provider = 'Plastic'  # project default provider
        _sc.set_provider('None')
        print(f'  SC: temporarily disabled (was {_sc_orig_provider})')
    else:
        _sc_was_enabled = False
except Exception as ex:
    _sc_was_enabled = False
    print(f'  SC: unable to toggle ({ex}); imports may stall on prompts')


def _asset_tools():
    return unreal.AssetToolsHelpers.get_asset_tools()


# ── Batching primitives ──────────────────────────────────────────────────
# Each stamp_* function used to: set_editor_property → modify → save_asset
# (and for BPs, compile_blueprint before save). That's ~700 paper sprites +
# ~120 flipbooks + ~200 BPs × ~200-500ms per save = many minutes of wall-
# clock during import. The expensive bits are package serialization,
# source-control consult, and asset-registry tagging — all of which UE
# handles in batch via save_dirty_packages.
#
# Strategy: callers still "save_asset" and "compile_blueprint" but those
# are no longer per-item flushes. Saves are deferred entirely (the final
# save_dirty_packages at the bottom of this script writes everything that's
# dirty in one pass). BP compiles are queued, deduped, and run as a single
# batch right before that final save.
#
# Tradeoff: if the script crashes mid-run almost nothing is persisted.
# Acceptable for an idempotent re-runnable importer.
_PENDING_BP_COMPILES = []
_PENDING_BP_IDS = set()

# Assets the commandlet context will NOT auto-dirty on re-stamp: an already-
# loaded, clean asset whose set_editor_property/modify() does not flag its
# package dirty in -game/commandlet mode (e.g. a re-imported PaperSprite whose
# pivot changed on a reimport). save_dirty_packages SKIPS these because they
# read as clean, so collect them and force-save the whole set in ONE batch at
# the end via save_loaded_assets(..., only_if_is_dirty=False).
_FORCE_SAVE_ASSETS = []
_FORCE_SAVE_IDS = set()

# == SAVE DISCIPLINE (read before adding any save) ============================
# The ONLY save_dirty_packages call in this whole script is the final one at
# the very bottom. Do NOT call save_asset / save_dirty_packages anywhere else,
# and ESPECIALLY not inside a per-asset loop: save_dirty_packages re-walks the
# ENTIRE dirty set on every call, so per-iteration use is quadratic and on a
# big character starves/times out the editor RPC (that was the recurring
# 'saving X over and over' regression). Route every persist through one of:
#   * _save(path)        - no-op; the final save_dirty_packages flushes every
#                          dirty package (covers fresh assets + all BP CDO
#                          writes, since compiles are deferred to the end).
#   * _force_save(asset) - for re-stamped assets the commandlet will not dirty;
#                          batched into one save_loaded_assets at the end.


def _save(path):
    # No-op. Final save_dirty_packages at the bottom of the script writes
    # every dirty package at once. Kept as a function so callers don't have
    # to change shape.
    pass


def _force_save(asset):
    # Queue an asset for the single batched force-save at the end (for assets
    # the commandlet context will not auto-dirty - see _FORCE_SAVE_ASSETS note
    # above). Deduped by id. NEVER save these per-item: that is the storm.
    if asset is None:
        return
    aid = id(asset)
    if aid in _FORCE_SAVE_IDS:
        return
    _FORCE_SAVE_IDS.add(aid)
    _FORCE_SAVE_ASSETS.append(asset)


def _compile(bp):
    # Queue a BP for batch compile. Each BP gets compiled at most once even
    # if multiple stamp passes write to its CDO and call us repeatedly.
    if bp is None:
        return
    bp_id = id(bp)
    if bp_id in _PENDING_BP_IDS:
        return
    _PENDING_BP_IDS.add(bp_id)
    _PENDING_BP_COMPILES.append(bp)


def _ensure_r1_parent(bp, r1_class):
    # Re-import safety net. The C++ 2D scaffold (CreateNewCharacter) parents the
    # CD / article BPs to the base Lua2D classes; R1 runtime behavior lives on
    # the R1 subclasses. On a FRESH create the parent_class set above is already
    # R1, but when the asset already exists (scaffolded earlier, or imported
    # before the R1 split) load_asset hands back the base-parented BP unchanged.
    # Reparent so re-imports always route to the R1 classes. No-op if already an
    # R1 (sub)class. Runs BEFORE get_default_object so stamping lands on the R1
    # CDO. reparent_blueprint + compile regenerate the class; we also re-queue a
    # deferred compile so the final batch flush re-marks it dirty for the save.
    if bp is None:
        return
    try:
        gc = bp.generated_class()
        if gc is not None and isinstance(unreal.get_default_object(gc), r1_class):
            return
        unreal.BlueprintEditorLibrary.reparent_blueprint(bp, r1_class)
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        _compile(bp)
        print(f'  reparent: {bp.get_name()} -> R1 subclass')
    except Exception as ex:
        print(f'  reparent: failed for {bp} ({ex})')


def _flush_pending():
    # Compile every queued BP, re-mark its package dirty (compile_blueprint
    # clears the dirty flag — see project memory on the CDO-write +
    # save_dirty_packages pattern), then let the caller's save_dirty_packages
    # write everything that's dirty.
    if not _PENDING_BP_COMPILES:
        print('  batch: no pending compiles')
        return
    print(f'  batch: compiling {len(_PENDING_BP_COMPILES)} BPs')
    for bp in _PENDING_BP_COMPILES:
        try:
            unreal.BlueprintEditorLibrary.compile_blueprint(bp)
            bp.modify()
        except Exception as ex:
            print(f'    compile fail on {bp}: {ex}')


# Asset-registry caching reduces overhead during bulk asset creation. Each
# new asset normally re-tags the registry; toggle the temporary cache so
# tagging is deferred and runs once at the end (set False).
try:
    _asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    _asset_registry.set_temporary_caching_mode(True)
    print('  asset-registry: temporary caching enabled (bulk import)')
except Exception as ex:
    _asset_registry = None
    print(f'  asset-registry: temp-caching toggle failed ({ex}); proceeding without')


DEST = f'/Game/ModContent/{MOD_ID}/UnrealAssets'
TEX_DEST = f'{DEST}/Textures'
SPR_DEST = f'{DEST}/Sprites'
FB_DEST  = f'{DEST}/Flipbooks'

unreal.EditorAssetLibrary.make_directory(DEST)
unreal.EditorAssetLibrary.make_directory(TEX_DEST)
unreal.EditorAssetLibrary.make_directory(SPR_DEST)
unreal.EditorAssetLibrary.make_directory(FB_DEST)

_strip_re = re.compile(r'(.+?)_strip(\d+)$')


def parse_strip(filename):
    # R1's workshop tooling tolerates whitespace and odd characters in
    # PNG filenames; modders ship things like 'fspecial_air_strip10 .png'
    # (trailing space inside Hodan's set) and R1 still resolves them via
    # sprite_get('fspecial_air'). Normalize to match: strip whitespace
    # from the stem before regex / asset-name use, so our parse_strip
    # match succeeds and the resulting UE asset name (T_<Char>_<stem>)
    # doesn't get rejected by the asset registry for invalid characters.
    stem = os.path.splitext(filename)[0].strip()
    m = _strip_re.match(stem)
    if m: return m.group(1).strip(), int(m.group(2))
    return stem, 1


def _apply_sprite_tex_settings(tex):
    # Idempotent sprite-atlas texture setup. Only dirties the package when a
    # property actually changes, so re-imports don't re-save every texture.
    # Returns True when something changed (caller may want to count/report).
    desired = (
        ('filter', unreal.TextureFilter.TF_NEAREST),
        ('mip_gen_settings', unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS),
        ('compression_settings', unreal.TextureCompressionSettings.TC_EDITOR_ICON),
        ('srgb', True),
    )
    changed = False
    for prop, val in desired:
        if tex.get_editor_property(prop) != val:
            tex.set_editor_property(prop, val)
            changed = True
    if changed:
        tex.modify()
    return changed


def _make_texture_task(png_path, asset_name):
    full = f'{TEX_DEST}/{asset_name}'
    if unreal.load_asset(full):
        return None
    task = unreal.AssetImportTask()
    task.filename = png_path
    task.destination_path = TEX_DEST
    task.destination_name = asset_name
    task.replace_existing = True
    task.automated = True
    # task.save is the per-task in-line save — leave OFF and let the final
    # save_dirty_packages flush the batch in one pass. Per-task save runs
    # through the SC subsystem on every file (Plastic SC checkout etc.),
    # which dominates the import wall-clock.
    task.save = False
    task.factory = unreal.TextureFactory()
    return task


def import_texture(png_path, asset_name, force_reimport=False):
    # force_reimport=True re-runs the AssetImportTask even when the asset
    # already exists, picking up new PNG bytes from disk (palette atlases
    # change between importer revisions). replace_existing on the task
    # overwrites the source data in place, so we don't try to delete the
    # asset first — delete_asset crashes ObjectTools::ForceDeleteObjects
    # when the texture is referenced by AnimationTextureOverrides etc.
    full = f'{TEX_DEST}/{asset_name}'
    existing = unreal.load_asset(full)
    if existing and not force_reimport:
        # Settings may have changed between importer revisions (e.g. the
        # TC_DEFAULT -> TC_EDITOR_ICON compression fix) — re-assert them on
        # existing assets too. No-op when already correct.
        _apply_sprite_tex_settings(existing)
        return existing
    task = unreal.AssetImportTask()
    task.filename = png_path
    task.destination_path = TEX_DEST
    task.destination_name = asset_name
    task.replace_existing = True
    task.automated = True
    task.save = False
    task.factory = unreal.TextureFactory()
    _asset_tools().import_asset_tasks([task])
    tex = unreal.load_asset(full)
    if tex:
        # UE TextureFactory auto-detects normal maps from blue-dominated pixel
        # content — palette atlases that recolor to predominantly blue (the
        # Blue skin's slot 5/6 cyan/blue colors) get mis-tagged as
        # TC_NORMALMAP + srgb=False, which BC5-compresses to red+green only
        # and reads as linear, producing a yellow/white tint at runtime.
        # TC_EDITOR_ICON (UserInterface2D) keeps sprite atlases UNCOMPRESSED:
        # TC_DEFAULT applies DXT1 block compression whenever both dimensions
        # are multiples of 4 (chroma-artifacts pixel art; Bhadra idle 264x32 /
        # dash 240x32) while odd-sized strips silently fall back to BGRA8 —
        # so only some animations looked degraded.
        _apply_sprite_tex_settings(tex)
    return tex


def bulk_import_textures(plan):
    # plan: list of (png_path, asset_name) — typically populated by
    # import_all_sprites scanning R1_SPRITES. Filters out already-imported
    # textures, batches the rest into a single import_asset_tasks call.
    tasks = []
    for png_path, asset_name in plan:
        task = _make_texture_task(png_path, asset_name)
        if task is not None:
            tasks.append(task)
    if tasks:
        print(f'  texture batch: importing {len(tasks)} new textures (saves deferred)')
        _asset_tools().import_asset_tasks(tasks)
    # Apply per-texture tweaks (filter, mips, compression) over the WHOLE
    # plan — not just fresh imports — so settings fixes between importer
    # revisions reach already-imported textures on re-import. The helper is
    # idempotent (only dirties on actual change); save_dirty_packages
    # flushes whatever changed.
    fixed = 0
    for _, asset_name in plan:
        tex = unreal.load_asset(f'{TEX_DEST}/{asset_name}')
        if tex and _apply_sprite_tex_settings(tex):
            fixed += 1
    if fixed:
        print(f'  texture batch: re-applied sprite settings on {fixed} existing textures')


def make_sprite(name, tex, x, y, w, h, sheet_w, sheet_h, pivot_in_frame):
    full = f'{SPR_DEST}/{name}'
    existing = unreal.load_asset(full)
    # Heavy work (texture binding + slicing layout) only on fresh assets —
    # re-doing it on every import is slow. Pivot properties are cheap and
    # DO change between runs when the upstream pivot extractor changes (see
    # reference_make_sprite_existing_skip memory), so always re-apply them.
    if existing:
        sprite = existing
        # Re-assert the source rect on every import. A sprite first created during
        # a buggy run (wrong sheet_w from async-unbuilt platform data) baked a wrong
        # source_uv/source_dimension; these are cheap to re-stamp so reimports self-
        # heal. The heavy slicing layout below stays create-only for speed.
        sprite.set_editor_property('source_uv', unreal.Vector2D(x, y))
        sprite.set_editor_property('source_dimension', unreal.Vector2D(w, h))
        sprite.set_editor_property('source_texture_dimension', unreal.Vector2D(sheet_w, sheet_h))
    else:
        factory = unreal.PaperSpriteFactory()
        sprite = _asset_tools().create_asset(name, SPR_DEST, unreal.PaperSprite, factory)
        sprite.set_editor_property('source_texture', tex)
        sprite.set_editor_property('source_uv', unreal.Vector2D(x, y))
        sprite.set_editor_property('source_dimension', unreal.Vector2D(w, h))
        sprite.set_editor_property('source_texture_dimension', unreal.Vector2D(sheet_w, sheet_h))
        sprite.set_editor_property('source_image_dimension_before_trimming', unreal.Vector2D(w, h))
        sprite.set_editor_property('origin_in_source_image_before_trimming', unreal.Vector2D(x, y))
    if pivot_in_frame is not None:
        # Custom pivot in absolute texture coords = source_uv + frame-relative pivot.
        sprite.set_editor_property('pivot_mode', unreal.SpritePivotMode.CUSTOM)
        sprite.set_editor_property('custom_pivot_point',
            unreal.Vector2D(x + pivot_in_frame[0], y + pivot_in_frame[1]))
    else:
        sprite.set_editor_property('pivot_mode', unreal.SpritePivotMode.BOTTOM_CENTER)
    sprite.modify()
    if existing:
        # The batched save_dirty_packages misses property changes re-applied to a
        # pre-existing (already-clean) sprite: in the commandlet Python context
        # modify() does not re-dirty the package, so re-imports kept the sprite's
        # FIRST-import pivots and the character drifted by frame_idx*frame_width
        # (stale pre-offset pivots never got overwritten). Queue for the single
        # batched force-save at the end instead of saving per-sprite here - a
        # reimport re-stamps ~700 sprites and per-sprite save_asset is the storm.
        _force_save(sprite)
    else:
        _save(full)
    return sprite


def fps_for_stem(stem):
    # R1 init.gml exposes per-anim speeds as frames-per-game-tick at 60Hz;
    # convert to frames-per-second. Stems without a specific override fall
    # back to either a global `image_speed` literal from init.gml (if the
    # modder set one) or 12 fps.
    overrides = {
        'idle':       'idle_anim_speed',
        'crouch':     'crouch_anim_speed',
        'walk':       'walk_anim_speed',
        'walkturn':   'walk_anim_speed',
        'dash':       'dash_anim_speed',
        'dashstart':  'dash_anim_speed',
        'dashstop':   'dash_anim_speed',
        'dashturn':   'dash_anim_speed',
        'pratfall':   'pratfall_anim_speed',
    }
    key = overrides.get(stem)
    if key and key in R1_PHYSICS:
        # 60Hz tick rate * frames-per-tick = frames-per-second.
        return float(R1_PHYSICS[key]) * 60.0
    # Global image_speed (R1's `image_speed = N` in init.gml).
    if 'image_speed' in R1_PHYSICS:
        return float(R1_PHYSICS['image_speed']) * 60.0
    return 12.0


def build_flipbook(stem, sprites):
    name = f'PFB_{CHAR}_{stem}'
    full = f'{FB_DEST}/{name}'
    fb = unreal.load_asset(full)
    if not fb:
        fb = _asset_tools().create_asset(name, FB_DEST, unreal.PaperFlipbook, unreal.PaperFlipbookFactory())
    fb.set_editor_property('frames_per_second', fps_for_stem(stem))
    keyframes = []
    for sp in sprites:
        kf = unreal.PaperFlipbookKeyFrame()
        kf.set_editor_property('sprite', sp)
        kf.set_editor_property('frame_run', 1)
        keyframes.append(kf)
    fb.set_editor_property('key_frames', keyframes)
    fb.modify()
    _save(full)
    return fb


# R1_BASE_SPRITES is emitted dynamically in WriteAssetImportStub (resolved
# relative to the importer binary, or overridden via R1_BASE_SPRITES_DIR) so
# it works on any machine — do NOT hardcode an absolute path here.


def _sheet_dims(png, tex):
    # True sheet dimensions from the PNG source header. UE blueprint_get_size_x()
    # returns the PLATFORM-DATA width, which UE builds ASYNC after import -- it
    # reports a placeholder (e.g. 32) until that build finishes. On the first
    # import after a launch most textures are not built yet, so frame_w came out
    # wrong and every strip frame's custom_pivot collapsed toward frame-local
    # (the reimport sprite-offset bug). The PNG header is synchronous and always
    # correct; fall back to the engine size only if the header cannot be read.
    try:
        with open(png, 'rb') as f:
            head = f.read(24)
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            w = (head[16] << 24) | (head[17] << 16) | (head[18] << 8) | head[19]
            h = (head[20] << 24) | (head[21] << 16) | (head[22] << 8) | head[23]
            if w > 0 and h > 0:
                return w, h
    except Exception as ex:
        print(f'  _sheet_dims: PNG header read failed for {png}: {ex}')
    return tex.blueprint_get_size_x(), tex.blueprint_get_size_y()


def _check_strip_pivots(stem, sprites, pivot, out_bug):
    # Loud guard: after the PNG-dims fix a multi-frame strip's pivot must track
    # source_uv (pivot.x - source_uv.x stays a constant frame-local pivot across
    # frames). If it does not, frame_w was wrong and the strip renders offset --
    # record the stem so the import reports it instead of shipping silent drift.
    if pivot is None or len(sprites) < 2:
        return
    p0 = sprites[0].get_editor_property('custom_pivot_point')
    u0 = sprites[0].get_editor_property('source_uv')
    p1 = sprites[-1].get_editor_property('custom_pivot_point')
    u1 = sprites[-1].get_editor_property('source_uv')
    d_piv = p1.x - p0.x
    d_uv = u1.x - u0.x
    if abs(d_uv) > 1 and abs(d_piv - d_uv) > max(2.0, 0.1 * abs(d_uv)):
        out_bug.append(stem)


def import_all_sprites():
    flipbooks = {}
    _pivot_bug_stems = []
    if not os.path.isdir(R1_SPRITES):
        print(f'  no sprites dir at {R1_SPRITES}; skipping')
        return flipbooks

    # Phase 1 — bulk texture import. One import_asset_tasks call instead of
    # ~120 individual ones. AssetTools handles the parallel decode, then we
    # come back through the per-stem loop to slice + flipbook.
    plan = []
    for fn in sorted(os.listdir(R1_SPRITES)):
        if not fn.lower().endswith('.png'): continue
        stem, _ = parse_strip(fn)
        png = os.path.join(R1_SPRITES, fn).replace(os.sep, '/')
        plan.append((png, f'T_{CHAR}_{stem}'))
    bulk_import_textures(plan)

    for fn in sorted(os.listdir(R1_SPRITES)):
        if not fn.lower().endswith('.png'): continue
        stem, n_frames = parse_strip(fn)
        png = os.path.join(R1_SPRITES, fn).replace(os.sep, '/')
        tex_name = f'T_{CHAR}_{stem}'
        tex = unreal.load_asset(f'{TEX_DEST}/{tex_name}')
        if not tex:
            print(f'  failed to import {fn}; skipping')
            continue
        sheet_w, sheet_h = _sheet_dims(png, tex)
        frame_w = sheet_w // n_frames
        # PIVOTS keys are case-folded at emit time; fold the lookup too.
        pivot = PIVOTS.get(stem.lower())
        if pivot is None and n_frames > 1:
            # Single-frame sprites commonly have no explicit origin, but a
            # multi-frame strip without one almost always means the load.gml
            # pivot extraction missed it - the silent BOTTOM_CENTER fallback
            # renders every frame anchored wrong.
            print(f'  WARN: multi-frame strip {stem} ({n_frames} frames) has no PIVOTS entry - falling back to BOTTOM_CENTER')
        sprites = []
        for i in range(n_frames):
            sp_name = f'PS_{CHAR}_{stem}' if n_frames == 1 else f'PS_{CHAR}_{stem}_{i:02d}'
            sp = make_sprite(sp_name, tex, i * frame_w, 0, frame_w, sheet_h, sheet_w, sheet_h, pivot)
            sprites.append(sp)
        _check_strip_pivots(stem, sprites, pivot, _pivot_bug_stems)
        flipbooks[stem] = build_flipbook(stem, sprites)

        # R1's crouch.png is one strip covering all three sub-states (start,
        # active, stand). R2 exposes them as separate states, so we slice
        # the strip into three sub-flipbooks here. Frame counts come from
        # init.gml's crouch_*_frames literals.
        if stem == 'crouch':
            startup  = int(R1_PHYSICS.get('crouch_startup_frames', 3))
            active   = int(R1_PHYSICS.get('crouch_active_frames',  max(1, n_frames - 6)))
            recovery = int(R1_PHYSICS.get('crouch_recovery_frames', 3))
            if startup + active + recovery <= n_frames:
                flipbooks['crouch_start'] = build_flipbook('crouch_start', sprites[0:startup])
                flipbooks['crouch']       = build_flipbook('crouch',       sprites[startup:startup+active])
                flipbooks['crouch_stand'] = build_flipbook('crouch_stand', sprites[startup+active:startup+active+recovery])
                print(f'  crouch: sliced {n_frames} frames -> {startup}/{active}/{recovery}')

    # Second pass: import R1 base-game effects extracted from R1's GameMaker
    # source tree via Tools/R1Importer/extract_r1_base_sprites_from_source.py.
    # Same _stripN naming convention so the same flow handles them. Stems
    # that collide with per-mod stems (rare) are skipped; the per-mod sprite
    # wins. Resulting flipbook stems live in the same dict and feed both
    # the regular char-data Animations TMap and stamp_vfx_renderer_bps.
    if os.path.isdir(R1_BASE_SPRITES):
        # Load pivot sidecar emitted by the extractor so
        # base sprites use their R1 GameMaker origin instead of (0,0).
        # Without this, R2 spawns flipbooks anchored top-left and effects
        # render shifted from the actual hit point.
        base_pivots = {}
        pivot_json = os.path.join(R1_BASE_SPRITES, '_pivots.json').replace(os.sep, '/')
        if os.path.isfile(pivot_json):
            try:
                import json
                with open(pivot_json, 'r') as f:
                    raw = json.load(f)
                base_pivots = {k: tuple(v) for k, v in raw.items()}
                print(f'  R1Compat: loaded {len(base_pivots)} base-sprite pivots')
            except Exception as ex:
                print(f'  R1Compat: pivot json read failed: {ex}')
        # Bulk-import all R1 base textures in one import_asset_tasks call,
        # then iterate to slice + flipbook. Same shape as Phase 1, just on
        # the R1Compat base-sprite staging dir instead of the mod's own.
        # Skips stems that the mod already owns (per-mod takes precedence
        # via the `if stem in flipbooks: continue` filter).
        plan = []
        plan_metadata = []  # (stem, n_frames)
        for fn in sorted(os.listdir(R1_BASE_SPRITES)):
            if not fn.lower().endswith('.png'): continue
            stem, n_frames = parse_strip(fn)
            if stem in flipbooks:
                continue
            png = os.path.join(R1_BASE_SPRITES, fn).replace(os.sep, '/')
            tex_name = f'T_{CHAR}_R1Base_{stem}'
            plan.append((png, tex_name))
            plan_metadata.append((stem, n_frames, tex_name, png))
        bulk_import_textures(plan)

        added = 0
        for stem, n_frames, tex_name, png in plan_metadata:
            tex = unreal.load_asset(f'{TEX_DEST}/{tex_name}')
            if not tex:
                continue
            sheet_w, sheet_h = _sheet_dims(png, tex)
            frame_w = sheet_w // n_frames
            pivot = base_pivots.get(stem)
            sprites = []
            for i in range(n_frames):
                sp_name = f'PS_{CHAR}_R1Base_{stem}_{i:02d}' if n_frames > 1 else f'PS_{CHAR}_R1Base_{stem}'
                sp = make_sprite(sp_name, tex, i * frame_w, 0, frame_w, sheet_h, sheet_w, sheet_h, pivot)
                sprites.append(sp)
            _check_strip_pivots(stem, sprites, pivot, _pivot_bug_stems)
            flipbooks[stem] = build_flipbook(stem, sprites)
            added += 1
        print(f'  R1Compat: imported {added} base-game effect flipbooks')
    if _pivot_bug_stems:
        print(f'  PIVOT_CHECK: ERROR {len(_pivot_bug_stems)} strip(s) frame-local (offset bug): {_pivot_bug_stems[:30]}')
    else:
        print('  PIVOT_CHECK: ok (all strips absolute)')
    return flipbooks


# ── State / attack key mapping ──────────────────────────────────────────
# R1 anim names → ERivalsCharacterState. Best-effort defaults; modder edits
# CD_<CHAR>::StateFlipbookKeys after import to refine.

STATE_MAP = {
    # R1-anim-stem → R2 ERivalsCharacterState. Backward variants share the
    # forward sprite — R1 mods rely on the engine flipping the sprite based
    # on facing direction, so the same flipbook works for both.
    'idle':       'IDLE',
    'crouch':     'CROUCH',
    'crouch_start': 'CROUCH_START',
    'crouch_stand': 'CROUCH_STAND',
    'walk':       'WALK',
    'walkturn':   'WALK_TURN',
    'dashstart':  'DASH',         # initial dash burst — R2's DASH state
    'dash':       'RUN',          # sustained run — R2's RUN state
    'dashstop':   'DASH_STOP',
    'dashturn':   'RUN_TURN',
    'jumpstart':  'JUMP_SQUAT',
    'jump':       'FULL_HOP',
    'jump_short': 'SHORT_HOP',
    'doublejump': 'DOUBLE_JUMP',
    # Note: 'plat' is R1's RESPAWN platform sprite, NOT fall-through.
    # R1 has no dedicated fall-through-platform sprite — character keeps
    # showing the airborne anim (jump). PLAT_DROP gets aliased to 'jump'
    # below to match.
    # Note: pratfall is intentionally NOT mapped to FALL. Per R1 docs the
    # 'jump' sprite covers both the rising and falling halves of normal
    # airtime — the double jump animation transitions into the falling
    # portion of the normal jump animation. The 'pratfall' sprite is for
    # R1's PS_PRATFALL (helpless air state after up-special / cancel into
    # dodge) which has no clean R2 equivalent. The flipbook is built but
    # unused by default; mods can wire it via Lua if needed.
    'walljump':   'WALL_JUMP',
    'land':       'LAND',
    'landinglag': 'LANDING_LAG',
    'parry':      'PARRY',
    'hurt':       'HITSTUN_LIGHT',
    'bouncehurt': 'TUMBLE',
    # Defensive movement options. R1 uses these stems by convention; every
    # roster character ships them and the audit-by-naming approach below
    # picks them up the same way as 'idle' / 'walk'. Without mappings here,
    # entering RollForward / AirDodge / etc. falls through to
    # DefaultAnimationKey and the character visually freezes on Idle.
    'airdodge':   'AIR_DODGE',
    'roll_forward':  'ROLL_FORWARD',
    'roll_backward': 'ROLL_BACKWARD',
    # R1 mods ship a single 'tech' for the on-the-spot ground tech.
    # Tech-rolls (forward/backward) reuse the regular roll sprites — see
    # ALIASES below. R1 has no 'techf'/'techb' convention; modders never
    # ship those.
    'tech':       'TECH_GROUND',
    'waveland':   'WAVE_LAND',
    # frozen is a CustomStatusState, not a base state — modder maps in skin.
    # spotdodge isn't here either — R1 reuses 'parry' for spot dodge by
    # convention (see SPOT_DODGE alias below).
}

# Backward variants point to forward sprites (engine flips for facing).
STATE_MAP_BACKWARD = {
    'jump':       'FULL_HOP_BACKWARD',
    'doublejump': 'DOUBLE_JUMP_BACKWARD',
    'jump_short': 'SHORT_HOP_BACKWARD',
}

# Map R1 AT_* enum names to R2 ERivalsCharacterAttack member names. R1 names
# come from set_attack_value/set_window_value/set_hitbox_value first args;
# R2 names are the unreal.RivalsCharacterAttack enum keys.
R1_AT_TO_R2_ATTACK = {
    'AT_JAB':           'JAB',
    'AT_DATTACK':       'D_ATTACK',
    'AT_FTILT':         'FTILT',
    'AT_DTILT':         'DTILT',
    'AT_UTILT':         'UTILT',
    'AT_NAIR':          'NAIR',
    'AT_FAIR':          'FAIR',
    'AT_BAIR':          'BAIR',
    'AT_UAIR':          'UAIR',
    'AT_DAIR':          'DAIR',
    'AT_NSPECIAL':      'NSPECIAL',
    'AT_FSPECIAL':      'FSPECIAL',
    'AT_USPECIAL':      'USPECIAL',
    'AT_DSPECIAL':      'DSPECIAL',
    'AT_NSPECIAL_AIR':  'NSPECIAL_AIR',
    'AT_FSPECIAL_AIR':  'FSPECIAL_AIR',
    'AT_USPECIAL_AIR':  'USPECIAL_AIR',
    'AT_DSPECIAL_AIR':  'DSPECIAL_AIR',
    'AT_FSTRONG':       'FSTRONG',
    'AT_USTRONG':       'USTRONG',
    'AT_DSTRONG':       'DSTRONG',
    'AT_TAUNT':         'TAUNT1',
    'AT_TAUNT_2':       'TAUNT2',
    'AT_TAUNT_3':       'TAUNT3',
    'AT_TAUNT_4':       'TAUNT4',
    'AT_INTRO':         'INTRO',
    'AT_GRAB':          'GRAB',
    'AT_PUMMEL':        'PUMMEL',
    'AT_FTHROW':        'FTHROW',
    'AT_BTHROW':        'BTHROW',
    'AT_UTHROW':        'UTHROW',
    'AT_DTHROW':        'DTHROW',
    'AT_EXTRA_1':       'EXTRA1',
    'AT_EXTRA_2':       'EXTRA2',
    'AT_EXTRA_3':       'EXTRA3',
    'AT_EXTRA_4':       'EXTRA4',
}


ATTACK_MAP = {
    'jab':       'JAB',
    'dattack':   'D_ATTACK',
    'ftilt':     'FTILT',
    'dtilt':     'DTILT',
    'utilt':     'UTILT',
    'nair':      'NAIR',
    'fair':      'FAIR',
    'bair':      'BAIR',
    'uair':      'UAIR',
    'dair':      'DAIR',
    'nspecial':      'NSPECIAL',
    'fspecial':      'FSPECIAL',
    'uspecial':      'USPECIAL',
    'dspecial':      'DSPECIAL',
    'nspecial_air':  'NSPECIAL_AIR',
    'fspecial_air':  'FSPECIAL_AIR',
    'uspecial_air':  'USPECIAL_AIR',
    'dspecial_air':  'DSPECIAL_AIR',
    'fstrong':   'FSTRONG',
    'ustrong':   'USTRONG',
    'dstrong':   'DSTRONG',
    'taunt':     'TAUNT1',
    # Extra taunts / extras: standard R1 attack-file stems. Both the
    # underscored and squashed spellings appear in the wild.
    'taunt_2':   'TAUNT2',
    'taunt2':    'TAUNT2',
    'taunt_3':   'TAUNT3',
    'taunt3':    'TAUNT3',
    'taunt_4':   'TAUNT4',
    'taunt4':    'TAUNT4',
    'extra_1':   'EXTRA1',
    'extra1':    'EXTRA1',
    'extra_2':   'EXTRA2',
    'extra2':    'EXTRA2',
    'extra_3':   'EXTRA3',
    'extra3':    'EXTRA3',
    'extra_4':   'EXTRA4',
    'extra4':    'EXTRA4',
    'intro':     'INTRO',
    'grab':      'GRAB',
    'pummel':    'PUMMEL',
    'fthrow':    'FTHROW',
    'bthrow':    'BTHROW',
    'uthrow':    'UTHROW',
    'dthrow':    'DTHROW',
}


def apply_movement_physics(cdo):
    # R1 init.gml literal → R2 URivalsCharacterData field. R1 px/frame
    # values get multiplied by SCALE to land in R2's unit system. The
    # value is supplied by the importer (--physics-scale CLI flag, default
    # 2.5 — matches the URivalsLua2DCharacterData visual sprite scale so
    # physical motion matches what the modder authored visually).
    SCALE = 2.5  # px-per-frame → R2 units
    # Mapping: R1 name → (R2 field, scaled?)
    MAP = [
        ('walk_speed',         'WalkSpeedMax',                True),
        ('walk_accel',         'WalkAccelerationMax',         True),
        ('walk_turn_time',     'WalkTurnFrames',              False),
        ('initial_dash_speed', 'DashSpeed',                   True),
        ('initial_dash_time',  'DashFrames',                  False),
        ('dash_stop_time',     'DashStopFrames',              False),
        ('dash_turn_time',     'RunTurnFrames',               False),
        ('dash_turn_accel',    'RunTurnAcceleration',         True),
        ('dash_speed',         'RunSpeedMax',                 True),
        ('ground_friction',    'FrictionGround',              True),
        ('air_friction',       'FrictionAir',                 True),
        ('gravity_speed',      'Gravity',                     True),
        ('hitstun_grav',       'HitstunGravity',              True),
        ('max_fall',           'FallSpeedMax',                True),
        ('fast_fall',          'FastFallSpeed',               True),
        ('air_accel',          'AirAcceleration',             True),
        ('air_max_speed',      'AirSpeedHorizontalMax',       True),
        ('max_jump_hsp',       'JumpSpeedHorizontalMax',      True),
        ('jump_speed',         'FullHopSpeed',                True),
        ('short_hop_speed',    'ShortHopSpeed',               True),
        ('djump_speed',        'DoubleJumpSpeed',             True),
        ('jump_change',        'DoubleJumpMaxHorizontalSpeed',True),
        ('max_djumps',         'MaxDoubleJumps',              False),
        ('air_dodge_speed',    'AirDodgeSpeed',               True),
        ('roll_forward_max',   'RollSpeed',                   True),
        ('land_time',          'LandFrames',                  False),
        # Additional R1 init.gml vars with R2 equivalents that were missing
        # from the prior MAP. Adds: dash_accel (R1 acceleration during dash
        # state), djump_decay (slow-down on consecutive djumps), gravity at
        # jump apex.
        ('dash_accel',         'DashAcceleration',            True),
        ('djump_decay',        'DoubleJumpSpeedDecay',        True),
        ('gravity_jump_speed', 'GravityJumpSpeed',            True),
        # Lua2D-specific fields. R1 has explicit duration vars for these
        # states; R2 has no equivalent on the base CharacterData, so
        # URivalsLua2DCharacterData adds them. Frame counts; not scaled.
        ('double_jump_time',   'DoubleJumpFrames',            False),
        ('walljump_time',      'WallJumpFrames',              False),
    ]
    set_count = 0
    for r1_name, r2_field, scale_it in MAP:
        if r1_name not in R1_PHYSICS:
            continue
        v = R1_PHYSICS[r1_name]
        if scale_it: v = v * SCALE
        # Convert int-like to int for the int32 fields.
        if not scale_it: v = int(v)
        try:
            cdo.set_editor_property(_pascal_to_snake(r2_field), v)
            set_count += 1
        except Exception as ex:
            print(f'  movement: failed to set {r2_field}: {ex}')

    # WallJumpSpeed: FVector2D field — R1 splits it into walljump_hsp / walljump_vsp.
    if 'walljump_hsp' in R1_PHYSICS or 'walljump_vsp' in R1_PHYSICS:
        hsp = float(R1_PHYSICS.get('walljump_hsp', 0)) * SCALE
        vsp = float(R1_PHYSICS.get('walljump_vsp', 0)) * SCALE
        try:
            cdo.set_editor_property('wall_jump_speed', unreal.Vector2D(hsp, vsp))
            set_count += 1
        except Exception as ex:
            print(f'  movement: failed to set wall_jump_speed: {ex}')

    # R1 knockback_adj → R2 Weight. R2's CalculateWeightModifier is
    # `200 / (weight + 100)` — so weight = 200/knockback_adj - 100.
    # R1 knockback_adj 0.9 (Hodan) → R2 weight ~122 (mediumweight).
    if 'knockback_adj' in R1_PHYSICS:
        adj = float(R1_PHYSICS['knockback_adj'])
        if adj > 0.01:
            weight = 200.0 / adj - 100.0
            try:
                cdo.set_editor_property('weight', weight)
                set_count += 1
            except Exception as ex:
                print(f'  movement: failed to set weight: {ex}')

    # ECB dimensions. R1 separates these conceptually:
    #   width      = ECB half-width for wall/floor collision (`scr_movement.gml`
    #                uses `x ± width/2` against par_block / par_jumpthrough).
    #                Convention is width=18 in every base char's init.gml;
    #                Hodan inherits the default since he doesn't set it.
    #   char_height = body-center reference for hitbox Y offsets — NOT an
    #                ECB height in R1 (R1 has no explicit ECB Y dimension;
    #                the floor check uses the hurtbox sprite mask). For R2,
    #                we use char_height as a reasonable ECB height since
    #                R2's UpdateECB needs both axes.
    r1_width  = R1_PHYSICS.get('width', 18.0)
    r1_height = R1_PHYSICS.get('char_height')
    if r1_height is not None:
        ecb_w = r1_width * 2.0 * SCALE   # full width (R1 width is half-extent)
        ecb_h = r1_height * SCALE
        try:
            cdo.set_editor_property('ecb_dimensions', unreal.Vector2D(ecb_w, ecb_h))
            set_count += 1
            print(f'  movement: ecb_dimensions from width/char_height = {r1_width*2}x{r1_height} (R1) -> {ecb_w:.1f}x{ecb_h:.1f} (R2)')
        except Exception as ex:
            print(f'  movement: failed to set ecb_dimensions: {ex}')

    # FlipbookScale is the pure R1px -> R2-unit sprite scale (the chosen
    # --scale, default 2.5). R1's `small_sprites` flag is NOT baked in here.
    # In R1, `Yy = 1 + small_sprites` (oPlayer/Draw_0.gml:3) is a per-FRAME
    # draw multiplier read live each tick, not a static scale — so baking it
    # in froze a runtime value and (worse) double-counted against owner-drawn
    # article sprites, whose draw calls already carry the small_sprites
    # compensation in their own xscale (e.g. Glub's ball draws at a literal 2).
    # The Lua2D character renderer instead multiplies the BODY scale by
    # (1 + small_sprites) at render time, reading the live `small_sprites`
    # inst var (RivalsLua2DCharacterEntity::GetSpriteScaleMultiplier). That
    # keeps FlipbookScale = our chosen scale, lets pool draws apply their own
    # xscale in full (so dynamic per-draw scaling works), and respects a
    # mid-game small_sprites flip. ECB/walk_speed/etc. stay unscaled.
    flipbook_scale = SCALE
    try:
        cdo.set_editor_property('flipbook_scale',
            unreal.Vector(flipbook_scale, 1.0, flipbook_scale))
        set_count += 1
    except Exception as ex:
        print(f'  movement: failed to set flipbook_scale: {ex}')

    print(f'  movement: applied {set_count} physics fields from R1 init.gml')


def _read_hurtbox_sprite_dims():
    # The damage-receiving hurtbox in R1 is a separate sprite assigned via
    # `hurtbox_spr = sprite_get(name)` in init.gml. The shape is the
    # OPAQUE-PIXEL MASK of that sprite — R1 uses GM's built-in mask_index
    # collision against it. R2 needs a single static box; the sprite's PNG
    # dimensions are a reasonable approximation.
    #
    # Returns (w, h) in R1 pixels or None if no hurtbox_spr ref found or
    # the sprite file is missing.
    import re, struct
    init_path = os.path.join(R1_ROOT, 'scripts', 'init.gml')
    if not os.path.isfile(init_path):
        return None
    try:
        with open(init_path, 'r', encoding='utf-8', errors='replace') as f:
            init_text = f.read()
    except Exception as ex:
        print(f'  hurtbox: failed to read init.gml: {ex}')
        return None
    # Match: hurtbox_spr = sprite_get(name)
    m = re.search(r'hurtbox_spr\s*=\s*sprite_get\s*\(\s*"([^"]+)"\s*\)', init_text)
    if not m:
        return None
    sprite_name = m.group(1)
    # R1 sprites are PNG files in the mod's sprites/ dir, named <sprite_name>.png
    # (sometimes with _stripN suffix for animations; the base hurtbox is
    # typically a single-frame static sprite).
    candidates = [
        os.path.join(R1_SPRITES, f'{sprite_name}.png'),
    ]
    import glob
    candidates.extend(glob.glob(os.path.join(R1_SPRITES, f'{sprite_name}_strip*.png')))
    path = next((p for p in candidates if os.path.isfile(p)), None)
    if not path:
        print(f'  hurtbox: hurtbox_spr="{sprite_name}" but {sprite_name}.png not found in {R1_SPRITES}')
        return None
    try:
        with open(path, 'rb') as f:
            head = f.read(24)
        if head[:8] != b'\x89PNG\r\n\x1a\n':
            return None
        width  = struct.unpack('>I', head[16:20])[0]
        height = struct.unpack('>I', head[20:24])[0]
        # If sprite is a strip, divide width by frame count (parsed from
        # the _stripN suffix). The base hurtbox sprite is usually 1-frame
        # but defensive.
        strip_match = re.search(r'_strip(\d+)\.png$', os.path.basename(path))
        if strip_match:
            n_frames = int(strip_match.group(1))
            if n_frames > 0:
                width = width // n_frames
        print(f'  hurtbox: from hurtbox_spr="{sprite_name}" ({path}) -> {width}x{height} (R1)')
        return (float(width), float(height))
    except Exception as ex:
        print(f'  hurtbox: failed to read {path}: {ex}')
        return None


def _pascal_to_snake(name):
    out = []
    for i, c in enumerate(name):
        if c.isupper() and i > 0:
            out.append('_')
        out.append(c.lower())
    return ''.join(out)


def stamp_attack_data_assets():
    # Stamp ATT_<CHAR>_<MOVE>.uasset per R1 attack so URivalsCharacterData::
    # AttackData has non-null entries. The R2 engine queries this map for
    # window timing; without entries, GetCurrentAttackData returns null and
    # the Attack-state machine breaks.
    #
    # We populate Windows array (lengths/IASA/anim frames) from R1's static
    # set_window_value chain. HitboxAttributes/HitboxOnHitProperties stay
    # empty — the runtime shim's GetActiveHitboxes override builds them from
    # r1_state each frame, which lets runtime hitbox mutations Just Work.
    #
    # Returns: dict {R2 enum name (e.g. 'JAB') -> generated class}, ready to
    # plug into AttackData TMap.
    att_dest = f'{DEST}/Attacks'
    if not unreal.EditorAssetLibrary.does_directory_exist(att_dest):
        unreal.EditorAssetLibrary.make_directory(att_dest)

    # R2's IsAttackValid path requires AttackData->GroundedAnimation OR
    # ->AerialAnimation to be non-null, even though 2D characters don't use
    # skeletal anims for attacks. Borrow AN_Cla_Idle as a stand-in (same
    # fallback we use for state-anim queries on 2D entities at runtime).
    # TODO: replace with a properly-built /Game/Lua2D/Anim_2DDummy once we
    # have an authoring step that runs the AnimDataController to populate
    # keys (currently the factory-created Anim_2DDummy is an empty husk).
    dummy_anim = unreal.load_asset('/Game/Characters/Clairen/Animation/Movement/AN_Cla_Idle')

    # Attack-set discovery. R1_ATTACKS only contains attacks whose set_*_value
    # calls used a LITERAL `AT_X` identifier as args[0] (Hodan-style). Glub
    # and similar mods use a local variable (`atk = AT_JAB; set_window_value(
    # atk, ...)`) which the static extractor can't resolve, so R1_ATTACKS
    # would be empty/incomplete for them.
    #
    # Per AttackDataExtractor.cs's architectural rule: the runtime shim's
    # r1_state is the source of truth for window/hitbox data; the static
    # stamp here just needs to exist so the R2 engine has UAssets to dispatch
    # to. So we enumerate the attacks the modder *authored a file for* under
    # `scripts/attacks/<name>.gml` and stamp every one, unioned with any
    # literal-extracted entries (covers attacks declared in init.gml/load.gml).
    file_discovered_ats = set()
    attacks_dir = os.path.join(R1_ROOT, 'scripts', 'attacks')
    if os.path.isdir(attacks_dir):
        # Reverse map ATTACK_MAP (fname -> R2) into R2 -> AT_X via
        # R1_AT_TO_R2_ATTACK, then resolve filenames -> AT_X.
        r2_to_at = {r2: at for at, r2 in R1_AT_TO_R2_ATTACK.items()}
        for entry in os.listdir(attacks_dir):
            if not entry.endswith('.gml'):
                continue
            stem = entry[:-len('.gml')].lower()
            r2_name = ATTACK_MAP.get(stem)
            if not r2_name:
                print(f'  attack: attacks/{entry} has no ATTACK_MAP entry - no ATT asset will be stamped for it')
                continue
            at_name = r2_to_at.get(r2_name)
            if at_name:
                file_discovered_ats.add(at_name)
            else:
                print(f'  attack: attacks/{entry} maps to {r2_name} but R1_AT_TO_R2_ATTACK has no reverse entry - skipped')

    combined_ats = sorted(set(R1_ATTACKS.keys()) | file_discovered_ats)
    if not combined_ats:
        return {}

    out = {}
    for at_name in combined_ats:
        bucket = R1_ATTACKS.get(at_name, {})
        r2_attack_name = R1_AT_TO_R2_ATTACK.get(at_name)
        if not r2_attack_name:
            print(f'  attack: skipped unmapped {at_name}')
            continue
        if not hasattr(unreal.RivalsCharacterAttack, r2_attack_name):
            print(f'  attack: R2 enum has no {r2_attack_name} (from {at_name})')
            continue

        # ATT_<CharShort>_<Move>. CHAR_SHORT mirrors
        # WorkshopToolStatics::CreateNewCharacter (`AttackDataPrefix = ATT_<short>_`)
        # so CD_'s AttackDataMapper picks these up via prefix.
        # Asset name must match the C++ scaffold's PascalCase convention so the
        # CD's AttackDataMapper resolves to the SAME asset. r2_attack_name is the
        # UE Python enum name (UPPER_SNAKE). Single-word names (DSTRONG) load
        # case-insensitively against the scaffold's Dstrong; but UNDERSCORED names
        # (D_ATTACK, LEDGE_ATTACK, GETUP_ATTACK) must collapse to the scaffold's
        # DAttack/LedgeAttack/GetupAttack -- otherwise the importer stamps a
        # second, orphan asset the CD never references (the move plays the empty
        # scaffold default; dash attack 'held one frame then nothing').
        asset_attack_name = (
            ''.join(p.capitalize() for p in r2_attack_name.split('_'))
            if '_' in r2_attack_name else r2_attack_name
        )
        asset_name = f'ATT_{CHAR_SHORT}_{asset_attack_name}'
        asset_path = f'{att_dest}/{asset_name}'
        att = unreal.load_asset(asset_path)
        if not att:
            bp_factory = unreal.BlueprintFactory()
            bp_factory.set_editor_property('parent_class', unreal.RivalsCharacterAttackData)
            att = _asset_tools().create_asset(asset_name, att_dest, unreal.Blueprint, bp_factory)
            print(f'  created {asset_path}')
        attdo = unreal.get_default_object(att.generated_class())

        # Build Windows array. R1 windows are 1-indexed; R2's TArray is 0-
        # indexed. AG_NUM_WINDOWS tells us how many windows the engine auto-
        # progresses through. R1 mods commonly define MORE windows than
        # NUM_WINDOWS for branch paths (e.g. Hodan's USTRONG declares 4 but
        # uses windows 5+6 for the grab branch entered via `window = 5;`).
        # We stamp the union — max(NUM_WINDOWS, highest-defined-index) — so
        # the runtime SetWindow() writeback can target any window the mod
        # references without crashing on a null GetCurrentAttackWindow().
        #
        # GENEROUS FLOOR: R1 attack data is imperative — Glub's jab authors
        # windows via `window_num=1; set_window_value(AT,window_num,...);
        # window_num+=1;` and the static extractor cannot pin down the
        # final count. Per the architectural rule in AttackDataExtractor.cs,
        # the shim's r1_state is the source of truth at runtime; the static
        # stamp here just needs enough windows that any explicit
        # Super_SetWindow(N) from the shim lands inside the array. 16 covers
        # every R1 attack we've seen (Hodan's USTRONG tops out at 6); raise
        # this if a future mod needs more.
        ATTACK_WINDOW_FLOOR = 16
        declared = int(bucket.get('attr_num', {}).get('AG_NUM_WINDOWS', 0))
        defined  = max(bucket.get('windows', {}).keys()) if bucket.get('windows') else 0
        num_windows = max(declared, defined, ATTACK_WINDOW_FLOOR)

        # Strong-attack CHARGE is now driven entirely at runtime by the shim
        # (r1_overrides.lua: mirrors attack_update.gml's smash_charging loop —
        # hold the live AG_STRONG_CHARGE_WINDOW window while the charge button
        # is held + strong_charge < 60, then advance). We deliberately bake NO
        # synthetic charge window and NO charge index here: R1 attack data is
        # imperative (variable attack names, array/file-driven, even rewritten
        # mid-match by stance characters), so the charge position can't be
        # statically extracted reliably — it only exists in the live r1_state.
        # The window list below is a plain linear 1:1 shell; the shim steers it.

        # ── BASIC mode: real R2-native hitboxes from the R1 HG_ data ────────
        # Advanced leaves HitboxAttributes/OnHitProperties empty (the R1Compat
        # shim's GetActiveHitboxes rebuilds them from r1_state each frame). Basic
        # has no shim, so statically approximate them here. This is a ~90%
        # heuristic: R1 attack data is imperative (runtime-conditional hitboxes,
        # create_hitbox spawns, mid-match rewrites) so static capture can't be
        # exact — frame data + damage/kb transfer cleanly; box->circle radius,
        # the autolink (361) angle, and runtime-only hitboxes are approximations.
        basic_hb_by_window = {}   # R1 window idx -> [(name, start_frame, life)]
        hb_attrs = unreal.Array(unreal.RivalsHitboxAttributes)
        hb_onhit = unreal.Array(unreal.RivalsHitboxOnHitProperties)
        if IMPORT_MODE != 'advanced':
            HB_SCALE = 2.5
            for hb_idx, hb in sorted(bucket.get('hitboxes', {}).items()):
                hbn = hb.get('num', {})
                if int(hbn.get('HG_HITBOX_TYPE', 1)) == 2:
                    continue   # TYPE 2 = projectile -> article (not stamped in basic)
                # Skip hitboxes with no static window. Runtime/conditional
                # hitboxes (grab-branch boxes, create_hitbox spawns) carry no
                # HG_WINDOW; defaulting them to window 1 frame 0 stamps a
                # spurious, often-giant box active from the attack's first frame
                # (e.g. ustrong's 130x130 grab-slam box hanging out during the
                # charge windup). The runtime shim builds these live; Basic drops
                # them -- part of the ~90% static-capture limit.
                hg_window = hbn.get('HG_WINDOW')
                if hg_window is None or int(hg_window) <= 0:
                    continue
                hbname = f'HB{hb_idx}'
                oh = unreal.RivalsHitboxOnHitProperties()
                oh.set_editor_property('name', hbname)
                oh.set_editor_property('damage', int(hbn.get('HG_DAMAGE', 0)))
                oh.set_editor_property('base_knockback', float(hbn.get('HG_BASE_KNOCKBACK', 0)))
                oh.set_editor_property('knockback_scaling', float(hbn.get('HG_KNOCKBACK_SCALING', 0)))
                ang = int(hbn.get('HG_ANGLE', 45))
                if ang > 360:
                    ang = 45   # 361 = R1 autolink/Sakurai angle -> combo-ish approximation
                oh.set_editor_property('knockback_angle', ang)
                hb_onhit.append(oh)
                at = unreal.RivalsHitboxAttributes()
                at.set_editor_property('name', hbname)
                w_px = float(hbn.get('HG_WIDTH', 0) or 0)
                h_px = float(hbn.get('HG_HEIGHT', 0) or 0)
                r_px = float(hbn.get('HG_RADIUS', 0) or 0)
                if r_px > 0:
                    radius = r_px * HB_SCALE
                elif w_px > 0 and h_px > 0:
                    radius = ((w_px + h_px) / 4.0) * HB_SCALE   # avg half-dim (box->circle)
                elif w_px > 0:
                    radius = (w_px / 2.0) * HB_SCALE
                elif h_px > 0:
                    radius = (h_px / 2.0) * HB_SCALE
                else:
                    radius = 20.0 * HB_SCALE
                at.set_editor_property('radius', radius)
                # 2D plane is (X horizontal, Z vertical); R1 Y is down-positive.
                ox = float(hbn.get('HG_HITBOX_X', 0)) * HB_SCALE
                oz = -float(hbn.get('HG_HITBOX_Y', 0)) * HB_SCALE
                at.set_editor_property('offset', unreal.Vector(ox, 0.0, oz))
                at.set_editor_property('on_hit_properties_name', hbname)
                at.set_editor_property('hit_response', unreal.RivalsHitboxHitResponse.HIT)
                at.set_editor_property('groundedness', unreal.RivalsCharacterStateCategory.GROUND_OR_AIR)
                hb_attrs.append(at)
                win = int(hg_window)
                start = int(hbn.get('HG_WINDOW_CREATION_FRAME', 0))
                life = max(int(hbn.get('HG_LIFETIME', 1)), 1)
                basic_hb_by_window.setdefault(win, []).append((hbname, start, life))

        # Strong-charge (Basic): R1's AG_STRONG_CHARGE_WINDOW names the windup
        # window that holds while the smash is charged. We mirror R2's native
        # charge on that window below (a 60-frame hold carrying a StrongReleased
        # cancel -> next window on release); only strongs. Advanced leaves charge
        # to the runtime shim, so this is gated to non-advanced in the loop.
        charge_win = int(bucket.get('attr_num', {}).get('AG_STRONG_CHARGE_WINDOW', 0))
        # r2_attack_name is the UE Python enum name (UPPER_SNAKE, e.g. 'DSTRONG').
        is_strong = r2_attack_name.upper() in ('FSTRONG', 'DSTRONG', 'USTRONG')

        windows = unreal.Array(unreal.RivalsCharacterAttackWindow)
        for win_idx in range(1, num_windows + 1):
            w = unreal.RivalsCharacterAttackWindow()
            r1w = bucket.get('windows', {}).get(win_idx, {})
            r1w_num = r1w.get('num', {})

            length = int(r1w_num.get('AG_WINDOW_LENGTH', 1))
            if IMPORT_MODE != 'advanced':
                # Basic drives windows natively: stamp the real length so R2's
                # WindowTimer==WindowLengthFrames transition fires, plus the
                # hitbox activations for this window built above.
                w.set_editor_property('window_length_frames', max(length, 1))
                hbwins = unreal.Array(unreal.RivalsHitboxWindow)
                for (hbname, start, life) in basic_hb_by_window.get(win_idx, []):
                    hw = unreal.RivalsHitboxWindow()
                    hw.set_editor_property('hitbox_name', hbname)
                    hw.set_editor_property('start_frame', start)
                    hw.set_editor_property('length_in_frames', life)
                    hbwins.append(hw)
                if len(hbwins) > 0:
                    w.set_editor_property('hitbox_windows', hbwins)

                # Per-window movement: R1 AG_WINDOW_HSPEED/VSPEED -> R2
                # VelocityData (SetVelocity at frame 0, scaled by the physics
                # factor; R1 y is down-positive so vertical negates). R2's
                # SetVelocity is facing-relative for attacks, matching R1's
                # forward-positive hspeed. This is what carries lunging attacks
                # (fstrong, dash attack) forward.
                hsp = float(r1w_num.get('AG_WINDOW_HSPEED', 0) or 0)
                vsp = float(r1w_num.get('AG_WINDOW_VSPEED', 0) or 0)
                if hsp != 0 or vsp != 0:
                    vd = unreal.RivalsWindowVelocityData()
                    vd.set_editor_property('velocity', unreal.Vector2D(hsp * 2.5, -vsp * 2.5))
                    # CONST_VELOCITY: R1 re-applies AG_WINDOW_HSPEED every frame
                    # the window is active (a held drive, not a one-shot impulse).
                    # SET_VELOCITY would set it once at frame 0 and let friction
                    # bleed it off, so lunges (fstrong, dash) fell short. Maintain
                    # it across the window instead.
                    vd.set_editor_property('horizontal_velocity_type', unreal.RivalsVelocityType.CONST_VELOCITY if hsp != 0 else unreal.RivalsVelocityType.NONE)
                    vd.set_editor_property('vertical_velocity_type', unreal.RivalsVelocityType.CONST_VELOCITY if vsp != 0 else unreal.RivalsVelocityType.NONE)
                    vd.set_editor_property('apply_velocity_on_window_frame', 0)
                    vd.set_editor_property('apply_velocity_until_frame', max(length, 1))
                    w.set_editor_property('velocity_data', [vd])

                # Strong-charge window: hold up to 60 frames; releasing the smash
                # button fires StrongReleased -> the next window (mirrors R2 stock,
                # e.g. Zetterburn fstrong's len-60 charge window). The natural
                # transition at 60 frames is max charge (auto-release).
                if is_strong and charge_win > 0 and win_idx == charge_win:
                    w.set_editor_property('window_length_frames', 60)
                    wc = unreal.RivalsWindowCancel()
                    wc.set_editor_property('window_cancel_type', unreal.RivalsWindowCancelType.STRONG_RELEASED)
                    wc.set_editor_property('window_cancel_frame', -1)
                    wc.set_editor_property('post_cancel_window_string_table_key', f'W{win_idx + 1}')
                    w.set_editor_property('window_cancels', [wc])
            else:
                # Advanced: a sentinel large length so R2's natural-transition
                # check (WindowTimer == WindowLengthFrames) never fires — R1Compat
                # owns transitions, calling SetWindow(next) when its r1_state mirror
                # of AG_WINDOW_LENGTH is reached. Decouples runtime set_window_value
                # writes; the real length lives in r1_state on the Lua side.
                w.set_editor_property('window_length_frames', 9999)

            # CRITICAL: each window needs a unique StringTableKey, and the
            # NEXT window's key in NextWindowStringTableKey, otherwise R2's
            # FindWindowIndex returns 0 for empty-string keys and the attack
            # loops back to window 0 forever. Last window's next must be
            # empty so EndAttackNaturally fires.
            #
            # When `defined > declared` (R1 mod authored more windows than the
            # AG_NUM_WINDOWS count — Hodan USTRONG declares 4 but defines 6
            # because W5/W6 are the conditional grab-slam branch), the engine
            # must STOP auto-progression at win_idx == declared so whiff paths
            # end naturally. Mod-side `SetWindow(declared+1)` (transpiled from
            # `if grabbed != -1 { window = 5; }`) still routes into W5/W6 for
            # the hit case. Without this terminator, engine plays through W5
            # on whiff and the slam fires unconditionally.
            w.set_editor_property('string_table_key', f'W{win_idx}')
            # Plain linear advance (the shim owns the charge detour at runtime;
            # no synthetic charge window is baked). The declared-count
            # terminator below ends engine progression where the mod declared
            # AG_NUM_WINDOWS, so mod-only trailing windows stay mod-driven.
            if declared > 0 and win_idx == declared and declared < num_windows:
                # End engine progression here; W{declared+1}+ are mod-only.
                w.set_editor_property('next_window_string_table_key', '')
            elif win_idx < num_windows:
                w.set_editor_property('next_window_string_table_key', f'W{win_idx + 1}')
            else:
                w.set_editor_property('next_window_string_table_key', '')

            # AG_WINDOW_CANCEL_TYPE is NOT stamped onto the R2 asset. R1's
            # type 1/2 is the jab-combo window-advance (continue to the next
            # window on an attack/special re-press, advance EARLY past
            # CANCEL_FRAME, END the attack at window end without a re-press)
            # - owned entirely by the shim's transition driver, which ports
            # attack_update.gml:185-204/229. It is NOT IASA: stamping
            # iasa_frame here made the character engine-ACTIONABLE at the
            # cancel frame, so a buffered attack press natively restarted
            # the attack (SetAttack -> window 0) in parallel with the shim's
            # cancel advance - the two raced per press timing (Guadua jab
            # skipped windows + lost the jab-3 swing SFX, 2026-06-09).

            # R1's anim-frame fields control which sprite frame is shown when
            # the window starts and how many frames it spans.
            anim_start = int(r1w_num.get('AG_WINDOW_ANIM_FRAME_START', 0))
            anim_frames = int(r1w_num.get('AG_WINDOW_ANIM_FRAMES', 0))
            w.set_editor_property('animation_start_frame', anim_start)
            if anim_frames > 0:
                w.set_editor_property('animation_length_frames', anim_frames)

            windows.append(w)
            # (No synthetic charge window — see the AG_STRONG_CHARGE_WINDOW note
            # above. R1's implicit charge hold is reproduced at runtime by the
            # shim holding the live charge window while the button is held.)
        attdo.set_editor_property('windows', windows)

        # HitboxAttributes / HitboxOnHitProperties: Advanced leaves these empty
        # (the runtime shim's GetActiveHitboxes builds them from r1_state); Basic
        # has no shim, so stamp the statically-approximated hitboxes built above.
        if IMPORT_MODE != 'advanced':
            attdo.set_editor_property('hitbox_attributes', hb_attrs)
            attdo.set_editor_property('hitbox_on_hit_properties', hb_onhit)

        # Required by R2's IsAttackValid check at attack-input time.
        if dummy_anim:
            attdo.set_editor_property('grounded_animation', dummy_anim)
            attdo.set_editor_property('aerial_animation', dummy_anim)

        # AG_LANDING_LAG → AttackData.LandingLagFrames. R2 uses this to size
        # the landing-lag state when an aerial connects with the ground.
        # When LandingLagAnimation is null (we don't stamp one), the engine
        # falls back to LandingLagDuration = LandingLagFrames * 2.
        #
        # Groundedness gate: R2 only consults LandingLagFrames when the
        # attack is `AirOnly`. R1 doesn't carry a groundedness flag — but
        # the canonical aerial attack names are well-known. Promote those
        # to AirOnly so the engine actually transitions on touchdown.
        AERIAL_ATTACKS = { 'AT_NAIR', 'AT_FAIR', 'AT_BAIR', 'AT_UAIR', 'AT_DAIR',
            'AT_NSPECIAL_AIR', 'AT_FSPECIAL_AIR', 'AT_USPECIAL_AIR', 'AT_DSPECIAL_AIR' }
        if at_name in AERIAL_ATTACKS:
            attdo.set_editor_property('groundedness',
                unreal.RivalsCharacterStateCategory.AIR_ONLY)
        landing_lag = int(bucket.get('attr_num', {}).get('AG_LANDING_LAG', 0))
        if landing_lag > 0:
            attdo.set_editor_property('landing_lag_frames', landing_lag)

        _compile(att)
        att.modify()
        # BP CDO writes (e.g. `groundedness` enum) are flushed by the final
        # _flush_pending + save_dirty_packages at the bottom. Compiles are
        # deferred, so nothing clobbers these writes before the end - no
        # per-attack save (it re-walked the whole dirty set every iteration =
        # the storm; see SAVE DISCIPLINE banner).
        _save(asset_path)

        out[r2_attack_name] = att.generated_class()

    print(f'  stamped {len(out)} attack-data assets')
    return out


def stamp_vfx_renderer_bps(flipbooks):
    # Per R1 hit-fx: stamp BP_VFX_<Char>_<sprite> as a Blueprint subclass of
    # ARivalsLua2DFlipbookVfxRenderer with the matching imported flipbook set
    # on its Flipbook UPROPERTY. Returns dict[sprite_name] = (generated_class, frame_count)
    # so the container stamper can wire RendererClass + EffectDuration entries.
    #
    # Two passes:
    #   1. Per-mod hit-fx from R1_HIT_FX (mod-defined hit_fx_create calls).
    #   2. R1 base-game effects (sprites with hfx_/dfx_/fx_ prefix in the
    #      imported set). These cover numeric R1 VFX IDs that the runtime
    #      shim resolves via R1.BaseVfxByID.
    vfx_dest = f'{DEST}/VFX'
    out = {}

    def stamp_one(sprite_name, frame_count, label):
        flipbook = flipbooks.get(sprite_name)
        if not flipbook:
            # No imported flipbook for this hit-fx sprite: no renderer BP is
            # stamped, so the runtime SpawnVfx lookup will fail with a bare
            # ''Error spawning vfx'' and no breadcrumb. Leave one here.
            print(f'  WARN: hit-fx ({label}) sprite {sprite_name} has no imported flipbook - no VFX renderer stamped; runtime SpawnVfx for it will fail')
            return
        bp_name = f'BP_VFX_{CHAR}_{sprite_name}'
        bp_path = f'{vfx_dest}/{bp_name}'
        bp = unreal.load_asset(bp_path)
        if not bp:
            bp_factory = unreal.BlueprintFactory()
            bp_factory.set_editor_property('parent_class', unreal.RivalsLua2DFlipbookVfxRenderer)
            bp = _asset_tools().create_asset(bp_name, vfx_dest, unreal.Blueprint, bp_factory)
            _save(bp_path)
            bp = unreal.load_asset(bp_path)
        cdo = unreal.get_default_object(bp.generated_class())
        cdo.set_editor_property('flipbook', flipbook)
        _compile(bp)
        bp.modify()
        _save(bp_path)
        out[sprite_name] = (bp.generated_class(), int(frame_count))

    # Pass 1: mod-defined hit_fx_create entries (frame count from extractor).
    for sprite_name, frame_count in R1_HIT_FX.items():
        stamp_one(sprite_name, frame_count, 'mod')

    # Pass 1b: prefix-expanded hit-fx. R1 mods build effect sprite names at
    # runtime (`base .. string(level)`); the extractor resolved the literal
    # base and we stamp every imported flipbook that shares it, so e.g.
    # sunball_explosion_lvl0/1/2 all get renderers off the single
    # sunball_explosion_lvl prefix. Duration = the resolved call-site length.
    for prefix, frame_count in R1_HIT_FX_PREFIX.items():
        for stem in flipbooks:
            if stem in out:
                continue
            if stem.startswith(prefix):
                stamp_one(stem, frame_count, 'prefix')

    # Pass 2: R1 base-game effects (frame count from imported flipbook's
    # actual key-frame count — what UMT extracted from data.win).
    for stem, fb in flipbooks.items():
        if stem in out:
            continue
        if not (stem.startswith('hfx_') or stem.startswith('dfx_') or stem.startswith('fx_')):
            continue
        try:
            kfs = fb.get_editor_property('key_frames')
            n = len(list(kfs)) if kfs else 12
        except Exception:
            n = 12
        stamp_one(stem, n, 'base')

    print(f'  stamped {len(out)} vfx renderer BPs')
    return out


def stamp_vfx_definition_container(vfx_renderers):
    # Build the per-mod URivalsVfxDefinitionAsset BP. VfxDefinitions is a
    # TMap<FString, FRivalsVfxDefinition> on the parent URivalsVfxDefinitionContainer.
    # Each entry pairs an R1 sprite name (key the runtime VFX container lookup
    # uses) with a definition referencing the matching renderer BP and frame
    # count. Returns the generated class so the character data wiring step can
    # set CharacterVfxContainerClass on CD_<CHAR>.
    #
    # We populate THREE buckets here:
    #   1. Per-mod entries from vfx_renderers (mod-defined hit_fx_create
    #      calls + base-prefixed sprites the mod shipped).
    #   2. Shared R1 base-game VFX from /Game/R1Compat/BaseVFX/VFX_R1Compat_Base
    #      (built once by scripts/build_r1compat_base_vfx.py). Every R1 mod
    #      references base sprites by name (water_light_omni_spr, etc.) via
    #      R1.BaseVfxByID — without these merged in, SpawnVfx falls through
    #      to UniversalVfxContainer (which doesn't have R1 names) and logs
    #      "Error spawning vfx <name>" warnings.
    # Mod entries take precedence on name collisions (mod ships its own
    # override of a base name).
    vfx_dest = f'{DEST}/VFX'
    container_name = f'VFX_{CHAR}'
    # Reuse the scaffold's original container at the char-folder root. CreateNewCharacter
    # (WorkshopToolStatics) stamps VFX_<Char> there and wires CharacterVfxContainerClass to it.
    # Stamping a SECOND container under /VFX/ produced a same-short-name duplicate -> identical
    # namespaced PrimaryAssetId -> the SnapNet render side resolved the wrong (empty) one and no
    # VFX rendered. Populate the root one the scaffold/CD already point at.
    container_path = f'{DEST}/{container_name}'
    container = unreal.load_asset(container_path)
    if not container:
        bp_factory = unreal.BlueprintFactory()
        bp_factory.set_editor_property('parent_class', unreal.RivalsVfxDefinitionAsset)
        container = _asset_tools().create_asset(container_name, DEST, unreal.Blueprint, bp_factory)
        print(f'  created {container_path}')
        _save(container_path)
        container = unreal.load_asset(container_path)
    cdo = unreal.get_default_object(container.generated_class())
    cdo.set_editor_property('vfx_category', unreal.Name(CHAR))

    # Direct set_editor_property on FRivalsVfxDefinition.renderer_class fails
    # with "cannot be edited on instances" (the field is EditDefaultsOnly,
    # which UE Python checks). Route through the C++ helper that does the
    # assignment via direct field write, bypassing the editor-property check.

    # Pass 1: shared base VFX. Add first so mod entries can overwrite on
    # collision (later add_vfx_definition calls overwrite same-key entries).
    base_count = 0
    base_path = '/Game/R1Compat/BaseVFX/VFX_R1Compat_Base'
    base_container = unreal.load_asset(base_path)
    if base_container:
        base_cdo = unreal.get_default_object(base_container.generated_class()) \
            if isinstance(base_container, unreal.Blueprint) else base_container
        try:
            base_defs = base_cdo.get_editor_property('vfx_definitions')
        except Exception as ex:
            print(f'  WARN: failed to read base vfx_definitions ({ex})')
            base_defs = None
        if base_defs:
            for key in list(base_defs.keys()):
                defn = base_defs[key]
                # renderer_class is exposed as the resolved BlueprintGeneratedClass
                # directly from Python — not a soft pointer needing resolution.
                rc = defn.get_editor_property('renderer_class')
                if not rc:
                    continue
                duration = defn.get_editor_property('effect_duration') or 12
                unreal.RivalsLua2DImporterHelpers.add_vfx_definition(
                    cdo, str(key), rc, int(duration))
                base_count += 1
    else:
        print(f'  WARN: base VFX container {base_path} not found — R1 base hit-fx will log spawn-error warnings')

    # Pass 2: per-mod entries.
    mod_count = 0
    if vfx_renderers:
        for sprite_name, (renderer_class, frame_count) in vfx_renderers.items():
            unreal.RivalsLua2DImporterHelpers.add_vfx_definition(
                cdo,
                sprite_name,
                renderer_class,
                int(frame_count))
            mod_count += 1

    if base_count + mod_count == 0:
        print(f'  no VFX entries to stamp; skipping container')
        return None

    _compile(container)
    container.modify()
    _save(container_path)
    print(f'  stamped {container_path}: {mod_count} mod + {base_count} base entries')
    return container.generated_class()


# ── FMOD / SFX stamping ───────────────────────────────────────────────────
# Mirrors the per-mod build pipeline:
#   1. R1Importer (C#) runs build_fmod_bank.py to produce
#      R1Compat_<ModID>.bank + .assets.bank + .strings.bank under
#      Game/Content/FMOD/Desktop/UGC/ AND a per-mod GUIDs snapshot at
#      FMODBuild/GUIDs/R1Compat_<ModID>.txt (with the event GUIDs).
#   2. Below, we read the GUIDs file, stamp UFMODBank + UFMODEvent uassets
#      with the matching AssetGuids, and build SFX_<Char> (a Blueprint
#      subclass of URivalsSoundEffectContainer) with both per-mod and
#      shared-base SFX entries.
#   3. stamp_character_data wires CD_<Char>.SoundEffectContainer to it.

_FMOD_BASE_BANK_NAME = 'R1Compat_Base'


def _parse_fmod_guids_file(path, bank_name, event_prefix):
    # Returns {bank_main: (guid, name) | None, events: [(guid, name)]}.
    # Skips silently when path doesn't exist (e.g. mod has no audio).
    import re as _re, os as _os
    out = {'bank_main': None, 'events': []}
    if not _os.path.exists(path):
        return out
    pat = _re.compile(r'\{([0-9a-f-]+)\}\s+(bank:|event:)(\S+)')
    with open(path) as f:
        for line in f:
            m = pat.search(line)
            if not m: continue
            guid_str, kind, path_str = m.group(1), m.group(2), m.group(3)
            if kind == 'bank:' and bank_name in path_str and path_str.endswith(bank_name):
                out['bank_main'] = (guid_str, bank_name)
            elif kind == 'event:' and path_str.startswith(event_prefix):
                out['events'].append((guid_str, path_str[len(event_prefix):]))
    return out


def _guid_str_to_unreal(guid_str):
    g = unreal.Guid()
    g.import_text(guid_str.replace('-', '').upper())
    return g


def _stamp_fmod_guid(asset, asset_guid, asset_path):
    asset.set_editor_property('asset_guid', asset_guid)
    asset.modify()
    _save(asset_path)


def _sanitize_fmod_uasset_name(name):
    # UE asset names allow only [A-Za-z0-9_]. FMOD event names from GML
    # can have spaces, hyphens, etc. (e.g. "sfx_waveland_hod - old").
    # Without sanitizing, _asset_tools().create_asset silently returns None
    # and the uasset never gets stamped — the SFX container ends up with
    # a TMap entry whose UFMODEvent ref is null and runtime PlaySFX
    # fails with "Invalid sound instance". Sanitization is uasset-name-
    # only; the SFX container's TMap key keeps the original GML name so
    # runtime sound_get lookups still match.
    out = re.sub(r'[^A-Za-z0-9_]+', '_', name).strip('_')
    return out or 'asset'


def _find_or_create_fmod_asset(asset_class, package_path, asset_name, asset_guid):
    safe_name = _sanitize_fmod_uasset_name(asset_name)
    full_path = f'{package_path}/{safe_name}'
    existing = unreal.load_asset(full_path)
    if existing:
        cur = existing.get_editor_property('asset_guid')
        if cur.to_string() != asset_guid.to_string():
            _stamp_fmod_guid(existing, asset_guid, full_path)
        return existing
    pkg = _asset_tools().create_asset(
        asset_name=safe_name, package_path=package_path, asset_class=asset_class, factory=None)
    if not pkg:
        return None
    _stamp_fmod_guid(pkg, asset_guid, full_path)
    return pkg


def _stamp_fmod_bank_and_events(parsed, bank_name, event_package_path):
    # Returns (bank_asset, {event_name: event_asset}). Skips if bank
    # not found in parsed GUIDs (e.g. base bank not built on this system).
    if not parsed['bank_main']:
        return None, {}
    bank_class = unreal.load_class(None, '/Script/FMODStudio.FMODBank')
    bank_dir = '/Game/FMOD/Banks/UGC'
    if not unreal.EditorAssetLibrary.does_directory_exist(bank_dir):
        unreal.EditorAssetLibrary.make_directory(bank_dir)
    bank_guid, _ = parsed['bank_main']
    bank_asset = _find_or_create_fmod_asset(bank_class, bank_dir, bank_name, _guid_str_to_unreal(bank_guid))

    event_class = unreal.load_class(None, '/Script/FMODStudio.FMODEvent')
    if not unreal.EditorAssetLibrary.does_directory_exist(event_package_path):
        unreal.EditorAssetLibrary.make_directory(event_package_path)
    event_assets = {}
    for guid, name in parsed['events']:
        ev = _find_or_create_fmod_asset(event_class, event_package_path, name, _guid_str_to_unreal(guid))
        if ev:
            event_assets[name] = ev
    return bank_asset, event_assets


def stamp_sfx_container():
    # Create SFX_<Char> Blueprint (URivalsSoundEffectContainer subclass) with
    # per-mod + shared-base SFX entries. Returns the generated class so
    # stamp_character_data can wire it. Returns None if no per-mod bank was
    # built (mod has no audio + no --fmod-cli) — CD wiring then falls back
    # to the universal SFX container only.
    import os as _os
    mod_bank_name = f'R1Compat_{MOD_ID}'
    mod_guids_file = _os.path.join(FMOD_BUILD_GUIDS_DIR, f'R1Compat_{MOD_ID}.txt')
    base_guids_file = _os.path.join(FMOD_BUILD_GUIDS_DIR, f'{_FMOD_BASE_BANK_NAME}.txt')

    print('-- SFX: stamping FMOD assets --')
    mod_parsed = _parse_fmod_guids_file(mod_guids_file, mod_bank_name, f'/R1Compat/{MOD_ID}/')
    mod_bank, mod_events = _stamp_fmod_bank_and_events(
        mod_parsed, mod_bank_name, f'/Game/FMOD/Events/R1Compat/{MOD_ID}')
    print(f'  per-mod: bank={mod_bank_name if mod_bank else "(missing)"} events={len(mod_events)}')

    base_parsed = _parse_fmod_guids_file(base_guids_file, _FMOD_BASE_BANK_NAME, '/R1Compat/Base/')
    base_bank, base_events = _stamp_fmod_bank_and_events(
        base_parsed, _FMOD_BASE_BANK_NAME, '/Game/FMOD/Events/R1Compat/Base')
    print(f'  base: bank={_FMOD_BASE_BANK_NAME if base_bank else "(missing)"} events={len(base_events)}')

    if not mod_bank and not base_bank:
        print('  no banks found — skipping SFX container stamp')
        return None

    sfx_class = unreal.load_class(None, '/Script/Rivals2.RivalsSoundEffectContainer')
    sfx_path = f'{DEST}/SFX_{CHAR}'
    sfx = unreal.load_asset(sfx_path)
    if not sfx:
        factory = unreal.BlueprintFactory()
        factory.set_editor_property('parent_class', sfx_class)
        sfx = _asset_tools().create_asset(asset_name=f'SFX_{CHAR}', package_path=DEST,
            asset_class=unreal.Blueprint, factory=factory)
        print(f'  created SFX_{CHAR} blueprint')

    cdo = unreal.get_default_object(sfx.generated_class()) if isinstance(sfx, unreal.Blueprint) else sfx
    banks = [b for b in (mod_bank, base_bank) if b]
    cdo.set_editor_property('associated_banks', banks)
    cdo.set_editor_property('sfx_category', unreal.Name(CHAR))

    # Build the SoundEffectData map. bCanBeStopped=True is REQUIRED for
    # StopSFX to actually stop a playing instance (RCE.cpp:1132) — without
    # it R1's `sound_stop` no-ops AND the implicit replace-on-replay of
    # legacy GM `sound_play` doesn't fire, so per-frame triggers stack.
    # Mod events overwrite base entries on key collisions (mod ships its
    # own override of a base sound name).
    data_type = unreal.RivalsSoundEffectData
    sfx_map = unreal.Map(unreal.Name, data_type)
    def _entry(ev):
        d = data_type()
        # SoundEffect UPROPERTY is EditDefaultsOnly; import_text bypasses the
        # editor-instance check that set_editor_property enforces.
        d.import_text(f'(SoundEffect="{ev.get_path_name()}",bCanBeStopped=True)')
        return d
    for name, ev in base_events.items():
        sfx_map[unreal.Name(name)] = _entry(ev)
    for name, ev in mod_events.items():
        sfx_map[unreal.Name(name)] = _entry(ev)
    cdo.set_editor_property('sound_effect_data', sfx_map)

    if isinstance(sfx, unreal.Blueprint):
        _compile(sfx)
        sfx.modify()
    _save(sfx_path)
    print(f'  stamped {sfx_path} with {len(sfx_map)} entries')
    return sfx.generated_class() if isinstance(sfx, unreal.Blueprint) else None


def stamp_character_data(flipbooks, attack_classes=None, vfx_container_class=None, sfx_container_class=None):
    if attack_classes is None:
        attack_classes = {}
    cd_path = f'{DEST}/CD_{CHAR}'
    cd = unreal.load_asset(cd_path)
    if not cd:
        bp_factory = unreal.BlueprintFactory()
        bp_factory.set_editor_property('parent_class', _CHAR_DATA_PARENT)
        cd = _asset_tools().create_asset(f'CD_{CHAR}', DEST, unreal.Blueprint, bp_factory)
        print(f'  created {cd_path}')
    # Advanced wires R1 runtime behavior, so the CD must be an R1 subclass even
    # when the scaffold (or a prior basic import) left it vanilla Lua2D. basic/
    # assetsonly keep the scaffold's Lua2D parent — a first-class R2-native char.
    if _ADVANCED:
        _ensure_r1_parent(cd, unreal.RivalsR1CharacterData)
    cdo = unreal.get_default_object(cd.generated_class())

    # Animations map: R1 stem → soft path to flipbook. We use the R1 name
    # as the key so the modder can match it against state/attack maps.
    anims = unreal.Map(unreal.Name, unreal.SoftObjectPath)
    for stem, fb in flipbooks.items():
        anims[stem] = unreal.SoftObjectPath(fb.get_path_name())
    cdo.set_editor_property('animations', anims)

    # Default animation key — pick 'idle' if we have it.
    if 'idle' in flipbooks:
        cdo.set_editor_property('default_animation_key', unreal.Name('idle'))

    # State key map. We add the forward STATE_MAP plus the BACKWARD variants
    # pointing at the same sprite stems — R1's engine flips sprites for
    # facing, R2 needs an explicit BACKWARD-state entry pointing at the same
    # flipbook so the sprite shows up at all.
    sm = unreal.Map(unreal.RivalsCharacterState, unreal.Name)
    for stem, state in STATE_MAP.items():
        if stem in flipbooks:
            sm[getattr(unreal.RivalsCharacterState, state)] = unreal.Name(stem)
    for stem, state in STATE_MAP_BACKWARD.items():
        if stem in flipbooks:
            sm[getattr(unreal.RivalsCharacterState, state)] = unreal.Name(stem)

    # Aliases: many R1 mods don't have separate sprites for short hops or
    # forward-facing jump variants — they share the regular jump anim, with R1
    # picking velocity by state. Substitute the corresponding base flipbook so
    # ShortHop/etc. don't fall through to Idle.
    ALIASES = [
        ('SHORT_HOP', 'jump_short', 'jump'),
        ('SHORT_HOP_BACKWARD', 'jump_short', 'jump'),
        ('FULL_HOP_BACKWARD', 'jump', 'jump'),
        ('DOUBLE_JUMP_BACKWARD', 'doublejump', 'doublejump'),
        # Per R1 docs the jump sprite covers both rising and falling parts
        # of normal airtime; FALL therefore reuses the same flipbook.
        ('FALL', 'jump', 'pratfall'),
        # R1 has no dedicated fall-through-platform sprite — character
        # stays in the jump/fall airborne anim during plat drop.
        ('PLAT_DROP', 'jump', 'jump'),
        # R1 has only `dashstop` for both R2 DASH_STOP and RUN_STOP.
        # Without RUN_STOP mapped, RunStop falls through to DefaultAnimationKey
        # ('idle') — which wedges the loop flag on the renderer because the
        # key swap to 'idle' happens during the non-looping RunStop state, and
        # the renderer only re-evaluates SetLooping on key swap. Subsequent
        # Idle has key=='idle' (no swap) → bLooping stays false → idle plays
        # once and stops. (Renderer ought to refresh SetLooping per tick;
        # that's a separate engine fix. Until then, mapping RUN_STOP to the
        # dashstop sprite keeps it on a non-default key.)
        ('RUN_STOP', 'dashstop', 'dash'),
        ('WALK_STOP', 'dashstop', 'walk'),
        # R1 ground-dodge uses the `parry` sprite by convention. R1 source
        # (e.g. objects/absa_anim.gml:140) all roster anim scripts:
        # `case player_state.dodge: sprite_index = goat_parry;`. Modders
        # follow the same convention — ship `parry`, no `spotdodge`.
        ('SPOT_DODGE', 'spotdodge', 'parry'),
        # R1 tech-rolls reuse the regular ground-roll sprites (absa_anim.gml
        # lines 167-179: `case tech_backward: sprite_index = goat_roll_backward;`
        # `case tech_forward: sprite_index = goat_roll_forward;`).
        # No R1 mod ships dedicated tech-roll sprites; map to roll_*.
        ('TECH_ROLL_FORWARD',  'tech_forward',  'roll_forward'),
        ('TECH_ROLL_BACKWARD', 'tech_backward', 'roll_backward'),
        # R1 doesn't separate getup from tech — `tech` is the in-place
        # standup-equivalent, and roll_forward/backward double as getup rolls
        # (no R1 mod ships dedicated getup sprites). R1 miss-tech enters
        # player_state.hitstun_land which plays the single-frame `hurtground`
        # sprite the whole time (tumble_ground_collision.gml). We map all
        # three R2 knockdown sub-states to that one frame since R1 has no
        # KnockdownStart/Knockdown/KnockdownHurt distinction.
        ('GETUP_NEUTRAL',       'tech',          'tech'),
        ('GETUP_ROLL_FORWARD',  'roll_forward',  'roll_forward'),
        ('GETUP_ROLL_BACKWARD', 'roll_backward', 'roll_backward'),
        ('KNOCKDOWN_START',     'hurtground',    'hurtground'),
        ('KNOCKDOWN',           'hurtground',    'hurtground'),
        ('KNOCKDOWN_HURT',      'hurtground',    'hurtground'),
        # R1 has no throw system so no `grabbed` sprite — the closest visual
        # is the regular hitstun pose. R1's anim scripts use the same `hurt`
        # sprite for both light and medium hitstun; reuse it here for the
        # R2 GRABBED state too.
        ('GRABBED',             'hurt',          'hurt'),
        # R1 has no shield-break animation. Closest match is the tumble
        # sprite (`spinhurt` in R1 convention per stinky_anim.gml), used for
        # spinning launches. Fall back to bouncehurt if a char skipped
        # spinhurt — both convey stunned/dazed reasonably.
        ('SHIELD_BREAK',        'spinhurt',      'bouncehurt'),
        ('SHIELD_BREAK_STUN',   'spinhurt',      'bouncehurt'),
    ]
    for state_name, primary_stem, fallback_stem in ALIASES:
        s = getattr(unreal.RivalsCharacterState, state_name)
        if s in sm:
            continue
        for stem in (primary_stem, fallback_stem):
            if stem in flipbooks:
                sm[s] = unreal.Name(stem)
                break

    cdo.set_editor_property('state_flipbook_keys', sm)

    # Attack key map.
    am = unreal.Map(unreal.RivalsCharacterAttack, unreal.Name)
    for stem, attack in ATTACK_MAP.items():
        if stem in flipbooks:
            am[getattr(unreal.RivalsCharacterAttack, attack)] = unreal.Name(stem)
    cdo.set_editor_property('attack_flipbook_keys', am)

    # Blank out the bone-driven hurtbox refs since 2D characters don't have a
    # proper skeleton. We supply a single body-shaped HurtboxDefinitions
    # entry derived from ECBDimensions so the character has SOMETHING the
    # hit-detection system can collide with.
    cdo.set_editor_property('hurtboxes_skeletal_mesh', None)
    cdo.set_editor_property('hurtboxes_physics_asset', None)

    # Hurtbox geometry. Independent of ECB: R1's hurtbox is the
    # `hurtbox_spr` sprite's mask; ECB is just `width` for wall collision.
    # Try the sprite first; fall back to ECB-shaped approximation if no
    # hurtbox_spr ref found.
    hurt_dims = _read_hurtbox_sprite_dims()
    HURT_SCALE = 2.5
    if hurt_dims is not None:
        hurt_w = hurt_dims[0] * HURT_SCALE
        hurt_h = hurt_dims[1] * HURT_SCALE
    else:
        ecb = cdo.get_editor_property('ecb_dimensions')
        hurt_w = float(ecb.x) if ecb else 50.0
        hurt_h = float(ecb.y) if ecb else 100.0
        print(f'  hurtbox: no hurtbox_spr — falling back to ECB-shaped {hurt_w:.1f}x{hurt_h:.1f}')

    # R2 NewCapsule = two endpoints + radius. For a body-shaped capsule:
    #   - If taller than wide (typical character): vertical capsule.
    #     radius = hurt_w/2; endpoints span Z from radius to hurt_h-radius.
    #   - If wider than tall (rare, e.g. crouched / quadrupedal char):
    #     horizontal capsule. radius = hurt_h/2; endpoints span X from
    #     -(hurt_w/2 - radius) to +(hurt_w/2 - radius) at Z = hurt_h/2.
    if hurt_h >= hurt_w:
        radius = max(8.0, hurt_w * 0.5)
        a = unreal.Vector(0.0, 0.0, radius)
        b = unreal.Vector(0.0, 0.0, max(radius + 1.0, hurt_h - radius))
    else:
        radius = max(8.0, hurt_h * 0.5)
        half_axis = max(0.0, hurt_w * 0.5 - radius)
        z_center = hurt_h * 0.5
        a = unreal.Vector(-half_axis, 0.0, z_center)
        b = unreal.Vector(+half_axis, 0.0, z_center)

    hb = unreal.RivalsHurtboxDefinition()
    hb.set_editor_property('hurtbox_definition_type',
                           unreal.RivalsHurtboxDefinitionType.NEW_CAPSULE)
    hb.set_editor_property('offset_from_origin', a)
    hb.set_editor_property('offset_from_origin2', b)
    hb.set_editor_property('hurtbox_radius', radius)
    hb.set_editor_property('hurtbox_name', 'Body')
    hb.set_editor_property('hurtbox_active', True)
    hbs = unreal.Array(unreal.RivalsHurtboxDefinition)
    hbs.append(hb)
    try:
        cdo.set_editor_property('hurtbox_definitions', hbs)
    except Exception as ex:
        print(f'  hurtbox_definitions: failed to set ({ex})')

    cdo.set_editor_property('lua_script_path', f'{MOD_ID}/Scripts/{CHAR}.lua')
    cdo.set_editor_property('lua_metatable_name', CHAR)

    # Wire AttackData TMap to the per-attack ATT_<CHAR>_<MOVE> assets stamped
    # earlier. Engine reads from this map for window timing and other static
    # attack metadata; runtime hitboxes come from the Lua override.
    if attack_classes:
        ad = unreal.Map(unreal.RivalsCharacterAttack, unreal.SoftClassPath)
        for r2_name, gen_class in attack_classes.items():
            ad[getattr(unreal.RivalsCharacterAttack, r2_name)] = unreal.SoftClassPath(gen_class.get_path_name())
        try:
            cdo.set_editor_property('attack_data', ad)
        except Exception as ex:
            # AttackData might be TMap<E, TSubclassOf<...>> rather than
            # SoftClassPath. Fall back.
            try:
                ad2 = unreal.Map(unreal.RivalsCharacterAttack, unreal.RivalsCharacterAttackData)
                for r2_name, gen_class in attack_classes.items():
                    ad2[getattr(unreal.RivalsCharacterAttack, r2_name)] = gen_class
                cdo.set_editor_property('attack_data', ad2)
            except Exception as ex2:
                print(f'  attack_data wire failed: {ex2}')

    # Stamp movement physics from R1 init.gml so the engine has real values
    # to drive walking / jumping / gravity (R2 reads these directly from
    # character data; r1_state is consulted only by Lua-overridden virtuals).
    apply_movement_physics(cdo)

    # Wire the per-mod VFX container so SpawnVfx(name) lookups for R1
    # hit-fx names (sweatwhirlhit, splash, etc.) resolve to the BP renderers
    # we stamped; without this they'd fall through to UniversalVfxContainer
    # and miss every mod-defined name.
    if vfx_container_class is not None:
        cdo.set_editor_property('character_vfx_container_class', vfx_container_class)

    # Wire the SFX container so PlaySFX(name) lookups for R1 sound names
    # (sfx_stinky_steam1, sfx_swipe_medium2, etc.) resolve via the per-mod
    # bank + the shared R1Compat_Base bank. Without this CD wire, PlaySFX
    # falls through to GameInstance->UniversalSfxContainer which only has
    # R2-named entries (Jump, Dash, ...).
    if sfx_container_class is not None:
        cdo.set_editor_property('sound_effect_container', sfx_container_class)

    _compile(cd)
    cd.modify()
    _save(cd_path)
    return cd


def stamp_articles(flipbooks):
    # Per-article AD_<Char>_Article<N>.uasset Blueprint of URivalsLua2DArticleData.
    # The matching `<Char>_Article<N>.lua` entry-point is emitted by R1Importer
    # alongside Hodan.lua. Together they let R1's `instance_create(obj_articleN)`
    # spawn an entity whose lifecycle hooks fire articleN_init / articleN_update.
    if not ARTICLE_NUMBERS:
        return {}
    art_dest = f'{DEST}/Articles'
    out = {}
    for n in ARTICLE_NUMBERS:
        article_metaname = f'{CHAR}_Article{n}'
        asset_name = f'AD_{article_metaname}'
        asset_path = f'{art_dest}/{asset_name}'
        ad = unreal.load_asset(asset_path)
        if not ad:
            bp_factory = unreal.BlueprintFactory()
            bp_factory.set_editor_property('parent_class', _ARTICLE_DATA_PARENT)
            ad = _asset_tools().create_asset(asset_name, art_dest, unreal.Blueprint, bp_factory)
            print(f'  created {asset_path}')
            # SoftClassPtr property writes silently fail on a freshly-created
            # BP CDO (the soft-class slot isn't initialized yet). Save then
            # reload to bake the asset before continuing.
            _save(asset_path)
            ad = unreal.load_asset(asset_path)
        if _ADVANCED:
            _ensure_r1_parent(ad, unreal.RivalsR1ArticleData)
        addo = unreal.get_default_object(ad.generated_class())
        # ArticleClass — the runtime entity to spawn. Lua2DArticleEntity wraps
        # the article as a sprite-rendered projectile; matches our 2D char.
        # basic uses the vanilla Lua2D entity; advanced uses the R1 subclass.
        addo.set_editor_property('article_class', _ARTICLE_ENTITY_CLASS)
        # Renderer — without this the article entity exists but nothing
        # draws. Lua2DArticleRenderer pulls the flipbook from
        # ArticleData.Animations[GetCurrent2DAnimation()].
        try:
            addo.set_editor_property('default_renderer_class',
                unreal.RivalsLua2DArticleRenderer)
        except Exception as ex:
            print(f'  article{n}: failed to set renderer_class: {ex}')
        # Lua wiring — script path is `<ModID>/Scripts/<File>.lua` (the
        # subsystem splits on the first '/' to extract the mod ID, then
        # resolves the rest under ModContent or the Steam workshop dir).
        # Metatable name matches `<Char>_Article<N> = Class(...)` in script.
        addo.set_editor_property('lua_script_path', f'{MOD_ID}/Scripts/{article_metaname}.lua')
        addo.set_editor_property('lua_metatable_name', article_metaname)

        # Default flipbook for the article — character-specific naming
        # (Hodan article1 = `vapour`, article3 = `sweatwhirl`) means we can't
        # rely on an `articleN` stem. Scan the article's GML init script for
        # the first `sprite_get('xxx')` call and try that stem against our
        # imported flipbooks; fall back to generic candidates.
        article_flipbook = None
        article_gml = f'{R1_ROOT}/scripts/article{n}_init.gml'
        sprite_name = None
        try:
            with open(article_gml, 'r', encoding='utf-8', errors='replace') as fh:
                gml_text = fh.read()
            import re as _re
            # R1 GML always quotes strings with double-quotes. The doubled
            # marks below are how C# verbatim strings escape a single quote
            # mark, so Python sees the pattern: sprite_get\s*\(\s*X(\w+)X\s*\)
            # where X is a single double-quote.
            m = _re.search(r'sprite_get\s*\(\s*"(\w+)"\s*\)', gml_text)
            if m:
                sprite_name = m.group(1)
        except Exception as ex:
            print(f'  article{n}: failed to scan {article_gml}: {ex}')
        candidates = []
        if sprite_name:
            # Strip common suffixes that aren't the spawn-default sprite.
            base = sprite_name
            for suf in ('_hurt', '_idle', '_strip', '_charge'):
                idx = base.find(suf)
                if idx > 0:
                    base = base[:idx]
                    break
            candidates.append(base)
            candidates.append(sprite_name)
        candidates.extend([f'article{n}', f'article{n}_idle'])
        for stem in candidates:
            if stem in flipbooks:
                article_flipbook = flipbooks[stem]
                break
        # Populate the Animations map with every imported flipbook keyed by
        # its sprite stem. R1 articles (and character animation scripts)
        # write `sprite_index = sprite_get('xxx')` and the engine renders
        # whatever stem they pointed at. We can't predict at import time
        # which stems an article will switch between (depends on per-frame
        # script logic), so make every imported sprite resolvable. The map
        # is just (Name → SoftObjectPath) — no runtime cost beyond the
        # import-time map population.
        anims = unreal.Map(unreal.Name, unreal.SoftObjectPath)
        for stem, fb in flipbooks.items():
            anims[stem] = unreal.SoftObjectPath(fb.get_path_name())
        addo.set_editor_property('animations', anims)
        # Default key — pick the article's discovered default if we found
        # one; otherwise default to 'empty_sprite', which the Lua2D article
        # renderer special-cases to HIDE the flipbook until the mod's
        # init/update assigns sprite_index. The old fallback to the first
        # imported flipbook picked the alphabetical-first stem ('airdodge'),
        # which flashed at the spawn point for a frame or two before the
        # mod sprite propagated (task #163) - same fix as the projectile
        # stamping path below.
        if article_flipbook:
            for stem, fb in flipbooks.items():
                if fb is article_flipbook:
                    addo.set_editor_property('default_animation_key', unreal.Name(stem))
                    break
        else:
            addo.set_editor_property('default_animation_key', unreal.Name('empty_sprite'))

        # --- R1 article hittability (systemic, all imported articles) ---
        # R1 articles flagged `is_hittable` can be struck by attacks. Glub's
        # DSP ball relies on this for a whole interaction class: the owner hits
        # it with normals (it bounces), grabs it with USP/SSP, and eats it with
        # NSP — ALL of which route through the ball's got_hit
        # (article{n}_hit.lua), which only fires when an attack's hitbox
        # confirms an overlap on the article. Two engine prerequisites the
        # importer was missing:
        #   1. A HURTBOX. R2 articles build hurtboxes from HurtboxDefinitions;
        #      with none, RivalsDamageInterface::QueryHurtboxes finds nothing
        #      and no overlap is ever generated. (R1's mask_index is mod-side
        #      state — it does NOT create an R2 hurtbox.)
        #   2. OWNER-HITTABILITY. R2 skips a hitbox overlap when the hitbox host
        #      and the target share an owner UNLESS the target's
        #      bCanBeHitByOwner is set (RivalsDamageInterface.cpp:439). R1 has
        #      no such gate (a character can hit its own article), so set it.
        #      bCanHitOwner is left default-false: an article's OWN hitbox
        #      should not hit its owner (R1's hit_player path excludes that;
        #      Glub's ball must not damage Glub).
        try:
            addo.set_editor_property('can_be_hit_by_owner', True)
        except Exception as ex:
            print(f'  article{n}: failed to set can_be_hit_by_owner: {ex}')
        # Hurtbox geometry: the R1 collision-mask sprite isn't imported as a
        # flipbook, so its exact dims aren't available at stamp time. Use a
        # modest sphere centered on the article origin, scaled to R2. Articles
        # are typically small (balls / projectiles); this makes them hittable.
        # Refine from the article's mask sprite later if precise sizing matters.
        try:
            HSCALE = 2.5
            radius = max(8.0, 16.0 * HSCALE)  # ~32 R1 px article extent
            hb = unreal.RivalsHurtboxDefinition()
            hb.set_editor_property('hurtbox_definition_type',
                                   unreal.RivalsHurtboxDefinitionType.NEW_CAPSULE)
            hb.set_editor_property('offset_from_origin', unreal.Vector(0.0, 0.0, 0.0))
            hb.set_editor_property('offset_from_origin2', unreal.Vector(0.0, 0.0, 0.0))
            hb.set_editor_property('hurtbox_radius', radius)
            hb.set_editor_property('hurtbox_name', 'Body')
            hb.set_editor_property('hurtbox_active', True)
            hbs = unreal.Array(unreal.RivalsHurtboxDefinition)
            hbs.append(hb)
            addo.set_editor_property('hurtbox_definitions', hbs)
        except Exception as ex:
            print(f'  article{n}: failed to stamp hurtbox_definitions: {ex}')

        # Stamp at least one window so ARivalsArticleEntity::GetCurrentWindow()
        # has something to index — the engine asserts hard on `Windows[0]` on
        # an article CDO with empty windows. R1 articles drive their own
        # window/lifetime via the per-tick Lua update; this default window is
        # just a placeholder to keep the engine's data-driven path off the
        # tripwire. StringTableKey 'First' matches the engine's standard
        # initial-window convention.
        try:
            existing_windows = addo.get_editor_property('windows')
            if not existing_windows or len(existing_windows) == 0:
                w = unreal.RivalsArticleWindow()
                w.set_editor_property('string_table_key', 'First')
                w.set_editor_property('window_length_frames', 9999)
                w.set_editor_property('next_window_string_table_key', 'First')
                ws = unreal.Array(unreal.RivalsArticleWindow)
                ws.append(w)
                addo.set_editor_property('windows', ws)
        except Exception as ex:
            print(f'  article{n}: failed to stamp default window: {ex}')

        _compile(ad)
        ad.modify()
        _save(asset_path)
        out[n] = ad.generated_class()
        print(f'  stamped {asset_name}')
    return out


def stamp_projectile_articles(flipbooks):
    # R1's HG_HITBOX_TYPE=2 means the hitbox is a projectile — R1's engine
    # spawns a projectile entity from the hitbox's HG_PROJECTILE_* properties.
    # R2 has no equivalent, so we generate a per-hitbox AD_<Char>_<Atk>_HB<N>_Proj
    # asset that the shim instance-creates on window entry. Projectile
    # velocity is a VISUAL travel rate authored against R1's sprite scale,
    # so use POSITION_SCALE (--position-scale CLI flag, default 2.5). This
    # is the AD-stamped fallback; runtime override in tick_projectile_hitboxes
    # also uses POSITION_SCALE.
    SCALE = 2.5  # R1 px/frame → R2 units (visual scale).
    out = {}
    proj_dest = f'{DEST}/Projectiles'
    for at_name, bucket in R1_ATTACKS.items():
        for hb_idx, hb in bucket.get('hitboxes', {}).items():
            num = hb.get('num', {})
            str_keys = hb.get('str', {})
            if int(num.get('HG_HITBOX_TYPE', 0)) != 2:
                continue

            # Asset / metatable / lua paths.
            tag = f'{at_name}_HB{hb_idx}'
            class_name = f'{CHAR}_{tag}_Proj'
            asset_name = f'AD_{class_name}'
            asset_path = f'{proj_dest}/{asset_name}'

            ad = unreal.load_asset(asset_path)
            if not ad:
                bp_factory = unreal.BlueprintFactory()
                bp_factory.set_editor_property('parent_class', unreal.RivalsR1ArticleData)
                ad = _asset_tools().create_asset(asset_name, proj_dest, unreal.Blueprint, bp_factory)
                print(f'  created {asset_path}')
                # SoftClassPtr writes need a saved+reloaded asset (see stamp_articles).
                _save(asset_path)
                ad = unreal.load_asset(asset_path)
            _ensure_r1_parent(ad, unreal.RivalsR1ArticleData)
            addo = unreal.get_default_object(ad.generated_class())
            addo.set_editor_property('article_class', unreal.RivalsR1ArticleEntity)
            try:
                addo.set_editor_property('default_renderer_class',
                    unreal.RivalsLua2DArticleRenderer)
            except Exception as ex:
                print(f'  proj {class_name}: failed to set renderer_class: {ex}')
            addo.set_editor_property('lua_script_path', f'{MOD_ID}/Scripts/{class_name}.lua')
            addo.set_editor_property('lua_metatable_name', class_name)
            # Set the originating attack so the article's GetAttack() returns
            # the right enum (FSPECIAL/NSPECIAL/etc). hitbox_update.gml branches
            # on `attack == AT_*` — without this it sees None and never matches.
            r2_attack_name = R1_AT_TO_R2_ATTACK.get(at_name)
            if r2_attack_name and hasattr(unreal.RivalsCharacterAttack, r2_attack_name):
                addo.set_editor_property('attack',
                    getattr(unreal.RivalsCharacterAttack, r2_attack_name))

            # Collision: Simple ECB sphere centered on the article. Destroy
            # on ground / wall / ceiling impact — matches R1's HG_PROJECTILE_
            # WALL_BEHAVIOR=0 default (the only value Hodan's mod sets).
            # Bouncing, GoToWindow, etc. would need finer translation; defer.
            try:
                # R1 TYPE=2 projectiles don't pause the inflictor on hit
                # (pHitBox/hurtbox_collision.gml:1450-1460 only pauses TYPE=1).
                # R2 propagates article hitpause to OwnerRival when
                # IsAttachedToOwner() is true (RivalsArticleEntity.cpp:93-99) —
                # which then gates the inflictor's UpdateState (RCE.cpp:6008)
                # and stops update.gml from firing. Explicitly clear the flag
                # so mod-side per-frame logic (sweatwhirl_charged_hit follow-up,
                # multihit slot 4 spawning) keeps ticking through the hit.
                addo.set_editor_property('is_attached_to_owner', False)
                # ALWAYS COMPLEX for projectiles. SIMPLE only resolves GROUND (its
                # capsule trace folds walls into HitGround), so it can't honor the
                # per-axis wall/ceiling responses below, and it never sets bGrounded
                # (which the shim reads via IsGrounded() to drive R1 `free`). COMPLEX
                # runs ResolveECBSides->HitWall + ResolveECBTop->HitCeiling +
                # ResolveECBBottom->HitGround/bGrounded. Wall passthrough (wall=1 ->
                # WallCollisionResponse=None) is handled by
                # ARivalsLua2DArticleEntity::ResolveECBSides, which skips side
                # resolution for None -- R2's base ResolveECBSides ejects out of walls
                # unconditionally (only the *response* is gated, not the teleport).
                addo.set_editor_property('ecb_type', unreal.ArticleEcbType.COMPLEX)
                # Size the ECB to the R1 sprite mask so R2's native rest matches R1.
                # R1 GROUNDS projectiles via the SPRITE mask (proj_movement.gml:19
                # forces mask_index = collision_sprite = sprite_index, and uses
                # bounds_bottom = y + (bbox_bottom - yoffset)), NOT the HG hitbox box
                # used for hit detection. radius = mask half-width.
                #
                # COORD FLIP (the bug this fixes): the sprite bbox (ox/oy/h) is in
                # R1/GM room coords (Y-DOWN, +Y below the pivot). R2's ecb_center_offset
                # is consumed in Y-UP coords -- GetECBPosition() places the Down point at
                # (origin.Y - EcbRadius + EcbCenterOffset.Y) and the rest-reposition adds
                # +EcbRadius - GetECBOffset() (RivalsArticleEntity.cpp:808,1230). So the
                # offset must be emitted in Y-UP. The mask bottom sits (oy + h) BELOW the
                # pivot (Y-down); to land the Down ECB there we need
                #   EcbCenterOffset.Y = halfw - (oy + h)   [Y-up]
                # i.e. the NEGATION of the naive Y-down center. Without the flip an
                # off-center-art projectile (bamboo, drawn high) gets its ECB pushed
                # ~2*offset too low and grounds/dies early. SCALE = POSITION_SCALE.
                _ecb_mask = str_keys.get('HG_PROJECTILE_MASK', '') or ''
                if (not _ecb_mask) or _ecb_mask == '-1':
                    _ecb_mask = str_keys.get('HG_PROJECTILE_SPRITE', '') or ''
                _ecb_bb = BBOXES.get(_ecb_mask)
                if _ecb_bb and _ecb_bb[0] > 0:
                    _ecb_w, _ecb_h, _ecb_ox, _ecb_oy = _ecb_bb
                    _ecb_halfw = _ecb_w * 0.5
                    _ecb_offy = (_ecb_halfw - _ecb_oy - _ecb_h) * SCALE
                    addo.set_editor_property('ecb_radius', float(_ecb_halfw * SCALE))
                    addo.set_editor_property('ecb_center_offset',
                        unreal.Vector2D(0.0, float(_ecb_offy)))
                    print(f'  proj {class_name}: ECB from mask {_ecb_mask} r={_ecb_halfw*SCALE:.1f} offY={_ecb_offy:.1f}')
                else:
                    addo.set_editor_property('ecb_radius', 16.0)
                addo.set_editor_property('should_get_out_of_ground_on_spawn', False)
                # DESTROY queues deactivation via QueueDeactivation, which
                # flips DeactivationQueued. Our EndFrame override and the new
                # OnDeactivated hook BOTH catch that path and run the death
                # chain — so the mod's `if (destroyed) { create_vapour... }`
                # branch fires before R2 destroys the article. NONE was tried
                # briefly but means projectiles never die from collision (R1
                # mods authoring against `if (!free)` etc. depend on R2 doing
                # the engine-level cleanup that R1's engine does).
                # Per-hitbox collision response, mirroring R1 proj_movement.gml
                # (WALL_BEHAVIOR macro 47, GROUND_BEHAVIOR macro 48):
                #   wall:   0=destroy 1=passthrough 2=bounce
                #   ground -1=destroy 0=stop+rest 1=passthrough 2=bounce
                # Was a blanket DESTROY, which vanished dspecial-air on contact
                # instead of letting it rest+plant.
                _R = unreal.ArticleCollisionResponse
                _gb = int(num.get('HG_PROJECTILE_GROUND_BEHAVIOR', 0))
                _wb = int(num.get('HG_PROJECTILE_WALL_BEHAVIOR', 0))
                _ground_map = {-1: _R.DESTROY, 0: _R.STOP, 1: _R.NONE, 2: _R.BOUNCE}
                addo.set_editor_property('ground_collision_response',
                    _ground_map.get(_gb, _R.DESTROY))
                addo.set_editor_property('wall_collision_response',
                    {0: _R.DESTROY, 1: _R.NONE, 2: _R.BOUNCE}.get(_wb, _R.DESTROY))
                # R1 has no separate ceiling behavior: proj_movement.gml's vsp loop
                # applies `grounds` to BOTH floor (vsp>0) and ceiling (vsp<0), so
                # ceiling = the ground map. Was hardcoded DESTROY, which destroyed a
                # rest/bounce projectile that touched a ceiling instead of stopping/
                # bouncing (e.g. a projectile reaching the stage top).
                addo.set_editor_property('ceiling_collision_response',
                    _ground_map.get(_gb, _R.DESTROY))
                # On-HIT destroy. R1 destroys a TYPE-2 projectile the instant it hits
                # an enemy when HG_PROJECTILE_ENEMY_BEHAVIOR (enemies) == 0 -- the
                # engine rule in hurtbox_collision.gml, not mod code. enemies>0 means
                # pierce that many enemies, so it must NOT die on first hit. R2's
                # native equivalent is the central ApplyHitboxEffect HasHitReaction
                # switch: DESTROY -> QueueDeactivation -> DeactivationQueued -> EndFrame
                # DestroyArticle, which is synchronous and (unlike the shim's per-frame
                # poll) NOT GetMatchFrame/hitpause-gated. Without this stamp every
                # imported projectile defaulted to NONE and only the laggy poll killed
                # it, so a leveling projectile (Hodan sweatwhirl) leveled up off its
                # own hit-spawned vapour instead of dying. Per-slot only -- the generic
                # fallback article learns enemies at runtime, so it keeps the poll.
                _enemies = int(num.get('HG_PROJECTILE_ENEMY_BEHAVIOR', 0))
                addo.set_editor_property('has_hit_reaction',
                    unreal.ArticleHitReaction.DESTROY if _enemies == 0
                    else unreal.ArticleHitReaction.NONE)
            except Exception as ex:
                print(f'  proj {class_name}: failed to set collision: {ex}')

            # R1's pHitBox/Draw_0.gml:9 SELF-RENDERS the projectile sprite:
            #   if (visible && sprite_index != empty_sprite)
            #       draw_sprite_ext(sprite_index, image_index, ..., proj_angle, ...)
            # So the article must render ITSELF from HG_PROJECTILE_SPRITE. Owner
            # draw events (pre_draw/post_draw) only ADD overlays on top (Guadua's
            # uspecial rope+arm, Hodan afterimages) — they do NOT redraw the
            # projectile sprite. The earlier blanket True hid every projectile
            # that carries a real sprite (Guadua's bamboo went invisible).
            # empty_sprite projectiles stay hidden at runtime: apply_sprite_index
            # pushes the empty_sprite key and the Lua2D renderer special-cases
            # it to hide the flipbook — mirroring Draw_0.gml's != empty_sprite gate.
            # Animations: stamp all flipbooks (mirrors stamp_articles), then
            # try to set default_animation_key from HG_PROJECTILE_SPRITE.
            anims = unreal.Map(unreal.Name, unreal.SoftObjectPath)
            for stem, fb in flipbooks.items():
                anims[stem] = unreal.SoftObjectPath(fb.get_path_name())
            addo.set_editor_property('animations', anims)
            proj_sprite = str_keys.get('HG_PROJECTILE_SPRITE', '')
            # R1 convention: `_hurt`-suffixed sprites are the collision/
            # hurtbox-mask visualisation (solid green/red dots), and the
            # paired non-suffixed sprite is the actual visible art. Some
            # mods set HG_PROJECTILE_SPRITE to the `_hurt` stem either by
            # convention or mistake — prefer the un-suffixed version when
            # one exists in our flipbook set.
            visible_sprite = proj_sprite
            if proj_sprite.endswith('_hurt'):
                base = proj_sprite[:-len('_hurt')]
                if base in flipbooks:
                    visible_sprite = base
            if visible_sprite and visible_sprite in flipbooks:
                addo.set_editor_property('default_animation_key', unreal.Name(visible_sprite))
            else:
                # Sprite isn't a real flipbook -- almost always empty_sprite (an
                # invisible damage box, e.g. Guadua's ground-DSP hitbox) or unset.
                # Default to 'empty_sprite', which the Lua2D article renderer
                # special-cases to HIDE the flipbook. The old fallback to the first
                # flipbook stem picked the alphabetical-first ('airdodge'), which
                # flashed for a couple frames at the spawn point before the snapshot's
                # Set2DAnimation(empty_sprite) took over (task #163).
                addo.set_editor_property('default_animation_key', unreal.Name('empty_sprite'))

            # Single window, length = HG_LIFETIME (R1 frames; R2 is also 60fps).
            # Velocity from HG_PROJECTILE_HSPEED/VSPEED scaled to R2 units.
            lifetime = int(num.get('HG_LIFETIME', 60))
            hsp = float(num.get('HG_PROJECTILE_HSPEED', 0)) * SCALE
            vsp = -float(num.get('HG_PROJECTILE_VSPEED', 0)) * SCALE  # R1 Y-down → R2 Y-up

            w = unreal.RivalsArticleWindow()
            w.set_editor_property('string_table_key', 'First')
            w.set_editor_property('window_length_frames', max(lifetime, 1))
            # Empty next-window key: when window timer hits HG_LIFETIME, R2's
            # FindWindowIndex returns INDEX_NONE and ArticleEntity::ArticleUpdate
            # calls Deactivate (RivalsArticleEntity.cpp:120). That funnels through
            # our entry-point's EndFrame hook just like HitGround/HitWall/etc.,
            # firing the mod's on-destroy chain via hitbox_update with
            # destroyed=true. (Looping back to First would keep the projectile
            # alive past R1's HG_LIFETIME, breaking R1 fidelity.)
            w.set_editor_property('next_window_string_table_key', '')
            if abs(hsp) > 0.001 or abs(vsp) > 0.001:
                vd = unreal.RivalsWindowVelocityData()
                vd.set_editor_property('velocity', unreal.Vector2D(hsp, vsp))
                vd.set_editor_property('apply_velocity_on_window_frame', 0)
                vds = unreal.Array(unreal.RivalsWindowVelocityData)
                vds.append(vd)
                w.set_editor_property('velocity_data', vds)
            ws = unreal.Array(unreal.RivalsArticleWindow)
            ws.append(w)
            addo.set_editor_property('windows', ws)

            _compile(ad)
            ad.modify()
            _save(asset_path)

            # Track for ArticleCreationData stub-stamp + RegisterNetProps
            # registration. Key matches the shim's runtime lookup format
            # (`proj_<AT_NAME>_<HB_IDX>` — see R1.tick_projectile_hitboxes).
            obj_name = f'proj_{at_name}_{hb_idx}'
            out[obj_name] = (class_name, ad.generated_class())
            print(f'  stamped {asset_name}')
    return out


def stamp_generic_projectile_article(flipbooks):
    # Generic fallback article for R1.create_hitbox(attack, slot) calls whose
    # (attack, slot) tuple doesn't match any per-slot stamped projectile. The
    # shim spawns this article and then writes the HG_PROJECTILE_* fields onto
    # the article's inst via R1._apply_projectile_snapshot — so a generic spawn
    # behaves identically to a per-slot one. Empower-style mods (Hodan's
    # hitbox_update.gml's create_hitbox(AT_NSPECIAL, 4) per frame) drive this
    # path; the (NSPECIAL, 4) row exists in attack data but isn't TYPE=2, so
    # stamp_projectile_articles skipped it.
    #
    # Down the road we may collapse ALL projectile articles to this single
    # asset — per-slot files only save a one-time snapshot copy at spawn and
    # don't justify their own .uasset / .lua. Keeping both for now for
    # incremental migration.
    class_name = f'{CHAR}_R1GenericHitbox'
    asset_name = f'AD_{class_name}'
    proj_dest  = f'{DEST}/Projectiles'
    asset_path = f'{proj_dest}/{asset_name}'

    ad = unreal.load_asset(asset_path)
    if not ad:
        bp_factory = unreal.BlueprintFactory()
        bp_factory.set_editor_property('parent_class', unreal.RivalsR1ArticleData)
        ad = _asset_tools().create_asset(asset_name, proj_dest, unreal.Blueprint, bp_factory)
        print(f'  created {asset_path}')
        _save(asset_path)
        ad = unreal.load_asset(asset_path)
    _ensure_r1_parent(ad, unreal.RivalsR1ArticleData)
    addo = unreal.get_default_object(ad.generated_class())
    addo.set_editor_property('article_class', unreal.RivalsR1ArticleEntity)
    try:
        addo.set_editor_property('default_renderer_class',
            unreal.RivalsLua2DArticleRenderer)
    except Exception as ex:
        print(f'  generic proj: failed to set renderer_class: {ex}')
    addo.set_editor_property('lua_script_path', f'{MOD_ID}/Scripts/{class_name}.lua')
    addo.set_editor_property('lua_metatable_name', class_name)
    # No compile-time attack — runtime R1.create_hitbox stamps inst.attack
    # before the snapshot helper runs. C++ attack attribution sees NONE; if
    # KO-attribution / hit-routing needs more, we add a SetAttack-style call
    # in create_hitbox once we know the symptom.

    try:
        # See stamp_projectile_articles for IsAttachedToOwner rationale.
        addo.set_editor_property('is_attached_to_owner', False)
        addo.set_editor_property('ecb_type', unreal.ArticleEcbType.SIMPLE)
        addo.set_editor_property('ecb_radius', 16.0)
        addo.set_editor_property('should_get_out_of_ground_on_spawn', False)
        # NONE, not DESTROY: this asset serves EVERY runtime-spawned
        # projectile whose ground behavior is only known at runtime
        # (_apply_projectile_snapshot stamps inst.grounds from the live
        # hitbox row). A baked DESTROY killed pass-through projectiles the
        # moment they touched stage geometry (Bhadra ground SSPECIAL's
        # grounds=1 slash spawned at the feet and died before its rail-spawn
        # condition could fire). The shim owns ground interaction for the
        # generic article: grounds=0 grounding via the can_be_grounded
        # probe, grounds=-1 destroy-on-ground in apply_projectile_gravity.
        addo.set_editor_property('ground_collision_response',
            unreal.ArticleCollisionResponse.NONE)
        addo.set_editor_property('wall_collision_response',
            unreal.ArticleCollisionResponse.NONE)
        addo.set_editor_property('ceiling_collision_response',
            unreal.ArticleCollisionResponse.NONE)
    except Exception as ex:
        print(f'  generic proj: failed to set collision: {ex}')

    anims = unreal.Map(unreal.Name, unreal.SoftObjectPath)
    for stem, fb in flipbooks.items():
        anims[stem] = unreal.SoftObjectPath(fb.get_path_name())
    addo.set_editor_property('animations', anims)
    # Default to empty_sprite (the Lua2D renderer hides it) rather than the
    # alphabetical-first flipbook stem. The generic article's real sprite is
    # written at runtime by _apply_projectile_snapshot (Set2DAnimation), so any
    # stamp-time default only shows for the spawn frames before that — and the
    # first stem ('airdodge') flashes there. empty_sprite renders nothing. (#163)
    addo.set_editor_property('default_animation_key', unreal.Name('empty_sprite'))

    # Single window, length=9999. R1._apply_projectile_snapshot reads
    # HG_LIFETIME at runtime and the death chain fires when inst.destroyed=true.
    # No velocity_data here; snapshot writes via SetVelocity.
    w = unreal.RivalsArticleWindow()
    w.set_editor_property('string_table_key', 'First')
    w.set_editor_property('window_length_frames', 9999)
    w.set_editor_property('next_window_string_table_key', '')
    ws = unreal.Array(unreal.RivalsArticleWindow)
    ws.append(w)
    addo.set_editor_property('windows', ws)

    _compile(ad)
    ad.modify()
    _save(asset_path)

    print(f'  stamped {asset_name}')
    return (class_name, ad.generated_class())


def import_portrait_texture(filename, asset_suffix, explicit_path=None):
    # R1 ships flat portrait PNGs in the workshop root (alongside config.ini
    # and the sprites/ folder), NOT under sprites/. Look for `filename`
    # (e.g. 'portrait.png') in R1_ROOT; if missing, return None so the
    # caller falls back to the existing stub portrait (CSS UI tolerates a
    # null brush and just shows blank).
    #
    # explicit_path lets callers override the source location — used for the
    # HUD icon, which is pre-padded by the C# side into a 1600x1600 canvas
    # to match WBP_HUD_PlayerSlot's authored brush size.
    png_path = explicit_path or os.path.join(R1_ROOT, filename).replace(os.sep, '/')
    if not os.path.isfile(png_path):
        print(f'  portrait: {filename} not found at {png_path}, skipping')
        return None
    asset_name = f'T_{CHAR}_{asset_suffix}'
    # Force re-import: portrait/hud sources can change between runs (user
    # tweaking hud.png, or the C# side re-padding hud_icon_padded.png with
    # a new layout). import_texture early-exits when the asset already
    # exists, which would silently keep the stale prior import — so pass
    # force_reimport=True, which re-runs the AssetImportTask with
    # replace_existing and overwrites the source data IN PLACE. The old
    # delete-then-import pattern crashed ObjectTools::ForceDeleteObjects
    # when the texture was still referenced (CSS portrait brush, skin
    # definitions) — same crash the palette-atlas path documents removing.
    print(f'  portrait: importing {filename} -> {asset_name}')
    return import_texture(png_path, asset_name, force_reimport=True)


def stamp_shield_element():
    # R1 ships a character `bg color` string in config.ini (fire/water/wind/
    # earth/aether — see GAME_START.gml global.elemental_bg_color). We map it
    # to one of stock R2's per-character shield-element material instances
    # so the workshop char's shield visualizes the correct element, instead
    # of inheriting the SK_Cha_Shield default (fire-themed Zetterburn MI).
    #
    # Mechanism: SkinDefinition.ShieldMaterialOverrides is a
    # TMap<FName, MaterialInterface> keyed by material slot name on
    # SK_Cha_Shield. The renderer iterates it and calls SetMaterialByName per
    # entry. We discover the element slot name by scanning the mesh's
    # material slots for the substring Element in the name (engine-side
    # naming convention: MAT_Cha_Shield_Element).
    element = (R1_CONFIG.get('bg color') or '').strip().lower()
    if not element or element == 'aether':
        # No override — keep the default shared shield material (fire-ish).
        # R1 'aether' is the neutral/no-element option.
        return
    # Map R1 element name -> stock R2 char's per-slot shield MIs. Each entry
    # is a list of (slot_substring, mi_path) pairs — we match the slot
    # substring against SK_Cha_Shield's material slot names so the override
    # lands in the right place. Element drives the inner body color/VFX,
    # Glass drives the outer rim/fresnel (without it, the rim stays whatever
    # SK_Cha_Shield's default is — typically Zet orange).
    #
    # Naming convention drift: Orc ships MI_Orc_ShieldElement, Zet/Kra/Wra
    # ship MI_*_DefaultShield*. Both patterns are listed explicitly.
    ELEMENT_TO_MIS = {
        'fire': [
            ('Element', '/Game/Characters/Zetterburn/Skins/Default/Shield/MI_Zet_DefaultShieldElement'),
            ('Glass',   '/Game/Characters/Zetterburn/Skins/Default/Shield/MI_Zet_DefaultShieldGlass'),
        ],
        'water': [
            ('Element', '/Game/Characters/Orcane/Skins/Default/Shield/MI_Orc_ShieldElement'),
            ('Glass',   '/Game/Characters/Orcane/Skins/Default/Shield/MI_Orc_ShieldGlass'),
        ],
        'earth': [
            ('Element', '/Game/Characters/Kragg/Skins/Default/Shield/MI_Kra_DefaultShieldElement'),
            ('Glass',   '/Game/Characters/Kragg/Skins/Default/Shield/MI_Kra_DefaultShieldGlass'),
        ],
        'wind': [
            ('Element', '/Game/Characters/Wrastor/Skins/Default/Shield/MI_Wra_DefaultShieldElement'),
            ('Glass',   '/Game/Characters/Wrastor/Skins/Default/Shield/MI_Wra_DefaultShieldGlass'),
        ],
        # 'air' = alias for wind (R1 stage convention; some workshop chars
        # use it instead of 'wind').
        'air': [
            ('Element', '/Game/Characters/Wrastor/Skins/Default/Shield/MI_Wra_DefaultShieldElement'),
            ('Glass',   '/Game/Characters/Wrastor/Skins/Default/Shield/MI_Wra_DefaultShieldGlass'),
        ],
        'lightning': [
            ('Element', '/Game/Characters/Clairen/Skins/Default/Shield/MI_Cla_DefaultShieldElement'),
            ('Glass',   '/Game/Characters/Clairen/Skins/Default/Shield/MI_Cla_DefaultShieldGlass'),
        ],
        'smoke': [
            ('Element', '/Game/Characters/Forsburn/Skins/Default/Shield/MI_For_DefaultShieldElement'),
            ('Glass',   '/Game/Characters/Forsburn/Skins/Default/Shield/MI_For_DefaultShieldGlass'),
        ],
        # No 'ice' mapping: Etalus's MI_Eta_*FrozenShield is the
        # shield-frozen status-effect material (opponent hits your shield
        # with a freeze move and it stays frozen), not his own shield
        # element. He uses SK_Cha_Shield's default. R1's 'ice' is a
        # stage-only element anyway (not in elemental_bg_color), so
        # workshop chars shouldn't author it as bg color.
    }
    mi_specs = ELEMENT_TO_MIS.get(element)
    if not mi_specs:
        print(f'  shield element: unknown bg color "{element}", leaving default')
        return
    # Pre-load the MIs so we can fail early if any are missing.
    loaded = []
    for slot_sub, mi_path in mi_specs:
        mi = unreal.load_asset(mi_path)
        if not mi:
            print(f'  shield element: failed to load {mi_path}')
            return
        loaded.append((slot_sub, mi))
    # Match each requested slot substring against the shared shield mesh's
    # actual material slot names. Avoids drift when the mesh is updated.
    mesh = unreal.load_asset('/Game/Characters/Shared/Shield/SK_Cha_Shield')
    if not mesh:
        print('  shield element: SK_Cha_Shield not found')
        return
    slot_assignments = []  # (FName slot, MaterialInstance mi)
    for slot_sub, mi in loaded:
        matched = None
        for slot in mesh.materials:
            if slot_sub in str(slot.material_slot_name):
                matched = slot.material_slot_name
                break
        if matched is None:
            print(f'  shield element: no slot containing {slot_sub} on SK_Cha_Shield')
            continue
        slot_assignments.append((matched, mi))
    if not slot_assignments:
        return
    # Apply to the Default skin definition. Workshop mods carry one skin
    # (named Default); if a mod ships multiple skins later we'd iterate.
    skin_path = f'/Game/ModContent/{MOD_ID}/UnrealAssets/Skins/Default/Data/Skin_{CHAR_SHORT}_Default'
    skin_bp = unreal.load_asset(skin_path)
    if not skin_bp or not hasattr(skin_bp, 'generated_class'):
        print(f'  shield element: skin def not found at {skin_path}')
        return
    skin_cdo = unreal.get_default_object(skin_bp.generated_class())
    overrides = skin_cdo.get_editor_property('shield_material_overrides') or unreal.Map(unreal.Name, unreal.SoftObjectPath)
    new_overrides = unreal.Map(unreal.Name, unreal.SoftObjectPath)
    # Python reflection unwraps existing TSoftObjectPtr<UMaterialInterface>
    # entries to the loaded UMaterialInterface*; we need to coerce them back
    # to SoftObjectPath before writing into the Map (whose declared value type
    # is SoftObjectPath). Hits any previously-stamped entry on re-import.
    for k, v in overrides.items():
        if v is None:
            continue
        if isinstance(v, unreal.SoftObjectPath):
            new_overrides[k] = v
        elif hasattr(v, 'get_path_name'):
            new_overrides[k] = unreal.SoftObjectPath(v.get_path_name())
    for slot_name, mi in slot_assignments:
        new_overrides[slot_name] = unreal.SoftObjectPath(mi.get_path_name())
    skin_cdo.set_editor_property('shield_material_overrides', new_overrides)
    _compile(skin_bp)
    skin_bp.modify()
    _save(skin_path)
    slot_log = ', '.join(f'{str(s)}={mi.get_name()}' for s, mi in slot_assignments)
    print(f'  shield element: {element} -> {slot_log}')


def stamp_palette_atlases_into_color_slots():
    # Reads palette_mapping.json next to assets_import.py and, for each
    # mapping entry, populates the matching CS_* asset's
    # AnimationTextureOverrides map with per-animation texture overrides.
    # The source PNGs live in <OUTPUT_ROOT>/palette_<N>/ — pre-rendered by
    # the C# PaletteSwap pass before this Python script runs.
    #
    # Color-slot naming: ERivalsColorSlot::Default maps to folder Neutral
    # via the ColorSlotNameMap in RivalsColorSlotData.h. Other names match
    # the enum value (Blue/Red/Green/etc.).
    import json
    mapping_path = os.path.join(OUTPUT_ROOT, 'palette_mapping.json').replace(os.sep, '/')
    if not os.path.isfile(mapping_path):
        print('  palette atlases: no palette_mapping.json, skipping per-color-slot atlas stamping')
        return
    with open(mapping_path, 'r') as f:
        mapping = json.load(f)
    entries = mapping.get('mappings', [])
    if not entries:
        return
    # ERivalsColorSlot enum value -> folder name (Default -> Neutral).
    color_slot_folder = {
        'Default': 'Neutral',
    }
    # Bulk-import all per-palette textures in ONE import_asset_tasks call,
    # then apply per-texture settings afterward. Looping one-at-a-time pops
    # a per-asset confirmation dialog in UE (each call is a separate import
    # transaction) and serializes on the Plastic SC plugin's checkout per
    # file — ~189 sprites x 3 palettes = ~567 dialogs and several minutes
    # of wall-clock. The batched form ships them all to UE's importer in
    # one shot, no popups.
    atlas_textures = {}  # (palette_id, anim_key) -> UTexture2D
    palette_ids_seen = set(e.get('r1_palette', -1) for e in entries)
    tasks = []
    task_plan = []  # (pal_id, stem, asset_name) for post-import lookup
    for pal_id in palette_ids_seen:
        if pal_id < 0:
            continue
        pal_dir = os.path.join(OUTPUT_ROOT, f'palette_{pal_id}').replace(os.sep, '/')
        if not os.path.isdir(pal_dir):
            continue
        for fn in sorted(os.listdir(pal_dir)):
            if not fn.lower().endswith('.png'):
                continue
            stem, _ = parse_strip(fn)  # strips _stripN suffix
            asset_name = f'T_{CHAR}_pal{pal_id}_{stem}'
            png_path = os.path.join(pal_dir, fn).replace(os.sep, '/')
            # AssetImportTask.replace_existing=True (set inside
            # _make_texture_task via the factory defaults) overwrites the
            # source data on re-import; combined with the batched call it
            # avoids the per-asset dialog. The earlier delete-then-import
            # path was both per-asset AND crashed in ForceDeleteObjects
            # when the texture was already referenced — both gone now.
            task = unreal.AssetImportTask()
            task.filename = png_path
            task.destination_path = TEX_DEST
            task.destination_name = asset_name
            task.replace_existing = True
            task.automated = True
            task.save = False
            task.factory = unreal.TextureFactory()
            tasks.append(task)
            task_plan.append((pal_id, stem, asset_name))
    if not tasks:
        print('  palette atlases: no per-palette PNGs to import (palette swap may have been skipped)')
        return
    print(f'  palette atlases: batch-importing {len(tasks)} textures...')
    _asset_tools().import_asset_tasks(tasks)
    for pal_id, stem, asset_name in task_plan:
        tex = unreal.load_asset(f'{TEX_DEST}/{asset_name}')
        if not tex:
            continue
        # See import_texture for why settings are forced — UE auto-detects
        # blue-dominated palette atlases as normal maps otherwise, and
        # TC_DEFAULT DXT1-compresses mult-of-4-sized atlases.
        _apply_sprite_tex_settings(tex)
        atlas_textures[(pal_id, stem)] = tex
    # Now stamp each mapping entry: find the CS_<CharShort>_<Skin>_<ColorSlotFolder>
    # asset and set its AnimationTextureOverrides map + per-palette portrait
    # and HUD icon (so non-Default color slots show recolored versions in CSS
    # and in-match HUD).
    #
    # Asset naming mirrors WorkshopToolStatics::CreateNewPalette (line ~1059):
    #   CS_<AnimationsPrefix.Right(4)><SkinIdentifier>_<Slot>
    # CreateNewCharacter sets AnimationsPrefix = AN_<CharShort>_ so Right(4)
    # yields <CharShort>_ — the CS asset name comes out as e.g.
    # CS_Hod_Default_Neutral.
    stamped = 0
    for entry in entries:
        pal_id = entry.get('r1_palette', -1)
        skin = entry.get('r2_skin', 'Default')
        color_slot = entry.get('r2_color_slot', 'Default')
        if pal_id < 0:
            continue
        folder_name = color_slot_folder.get(color_slot, color_slot)
        cs_path = (f'/Game/ModContent/{MOD_ID}/UnrealAssets/Skins/{skin}/Data/Palettes/'
                   f'{folder_name}/CS_{CHAR_SHORT}_{skin}_{folder_name}')
        cs_bp = unreal.load_asset(cs_path)
        if not cs_bp or not hasattr(cs_bp, 'generated_class'):
            print(f'  palette atlases: CS asset not found at {cs_path} (skin={skin} slot={color_slot})')
            continue
        cs_cdo = unreal.get_default_object(cs_bp.generated_class())

        # Per-palette CharacterSelectPortrait + HudIconTexture overrides.
        # For palette 0 we leave the base portrait/hud (already stamped by
        # stamp_portrait_on_color_slots earlier in this run). For palette > 0
        # we import the pre-recolored variants and overwrite.
        if pal_id > 0:
            portrait_src = os.path.join(OUTPUT_ROOT, f'palette_{pal_id}_portrait.png').replace(os.sep, '/')
            if os.path.isfile(portrait_src):
                pal_portrait = import_portrait_texture(
                    f'palette_{pal_id}_portrait.png', f'pal{pal_id}_Portrait', portrait_src)
                if pal_portrait is not None:
                    cs_cdo.set_editor_property('character_select_portrait', pal_portrait)
            hud_src = os.path.join(OUTPUT_ROOT, f'palette_{pal_id}_hud_padded.png').replace(os.sep, '/')
            if os.path.isfile(hud_src):
                pal_hud = import_portrait_texture(
                    f'palette_{pal_id}_hud_padded.png', f'pal{pal_id}_HudIcon', hud_src)
                if pal_hud is not None:
                    cs_cdo.set_editor_property('hud_icon_texture', pal_hud)

        # Build the override map: anim key -> texture for this palette.
        # Palette 0 is identity (no override needed); skip stamping for it.
        if pal_id == 0:
            try:
                cs_cdo.set_editor_property('animation_texture_overrides',
                    unreal.Map(unreal.Name, unreal.SoftObjectPath))
            except Exception:
                pass
            _compile(cs_bp)
            cs_bp.modify()
            _save(cs_path)
            stamped += 1
            continue
        anims = unreal.Map(unreal.Name, unreal.SoftObjectPath)
        # R1's crouch.png is sliced into three sub-flipbooks (crouch_start /
        # crouch / crouch_stand) that all share one underlying texture — so
        # one palette atlas covers all three. Mirror the AnimationTextureOverrides
        # entry under each sub-key, otherwise crouch_start/crouch_stand fall
        # back to the base-palette texture mid-state-transition.
        sliced_aliases = {
            'crouch': ('crouch_start', 'crouch_stand'),
        }
        for (p, key), tex in atlas_textures.items():
            if p != pal_id:
                continue
            sop = unreal.SoftObjectPath(tex.get_path_name())
            anims[unreal.Name(key)] = sop
            for alias in sliced_aliases.get(key, ()):
                anims[unreal.Name(alias)] = sop
        try:
            cs_cdo.set_editor_property('animation_texture_overrides', anims)
        except Exception as ex:
            print(f'  palette atlases: set_editor_property failed on {cs_path}: {ex}')
            continue
        _compile(cs_bp)
        cs_bp.modify()
        _save(cs_path)
        stamped += 1
        print(f'  palette atlases: stamped {len(anims)} overrides on {cs_path}')
    if stamped:
        print(f'  palette atlases: stamped overrides on {stamped} color slots')


def stamp_portrait_on_color_slots(portrait_tex, hud_icon_tex):
    # The modkit's CreateNewCharacter flow stamps a default Skin tree:
    #   .../Skins/Default/Data/Skin_Default
    #   .../Skins/Default/Data/Palettes/{Neutral,Blue,Red,Green,...}/CS_Default_{ColorSlot}
    # Each CS_* is a Blueprint subclass of URivalsColorSlotData. The in-game
    # HUD player slot, loading screen, and large CSS card all read
    # ColorSlotData->CharacterSelectPortrait at runtime — not the char def's
    # CharacterSelectPortraitSmall (that's the small CSS thumbnail surface).
    #
    # HudIconTexture is the workshop-mod escape hatch added in Phase 1.5:
    # stock R2 chars rely on URivalsCharacterWidgetData::Offsets to crop the
    # full portrait into a face shot for the HUD slot, but that data asset
    # isn't writable from mods. R1 mods ship a dedicated 48x32 hud.png; we
    # stamp it as HudIconTexture and the HUD widget prefers it.
    #
    # Phase 1 stamps the same portrait/icon on every color slot. Phase 5
    # will replace each with its per-palette pre-rendered variant once the
    # palette-swap pipeline lands.
    if portrait_tex is None and hud_icon_tex is None:
        return
    palettes_root = f'/Game/ModContent/{MOD_ID}/UnrealAssets/Skins/Default/Data/Palettes'
    if not unreal.EditorAssetLibrary.does_directory_exist(palettes_root):
        print(f'  portrait: no skin palettes directory at {palettes_root}; skipping CS_* stamping')
        return
    # list_assets recursively returns every asset under the Palettes/ tree;
    # filter to CS_* (the URivalsColorSlotData blueprints).
    stamped = 0
    for asset_path in unreal.EditorAssetLibrary.list_assets(palettes_root, True, False):
        # asset_path is like /Game/.../CS_Default_Neutral.CS_Default_Neutral.
        leaf = asset_path.rsplit('/', 1)[-1].split('.', 1)[0]
        if not leaf.startswith('CS_'):
            continue
        cs_bp = unreal.load_asset(asset_path)
        if not cs_bp or not hasattr(cs_bp, 'generated_class'):
            continue
        cs_cdo = unreal.get_default_object(cs_bp.generated_class())
        try:
            if portrait_tex is not None:
                cs_cdo.set_editor_property('character_select_portrait', portrait_tex)
            if hud_icon_tex is not None:
                cs_cdo.set_editor_property('hud_icon_texture', hud_icon_tex)
        except Exception as ex:
            print(f'  portrait: failed to set on {leaf}: {ex}')
            continue
        _compile(cs_bp)
        cs_bp.modify()
        _save(asset_path.rsplit('.', 1)[0])
        stamped += 1
    print(f'  portrait: stamped CharacterSelectPortrait/HudIconTexture on {stamped} color-slot assets')


def stamp_character_definition(cd):
    # Char_ uses CHAR_SHORT (matches WorkshopToolStatics::CreateNewCharacter's
    # Char_<short> naming). The standalone-CLI fallback create-from-scratch
    # path below also uses CHAR_SHORT so both flows produce the same asset.
    char_path = f'{DEST}/Char_{CHAR_SHORT}'
    ch = unreal.load_asset(char_path)
    if not ch:
        bp_factory = unreal.BlueprintFactory()
        bp_factory.set_editor_property('parent_class', unreal.RivalsLuaCharacterDefinition)
        ch = _asset_tools().create_asset(f'Char_{CHAR_SHORT}', DEST, unreal.Blueprint, bp_factory)
        print(f'  created {char_path}')
    chdo = unreal.get_default_object(ch.generated_class())
    # ModID isn't a property on URivalsLuaCharacterDefinition — PakManager sets
    # it from the asset path at load time. ImmutableName is read-only via
    # editor properties (C++-only), and apparently auto-populated.
    # Display name + info text come from R1's config.ini if present.
    display = R1_CONFIG.get('name') or CHAR
    chdo.set_editor_property('display_name', unreal.Text(display))
    # Info text: R1's `description` or `info_text` / `info text` keys.
    info = R1_CONFIG.get('description') or R1_CONFIG.get('info_text') or R1_CONFIG.get('info text')
    if info:
        for prop_name in ('info_text', 'character_info_text', 'description'):
            try:
                chdo.set_editor_property(prop_name, unreal.Text(info))
                break
            except Exception:
                continue
    chdo.set_editor_property('character_data', cd.generated_class())
    # CharacterSelectPortraitSmall feeds the CSS character-button thumbnail,
    # leaderboard avatars, match-history rows, player profile entries — every
    # spot that does `Def->CharacterSelectPortraitSmall` (10+ surfaces).
    # We use the R1-shipped portrait.png here (350x350 native; UE downsamples
    # for the small UI placements). The in-game HUD player slot reads
    # ColorSlotData->CharacterSelectPortrait instead, which gets wired by
    # the per-skin ColorSlotData stamping in Phase 5.
    portrait_tex = import_portrait_texture('portrait.png', 'Portrait')
    if portrait_tex is not None:
        chdo.set_editor_property('character_select_portrait_small', portrait_tex)
    _compile(ch)
    ch.modify()
    _save(char_path)
    # The in-game HUD / loading screen / large CSS card all read from
    # ColorSlotData->CharacterSelectPortrait, NOT char def's
    # CharacterSelectPortraitSmall. Stamp every color slot under the default
    # skin with the same portrait for now; per-color variants come in Phase 5.
    #
    # R1's hud.png (48x32) is a dedicated HUD-sized icon, separate from the
    # 350x350 portrait.png. Stamp it on ColorSlotData->HudIconTexture so the
    # HUD widget displays the right art without needing to fall back to
    # cropping the full portrait (which workshop mods can't configure since
    # the crop transforms live in a non-mod-writable global data asset).
    hud_icon_tex = import_portrait_texture('hud.png', 'HudIcon', HUD_ICON_PADDED)
    stamp_portrait_on_color_slots(portrait_tex, hud_icon_tex)
    # Per-palette pre-rendered atlases -> per-color-slot AnimationTextureOverrides.
    # See PaletteSwap.cs for the recoloring algorithm and palette_mapping.json
    # for which R1 palettes feed which R2 (skin, color slot) tuples.
    stamp_palette_atlases_into_color_slots()
    stamp_shield_element()
    return ch


def relocate_scripts():
    # The transpiled Lua + R1Compat shim were emitted to OUTPUT_ROOT/Scripts/.
    # The engine's LoadLuaScript resolves <ModID>/Scripts/<name>.lua under
    # Game/Content/ModContent/, so we mirror them in once we know where the
    # project's content root lives.
    import shutil, sys
    project_dir = unreal.SystemLibrary.get_project_directory().rstrip('/')
    target = f'{project_dir}/Content/ModContent/{MOD_ID}/Scripts'
    src    = f'{OUTPUT_ROOT}/Scripts'
    if not os.path.isdir(src):
        print(f'  scripts: {src} missing — skipping copy')
        return
    if os.path.abspath(src) == os.path.abspath(target):
        print(f'  scripts: source == target ({src}); no copy needed')
        return
    os.makedirs(target, exist_ok=True)
    for root, _, files in os.walk(src):
        rel = os.path.relpath(root, src)
        dst = os.path.join(target, rel) if rel != '.' else target
        os.makedirs(dst, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(dst, f))
    print(f'  scripts: copied to {target}')


print(f'asset_import: starting for {CHAR} (mod {MOD_ID})')
relocate_scripts()
flipbooks = import_all_sprites()
print(f'  imported {len(flipbooks)} flipbooks')

# ── Mode-gated stamping ──────────────────────────────────────────────────
# assetsonly: a vanilla char shell with art/audio only — no moves. basic: +
# best-attempt gameplay DATA (attacks, hitboxes, named articles) on vanilla
# Lua2D classes for the modder to drive. advanced: the full R1 port.
#
# Projectile / generic articles model R1's create_hitbox(TYPE=2) auto-spawn —
# an R1-runtime concept. Only advanced auto-stamps them; a basic (R2-native)
# char spawns projectiles from its own articles. The TYPE=2 hitbox DATA is
# still stamped onto the attack assets in basic, so nothing is lost.
if IMPORT_MODE != 'assetsonly':
    attack_classes = stamp_attack_data_assets()
else:
    attack_classes = {}

if IMPORT_MODE == 'assetsonly':
    article_classes = {}
    projectile_articles = {}
    generic_projectile = None
elif IMPORT_MODE == 'basic':
    article_classes = stamp_articles(flipbooks)
    projectile_articles = {}
    generic_projectile = None
else:  # advanced
    article_classes = stamp_articles(flipbooks)
    projectile_articles = stamp_projectile_articles(flipbooks)
    # Generic fallback article: always stamped, independent of TYPE=2 hitbox
    # presence. R1.create_hitbox falls through to it when no per-slot match
    # exists. See ModStamper.WriteOneProjectileEntryPoint generic branch + the
    # r1_misc.lua R1.create_hitbox lookup chain.
    generic_projectile = stamp_generic_projectile_article(flipbooks)

if IMPORT_MODE != 'assetsonly':
    vfx_renderers = stamp_vfx_renderer_bps(flipbooks)
    vfx_container_class = stamp_vfx_definition_container(vfx_renderers)
else:
    vfx_container_class = None
sfx_container_class = stamp_sfx_container()
cd = stamp_character_data(flipbooks, attack_classes, vfx_container_class, sfx_container_class)
# Migration: older imports stamped a duplicate VFX container under /VFX/ (same short name as the
# scaffold's root VFX_<Char>, so a colliding namespaced PrimaryAssetId -> render side resolved the
# wrong one). CD now points at the root container; delete the stale /VFX/ copy if present. The
# BP_VFX_<Char>_* renderer assets stay under /VFX/ -- only the duplicate container is removed.
_stale_vfx_container = f'{DEST}/VFX/VFX_{CHAR}'
if unreal.EditorAssetLibrary.does_asset_exist(_stale_vfx_container):
    unreal.EditorAssetLibrary.delete_asset(_stale_vfx_container)
    print(f'  migrated: removed stale duplicate VFX container {_stale_vfx_container}')
ch = stamp_character_definition(cd)
print(f'  stamped CD_{CHAR} + Char_{CHAR_SHORT}')

# Stub-stamp ArticleCreationData on the character's first attack so the
# subsystem walks each AD_<Char>_Article<N> at character-load time and runs
# LoadLuaScript on it. We don't actually want a data-driven spawn — the
# CreationWindowStringTableKey is left empty so FindWindowIndex returns -1
# and the engine's per-frame spawn check never matches. Real spawns happen
# from R1.instance_create().
if (article_classes or projectile_articles or generic_projectile) and attack_classes:
    # Pick the most-broadly-existing attack as our anchor (JAB is universal).
    anchor_attack = None
    for candidate in ('JAB', 'IDLE', 'NSPECIAL', 'TAUNT1'):
        if candidate in attack_classes:
            anchor_attack = candidate
            break
    if anchor_attack:
        anchor_path = f'{DEST}/Attacks/ATT_{CHAR_SHORT}_{anchor_attack}'
        anchor = unreal.load_asset(anchor_path)
        if anchor:
            anchor_cdo = unreal.get_default_object(anchor.generated_class())
            acds = unreal.Array(unreal.ArticleCreationData)
            # Regular articles (obj_articleN script-spawned)
            for n, art_class in article_classes.items():
                acd = unreal.ArticleCreationData()
                acd.set_editor_property('article_data', art_class)
                acd.set_editor_property('creation_window_string_table_key', '')
                acds.append(acd)
            # Projectile articles (TYPE=2 hitbox-spawned)
            for obj_name, (cls_name, art_class) in projectile_articles.items():
                acd = unreal.ArticleCreationData()
                acd.set_editor_property('article_data', art_class)
                acd.set_editor_property('creation_window_string_table_key', '')
                acds.append(acd)
            # Generic fallback projectile article — same stub-stamp so the
            # subsystem walks it at character-load and exposes the
            # _R1_ArticleData_<Char>_R1GenericHitbox global to Lua.
            if generic_projectile:
                _gen_cls_name, gen_art_class = generic_projectile
                acd = unreal.ArticleCreationData()
                acd.set_editor_property('article_data', gen_art_class)
                acd.set_editor_property('creation_window_string_table_key', '')
                acds.append(acd)
            anchor_cdo.set_editor_property('article_creation_data', acds)
            _compile(anchor)
            anchor.modify()
            _save(anchor_path)
            print(f'  stub-stamped ArticleCreationData on ATT_{CHAR_SHORT}_{anchor_attack} ({len(acds)} entries)')

# ── Batch finalize ───────────────────────────────────────────────────────
# Compile every queued BP and re-mark its package dirty so the trailing
# save_dirty_packages flushes the CDO writes. Then drop the temp asset-
# registry caching mode so subsequent editor work sees a coherent registry.
print('==== batch flush ====')
_flush_pending()
if _asset_registry is not None:
    try:
        _asset_registry.set_temporary_caching_mode(False)
        print('  asset-registry: temp caching disabled')
    except Exception as ex:
        print(f'  asset-registry: temp-caching restore failed ({ex})')

# `save_asset` silently returns False for some Blueprint CDO writes (notably
# enum properties like `groundedness`) — the in-memory edit takes but the
# package never gets flushed. `save_dirty_packages` actually walks the dirty
# package set and writes them in one pass. THIS is the only save_dirty_packages
# in the script (see SAVE DISCIPLINE banner near the top).
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True)

# Force-save the assets the commandlet context would not auto-dirty (re-stamped
# existing sprites etc.) in ONE batch. only_if_is_dirty=False saves them even
# though they read as clean - replaces the per-sprite save_asset storm.
if _FORCE_SAVE_ASSETS:
    print(f'  batch force-save: {len(_FORCE_SAVE_ASSETS)} re-stamped assets')
    unreal.EditorAssetLibrary.save_loaded_assets(_FORCE_SAVE_ASSETS, False)

# Restore SC as the very LAST step - every save above has flushed, so the
# re-enabled provider cannot pop checkout modals mid-script. Uses the
# provider name captured at disable time (reading it here returns 'None').
if _sc_was_enabled:
    try:
        _sc.set_provider(_sc_orig_provider or 'Plastic')
        print(f'  SC: re-enabled ({_sc_orig_provider})')
    except Exception as ex:
        print(f'  SC: unable to restore ({ex}); user may want to flip manually')

print('asset_import: done')
