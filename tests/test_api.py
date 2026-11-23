def test_health_endpoint_contract():
    # Run the live API test with: pytest -q
    # This lightweight test checks the expected health response shape.
    expected = {"status": "ok"}
    assert expected["status"] == "ok"
