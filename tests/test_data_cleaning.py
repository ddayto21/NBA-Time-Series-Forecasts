# test_data_cleaning.py
import os
import shutil
import pandas as pd
import pytest
from src.data_collection.data_cleaning import DataCleaner

@pytest.fixture
def cleaner():
    """Returns a new instance of DataCleaner."""
    return DataCleaner()

@pytest.fixture
def tmp_csv(tmp_path, request):
    """
    Creates a temporary CSV file with optional initial content.
    Use param `content` in the test to specify content.
    """
    content = request.param if hasattr(request, 'param') else ""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(content, encoding="utf-8")
    return csv_file

# -----------------------------------------------------------------------------
# 1. Test backup_file
# -----------------------------------------------------------------------------
def test_backup_file(cleaner, tmp_csv):
    # file: tmp_csv
    file_path = str(tmp_csv)
    cleaner.backup_file(file_path)
    backup_path = file_path.replace(".csv", "_backup.csv")
    assert os.path.exists(backup_path), "Backup file should be created."

def test_backup_file_nonexistent(cleaner, tmp_path):
    # Nonexistent file
    non_file_path = str(tmp_path / "nonexistent.csv")
    cleaner.backup_file(non_file_path)
    backup_path = non_file_path.replace(".csv", "_backup.csv")
    assert not os.path.exists(backup_path), "No backup should be created for nonexistent file."

# -----------------------------------------------------------------------------
# 2. Test remove_columns
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tmp_csv", [
    "Team,Year,Eastern Conference,Western Conference\nLakers,2020,Yes,No\nCeltics,2020,No,Yes\n"
], indirect=True)
def test_remove_columns(cleaner, tmp_csv):
    file_path = str(tmp_csv)
    cleaner.remove_columns(file_path, ["Eastern Conference", "Western Conference"])
    df = pd.read_csv(file_path)
    assert "Eastern Conference" not in df.columns
    assert "Western Conference" not in df.columns
    assert df.columns[0] == "Team"

# -----------------------------------------------------------------------------
# 3. Test clean_mvp
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tmp_csv", [
    "Player,Year,Pts Won,Extra,Share\nJohn Doe,2001,100,X,0.5\nJane Smith,2002,200,Y,0.7\n"
], indirect=True)
def test_clean_mvp(cleaner, tmp_csv):
    file_path = str(tmp_csv)
    df = cleaner.clean_mvp(file_path)
    assert list(df.columns) == ["Player", "Year", "Pts Won", "Share"], "Columns mismatch."
    assert len(df) == 2, "Should have two rows."

# -----------------------------------------------------------------------------
# 4. Test single_row + clean_players
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tmp_csv", [
    """Rk,Player,Year,Tm\n1,John Doe,2001,LAL\n2,John Doe,2001,TOT\n3,Jane Smith,2001,LAC""",
], indirect=True)
def test_clean_players(cleaner, tmp_csv):
    file_path = str(tmp_csv)
    df = cleaner.clean_players(file_path)
    # TOT row should override LAL row for John Doe
    row_john = df[df["Player"] == "John Doe"].iloc[0]
    assert row_john["Tm"] == "LAL", "John's TOT row should rename Tm to last row's Tm."
    # Jane is unaffected
    row_jane = df[df["Player"] == "Jane Smith"].iloc[0]
    assert row_jane["Tm"] == "LAC"

# -----------------------------------------------------------------------------
# 5. Test clean_teams
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tmp_csv", [
    "Team,W\nLakers,Division Champs\nCeltics,50\n"
], indirect=True)
def test_clean_teams(cleaner, tmp_csv):
    file_path = str(tmp_csv)
    df = cleaner.clean_teams(file_path)
    # One row should be removed (the one with 'Division')
    assert len(df) == 1
    assert df.iloc[0]["Team"] == "Celtics"

# -----------------------------------------------------------------------------
# 6. Test clean_nick_names
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tmp_csv", [
    """prefix_1,name,prefix_2
lac,los angeles clippers,extra
lal,los angeles lakers,extra
"""], indirect=True)
def test_clean_nick_names(cleaner, tmp_csv):
    file_path = str(tmp_csv)
    cleaner.clean_nick_names(file_path)
    df = pd.read_csv(file_path)
    assert "prefix_2" not in df.columns
    assert list(df.columns) == ["Abbreviation", "Name"]
    assert df.iloc[0]["Abbreviation"] == "LAC"
    assert df.iloc[1]["Name"] == "Los Angeles Lakers"

# -----------------------------------------------------------------------------
# 7. Test nick_names
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tmp_csv", [
    """Abbreviation,Name
LAC,Los Angeles Clippers
LAL,Los Angeles Lakers
"""], indirect=True)
def test_nick_names(cleaner, tmp_csv):
    file_path = str(tmp_csv)
    data = cleaner.nick_names(file_path)
    assert "LAC" in data
    assert data["LAL"] == "Los Angeles Lakers"

# -----------------------------------------------------------------------------
# 8. Test merge_datasets
# -----------------------------------------------------------------------------
def test_merge_datasets(cleaner):
    players_df = pd.DataFrame({
        "Player": ["John Doe", "Jane Smith"],
        "Year": [2001, 2001],
        "Tm": ["LAL", "BOS"]
    })
    mvps_df = pd.DataFrame({
        "Player": ["John Doe"],
        "Year": [2001],
        "Pts Won": [150],
        "Pts Max": [200],
        "Share": [0.75]
    })

    merged = cleaner.merge_datasets(players_df, mvps_df)
    assert len(merged) == 2, "Should have two rows after outer merge."
    # Check John's row has MVP data
    row_john = merged[merged["Player"] == "John Doe"].iloc[0]
    assert row_john["Pts Won"] == 150
    assert row_john["Pts Max"] == 200
    assert row_john["Share"] == 0.75

    # Jane has no MVP data, should be 0
    row_jane = merged[merged["Player"] == "Jane Smith"].iloc[0]
    assert row_jane["Pts Won"] == 0
    assert row_jane["Pts Max"] == 0
    assert row_jane["Share"] == 0