
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json


base_config = Path() / 'config.json'
plugins_cmd_config = Path() / 'configs' / 'plugins2cmd_config.json'
plugins_setting = Path() / 'configs' / 'plugins_setting.json'


def init_config():
    if not base_config.exists():
        base_config.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {
            'apikey': {
                'LOLICON_KEY': '',
                'TL_KEY': [],
            },
            'sql': {
                'bind': '',
                'sql_name': '',
                'user': '',
                'password': '',
                'address': '',
                'port': '',
                'database': '',
            },
            'path': {
                'IMAGE_PATH': '',
                'VOICE_PATH': '',
                'TXT_PATH': '',
                'LOG_PATH': '',
                'DATA_PATH': '',
                'DRAW_PATH': '',
                'TEMP_PATH': '',
            },
            'proxy': {
                'system_proxy': '',
                'buff_proxy': ''
            },
            'level': {
                'DELETE_IMG_LEVEL': 7,
                'MOVE_IMG_LEVEL': 7,
                'UPLOAD_LEVEL': 6,
                'BAN_LEVEL': 5,
                'OC_LEVEL': 2,
                'MUTE_LEVEL': 5,
            },
            'auth': {
                'ADMIN_DEFAULT_AUTH': 5,
                'admin_plugins_auth': {
                    "admin_bot_manage": 2,
                    "ban": 5,
                    "delete_img": 7,
                    "move_img": 7,
                    "upload_img": 6,
                    "admin_help": 1,
                    "mute": 5
                }
            }
        }
        with open(base_config, 'w', encoding='utf8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
    if not plugins_cmd_config.exists():
        plugins_cmd_config.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {
            'base_config': {
                'sign_in': ['??????'],
                'send_img': ['????????????', '??????', '??????', '??????'],
                'acg':['acg','??????'],
                'mc': ['mc'],
                'send_setu': ['??????', '??????', '??????', '?????????'],
                'white2black': ['?????????', '????????????'],
                'luxun': ['????????????', '?????????'],
                'fake_msg': ['?????????'],
                'buy': ['??????', '????????????'],
                'my_gold': ['????????????'],
                'my_props': ['????????????'],
                'shop_handle': ['??????'],
                'update_pic': ['??????', '????????????', '????????????'],
                'poke': ['?????????'],
                'translate': ['??????', '??????', '??????', '??????', '??????', '??????', '??????'],

            }
        }
        with open(plugins_cmd_config, 'w', encoding='utf8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
    if not plugins_setting.exists():
        plugins_setting.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {
            'base': {
                'IMAGE_DIR_LIST': ["??????", "??????", "??????", "??????"],
                'BAN_RESULT': "????????????????????????.",
            },
            'fudu': {
                'FUDU_PROBABILITY': 0.7,
            },
            'sign': {
                'MAX_SIGN_GOLD': 200,
            },
            'send_setu': {
                'INITIAL_SETU_PROBABILITY': 0.7,
                'MAX_SETU_R_COUNT': 5,
                'DOWNLOAD_SETU': True,
            },
            'malicious_ban': {
                'MALICIOUS_BAN_TIME': 30,
                'MALICIOUS_BAN_COUNT': 8,
                'MALICIOUS_CHECK_TIME': 5,
            },
            'mute': {
                'MUTE_DEFAULT_COUNT': 10,
                'MUTE_DEFAULT_TIME': 7,
                'MUTE_DEFAULT_DURATION': 10,
            },
            'update_gocq': {
                'UPDATE_GOCQ_GROUP': [],
            },
        }
        with open(plugins_setting, 'w', encoding='utf8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)



