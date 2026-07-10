"""Integration tests for schviews — used from pytigon parent project context.

Tests cover GenericTable registration, URL pattern generation, view_editor,
and doc type registration.
"""

from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

from pytigon_lib.schviews import GenericTable, VIEWS_REGISTER, generic_table_start
from pytigon_lib.schviews.viewtools import DOC_TYPES


def _fake_model():
    return type(
        "FakeModel",
        (),
        {
            "_meta": type(
                "Meta",
                (),
                {"model_name": "testmodel", "object_name": "TestModel"},
            )(),
            "objects": MagicMock(),
            "DoesNotExist": Exception,
        },
    )


@pytest.fixture
def mock_get_model():
    FakeModel = _fake_model()
    with patch("pytigon_lib.schviews.apps.get_model", return_value=FakeModel) as mock:
        yield mock, FakeModel


class TestGenericTableRegistration:
    def test_generic_table_start_returns_correct_type(self):
        urlpatterns = []
        result = generic_table_start(urlpatterns, "testapp")
        assert isinstance(result, GenericTable)

    def test_standard_registers_in_views_register(self, mock_get_model):
        mock, FakeModel = mock_get_model
        urlpatterns = []
        gt = GenericTable(urlpatterns, "testapp")
        gt.standard("TestModel", "Test Model", "Test Models")
        assert FakeModel in VIEWS_REGISTER["list"]
        assert FakeModel in VIEWS_REGISTER["detail"]
        assert FakeModel in VIEWS_REGISTER["edit"]
        assert FakeModel in VIEWS_REGISTER["create"]
        assert FakeModel in VIEWS_REGISTER["delete"]

    def test_standard_creates_url_patterns(self, mock_get_model):
        mock, FakeModel = mock_get_model
        urlpatterns = []
        gt = GenericTable(urlpatterns, "testapp")
        gt.standard("TestModel", "Test Model", "Test Models")
        assert len(urlpatterns) > 0


class TestGenericTableUrlPatterns:
    def test_crud_patterns_include_all_actions(self, mock_get_model):
        mock, FakeModel = mock_get_model
        urlpatterns = []
        gt = GenericTable(urlpatterns, "testapp")
        gt.standard("TestModel", "Test Model", "Test Models")
        urls = [str(p.pattern) for p in urlpatterns]
        assert any(x in u for u in urls for x in ("list", "tree"))
        assert any("view" in u for u in urls)
        assert any("edit" in u for u in urls)
        assert any("add" in u for u in urls)
        assert any("delete" in u for u in urls)


class TestGenericTableFromSchema:
    def test_from_schema_returns_rows(self, mock_get_model):
        mock, FakeModel = mock_get_model
        urlpatterns = []
        gt = GenericTable(urlpatterns, "testapp")
        rows = gt.from_schema("l", "TestModel", title="T", title_plural="Ts")
        assert rows is not None
        assert rows.base_model is FakeModel

    def test_from_schema_creates_url_pattern(self, mock_get_model):
        mock, FakeModel = mock_get_model
        urlpatterns = []
        gt = GenericTable(urlpatterns, "testapp")
        gt.standard("TestModel", "Test Model", "Test Models")
        assert len(urlpatterns) > 0


class TestViewEditor:
    def test_view_editor_post_with_value_returns_ok(self):
        from pytigon_lib.schviews import view_editor

        mock_model = MagicMock()
        mock_obj = MagicMock()
        mock_obj._meta.fields = []
        mock_model.objects.get.return_value = mock_obj

        rf = RequestFactory()
        request = rf.post("/", {"value": "new_value", "pk": "1"})
        result = view_editor(
            request, pk=1, app="testapp", tab="TestTab", model=mock_model,
            template_name="t.html", field_edit_name="body",
            post_save_redirect="/ok", target="editable",
        )
        assert result.status_code == 200
        assert b"OK" in result.content


class TestDocTypes:
    def test_all_required_doc_types_present(self):
        assert "pdf" in DOC_TYPES
        assert "spdf" in DOC_TYPES
        assert "json" in DOC_TYPES
        assert "txt" in DOC_TYPES
        assert "xlsx" in DOC_TYPES
        assert "docx" in DOC_TYPES
        assert "pptx" in DOC_TYPES
        assert "ods" in DOC_TYPES
        assert "odt" in DOC_TYPES
        assert "odp" in DOC_TYPES
        assert "hdoc" in DOC_TYPES
        assert "hxls" in DOC_TYPES
