"""Use the existing encrypted provider setting for the deployed DeepSeek key."""

import os

import frappe
from frappe.utils import password

from ai_assistant.ai_assistant.model_client import DEEPSEEK_BASE_URL, is_official_deepseek_url


def execute():
    doctype = "AI Assistant Settings"
    saved = frappe.db.get_singles_dict(doctype)
    if saved.get("deepseek_api_key"):
        return
    legacy_key = frappe.conf.get("overseas_cost_ai_api_key") or os.environ.get("OVERSEAS_COST_AI_API_KEY")
    legacy_base = (
        frappe.conf.get("overseas_cost_ai_base_url")
        or os.environ.get("OVERSEAS_COST_AI_BASE_URL")
        or os.environ.get("DEEPSEEK_BASE_URL")
        or DEEPSEEK_BASE_URL
    )
    global_key = frappe.conf.get("deepseek_api_key") or os.environ.get("DEEPSEEK_API_KEY")
    if not legacy_key or (global_key and global_key != legacy_key):
        return
    if not is_official_deepseek_url(legacy_base) or not is_official_deepseek_url(
        saved.get("deepseek_base_url") or legacy_base
    ):
        return
    values = {"deepseek_api_key": "********", "deepseek_base_url": legacy_base}
    legacy_model = frappe.conf.get("overseas_cost_ai_model") or os.environ.get("OVERSEAS_COST_AI_MODEL")
    if legacy_model:
        values["deepseek_model"] = legacy_model
    vision = frappe.conf.get("overseas_cost_ai_vision_model") or os.environ.get("OVERSEAS_COST_AI_VISION_MODEL")
    if vision and not saved.get("deepseek_vision_model"):
        values["deepseek_vision_model"] = vision
    password.set_encrypted_password(doctype, doctype, legacy_key, "deepseek_api_key")
    frappe.db.set_single_value(doctype, values)
