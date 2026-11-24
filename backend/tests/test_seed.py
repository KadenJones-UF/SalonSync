"""Tests for the database seeding CLI command and fixtures."""
import pytest
from app.models.note import Note
from app.models.user import User
from app.seed import seed_database

def test_seed_database_creates_users_and_notes(app):
    """Verify that seed_database populates designated users and 150+ authentic notes."""
    with app.app_context():
        stats = seed_database()
        assert stats["users_created"] == 4
        assert stats["notes_created"] >= 150
        assert stats["total_notes"] >= 150

        # Verify designated moderator exists
        mod = User.query.filter_by(role="moderator").first()
        assert mod is not None
        assert mod.username == "moderator_admin"
        assert mod.check_password("ModPassword2026!") is True

        # Verify stylist members exist
        members = User.query.filter_by(role="member").all()
        assert len(members) == 3
        member_usernames = [m.username for m in members]
        assert "jane_stylist" in member_usernames
        assert "carlos_color" in member_usernames
        assert "elena_balayage" in member_usernames

        # Verify authentic brands and shades
        brands = {n.brand for n in Note.query.all()}
        assert "Redken" in brands
        assert "Wella" in brands
        assert "Schwarzkopf" in brands
        assert "L'Oreal" in brands
        assert "Pulp Riot" in brands

        # Verify both public and private notes exist
        public_count = Note.query.filter_by(is_public=True).count()
        private_count = Note.query.filter_by(is_public=False).count()
        assert public_count > 0
        assert private_count > 0


def test_seed_database_idempotency(app):
    """Verify that running seed_database repeatedly is idempotent and does not create duplicates."""
    with app.app_context():
        # First run
        stats1 = seed_database()
        initial_notes = stats1["total_notes"]
        initial_users = stats1["total_users"]

        # Second run
        stats2 = seed_database()
        assert stats2["users_created"] == 0
        assert stats2["notes_created"] == 0
        assert stats2["total_notes"] == initial_notes
        assert stats2["total_users"] == initial_users


def test_seed_cli_runner(app):
    """Verify invocation of the 'flask seed' CLI command."""
    runner = app.test_cli_runner()
    result = runner.invoke(args=["seed"])
    assert result.exit_code == 0
    assert "Seeding SalonSync demonstration fixtures..." in result.output
    assert "Done!" in result.output
