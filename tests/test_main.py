def test_load_dotenv():
    from dotenv import load_dotenv
    assert load_dotenv() is not None