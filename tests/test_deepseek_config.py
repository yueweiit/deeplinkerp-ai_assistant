from unittest.mock import Mock

import frappe
import pytest

from ai_assistant.ai_assistant import model_client
from ai_assistant.patches import migrate_deepseek_settings


def test_migrates_production_overseas_key_to_encrypted_single_once(monkeypatch):
    from frappe.utils import password

    legacy = {
        "overseas_cost_ai_api_key": "synthetic-secret",
        "overseas_cost_ai_model": "deepseek-v4-flash",
        "overseas_cost_ai_vision_model": "deepseek-v4-flash-vision-exp",
    }
    saved = {"deepseek_model": "deepseek-flash"}
    db = Mock()
    db.get_singles_dict.return_value = saved
    db.set_single_value.side_effect = lambda _, values: saved.update(values)
    monkeypatch.setattr(frappe, "db", db)
    monkeypatch.setattr(frappe, "conf", legacy)
    encrypt = Mock()
    monkeypatch.setattr(password, "set_encrypted_password", encrypt)
    migrate_deepseek_settings.execute()
    migrate_deepseek_settings.execute()
    encrypt.assert_called_once_with("AI Assistant Settings", "AI Assistant Settings", "synthetic-secret", "deepseek_api_key")
    assert saved["deepseek_api_key"] == "********"
    assert saved["deepseek_model"] == "deepseek-v4-flash"
    assert saved["deepseek_vision_model"] == "deepseek-v4-flash-vision-exp"
    assert legacy["overseas_cost_ai_api_key"] == "synthetic-secret"


def test_deepseek_connection_uses_official_post_and_sanitizes_provider_errors(monkeypatch):
    monkeypatch.setattr(model_client, "_", lambda message: message)
    config = {"api_key": "synthetic-secret", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-flash"}
    reply = Mock(status_code=200)
    reply.json.return_value = {"choices": [{"finish_reason": "stop", "message": {"content": '{"ok":true}'}}]}
    post = Mock(return_value=reply)
    monkeypatch.setattr(model_client.requests, "post", post)
    assert model_client.request_deepseek_json(config, [{"role": "user", "content": "Return a JSON object."}]) == {"ok": True}
    assert post.call_args.args == ("https://api.deepseek.com/v1/chat/completions",)
    assert post.call_args.kwargs["allow_redirects"] is False
    assert post.call_args.kwargs["json"]["response_format"] == {"type": "json_object"}
    post.reset_mock()
    with pytest.raises(model_client.DeepSeekError):
        model_client.request_deepseek_json({**config, "base_url": "https://other.invalid/v1"}, [])
    post.assert_not_called()
    reply.status_code = 401
    reply.text = "synthetic-secret"
    with pytest.raises(model_client.DeepSeekError) as error:
        model_client.request_deepseek_json(config, [])
    assert "synthetic-secret" not in str(error.value)
