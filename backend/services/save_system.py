"""
存档系统
管理游戏保存和加载
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Company


class SaveSystem:
    """存档系统类"""
    
    def __init__(self, save_dir: Optional[str] = None):
        if save_dir:
            self.save_dir = Path(save_dir)
        else:
            self.save_dir = Path.home() / ".openclaw" / "workspace-car-export" / "ai-startup-simulator" / "data" / "saves"
        
        # 确保目录存在
        self.save_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, company: Company, save_name: str = "autosave") -> bool:
        """
        保存游戏
        """
        try:
            save_file = self.save_dir / f"{save_name}.json"
            
            save_data = {
                "version": "1.0",
                "saved_at": datetime.now().isoformat(),
                "company": company.to_dict(),
                "metadata": {
                    "day": company.day,
                    "name": company.name,
                    "cash": company.cash,
                    "reputation": company.reputation,
                }
            }
            
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def load(self, save_name: str = "autosave") -> Optional[Company]:
        """
        加载游戏
        """
        try:
            save_file = self.save_dir / f"{save_name}.json"
            
            if not save_file.exists():
                return None
            
            with open(save_file, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            
            company = Company.from_dict(save_data["company"])
            return company
        
        except Exception as e:
            print(f"Load error: {e}")
            return None
    
    def delete(self, save_name: str) -> bool:
        """删除存档"""
        try:
            save_file = self.save_dir / f"{save_name}.json"
            if save_file.exists():
                save_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Delete error: {e}")
            return False
    
    def list_saves(self) -> List[dict]:
        """列出所有存档"""
        saves = []
        
        for save_file in self.save_dir.glob("*.json"):
            try:
                with open(save_file, "r", encoding="utf-8") as f:
                    save_data = json.load(f)
                
                saves.append({
                    "name": save_file.stem,
                    "saved_at": save_data.get("saved_at", "Unknown"),
                    "metadata": save_data.get("metadata", {}),
                })
            except:
                continue
        
        return sorted(saves, key=lambda x: x["saved_at"], reverse=True)
    
    def get_save_info(self, save_name: str) -> Optional[dict]:
        """获取存档信息"""
        save_file = self.save_dir / f"{save_name}.json"
        
        if not save_file.exists():
            return None
        
        try:
            with open(save_file, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            
            return {
                "name": save_name,
                "version": save_data.get("version", "Unknown"),
                "saved_at": save_data.get("saved_at", "Unknown"),
                "metadata": save_data.get("metadata", {}),
            }
        except:
            return None
    
    def backup(self, save_name: str) -> bool:
        """创建存档备份"""
        try:
            save_file = self.save_dir / f"{save_name}.json"
            backup_file = self.save_dir / f"{save_name}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            
            if save_file.exists():
                import shutil
                shutil.copy2(save_file, backup_file)
                return True
            
            return False
        except Exception as e:
            print(f"Backup error: {e}")
            return False
    
    def auto_cleanup(self, keep_count: int = 5) -> int:
        """
        自动清理旧备份
        保留最近的 keep_count 个备份
        返回删除的文件数
        """
        deleted = 0
        backups = sorted(
            self.save_dir.glob("*.backup.*.json"),
            key=lambda x: x.name,
            reverse=True
        )
        
        for backup_file in backups[keep_count:]:
            try:
                backup_file.unlink()
                deleted += 1
            except:
                continue
        
        return deleted


# 全局存档系统实例
_save_system: Optional[SaveSystem] = None


def get_save_system() -> SaveSystem:
    """获取存档系统实例"""
    global _save_system
    if _save_system is None:
        _save_system = SaveSystem()
    return _save_system
