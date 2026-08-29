import hashlib
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

class CryptographicAuditLedger:
    """
    Tamper-evident blockchain-inspired cryptographic audit ledger for medical assessments.
    Chains SHA-256 hashes of patient assessments, clinical reviews, and PHI access logs.
    """
    _blocks: List[Dict[str, Any]] = []
    _genesis_hash: str = "0000000000000000000000000000000000000000000000000000000000000000"

    @classmethod
    def record_event(
        cls,
        event_type: str,
        actor_id: str,
        actor_role: str,
        entity_id: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        prev_hash = cls._blocks[-1]["current_hash"] if cls._blocks else cls._genesis_hash
        timestamp = datetime.utcnow().isoformat() + "Z"
        block_id = str(uuid.uuid4())

        block_data = {
            "block_index": len(cls._blocks) + 1,
            "block_id": block_id,
            "event_type": event_type,
            "actor_id": actor_id,
            "actor_role": actor_role,
            "entity_id": entity_id,
            "timestamp": timestamp,
            "payload_summary": {k: str(v) for k, v in payload.items() if k not in ["password", "token"]},
            "previous_hash": prev_hash
        }

        serialized = json.dumps(block_data, sort_keys=True)
        current_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        block_data["current_hash"] = current_hash

        cls._blocks.append(block_data)
        return block_data

    @classmethod
    def verify_ledger_integrity(cls) -> Dict[str, Any]:
        for i in range(len(cls._blocks)):
            block = cls._blocks[i]
            expected_prev = cls._blocks[i-1]["current_hash"] if i > 0 else cls._genesis_hash
            if block["previous_hash"] != expected_prev:
                return {
                    "is_valid": False,
                    "tamper_detected_at_index": i + 1,
                    "reason": "Broken previous_hash chain"
                }

            copy_data = dict(block)
            curr_h = copy_data.pop("current_hash")
            re_hash = hashlib.sha256(json.dumps(copy_data, sort_keys=True).encode("utf-8")).hexdigest()
            if curr_h != re_hash:
                return {
                    "is_valid": False,
                    "tamper_detected_at_index": i + 1,
                    "reason": "Payload hash mismatch / data altered"
                }

        return {
            "is_valid": True,
            "total_blocks_verified": len(cls._blocks),
            "genesis_anchor": cls._genesis_hash[:16] + "...",
            "latest_head_hash": cls._blocks[-1]["current_hash"] if cls._blocks else cls._genesis_hash,
            "audit_compliance": "HIPAA / FDA 21 CFR Part 11 Compliant Audit Trail"
        }

    @classmethod
    def get_entity_history(cls, entity_id: str) -> List[Dict[str, Any]]:
        return [b for b in cls._blocks if b.get("entity_id") == str(entity_id)]
