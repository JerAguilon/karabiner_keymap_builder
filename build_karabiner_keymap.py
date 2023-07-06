#!/usr/bin/env python3

def build_lt(mod, key, to, layer='layer1'):
    init = {
            "from": {
                "modifiers": {
                    "optional": [
                        "any"
                        ]
                    },
                "simultaneous": [
                    {
                        "key_code": mod,
                        },
                    {
                        "key_code": key
                        }
                    ],
                "simultaneous_options": {
                    "key_down_order": "strict",
                    "key_up_order": "strict_inverse",
                    "to_after_key_up": [
                        {
                            "set_variable": {
                                "name": layer,
                                "value": 0
                                }
                            }
                        ]
                    }
                },
            "parameters": {
                "basic.simultaneous_threshold_milliseconds": 500
                },
            "to": [
                {
                    "set_variable": {
                        "name": layer,
                        "value": 1
                        }
                    },
                {
                    "key_code": to,
                    }
                ],
            "type": "basic"
            }
    continual = {
            "conditions": [
                {
                    "name": layer,
                    "type": "variable_if",
                    "value": 1
                    }
                ],
            "from": {
                "key_code": key,
                "modifiers": {
                    "optional": [
                        "any"
                        ]
                    }
                },
            "to": [
                {
                    "key_code": to,
                    }
                ],
            "type": "basic"
            }
    return [init, continual]

def build(rules):
    return {
        "global": {
            "check_for_updates_on_startup": True,
            "show_in_menu_bar": True,
            "show_profile_name_in_menu_bar": True
        },
        "profiles": [
            {
                "complex_modifications": {
                    "parameters": {
                        "basic.simultaneous_threshold_milliseconds": 50,
                        "basic.to_delayed_action_delay_milliseconds": 500,
                        "basic.to_if_alone_timeout_milliseconds": 1000,
                        "basic.to_if_held_down_threshold_milliseconds": 500
                    },
                    "rules": rules,
                },
                "devices": [
                ],
                "name": "Default profile",
                "selected": True,
                "simple_modifications": [],
                "virtual_hid_keyboard": {
                    "caps_lock_delay_milliseconds": 0,
                    "country_code": 0,
                    "keyboard_type": "ansi"
                }
            }
        ]
    }


if __name__ == '__main__':
    import pprint
    import json
    import os.path
    space_tap_layers = [
        "spacebar",
        "tab",
    ]
    mappings = {
        'h': 'left_arrow',
        'j': 'down_arrow',
        'k': 'up_arrow',
        'l': 'right_arrow',

        'y': 'hyphen',
        'u': 'equal_sign',
        'i': 'open_bracket',
        'o': 'close_bracket',
        'p': 'backslash',

        # Since caps lock is backspace
        'caps_lock': 'caps_lock',

        'q': 'escape',
        '1': 'f1',
        '2': 'f2',
        '3': 'f3',
        '4': 'f4',
        '5': 'f5',
        '6': 'f6',
        '7': 'f7',
        '8': 'f8',
        '9': 'f9',
        '10': 'f10',
        '11': 'f11',
        '12': 'f12',
    }
    l1_rules = []
    for key in space_tap_layers:
        for (f, t) in mappings.items():
            l1_rules += build_lt(key, f, t)
    l1_rules = {
        "description": "layer1 rules",
        "manipulators": l1_rules,
    }

    basic_rules = {
        "description": "basic rules",
        "manipulators": [
            {
                "from": {
                    "key_code": "caps_lock",
                },
                "to": [
                    {
                        "key_code": "escape"
                    }
                ],
                "type": "basic"
            }
        ]
    }

    rules = [l1_rules, basic_rules]
    fname = os.path.expanduser('~/.config/karabiner/karabiner.json')
    with open(fname, 'w') as fp:
        json.dump(build(rules), fp, sort_keys=True, indent=4)
    print(f"Created {fname}")
