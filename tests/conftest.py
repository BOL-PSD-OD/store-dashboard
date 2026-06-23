import pytest

@pytest.fixture
def form():
    """New-form fixture: Section 1 screening, Section 3 business+payment,
    Section 4 awareness, plus the S0_Q1 interview date and a geopoint."""
    return {
        "content": {
            "survey": [
                {"type": "date", "name": "S0_Q1", "label": ["0.1 ວັນທີ"]},
                {"type": "begin_group", "name": "Section_1"},
                {"type": "select_one YN", "name": "S1_Q1", "label": ["1.1 owner?"]},
                {"type": "end_group"},
                {"type": "begin_group", "name": "Section_3"},
                {"type": "select_one biz_type", "name": "S3_Q1", "label": ["3.1 biz type"]},
                {"type": "select_one shop_name", "name": "S3_Q2", "label": ["3.2 shop"]},
                {"type": "select_one district", "name": "S3_Q3", "label": ["3.3 district"]},
                {"type": "select_one village", "name": "S3_Q4", "label": ["3.4 village"]},
                {"type": "select_one license", "name": "S3_Q6", "label": ["3.6 license"]},
                {"type": "select_multiple acquirer", "name": "S3_Q7", "label": ["3.7 acquirer"]},
                {"type": "select_multiple QR", "name": "S3_Q9", "label": ["3.9 QR"]},
                {"type": "select_multiple psp", "name": "S3_Q10", "label": ["3.10 psp"]},
                {"type": "select_one YN_Use", "name": "S3_Q12", "label": ["3.12 use domestic"]},
                {"type": "select_one int", "name": "S3_Q15", "label": ["3.15 interested"]},
                {"type": "select_one profit", "name": "S3_Q17", "label": ["3.17 revenue"]},
                {"type": "end_group"},
                {"type": "begin_group", "name": "Section_4"},
                {"type": "select_one learn", "name": "S4_Q1", "label": ["4.1 aware?"]},
                {"type": "select_one learn", "name": "S4_Q2", "label": ["4.2 aware?"]},
                {"type": "end_group"},
                {"type": "geopoint", "name": "geopoint", "label": ["geo"]},
            ],
            "choices": [
                {"list_name": "YN", "name": "1", "label": ["ແມ່ນ"]},
                {"list_name": "YN", "name": "0", "label": ["ບໍ່ແມ່ນ"]},
                {"list_name": "biz_type", "name": "restaurant", "label": ["ຮ້ານອາຫານ"]},
                {"list_name": "biz_type", "name": "hotel", "label": ["ໂຮງແຮມ"]},
                {"list_name": "shop_name", "name": "H001", "label": ["ໂຮງແຮມ ໜຶ່ງ"]},
                {"list_name": "shop_name", "name": "other_shop", "label": ["ອື່ນໆ"]},
                {"list_name": "district", "name": "d01", "label": ["ມ. ຈອມເພັດ"]},
                {"list_name": "district", "name": "d02", "label": ["ມ. ຫຼວງພະບາງ"]},
                {"list_name": "village", "name": "v01", "label": ["ບ. ໜຶ່ງ"]},
                {"list_name": "license", "name": "1", "label": ["ມີໃບທະບຽນວິສາຫະກິດ"]},
                {"list_name": "license", "name": "0", "label": ["ບໍ່ມີໃບທະບຽນວິສາຫະກິດ"]},
                {"list_name": "acquirer", "name": "1", "label": ["ຮັບຊຳລະພາຍໃນ"]},
                {"list_name": "acquirer", "name": "2", "label": ["ຮັບຊຳລະຕ່າງປະເທດ"]},
                {"list_name": "acquirer", "name": "3", "label": ["ບໍ່ມີເຄື່ອງມືຮັບຊຳລະ"]},
                {"list_name": "QR", "name": "1", "label": ["Lao QR"]},
                {"list_name": "QR", "name": "2", "label": ["QR ຮ້ານຄ້າ"]},
                {"list_name": "psp", "name": "1", "label": ["BCEL"]},
                {"list_name": "psp", "name": "2", "label": ["JDB"]},
                {"list_name": "YN_Use", "name": "1", "label": ["ໃຊ້ບໍລິການພາຍໃນ"]},
                {"list_name": "YN_Use", "name": "0", "label": ["ບໍ່ໄດ້ໃຊ້"]},
                {"list_name": "int", "name": "1", "label": ["ສົນໃຈ"]},
                {"list_name": "int", "name": "0", "label": ["ບໍ່ສົນໃຈ"]},
                {"list_name": "profit", "name": "1", "label": ["ບໍ່ເກີນ 400 ລ້ານ"]},
                {"list_name": "profit", "name": "2", "label": ["400 – 4,500 ລ້ານ"]},
                {"list_name": "learn", "name": "1", "label": ["ເຄີຍໄດ້ຮັບຟັງແລ້ວ"]},
                {"list_name": "learn", "name": "0", "label": ["ບໍ່ເຄີຍ"]},
            ],
        }
    }

@pytest.fixture
def subs():
    return [
        # both domestic+foreign, not using, interested -> both_int
        {"S0_Q1": "2026-06-29", "S1_Q1": "1", "Section_3/S3_Q1": "restaurant",
         "S3_Q2": "other_shop", "S3_Q2_oth": "Taiwan", "S3_Q3": "d02", "S3_Q4": "v01",
         "S3_Q6": "1", "S3_Q7": "1 2", "S3_Q9": "1", "S3_Q10": "1 2", "S3_Q12": "0",
         "S3_Q15": "1", "S3_Q17": "2", "S4_Q1": "1", "S4_Q2": "0",
         "geopoint": "19.88 102.13 300 5", "_submission_time": "2026-06-29T03:00:00", "_id": 1},
        # foreign only, not using, not interested -> foreign_unint
        {"S0_Q1": "2026-06-29", "S1_Q1": "0", "Section_3/S3_Q1": "hotel",
         "S3_Q2": "H001", "S3_Q3": "d01", "S3_Q4": "v01", "S3_Q6": "0", "S3_Q7": "2",
         "S3_Q10": "1", "S3_Q12": "0", "S3_Q15": "0", "S3_Q17": "1", "S4_Q1": "0",
         "S4_Q2": "1", "_submission_time": "2026-06-29T10:00:00", "_id": 2},
    ]
