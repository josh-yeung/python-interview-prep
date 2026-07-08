ALLOWED_TOP_LEVEL_KEYS = frozenset({
    "PIPELINE_NAME",
    "ACTIONS",
    "RETRIES",
    "OPTIONS",
})

ALLOWED_ACTIONS = frozenset({
    "read",
    "write",
    "transform",
    "validate",
    "publish",
})

MAX_RETRIES = 10
