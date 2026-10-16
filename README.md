### AI Assistant

My ERPNext AI Assistant

独立仓库为 [yueweiit/deeplinkerp-ai_assistant](https://github.com/yueweiit/deeplinkerp-ai_assistant)，开发主线和 PR 目标均为 `main`。Frappe App 名保持 `ai_assistant`。

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app --branch main ai_assistant https://github.com/yueweiit/deeplinkerp-ai_assistant.git
bench install-app ai_assistant
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/ai_assistant
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
