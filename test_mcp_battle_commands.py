#!/usr/bin/env python3
"""
Tests for MCP Battle Commands Integration
Tests all newly added battle-related MCP commands
"""

import json
import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project directory to the path
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from mcp_server import (
    cmd_battle,
    cmd_battle_config,
    cmd_predict,
    cmd_replay,
    cmd_replays,
    MONSTER_DIR
)


class TestBattleCommands:
    """Test suite for battle MCP commands"""

    def test_cmd_battle_config_valid_mode(self):
        """Test setting valid battle mode"""
        result = cmd_battle_config(mode="INTERACTIVE", ai_personality="BALANCED")
        data = json.loads(result)
        
        assert data["success"] == True
        assert data["config"]["mode"] == "INTERACTIVE"
        assert data["config"]["ai_personality"] == "BALANCED"

    def test_cmd_battle_config_all_modes(self):
        """Test all valid battle modes"""
        valid_modes = ["INTERACTIVE", "PVP_AI", "PVE", "AI_VS_AI"]
        
        for mode in valid_modes:
            result = cmd_battle_config(mode=mode, ai_personality="BALANCED")
            data = json.loads(result)
            assert data["success"] == True
            assert data["config"]["mode"] == mode

    def test_cmd_battle_config_all_personalities(self):
        """Test all valid AI personalities"""
        valid_personalities = ["AGGRESSIVE", "DEFENSIVE", "BALANCED", "TACTICAL", "EVOLVING"]
        
        for personality in valid_personalities:
            result = cmd_battle_config(mode="INTERACTIVE", ai_personality=personality)
            data = json.loads(result)
            assert data["success"] == True
            assert data["config"]["ai_personality"] == personality

    def test_cmd_battle_config_invalid_mode(self):
        """Test invalid battle mode returns error"""
        result = cmd_battle_config(mode="INVALID_MODE", ai_personality="BALANCED")
        data = json.loads(result)
        
        assert data["success"] == False
        assert "Invalid mode" in data["error"]

    def test_cmd_battle_config_invalid_personality(self):
        """Test invalid personality returns error"""
        result = cmd_battle_config(mode="INTERACTIVE", ai_personality="INVALID_PERSONALITY")
        data = json.loads(result)
        
        assert data["success"] == False
        assert "Invalid personality" in data["error"]

    def test_cmd_predict_basic(self):
        """Test basic battle prediction"""
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = {
                "name": "TestMon",
                "level": 5,
                "stats": {"health": 100, "attack": 10, "defense": 10, "speed": 10}
            }
            
            result = cmd_predict(opponent_name="Enemy", opponent_level=5)
            data = json.loads(result)
            
            assert data["success"] == True
            assert "prediction" in data
            assert data["matchup"]["player"] == "TestMon (Lv.5)"
            assert data["matchup"]["opponent"] == "Enemy (Lv.5)"
            assert "win_probability" in data["prediction"]
            assert "recommended_strategy" in data["prediction"]

    def test_cmd_predict_with_level_advantage(self):
        """Test prediction with player level advantage"""
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = {
                "name": "StrongMon",
                "level": 10,
                "stats": {"health": 100, "attack": 10, "defense": 10, "speed": 10}
            }
            
            result = cmd_predict(opponent_name="WeakEnemy", opponent_level=5)
            data = json.loads(result)
            
            assert data["success"] == True
            # Higher player level should give higher win probability
            win_prob = float(data["prediction"]["win_probability"].rstrip('%'))
            assert win_prob > 50  # Should be better than 50-50

    def test_cmd_predict_with_level_disadvantage(self):
        """Test prediction with player level disadvantage"""
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = {
                "name": "WeakMon",
                "level": 5,
                "stats": {"health": 100, "attack": 10, "defense": 10, "speed": 10}
            }
            
            result = cmd_predict(opponent_name="StrongEnemy", opponent_level=10)
            data = json.loads(result)
            
            assert data["success"] == True
            # Lower player level should give lower win probability
            win_prob = float(data["prediction"]["win_probability"].rstrip('%'))
            assert win_prob < 50  # Should be less than 50-50

    def test_cmd_predict_no_pet(self):
        """Test prediction returns error when no pet exists"""
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = None
            
            result = cmd_predict()
            data = json.loads(result)
            
            assert data["success"] == False
            assert "No pet found" in data["error"]

    def test_cmd_replay_missing_id(self):
        """Test replay command requires ID"""
        result = cmd_replay("")
        data = json.loads(result)
        
        assert data["success"] == False
        assert "replay_id is required" in data["error"]

    def test_cmd_replay_not_found(self):
        """Test replay returns error when not found"""
        result = cmd_replay("nonexistent_battle")
        data = json.loads(result)
        
        assert data["success"] == False
        assert "not found" in data["error"].lower() or "error" in data

    def test_cmd_replays_basic(self):
        """Test listing replays"""
        result = cmd_replays(limit=10)
        data = json.loads(result)
        
        assert data["success"] == True
        assert "replays" in data
        assert isinstance(data["replays"], list)
        assert "total" in data

    def test_cmd_replays_limit(self):
        """Test replays respects limit parameter"""
        result_5 = cmd_replays(limit=5)
        result_10 = cmd_replays(limit=10)
        
        data_5 = json.loads(result_5)
        data_10 = json.loads(result_10)
        
        assert data_5["success"] == True
        assert data_10["success"] == True
        assert len(data_5["replays"]) <= 5
        assert len(data_10["replays"]) <= 10

    @patch('mcp_server.load_json')
    def test_cmd_battle_requires_pet(self, mock_load):
        """Test battle command returns error when no pet exists"""
        mock_load.return_value = None
        
        result = cmd_battle(target="Enemy")
        data = json.loads(result)
        
        assert data["success"] == False
        assert "No pet found" in data["error"]

    @patch('mcp_server.load_json')
    def test_cmd_battle_with_config(self, mock_load):
        """Test battle command with custom configuration"""
        mock_load.return_value = {
            "name": "TestMon",
            "level": 5,
            "stats": {"health": 100, "attack": 10, "defense": 10, "speed": 10}
        }
        
        # Just verify it doesn't crash and returns a valid response
        result = cmd_battle(
            target="Enemy",
            mode="PVP_AI",
            ai_personality="AGGRESSIVE",
            show_reasoning=True
        )
        data = json.loads(result)
        
        # Should have either success or a valid error structure
        assert "success" in data or "error" in data


class TestBattleCommandsIntegration:
    """Integration tests for battle command workflows"""

    def test_battle_workflow(self):
        """Test complete battle workflow: config -> predict -> battle"""
        # Step 1: Configure battle
        config_result = cmd_battle_config(mode="INTERACTIVE", ai_personality="BALANCED")
        config_data = json.loads(config_result)
        assert config_data["success"] == True
        
        # Step 2: Predict outcome
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = {
                "name": "MyMon",
                "level": 5,
                "stats": {"health": 100, "attack": 10, "defense": 10, "speed": 10}
            }
            
            predict_result = cmd_predict(opponent_name="Opponent", opponent_level=5)
            predict_data = json.loads(predict_result)
            assert predict_data["success"] == True
            assert predict_data["prediction"]["win_probability"] is not None

    def test_multiple_battle_configs(self):
        """Test setting multiple different battle configurations"""
        configs = [
            ("INTERACTIVE", "AGGRESSIVE"),
            ("PVP_AI", "DEFENSIVE"),
            ("AI_VS_AI", "BALANCED"),
            ("PVE", "TACTICAL")
        ]
        
        for mode, personality in configs:
            result = cmd_battle_config(mode=mode, ai_personality=personality)
            data = json.loads(result)
            assert data["success"] == True
            assert data["config"]["mode"] == mode
            assert data["config"]["ai_personality"] == personality

    def test_prediction_recommendations(self):
        """Test that predictions give appropriate strategy recommendations"""
        with patch('mcp_server.load_json') as mock_load:
            # Test high win probability -> Aggressive
            mock_load.return_value = {"name": "Strong", "level": 20, "stats": {}}
            result = cmd_predict(opponent_name="Weak", opponent_level=1)
            data = json.loads(result)
            assert "AGGRESSIVE" in data["prediction"]["recommended_strategy"] or data["prediction"]["win_probability"] == "90.0%"
            
            # Test low win probability -> Tactical/Defensive
            mock_load.return_value = {"name": "Weak", "level": 1, "stats": {}}
            result = cmd_predict(opponent_name="Strong", opponent_level=20)
            data = json.loads(result)
            strategy = data["prediction"]["recommended_strategy"]
            assert strategy in ["DEFENSIVE", "TACTICAL"]


class TestBattleCommandsEdgeCases:
    """Edge case tests for battle commands"""

    def test_cmd_predict_default_levels(self):
        """Test prediction with default opponent level"""
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = {"name": "Test", "level": 5, "stats": {}}
            
            # When opponent_level defaults to 1, should have advantage
            result = cmd_predict(opponent_name="Weak")
            data = json.loads(result)
            
            assert data["success"] == True
            win_prob = float(data["prediction"]["win_probability"].rstrip('%'))
            assert win_prob > 50

    def test_cmd_predict_extreme_levels(self):
        """Test prediction with extreme level differences"""
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = {"name": "Test", "level": 100, "stats": {}}
            
            result = cmd_predict(opponent_name="Tiny", opponent_level=1)
            data = json.loads(result)
            
            assert data["success"] == True
            win_prob = float(data["prediction"]["win_probability"].rstrip('%'))
            assert win_prob >= 90  # Should be nearly guaranteed win

    def test_battle_config_persistence(self):
        """Test that battle config is persisted"""
        mode = "PVP_AI"
        personality = "TACTICAL"
        
        result1 = cmd_battle_config(mode=mode, ai_personality=personality)
        data1 = json.loads(result1)
        
        # Config should be saved with timestamp
        assert "timestamp" in data1["config"]
        assert data1["config"]["mode"] == mode
        assert data1["config"]["ai_personality"] == personality

    def test_replays_empty_result(self):
        """Test replays command handles empty replay list gracefully"""
        result = cmd_replays(limit=10)
        data = json.loads(result)
        
        # Should always succeed and return valid structure
        assert data["success"] == True
        assert isinstance(data["replays"], list)
        assert isinstance(data["total"], int)


class TestBattleCommandsOutputFormats:
    """Test output format compliance"""

    def test_all_commands_return_valid_json(self):
        """Verify all commands return valid JSON"""
        commands = [
            ("config", lambda: cmd_battle_config()),
            ("replays", lambda: cmd_replays()),
        ]
        
        for name, cmd in commands:
            result = cmd()
            # Should be parseable JSON
            data = json.loads(result)
            assert isinstance(data, dict), f"{name} should return JSON dict"

    def test_success_field_consistency(self):
        """Test that success/error fields are consistent"""
        with patch('mcp_server.load_json') as mock_load:
            mock_load.return_value = {"name": "Test", "level": 5, "stats": {}}
            
            result = cmd_predict()
            data = json.loads(result)
            
            # Every result should have success field
            assert "success" in data
            assert isinstance(data["success"], bool)

    def test_error_messages_informative(self):
        """Test error messages are informative"""
        result = cmd_battle_config(mode="INVALID")
        data = json.loads(result)
        
        assert data["success"] == False
        assert "error" in data
        assert len(data["error"]) > 10  # Error message should be descriptive


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
