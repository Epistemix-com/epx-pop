import pytest

from epxpop import SynthPop


@pytest.fixture(scope="session")
def synth_pop_2010():
    return SynthPop(country="usa", version="US_2010.v5")


def test_load_people(synth_pop_2010: SynthPop) -> None:
    for people_df in [
        synth_pop_2010.load_people(["Loving_County_TX"], include_gq_people=False),
        synth_pop_2010.load_people(["Loving_County_TX"], include_gq_people=True),
    ]:
        assert len(people_df.index) == 70
        assert list(people_df.columns) == [
            "ID",
            "AGE",
            "sex",
            "race",
            "household_relationship",
            "household_income",
        ]


def test_load_households(synth_pop_2010: SynthPop) -> None:
    hh_df = synth_pop_2010.load_households(["Loving_County_TX"])
    assert len(hh_df.index) == 39
    assert list(hh_df.columns) == ["ID", "LAT", "LON", "ELEV", "income", "Block_Group"]
    assert len(hh_df.pipe(lambda df: df[df["Block_Group"].isna()])) == 0

    # Single name with two FIPS codes, 06069 06085
    hh_df = synth_pop_2010.load_households(["San_Jose-Sunnyvale-Santa_Clara_CA_MSA"])
    assert len(hh_df.index) == 16805 + 604204
    assert len(hh_df.pipe(lambda df: df[df["Block_Group"].isna()])) == 0

    # Two names with a single FIPS code each
    hh_df = synth_pop_2010.load_households(
        ["San_Benito_County_CA", "Santa_Clara_County_CA"]
    )
    assert len(hh_df.index) == 16805 + 604204
    assert len(hh_df.pipe(lambda df: df[df["Block_Group"].isna()])) == 0


def test_load_gq_people(synth_pop_2010: SynthPop) -> None:
    gq_df = synth_pop_2010.load_gq_people(["Allegheny_County_PA"])
    assert len(gq_df.index) == 30583
    assert list(gq_df.columns) == [
        "ID",
        "AGE",
        "sex",
        "race",
        "ROLE",
        "PLACE",
        "Block_Group",
        "gq_type",
    ]
    assert len(gq_df.pipe(lambda df: df[df["Block_Group"].isna()])) == 0

    # Single name with two FIPS codes, 06069 06085
    gq_df = synth_pop_2010.load_gq_people(["San_Jose-Sunnyvale-Santa_Clara_CA_MSA"])
    assert len(gq_df.index) == 129 + 21218
    assert len(gq_df.pipe(lambda df: df[df["Block_Group"].isna()])) == 0

    # Two names with a single FIPS code each
    gq_df = synth_pop_2010.load_gq_people(
        ["San_Benito_County_CA", "Santa_Clara_County_CA"]
    )
    assert len(gq_df.index) == 129 + 21218
    assert len(gq_df.pipe(lambda df: df[df["Block_Group"].isna()])) == 0


def test_load_people_household_xref(synth_pop_2010: SynthPop) -> None:
    xref_df = synth_pop_2010.load_people_household_xref(["Loving_County_TX"])
    assert len(xref_df.index) == 70
    assert list(xref_df.columns) == ["ID", "PLACE", "ROLE"]

    # Single name with two FIPS codes, 06069 06085
    xref_df = synth_pop_2010.load_people_household_xref(
        ["San_Jose-Sunnyvale-Santa_Clara_CA_MSA"]
    )
    assert len(xref_df.index) == 55208 + 1746026

    # Two names with a single FIPS code each
    xref_df = synth_pop_2010.load_people_household_xref(
        ["San_Benito_County_CA", "Santa_Clara_County_CA"]
    )
    assert len(xref_df.index) == 55208 + 1746026
