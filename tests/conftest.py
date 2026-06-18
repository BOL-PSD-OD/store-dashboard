import pytest

@pytest.fixture
def form():
    return {
        "content": {
            "survey": [
                {"type": "begin_group", "name": "Section_2"},
                {"type": "select_one YN", "name": "S1_Q1", "label": ["1.1 owner?"]},
                {"type": "select_one biz_type", "name": "S2_Q1", "label": ["2.1 biz type"]},
                {"type": "select_one license", "name": "S2_Q3", "label": ["2.3 license"]},
                {"type": "select_one market", "name": "S2_Q4", "label": ["2.4 market"]},
                {"type": "select_one QR", "name": "S2_Q5", "label": ["2.5 QR"]},
                {"type": "select_one status", "name": "S2_Q7", "label": ["2.7 status"]},
                {"type": "select_multiple psp", "name": "S2_Q8", "label": ["2.8 psp"]},
                {"type": "select_one YN", "name": "S2_Q11", "label": ["2.11 night market"]},
                {"type": "select_one learn", "name": "S3_Q1", "label": ["3.1 aware?"]},
                {"type": "end_group"},
            ],
            "choices": [
                {"list_name": "YN", "name": "1", "label": ["ແມ່ນ"]},
                {"list_name": "YN", "name": "0", "label": ["ບໍ່ແມ່ນ"]},
                {"list_name": "biz_type", "name": "restaurant", "label": ["ຮ້ານອາຫານ"]},
                {"list_name": "biz_type", "name": "hotel", "label": ["ໂຮງແຮມ"]},
                {"list_name": "license", "name": "1", "label": ["ມີໃບທະບຽນວິສາຫະກິດ"]},
                {"list_name": "license", "name": "0", "label": ["ບໍ່ມີໃບທະບຽນວິສາຫະກິດ"]},
                {"list_name": "status", "name": "1", "label": ["ມີບັນຊີ"]},
                {"list_name": "status", "name": "3", "label": ["ບໍ່ມີບັນຊີ"]},
                {"list_name": "psp", "name": "1", "label": ["BCEL"]},
                {"list_name": "psp", "name": "2", "label": ["JDB"]},
                {"list_name": "learn", "name": "1", "label": ["ເຄີຍໄດ້ຮັບຟັງແລ້ວ"]},
                {"list_name": "learn", "name": "0", "label": ["ບໍ່ເຄີຍ"]},
            ],
        }
    }

@pytest.fixture
def subs():
    return [
        {"S1_Q1": "1", "Section_2/S2_Q1": "restaurant", "S2_Q3": "1",
         "S2_Q4": "1", "S2_Q5": "1", "S2_Q7": "1", "S2_Q8": "1 2",
         "S2_Q11": "1", "S3_Q1": "1", "_submission_time": "2026-06-29T03:00:00",
         "_geopoint_latitude": 19.88, "_geopoint_longitude": 102.13, "_id": 1},
        {"S1_Q1": "0", "Section_2/S2_Q1": "hotel", "S2_Q3": "0",
         "S2_Q4": "0", "S2_Q5": "0", "S2_Q7": "3", "S2_Q8": "1",
         "S2_Q11": "0", "S3_Q1": "0", "_submission_time": "2026-06-29T10:00:00",
         "_geopoint_latitude": None, "_geopoint_longitude": None, "_id": 2},
    ]
