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

def build_layer_rules(label, activations , mappings):
    l2_rules = []
    for key in activations:
        for (f, t) in mappings.items():
            l2_rules += build_lt(key, f, t)
    return {
        "description": f"{label} rules",
        "manipulators": l2_rules,
    }


if __name__ == '__main__':
    import pprint
    import json
    import os.path
    activations = [
        "tab",
    ]
    mappings = {
        'h': 'left_arrow',
        'j': 'down_arrow',
        'k': 'up_arrow',
        'l': 'right_arrow',

        # Since caps lock is backspace
        'caps_lock': 'caps_lock',

        'q': 'f1',
        'w': 'f2',
        'e': 'f3',
        'r': 'f4',
        't': 'f5',
        'y': 'f6',
        'u': 'f7',
        'i': 'f8',
        'o': 'f9',
        'p': 'f0',
    }
    l2_rules = build_layer_rules("layer2", activations, mappings)

    activations = [
        "spacebar",
    ]
    mappings = {
        'h': 'hyphen',
        'j': 'equal_sign',
        'k': 'open_bracket',
        'l': 'close_bracket',
        'semicolon': 'backslash',

        # Since caps lock is backspace
        'caps_lock': 'caps_lock',

        'q': '1',
        'w': '2',
        'e': '3',
        'r': '4',
        't': '5',
        'y': '6',
        'u': '7',
        'i': '8',
        'o': '9',
        'p': '0',

    }
    l1_rules = build_layer_rules("layer1", activations, mappings)

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

    rules = [l1_rules, l2_rules, basic_rules]
    fname = os.path.expanduser('~/.config/karabiner/karabiner.json')
    output = build(rules)
    pprint.pprint(output)
    with open(fname, 'w') as fp:
        json.dump(output, fp, sort_keys=True, indent=4)
    print(f"Created {fname}")
