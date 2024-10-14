# pyright:reportAssignmentType=false

import json
import re

with open("data/idiom-formmated-rf.json", mode='r', encoding="utf-8") as original_file:
    original_data = json.load(original_file)

replacement = ['a', 'e', 'i', 'o', 'u', 'v', 'v']

shengmu_check = [
    'zh', 'ch', 'sh',
    'b', 'p', 'f', 'd', 't', 'l',
    'k', 'h', 'j', 'q', 'x', 'r', 'z', 'c', 's',
    'w', 'y',
    'm', 'n', 'g',
]
yunmu_check = ['i', 'u', 'ü', 'v', 'a', 'ia', 'ua', 'o', 'uo', 'e', 'ê', 'ie', 'üe', 'ue', 'ui', 'iu', 'er', 'ai', 'uai', 'ei', 'uei', 'ao', 'iao', 'ou',
               'iou', 'an', 'ian', 'uan', 'üan', 'en', 'uen', 'un', 'in', 'ün', 'ang', 'iang', 'uang', 'eng', 'ing', 'ueng', 'ong', 'iong']

sheng_diao = [
    ['ā', 'ē', 'ī', 'ō', 'ū', 'ǖ'],
    ['á', 'é', 'í', 'ó', 'ú', 'ǘ'],
    ['ǎ', 'ě', 'ǐ', 'ǒ', 'ǔ', 'ǚ'],
    ['à', 'è', 'ì', 'ò', 'ù', 'ǜ'],
]

qingsheng = ['a', 'e', 'i', 'o', 'u', 'ü', 'v']
string_counts: dict[str, int] = {}


def findpart(check: list[str], string: str) -> str:
    for ch in check:
        if ch in string and string.startswith(ch):
            return ch
    return ""


def rf_notaion(word: str) -> tuple[str, str, str]:
    for tone_idx, tonegroup in enumerate(sheng_diao):
        for zhuyin_index, zhuyin in enumerate(tonegroup):
            if zhuyin in word:
                shengmu: str = findpart(shengmu_check, word)
                word = word.replace(zhuyin, replacement[zhuyin_index])
                yunmu = word.removeprefix(shengmu)

                return shengmu, yunmu, f"{word}{tone_idx+1}"
    # 轻声
    for zhuyin_index, zhuyin in enumerate(replacement):
        if zhuyin in word:
            shengmu: str = findpart(shengmu_check, word)
            word = word.replace(zhuyin, replacement[zhuyin_index])
            yunmu = word.removeprefix(shengmu)

            return shengmu, yunmu, "{word}0"

    return "err", "err", f"{word}_"


def record_string(s) -> dict[str, int]:
    global string_counts
    string_counts[s] = string_counts[s] + 1 if s in string_counts else 1
    return string_counts


mirror_data: list[dict[str, str]] = []


for idiom in original_data:
    idiom_opt: dict[str, str] = {}
    pinyinlist_opt: list[str] = []
    shengmulist: list[str] = []
    yunmulist: list[str] = []

    idiom: dict[str, str] = idiom

    pinyin: str = idiom.get("pinyin")
    pinyinlist: list[str] = re.split(r'[ 　,，；：;]+', pinyin)
    if len(pinyinlist) == 4:
        fullword: str = idiom.get("word")
        for pinyin in pinyinlist:
            shengmu, yunmu, rf_pinyin = rf_notaion(pinyin)
            pinyinlist_opt.append(rf_pinyin)
            shengmulist.append(shengmu)
            yunmulist.append(yunmu)

            # 注释部分为纠错检查
            # if shengmu not in shengmu_check and shengmu != "":
            #     input(f"shengmuERR {\
            #           shengmu} {yunmu} {pinyin} {rf_pinyin} {fullword}")
            # if yunmu not in yunmu_check:
            #     input(f"yunmuERR {\
            #           shengmu} {yunmu} {pinyin} {rf_pinyin} {fullword}")
            # record_string(f"{shengmu}")
            # record_string(f"{yunmu}")

        idiom_opt.update({"pinyinplain": ",".join(pinyinlist_opt)})
        idiom_opt.update({"shengmu": ",".join(shengmulist)})
        idiom_opt.update({"yunmu": ",".join(yunmulist)})
        idiom_opt.update({"word": fullword})

        mirror_data.append(idiom_opt)


with open("data/idiom-small-rf.json", mode='w', encoding="utf-8") as mirror_file:
    json.dump(mirror_data, mirror_file, ensure_ascii=False)

# print(string_counts)
