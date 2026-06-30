import pytest


@pytest.fixture
def form():
    """New-form fixture (2026-07 revision): Section 1 screening, Section 2
    awareness (learn), Section 3 business + payment. Section 3.1 now leads with a
    `select_one License` question (S3.1_Q1), pushing the free-text detail fields
    down one: district S3.1_Q2, village S3.1_Q3, owner S3.1_Q4, nationality
    S3.1_Q5, phone S3.1_Q6. Plus S0_Q1 date."""
    return {
        "content": {
            "survey": [
                {"type": "date", "name": "S0_Q1", "label": ["0.1 ວັນທີ"]},
                {"type": "begin_group", "name": "Section_1"},
                {"type": "select_one YN", "name": "S1_Q1", "label": ["1.1 owner?"]},
                {"type": "end_group"},
                {"type": "begin_group", "name": "Section_2"},
                {"type": "select_one learn", "name": "S2_Q1", "label": ["2.1 aware?"]},
                {"type": "select_one learn", "name": "S2_Q2", "label": ["2.2 aware?"]},
                {"type": "select_one learn", "name": "S2_Q3", "label": ["2.3 aware?"]},
                {"type": "end_group"},
                {"type": "begin_group", "name": "Section_3"},
                {"type": "select_one biz_type", "name": "S3_Q1", "label": ["3.1 biz type"]},
                {"type": "select_one shop_name", "name": "S3_Q2", "label": ["3.2 shop"]},
                {"type": "begin_group", "name": "Section_3.1"},
                {"type": "select_one License", "name": "S3.1_Q1", "label": ["ໃບທະບຽນ"]},
                {"type": "text", "name": "S3.1_Q2", "label": ["ເມືອງ"]},
                {"type": "text", "name": "S3.1_Q3", "label": ["ບ້ານ"]},
                {"type": "text", "name": "S3.1_Q4", "label": ["ຊື່ເຈົ້າຂອງຮ້ານ"]},
                {"type": "text", "name": "S3.1_Q5", "label": ["ສັນຊາດ"]},
                {"type": "text", "name": "S3.1_Q6", "label": ["ເບີໂທ"]},
                {"type": "end_group"},
                {"type": "begin_group", "name": "Section_3.2"},
                {"type": "select_one YN", "name": "S3_Q3", "label": ["3.3 night market"]},
                {"type": "select_multiple acquirer", "name": "S3_Q4", "label": ["3.4 acquirer"]},
                {"type": "select_multiple Payment", "name": "S3_Q5", "label": ["3.5 payment"]},
                {"type": "select_multiple QR", "name": "S3_Q6", "label": ["3.6 QR"]},
                {"type": "select_multiple psp", "name": "S3_Q7", "label": ["3.7 psp lao qr"]},
                {"type": "select_multiple psp", "name": "S3_Q8", "label": ["3.8 psp merchant"]},
                {"type": "select_one YN_Use", "name": "S3_Q9", "label": ["3.9 use domestic"]},
                {"type": "select_multiple psp", "name": "S3_Q10", "label": ["3.10 psp foreign"]},
                {"type": "select_multiple Network", "name": "S3_Q11", "label": ["3.11 foreign tools"]},
                {"type": "select_one int", "name": "S3_Q12", "label": ["3.12 interested"]},
                {"type": "select_multiple why", "name": "S3_Q13", "label": ["3.13 why"]},
                {"type": "select_one profit", "name": "S3_Q14", "label": ["3.14 revenue"]},
                {"type": "end_group"},
                {"type": "end_group"},
                {"type": "geopoint", "name": "geopoint", "label": ["geo"]},
            ],
            "choices": [
                {"list_name": "YN", "name": "1", "label": ["ແມ່ນ"]},
                {"list_name": "YN", "name": "0", "label": ["ບໍ່ແມ່ນ"]},
                {"list_name": "License", "name": "1", "label": ["ມີໃບທະບຽນ"]},
                {"list_name": "License", "name": "0", "label": ["ບໍ່ມີໃບທະບຽນ"]},
                {"list_name": "learn", "name": "1", "label": ["ເຄີຍໄດ້ຮັບຟັງແລ້ວ"]},
                {"list_name": "learn", "name": "0", "label": ["ບໍ່ເຄີຍ"]},
                {"list_name": "biz_type", "name": "restaurant", "label": ["ຮ້ານອາຫານ"]},
                {"list_name": "biz_type", "name": "hotel", "label": ["ໂຮງແຮມ"]},
                {"list_name": "shop_name", "name": "H001", "label": ["ໂຮງແຮມ ໜຶ່ງ"]},
                {"list_name": "shop_name", "name": "other_shop", "label": ["ອື່ນໆ"]},
                {"list_name": "acquirer", "name": "1", "label": ["ຮັບຊຳລະພາຍໃນ"]},
                {"list_name": "acquirer", "name": "2", "label": ["ຮັບຊຳລະຕ່າງປະເທດ"]},
                {"list_name": "acquirer", "name": "3", "label": ["ບໍ່ມີເຄື່ອງມືຮັບຊຳລະ"]},
                {"list_name": "Payment", "name": "1", "label": ["ຮັບບັດຊຳລະ"]},
                {"list_name": "Payment", "name": "0", "label": ["E-Money"]},
                {"list_name": "QR", "name": "1", "label": ["Lao QR"]},
                {"list_name": "QR", "name": "2", "label": ["QR ສ່ວນບຸກຄົນ"]},
                {"list_name": "psp", "name": "1", "label": ["BCEL"]},
                {"list_name": "psp", "name": "2", "label": ["JDB"]},
                {"list_name": "Network", "name": "1", "label": ["Alipay"]},
                {"list_name": "Network", "name": "2", "label": ["Alipay Plus"]},
                {"list_name": "Network", "name": "3", "label": ["Wechat Pay"]},
                {"list_name": "YN_Use", "name": "1", "label": ["ໃຊ້ບໍລິການພາຍໃນ"]},
                {"list_name": "YN_Use", "name": "0", "label": ["ບໍ່ໄດ້ໃຊ້"]},
                {"list_name": "int", "name": "1", "label": ["ສົນໃຈ"]},
                {"list_name": "int", "name": "0", "label": ["ບໍ່ສົນໃຈ"]},
                {"list_name": "why", "name": "1", "label": ["ອັດຕາແລກປ່ຽນ"]},
                {"list_name": "why", "name": "2", "label": ["ຄ່າທຳນຽມສູງ"]},
                {"list_name": "profit", "name": "1", "label": ["ຕໍ່າກວ່າ 30 ລ້ານ"]},
                {"list_name": "profit", "name": "2", "label": ["30 – 100 ລ້ານ"]},
            ],
        }
    }


@pytest.fixture
def subs():
    return [
        # both domestic+foreign, not using, interested -> both_int
        # PSP: Lao QR (S3_Q7) -> BCEL+JDB, merchant QR (S3_Q8) -> JDB
        {"S0_Q1": "2026-06-29", "S1_Q1": "1", "Section_3/S3_Q1": "restaurant",
         "S3_Q2": "other_shop", "S3_Q2_oth": "Taiwan", "S3.1_Q1": "1", "S3.1_Q2": "ຫຼວງພະບາງ",
         "S3.1_Q3": "ບ. ໜຶ່ງ", "S3.1_Q5": "ລາວ", "S3_Q4": "1 2", "S3_Q6": "1", "S3_Q7": "1 2", "S3_Q8": "2",
         "S3_Q9": "0", "S3_Q11": "1 2 3", "S3_Q12": "1", "S3_Q14": "2",
         "S2_Q1": "1", "S2_Q2": "0", "S2_Q3": "1",
         "geopoint": "19.88 102.13 300 5", "_submission_time": "2026-06-29T03:00:00", "_id": 1},
        # foreign only, not using, not interested -> foreign_unint
        # PSP: foreign acceptance (S3_Q10) -> BCEL
        {"S0_Q1": "2026-06-29", "S1_Q1": "0", "Section_3/S3_Q1": "hotel",
         "S3_Q2": "H001", "S3.1_Q2": "ຈອມເພັດ", "S3.1_Q5": "ໄທ", "S3_Q4": "2", "S3_Q10": "1",
         "S3_Q11": "1", "S3_Q9": "0", "S3_Q12": "0", "S3_Q14": "1",
         "S2_Q1": "0", "_submission_time": "2026-06-29T10:00:00", "_id": 2},
    ]
