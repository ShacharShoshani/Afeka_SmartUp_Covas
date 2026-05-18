import json
from pathlib import Path
from covas.state import save_active_profile, load_active_profile
from covas.constants import STATE_FILE

def test_save_and_load_active_profile(tmp_path, mocker):
    # Mock STATE_FILE to use a temporary path
    test_state_file = tmp_path / ".covas_state.json"
    mocker.patch("covas.state.STATE_FILE", test_state_file)
    
    save_active_profile("test-profile")
    assert test_state_file.exists()
    
    with open(test_state_file, "r") as f:
        data = json.load(f)
        assert data["active_profile"] == "test-profile"
    
    loaded = load_active_profile()
    assert loaded == "test-profile"

def test_load_non_existent_profile(tmp_path, mocker):
    test_state_file = tmp_path / "non_existent.json"
    mocker.patch("covas.state.STATE_FILE", test_state_file)
    
    assert load_active_profile() is None

def test_load_corrupt_profile(tmp_path, mocker):
    test_state_file = tmp_path / "corrupt.json"
    mocker.patch("covas.state.STATE_FILE", test_state_file)
    
    with open(test_state_file, "w") as f:
        f.write("invalid json")
    
    assert load_active_profile() is None
