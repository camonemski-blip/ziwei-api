# -*- coding: utf-8 -*-
"""
紫微斗數結構化推理 - 命主：1971年8月10日午時 女
支援任何虛歲的大限分析，可用於驗證過去事件
"""

# 本命十二宮資料（直接從文墨天機命盤轉錄）
benming = {
    "命宮": {
        "干支": "辛丑", "主星": [("武曲", "廟"), ("貪狼", "廟")], "自化": [], "輔星": [], "小星": ["蜚廉"],
        "大限": "5~14"
    },
    "兄弟宮": {
        "干支": "庚子", "主星": [("天同", "旺", "↓忌"), ("太陰", "廟", "↓科")], "自化": ["天同忌(離心)", "太陰科(離心)"],
        "輔星": [], "小星": ["天才","天壽","臺輔","解神","天空","咸池"], "大限": "115~124"
    },
    "夫妻宮": {
        "干支": "己亥", "主星": [("天府", "得")], "自化": [], "輔星": [], "小星": ["鳳閣","年解"], "大限": "105~114"
    },
    "子女宮": {
        "干支": "戊戌", "主星": [], "自化": [], "輔星": [("文曲", "陷", "生年科"), ("擎羊", "廟")],
        "小星": ["天喜","八座","恩光","寡宿"], "大限": "95~104"
    },
    "財帛宮": {
        "干支": "丁酉", "主星": [("廉貞", "平"), ("破軍", "陷")], "自化": [], "輔星": [("左輔", "陷"), ("祿存", "廟")],
        "小星": ["天官","破碎"], "大限": "85~94"
    },
    "疾厄宮": {
        "干支": "丙申", "主星": [], "自化": [], "輔星": [("陀羅", "陷")], "小星": ["天使","封誥","天巫","劫煞","天德"],
        "大限": "75~84"
    },
    "遷移宮": {
        "干支": "乙未", "主星": [], "自化": [], "輔星": [], "小星": ["天哭","華蓋"], "大限": "65~74"
    },
    "交友宮": {
        "干支": "甲午", "主星": [], "自化": [], "輔星": [("天鉞", "旺")], "小星": ["天姚","天傷","天廚","龍德"],
        "大限": "55~64"
    },
    "官祿宮": {
        "干支": "癸巳", "主星": [("紫微", "旺"), ("七殺", "平")], "自化": [], "輔星": [("右弼", "平"), ("地劫", "不"), ("地空", "廟"), ("天馬", "平")],
        "小星": ["天福","截空","天虛"], "大限": "45~54"
    },
    "田宅宮": {
        "干支": "壬辰", "主星": [("天機", "利", "↑忌"), ("天梁", "廟", "↓祿")], "自化": ["天機忌(向心)", "天梁祿(離心)"],
        "輔星": [("文昌", "得", "生年忌"), ("鈴星", "陷")],
        "小星": ["紅鸞","三臺","天貴","截空","陰煞","大耗","月德"], "大限": "35~44"
    },
    "福德宮": {
        "干支": "辛卯", "主星": [("天相", "陷")], "自化": [], "輔星": [("火星", "利")], "小星": ["龍池","天月","旬空"],
        "大限": "25~34", "來因宮": True
    },
    "父母宮": {
        "干支": "庚寅", "主星": [("太陽", "旺", "生年權", "↓祿"), ("巨門", "廟", "生年祿")], "自化": ["太陽祿(離心)"],
        "輔星": [("天魁", "旺")], "小星": ["天刑","旬空","孤辰"], "大限": "15~24"
    }
}

# 十天干四化表
si_hua_table = {
    "甲": {"祿": "廉貞", "權": "破軍", "科": "武曲", "忌": "太陽"},
    "乙": {"祿": "天機", "權": "天梁", "科": "紫微", "忌": "太陰"},
    "丙": {"祿": "天同", "權": "天機", "科": "文昌", "忌": "廉貞"},
    "丁": {"祿": "太陰", "權": "天同", "科": "天機", "忌": "巨門"},
    "戊": {"祿": "貪狼", "權": "太陰", "科": "右弼", "忌": "天機"},
    "己": {"祿": "武曲", "權": "貪狼", "科": "天梁", "忌": "文曲"},
    "庚": {"祿": "太陽", "權": "武曲", "科": "太陰", "忌": "天同"},
    "辛": {"祿": "巨門", "權": "太陽", "科": "文曲", "忌": "文昌"},
    "壬": {"祿": "天梁", "權": "紫微", "科": "左輔", "忌": "武曲"},
    "癸": {"祿": "破軍", "權": "巨門", "科": "太陰", "忌": "貪狼"}
}

# 輔助函數
def find_star_location(star_name, benming):
    for palace, info in benming.items():
        for s in info["主星"]:
            if s[0] == star_name:
                return palace
        if info.get("輔星"):
            for aux in info["輔星"]:
                if aux[0] == star_name:
                    return palace
    return None

def get_daxian_by_age(age, benming):
    """根據虛歲返回對應的大限命宮名稱"""
    for palace, info in benming.items():
        if "大限" not in info:
            continue
        range_str = info["大限"]
        if "~" not in range_str:
            continue
        start, end = map(int, range_str.split("~"))
        if start <= age <= end:
            return palace
    return None

palace_order = ["命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮", "遷移宮", "交友宮", "官祿宮", "田宅宮", "福德宮", "父母宮"]

def get_daxian_map(ming_palace):
    """以大限命宮為起點，返回大限十二宮對應的本命宮位映射（逆時針順序）"""
    idx = palace_order.index(ming_palace)
    mapping = {}
    for i, p in enumerate(palace_order):
        mapping[p] = palace_order[(idx + i) % 12]
    return mapping

def feixing(palace_name, benming, si_hua_table):
    gan = benming[palace_name]["干支"][0]
    si_hua = si_hua_table.get(gan, {})
    result = {}
    for t, star in si_hua.items():
        locate = find_star_location(star, benming)
        result[t] = {"星": star, "落宮": locate}
    return result

def analyze_age(age, benming, si_hua_table, palace_order):
    """給定虛歲，輸出完整的大限分析"""
    daxian_ming = get_daxian_by_age(age, benming)
    if daxian_ming is None:
        return f"錯誤：找不到年齡 {age} 對應的大限"
    
    daxian_map = get_daxian_map(daxian_ming)
    daxian_guanlu = daxian_map["官祿宮"]
    daxian_caibo = daxian_map["財帛宮"]
    daxian_fuqi = daxian_map["夫妻宮"]
    
    guanlu_info = benming[daxian_guanlu]
    ganlu_gan = guanlu_info["干支"][0]
    fei = feixing(daxian_guanlu, benming, si_hua_table)
    fei_ji_star = fei.get("忌", {}).get("星")
    fei_ji_luo = fei.get("忌", {}).get("落宮")
    
    # 處理借星
    guanlu_stars = guanlu_info["主星"]
    if not guanlu_stars:
        idx = palace_order.index(daxian_guanlu)
        duigong = palace_order[(idx + 6) % 12]
        duigong_stars = benming[duigong]["主星"]
        star_desc = f"空宮，借對宮{duigong}之{duigong_stars}"
    else:
        star_desc = str(guanlu_stars)
    
    output = []
    output.append(f"=== 虛歲 {age} 分析 ===")
    output.append(f"大限命宮：{daxian_ming}（{benming[daxian_ming]['大限']}歲）")
    output.append(f"大限官祿宮：本命{daxian_guanlu}（{star_desc}）")
    output.append(f"大限財帛宮：本命{daxian_caibo}")
    output.append(f"大限夫妻宮：本命{daxian_fuqi}")
    output.append("")
    output.append(f"大限官祿宮天干『{ganlu_gan}』引發四化：")
    for t, v in fei.items():
        output.append(f"  {t}：{v['星']} → {v['落宮']}")
    output.append("")
    output.append(f"飛忌（{fei_ji_star}）落{fei_ji_luo}，是否等於大限夫妻宮？ {fei_ji_luo == daxian_fuqi}")
    output.append("-" * 50)
    return "\n".join(output)

# ================= 主程式：可一次分析多個年齡 =================
if __name__ == "__main__":
    # 您可以修改這裡要分析的年齡列表（例如從1到120歲，或只挑幾個關鍵年齡）
    ages_to_analyze = [10, 20, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
    
    print("="*60)
    print("紫微斗數大限分析（驗證用）")
    print("="*60)
    print("")
    
    for age in ages_to_analyze:
        result = analyze_age(age, benming, si_hua_table, palace_order)
        print(result)
        print("")
    
    # 也可以讓使用者自己輸入
    print("="*60)
    try:
        user_age = int(input("請輸入您想查詢的虛歲年齡（例如 42）："))
        print(analyze_age(user_age, benming, si_hua_table, palace_order))
    except:
        pass