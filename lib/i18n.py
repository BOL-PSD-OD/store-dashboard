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
    "nav_map":          {"lo": "ແຜນທີ່", "en": "Map"},
    "map_open_newtab":  {"lo": "ເປີດແຜນທີ່ໃນແທັບໃໝ່", "en": "Open map in a new tab"},
    "dashboard_title":  {"lo": "ພາບລວມການສຳຫຼວດ", "en": "Survey Overview"},
    "kpi_total":        {"lo": "ຮ້ານທັງໝົດ", "en": "Total stores"},
    "kpi_today":        {"lo": "ເກັບໄດ້ມື້ນີ້", "en": "Collected today"},
    "kpi_days":         {"lo": "ຈຳນວນວັນທີ່ເກັບ", "en": "Days collected"},
    "kpi_districts":    {"lo": "ຈຳນວນເມືອງ", "en": "Districts covered"},
    "kpi_villages":     {"lo": "ຈຳນວນບ້ານ", "en": "Villages covered"},
    "chart_daily":      {"lo": "ຈຳນວນຟອມຕໍ່ວັນ", "en": "Forms per day"},
    "chart_biztype":    {"lo": "ປະເພດຮ້ານຄ້າ", "en": "Store type"},
    "chart_license":    {"lo": "ໃບທະບຽນວິສາຫະກິດ", "en": "Enterprise registration"},
    "chart_status":     {"lo": "ສະຖານະພາບ", "en": "Account status"},
    "chart_revenue":    {"lo": "ລະດັບລາຍຮັບ / ຂະໜາດ", "en": "Revenue / SME size"},
    "chart_qr":         {"lo": "QR ພາຍໃນ", "en": "Domestic QR"},
    "chart_network":    {"lo": "ເຄື່ອງມືຮັບຊຳລະຕ່າງປະເທດ", "en": "Foreign payment apps"},
    "chart_district":   {"lo": "ເມືອງ", "en": "District"},
    "chart_awareness":  {"lo": "ຄວາມຮັບຮູ້ກ່ຽວກັບລະບຽບການ", "en": "Regulation awareness"},
    "section4_questions": {"lo": "ຄຳຖາມໝວດທີ່ 04", "en": "Section 04 questions"},
    "chart_psp":        {"lo": "ທະນາຄານ / ຜູ້ໃຫ້ບໍລິການ", "en": "Banks / PSPs used"},
    "psp_ctx_laoqr":    {"lo": "Lao QR", "en": "Lao QR"},
    "psp_ctx_merchant": {"lo": "QR ຮ້ານຄ້າ", "en": "Merchant QR"},
    "psp_ctx_foreign":  {"lo": "ຮັບຊຳລະຕ່າງປະເທດ", "en": "Foreign payment"},
    "aware_yes":        {"lo": "ເຄີຍຮັບຮູ້", "en": "Aware"},
    "aware_no":         {"lo": "ບໍ່ເຄີຍ", "en": "Not aware"},
    "filter_biztype":   {"lo": "ປະເພດຮ້ານ", "en": "Store type"},
    "filter_district":  {"lo": "ເມືອງ", "en": "District"},
    "filter_status":    {"lo": "ສະຖານະພາບ", "en": "Account status"},
    "search_store":     {"lo": "ຄົ້ນຫາຊື່ຮ້ານ", "en": "Search store name"},
    "all":              {"lo": "ທັງໝົດ", "en": "All"},
    "results_count":    {"lo": "ພົບ {n} ຮ້ານ", "en": "{n} stores found"},
    "select_store":     {"lo": "ເລືອກຮ້ານເພື່ອເບິ່ງລາຍລະອຽດ", "en": "Select a store to view details"},
    "no_data":          {"lo": "ຍັງບໍ່ມີຂໍ້ມູນ", "en": "No data yet"},
    "section_1":        {"lo": "I. ຜູ້ໃຫ້ສຳພາດ", "en": "I. Interviewee"},
    "section_2":        {"lo": "II. ຂໍ້ມູນເຈົ້າຂອງ / ຜູ້ຕິດຕໍ່", "en": "II. Owner & contact"},
    "section_3":        {"lo": "III. ຂໍ້ມູນຮ້ານ & ການຊຳລະ", "en": "III. Business & payment"},
    "section_4":        {"lo": "IV. ຄວາມຮັບຮູ້ລະບຽບການ", "en": "IV. Regulation awareness"},
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
    ("acquirer", "1"): "Domestic",
    ("acquirer", "2"): "Foreign",
    ("acquirer", "3"): "No payment tool",
    ("QR", "1"): "Lao QR",
    ("QR", "2"): "Merchant QR",
    ("YN", "1"): "Yes",
    ("YN", "0"): "No",
    ("YN_Use", "1"): "Uses domestic",
    ("YN_Use", "0"): "Does not use domestic",
    ("int", "1"): "Interested",
    ("int", "0"): "Not interested",
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
