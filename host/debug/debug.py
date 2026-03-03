def debug_response(response):
    print(f"[DEBUG] Agent response type: {type(response)}")
    print(f"[DEBUG] Agent response keys: {response.keys() if isinstance(response, dict) else 'N/A'}")
    if "messages" in response:
        print(f"[DEBUG] Number of messages: {len(response['messages'])}")
        for i, msg in enumerate(response['messages']):
            if hasattr(msg, 'type'):
                msg_type = msg.type
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    print(f"[DEBUG] Message {i}: type={msg_type}, has tool_calls")
                else:
                    print(f"[DEBUG] Message {i}: type={msg_type}")