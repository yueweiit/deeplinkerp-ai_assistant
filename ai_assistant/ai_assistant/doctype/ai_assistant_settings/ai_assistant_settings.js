frappe.ui.form.on("AI Assistant Settings", {
	refresh(frm) {
		frm.set_intro(__("DeepSeek settings are shared by bank statement import, overseas costing, and AI Assistant."));
		if (!frm.is_dirty()) {
			frm.add_custom_button(__("Test DeepSeek"), async () => {
				const {message} = await frappe.call({
					method: "ai_assistant.ai_assistant.model_client.test_deepseek_connection",
					type: "POST",
					freeze: true,
				});
				if (message?.model) {
					frappe.show_alert({message: __("DeepSeek connection successful"), indicator: "green"});
				}
			});
		}
	}
});
