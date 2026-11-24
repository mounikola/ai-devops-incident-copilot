json={
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseMimeType": "application/json",
        "responseSchema": {
            "type": "OBJECT",
            "properties": {
                "summary": {"type": "STRING"},
                "severity": {
                    "type": "STRING",
                    "enum": ["low", "medium", "high", "critical"],
                },
                "likely_cause": {"type": "STRING"},
                "confidence": {"type": "NUMBER"},
                "evidence": {"type": "ARRAY", "items": {"type": "STRING"}},
                "recommended_steps": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": [
                "summary",
                "severity",
                "likely_cause",
                "confidence",
                "evidence",
                "recommended_steps",
            ],
        },
    },
},
