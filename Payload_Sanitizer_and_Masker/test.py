from main import sanitize_payload

payload = {
    "transaction_id": "tx_9988",
    "metadata": {
        "user": "alice",
        "CREDIT_CARD": "1234-5678-9012-3456",
        "history": [
            {"action": "login", "Password": "secret_password_123"}
        ]
    }
}

sensitive_keys = {"credit_card", "password"}

print(sanitize_payload(payload, sensitive_keys))

# Expected Output:
# {
#     "transaction_id": "tx_9988",
#     "metadata": {
#         "user": "alice",
#         "CREDIT_CARD": "***MASKED***",
#         "history": [
#             {"action": "login", "Password": "***MASKED***"}
#         ]
#     }
# }