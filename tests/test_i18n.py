from lib import i18n

def test_t_returns_language():
    assert i18n.t("dashboard_title", "lo") == i18n.UI["dashboard_title"]["lo"]
    assert i18n.t("dashboard_title", "en") == i18n.UI["dashboard_title"]["en"]

def test_t_missing_key_returns_key():
    assert i18n.t("__nope__", "lo") == "__nope__"

def test_choice_label_en_override():
    assert i18n.choice_label("biz_type", "restaurant", "ຮ້ານອາຫານ", "en") == "Restaurant"

def test_choice_label_lo_uses_form_label():
    assert i18n.choice_label("biz_type", "restaurant", "ຮ້ານອາຫານ", "lo") == "ຮ້ານອາຫານ"

def test_choice_label_en_no_override_falls_back():
    assert i18n.choice_label("biz_type", "unknown", "ຕົ້ນສະບັບ", "en") == "ຕົ້ນສະບັບ"
