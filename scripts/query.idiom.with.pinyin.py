import copy
import json
import re


def form_re_pattern(input_string: str) -> list[re.Pattern]:
    # if input_string.startswith("-"):
    #     pattern_list: list[re.Pattern] = []
    #     pattern_strings = re.split(r'[ 　,，；：;]+', input_string[1:])
    #     for anychar in pattern_strings:
    #         pattern_list.append(re.compile(f".*{anychar}.*"))
    #     return pattern_list
    # else:
    groups = input_string.split()
    processed_groups = [group.replace('?', '.*') for group in groups]
    regex_pattern = ','.join(processed_groups)
    optimized_pattern = re.sub(r'\.\*\.\*', '.*', regex_pattern)
    return [re.compile(f"^{optimized_pattern}$")]


def query_dict_with_regex(data: list[dict[str, str]], pattern_list: list[re.Pattern]) -> list[dict[str, str]]:
    pattern = pattern_list[0]

    subset_list: list[dict[str, str]] = []

    for entry in data:
        pinyin: str = entry.get('pinyinplain', '')
        if pattern.match(pinyin):
            subset_list.append(entry)
    return subset_list


def exclude_from_subset(data: list[dict[str, str]],  exclude_string: str) -> list[dict[str, str]]:
    subset: list[dict[str, str]] = copy.deepcopy(data)
    exclude_list = re.split(r'[ 　,，；：;]+', exclude_string[1:])
    for entry in data:
        test_seq = (entry.get('shengmu', '')+entry.get('yunmu', '')).split(",")
        for test_part in test_seq:
            if test_part in exclude_list:
                print(f" - 排除{entry.get('word', '')}")
                subset.remove(entry)
                break
    return subset


def show_possible(data: list[dict[str, str]], threshold=100):
    if (wll := len(data)) > threshold:
        print(f"太多可能项({wll})")
    elif wll == 0:
        print(f"没有可能项，检查输入")
    else:
        word_list: list[str] = []
        shengmu_list: list[str] = []
        for entry in data:
            word_list.append(entry.get('word', ''))
            shengmu_list.append(entry.get('shengmu', ''))
        print("可能是:")
        for word, shengmu in zip(word_list, shengmu_list):
            print(f" - {word}: {shengmu}")



with open('data/idiom-small-rf.json', mode='r', encoding="utf-8")as src:
    dictionary = json.load(src)


try:
    while True:
        pattern = form_re_pattern(input("\n第一次匹配: "))
        subset = query_dict_with_regex(dictionary, pattern)
        if subset != []:
            try:
                while True:
                    show_possible(subset)
                    input_s = input("继续输入/-排除声部/exit(^C): ")
                    if input_s == "exit":
                        break
                    elif input_s.startswith("-"):
                        subset = exclude_from_subset(subset, input_s)
                    elif "?" in input_s:
                        pattern = form_re_pattern(input_s)
                        subset = query_dict_with_regex(subset, pattern)
                    else:
                        continue
            except KeyboardInterrupt:
                continue
except KeyboardInterrupt:
    exit(0)