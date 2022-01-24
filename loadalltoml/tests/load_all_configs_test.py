from pathlib import Path

from load_all_toml import LoadAllToml

WORKING = Path(__file__).resolve().parent  # Where is this file running?
CONFIG_PATH = str(WORKING / "configs")

EXPECTED_LOAD_COUNT = 3


def test_len_of_no_loaded() -> None:
    assert not len(LoadAllToml(CONFIG_PATH))


def test_len_of_loaded_fixtures() -> None:
    loader = LoadAllToml(CONFIG_PATH)
    loader.load()
    assert len(loader) == EXPECTED_LOAD_COUNT


def test_confirm_reset_on_load() -> None:
    loader = LoadAllToml(CONFIG_PATH)
    loader._loaded_configs["test_sample"] = {}
    loader.load()
    assert "test_sample" not in loader._loaded_configs


def test_fall_through_on_invalid_file() -> None:
    # Give it a file that will fail parsing
    loader = LoadAllToml(str(WORKING), "*.py")
    loader.load()
    assert not len(loader)
