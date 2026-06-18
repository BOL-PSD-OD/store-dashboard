"""UI strings (lo/en), translation helper, English choice-label overrides."""
from __future__ import annotations

DEFAULT_LANG = "lo"

UI = {
    "app_title":        {"lo": "ລະບົບລາຍງານການສຳຫຼວດຮ້ານຄ້າ", "en": "Store Survey Dashboard"},
    "login_title":      {"lo": "ເຂົ້າສູ່ລະບົບ", "en": "Sign in"},
    "password":         {"lo": "ລະຫັດຜ່ານ", "en": "Password"},
    "login_btn":        {"lo": "ເຂົ້າສູ່ລະບົບ", "en": "Sign in"},
    "login_error":      {"lo": "ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ", "en": "Wrong password"},
    "logout":           {"lo": "ອອກຈາກລະບົບ", "en": "Log out"},
    "refresh":          {"lo": "ໂຫຼດຂໍ້ມູນໃໝ່", "en": "Refresh"},
    "language":         {"lo": "ພາສາ", "en": "Language"},
    "nav_dashboard":    {"lo": "ພາບລວມ", "en": "Dashboard"},
    "nav_profiles":     {"lo": "ຂໍ້ມູນຮ້ານ", "en": "Store Profiles"},
    "dashboard_title":  {"lo": "ພາບລວມການສຳຫຼວດ", "en": "Survey Overview"},
    "kpi_total":        {"lo": "ຮ້ານທັງໝົດ", "en": "Total stores"},
    "kpi_today":        {"lo": "ເກັບໄດ້ມື້ນີ້", "en": "Collected today"},
    "kpi_days":         {"lo": "ຈຳນວນວັນທີ່ເກັບ", "en": "Days collected"},
    "kpi_districts":    {"lo": "ຈຳນວນເມືອງ", "en": "Districts covered"},
    "chart_daily":      {"lo": "ຈຳນວນຟອມຕໍ່ວັນ", "en": "Forms per day"},
    "chart_biztype":    {"lo": "ປະເພດຮ້ານຄ້າ", "en": "Store type"},
    "chart_license":    {"lo": "ໃບທະບຽນວິສາຫະກິດ", "en": "Enterprise registration"},
    "chart_status":     {"lo": "ສະຖານະບັນຊີ", "en": "Account status"},
    "chart_market":     {"lo": "ບຸກຄົນ / ນິຕິບຸກຄົນ", "en": "Personal / Business"},
    "chart_qr":         {"lo": "ປ້າຍ QR", "en": "QR sign"},
    "chart_night":      {"lo": "ຕະຫຼາດກາງຄືນ", "en": "Night market"},
    "chart_awareness":  {"lo": "ຄວາມຮັບຮູ້ກ່ຽວກັບລະບຽບການ", "en": "Regulation awareness"},
    "chart_psp":        {"lo": "ທະນາຄານ / ຜູ້ໃຫ້ບໍລິການ", "en": "Banks / PSPs used"},
    "aware_yes":        {"lo": "ເຄີຍຮັບຮູ້", "en": "Aware"},
    "aware_no":         {"lo": "ບໍ່ເຄີຍ", "en": "Not aware"},
    "filter_biztype":   {"lo": "ປະເພດຮ້ານ", "en": "Store type"},
    "filter_district":  {"lo": "ເມືອງ", "en": "District"},
    "filter_status":    {"lo": "ສະຖານະບັນຊີ", "en": "Account status"},
    "search_store":     {"lo": "ຄົ້ນຫາຊື່ຮ້ານ", "en": "Search store name"},
    "all":              {"lo": "ທັງໝົດ", "en": "All"},
    "results_count":    {"lo": "ພົບ {n} ຮ້ານ", "en": "{n} stores found"},
    "select_store":     {"lo": "ເລືອກຮ້ານເພື່ອເບິ່ງລາຍລະອຽດ", "en": "Select a store to view details"},
    "no_data":          {"lo": "ຍັງບໍ່ມີຂໍ້ມູນ", "en": "No data yet"},
    "section_1":        {"lo": "I. ຂໍ້ມູນຜູ້ໃຫ້ສຳພາດ", "en": "I. Interviewee"},
    "section_2":        {"lo": "II. ຂໍ້ມູນຮ້ານຄ້າ", "en": "II. Store info"},
    "section_3":        {"lo": "III. ຄວາມຮັບຮູ້ລະບຽບການ", "en": "III. Regulation awareness"},
    "section_4":        {"lo": "IV. ທີ່ຕັ້ງ", "en": "IV. Location"},
}

# English overrides for categorical choice labels shown in charts/filters.
CHOICE_EN = {
    ("biz_type", "tour"): "Tour company",
    ("biz_type", "hotel"): "Hotel",
    ("biz_type", "restaurant"): "Restaurant",
    ("biz_type", "spa"): "Spa / massage",
    ("biz_type", "souvenir"): "Souvenir shop",
    ("biz_type", "night_market"): "Night-market stall",
    ("biz_type", "oth_biz"): "Other",
    ("license", "1"): "Has registration",
    ("license", "0"): "No registration",
    ("status", "1"): "Has account",
    ("status", "2"): "Opening account",
    ("status", "3"): "No account",
    ("market", "1"): "Personal Merchant",
    ("market", "0"): "Business Merchant",
    ("QR", "1"): "Lao QR",
    ("QR", "0"): "Store QR",
    ("YN", "1"): "Yes",
    ("YN", "0"): "No",
    ("learn", "1"): "Aware",
    ("learn", "0"): "Not aware",
}


def t(key: str, lang: str) -> str:
    entry = UI.get(key)
    if not entry:
        return key
    return entry.get(lang, entry.get(DEFAULT_LANG, key))


def choice_label(list_name: str, code: str, lao_label: str, lang: str) -> str:
    if lang == "en":
        return CHOICE_EN.get((list_name, str(code)), lao_label)
    return lao_label
