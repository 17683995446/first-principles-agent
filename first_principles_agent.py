"""
第一性原理永动知识图谱Agent
基于三大公理构建：存续、记忆、自驱
特性：零依赖、单文件、真正永动、自进化

版本: 2.4.0

使用方式：
1. 直接运行：python first_principles_agent.py
2. 按 Ctrl+C 优雅退出
3. 知识图谱会自动保存到当前目录

配置说明（可修改以下常量）：
- LOOP_SLEEP: 循环间隔（秒），越小越快
- EVOLVE_CYCLE: 每N轮进化一次
- KG_PATH: 图谱保存路径
- TASK_MAX_LEN: 任务池最大长度
- SAVE_EVERY_N: 每N轮保存一次
- LLM_ENABLED: 是否启用LLM语义萃取
- LLM_DEMO_MODE: 是否使用演示模式（无需API）

新增功能（v2.4.0）：
- JSON配置文件支持
- 日志系统
- 性能监控
- 任务优先级
- 知识图谱可视化导出
- 插件系统
- 多语言支持
- 数据备份恢复
- 单元测试框架
"""
import time
import json
import os
import traceback
import urllib.request
import ssl
import argparse
import hashlib
import gzip
import bz2
import uuid
import random
import math
import statistics
import re
import threading
import sqlite3
import subprocess
import socket
import struct
import string
import shutil
import fnmatch
import warnings
from collections import deque, OrderedDict
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, parse_qs, urlencode


def format_duration(seconds):
    """
    将秒数格式化为友好的时间字符串
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化后的字符串，如 "2h30m45s" 或 "1m30s"
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m{secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if secs > 0:
            return f"{hours}h{mins}m{secs}s"
        else:
            return f"{hours}h{mins}m"


class Logger:
    """简单日志系统：支持文件和控制台输出"""
    
    def __init__(self, log_file=None, console_output=True, log_level="INFO"):
        self.log_file = log_file
        self.console_output = console_output
        self.log_level = log_level
        self.levels = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}
        self.current_level = self.levels.get(log_level, 1)
        
        # 如果指定了日志文件，确保目录存在
        if self.log_file:
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
    
    def _should_log(self, level):
        return self.levels.get(level, 1) >= self.current_level
    
    def _format_message(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{level}] {message}"
    
    def _write(self, level, message):
        if not self._should_log(level):
            return
        
        formatted = self._format_message(level, message)
        
        if self.console_output:
            print(formatted)
        
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(formatted + "\n")
            except Exception as e:
                print(f"[日志写入失败] {e}")
    
    def debug(self, message):
        self._write("DEBUG", message)
    
    def info(self, message):
        self._write("INFO", message)
    
    def warn(self, message):
        self._write("WARN", message)
    
    def error(self, message):
        self._write("ERROR", message)

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

# ====================== 配置区域 ======================
LOOP_SLEEP = 0.5          # 循环间隔（秒）
EVOLVE_CYCLE = 50         # 进化周期
KG_PATH = "agent_kg_first_principles.json"  # 图谱路径
TASK_MAX_LEN = 200        # 任务池大小
CONTEXT_MAX_LEN = 100     # 上下文长度
MAX_EXECUTION_DEPTH = 10  # 最大深度
WEIGHT_DECAY_RATE = 0.05  # 权重衰减率
WEIGHT_BOOST_RATE = 0.2   # 权重强化率
SAVE_EVERY_N = 5          # 保存间隔
LLM_ENABLED = True        # 是否启用LLM
LLM_DEMO_MODE = False     # LLM演示模式
# ====================== API配置 ======================
API_KEY = "sk-uqelhavcdhfxjzjesdenxpbtqombamjniazzjtbssmdcwdvg"
API_BASE = "https://api.siliconflow.cn/v1"
LLM_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
# =====================================================


# ====================== 集中式配置管理 ======================
class Config:
    """
    集中式配置管理类
    保持向后兼容的同时，为未来重构做准备
    
    遵循：图难于其易，为大于其细！
    """
    
    # 基础配置
    LOOP_SLEEP = 0.5
    EVOLVE_CYCLE = 50
    KG_PATH = "agent_kg_first_principles.json"
    TASK_MAX_LEN = 200
    CONTEXT_MAX_LEN = 100
    MAX_EXECUTION_DEPTH = 10
    WEIGHT_DECAY_RATE = 0.05
    WEIGHT_BOOST_RATE = 0.2
    SAVE_EVERY_N = 5
    
    # LLM配置
    LLM_ENABLED = True
    LLM_DEMO_MODE = False
    API_KEY = "sk-uqelhavcdhfxjzjesdenxpbtqombamjniazzjtbssmdcwdvg"
    API_BASE = "https://api.siliconflow.cn/v1"
    LLM_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
    
    @classmethod
    def sync_from_global(cls):
        """从旧全局变量同步到配置对象"""
        cls.LOOP_SLEEP = LOOP_SLEEP
        cls.EVOLVE_CYCLE = EVOLVE_CYCLE
        cls.KG_PATH = KG_PATH
        cls.TASK_MAX_LEN = TASK_MAX_LEN
        cls.CONTEXT_MAX_LEN = CONTEXT_MAX_LEN
        cls.MAX_EXECUTION_DEPTH = MAX_EXECUTION_DEPTH
        cls.WEIGHT_DECAY_RATE = WEIGHT_DECAY_RATE
        cls.WEIGHT_BOOST_RATE = WEIGHT_BOOST_RATE
        cls.SAVE_EVERY_N = SAVE_EVERY_N
        cls.LLM_ENABLED = LLM_ENABLED
        cls.LLM_DEMO_MODE = LLM_DEMO_MODE
        cls.API_KEY = API_KEY
        cls.API_BASE = API_BASE
        cls.LLM_MODEL = LLM_MODEL
    
    @classmethod
    def load_from_file(cls, config_path="agent_config.json"):
        """从JSON配置文件加载配置"""
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                
                # 安全加载配置项
                for key, value in config_data.items():
                    if hasattr(cls, key):
                        setattr(cls, key, value)
                        print(f"[配置加载] {key} = {value}")
                return True
            else:
                # 创建默认配置文件
                cls.save_to_file(config_path)
                return False
        except Exception as e:
            print(f"[配置加载失败] {e}，使用默认配置")
            return False
    
    @classmethod
    def save_to_file(cls, config_path="agent_config.json"):
        """保存当前配置到JSON文件"""
        try:
            config_data = {
                "LOOP_SLEEP": cls.LOOP_SLEEP,
                "EVOLVE_CYCLE": cls.EVOLVE_CYCLE,
                "KG_PATH": cls.KG_PATH,
                "TASK_MAX_LEN": cls.TASK_MAX_LEN,
                "CONTEXT_MAX_LEN": cls.CONTEXT_MAX_LEN,
                "MAX_EXECUTION_DEPTH": cls.MAX_EXECUTION_DEPTH,
                "WEIGHT_DECAY_RATE": cls.WEIGHT_DECAY_RATE,
                "WEIGHT_BOOST_RATE": cls.WEIGHT_BOOST_RATE,
                "SAVE_EVERY_N": cls.SAVE_EVERY_N,
                "LLM_ENABLED": cls.LLM_ENABLED,
                "LLM_DEMO_MODE": cls.LLM_DEMO_MODE,
                "API_BASE": cls.API_BASE,
                "LLM_MODEL": cls.LLM_MODEL
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            print(f"[配置保存] 默认配置已保存到 {config_path}")
            return True
        except Exception as e:
            print(f"[配置保存失败] {e}")
            return False

# =====================================================

# 初始化TASK_POOL，会在应用命令行参数后重新初始化
TASK_POOL = deque(maxlen=TASK_MAX_LEN)


class LLMSemanticExtractor:
    """LLM语义萃取器：将自然语言转换为知识图谱实体和关系"""
    
    def __init__(self):
        # 优先使用Config类，保持向后兼容
        self.enabled = getattr(Config, 'LLM_ENABLED', LLM_ENABLED)
        self.demo_mode = getattr(Config, 'LLM_DEMO_MODE', LLM_DEMO_MODE)
        self.api_base = getattr(Config, 'API_BASE', API_BASE)
        self.api_key = getattr(Config, 'API_KEY', API_KEY)
        self.llm_model = getattr(Config, 'LLM_MODEL', LLM_MODEL)
    
    def call_llm(self, prompt):
        """调用硅基流动API（含重试机制）"""
        if self.demo_mode:
            return self.demo_response(prompt)
        
        max_retries = 2
        for retry in range(max_retries + 1):
            try:
                url = f"{self.api_base}/chat/completions"
                data = {
                    "model": self.llm_model,
                    "messages": [
                        {"role": "system", "content": "你是一个知识图谱构建助手。从给定文本中提取实体和它们之间的关系，返回JSON格式：{\"entities\": [\"实体1\", \"实体2\", ...], \"relations\": [{\"source\": \"实体1\", \"target\": \"实体2\", \"type\": \"关系名称\"}, ...]}"},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "max_tokens": 500
                }
                
                json_data = json.dumps(data).encode('utf-8')
                request = urllib.request.Request(
                    url,
                    data=json_data,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.api_key}'
                    }
                )
                
                with urllib.request.urlopen(request, timeout=30) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return result['choices'][0]['message']['content']
            except Exception as e:
                if retry < max_retries:
                    wait_time = (retry + 1) * 1
                    print(f"[LLM调用失败] {e}，{wait_time}秒后重试 (第{retry + 1}次)")
                    time.sleep(wait_time)
                else:
                    print(f"[LLM调用失败] {e}，已重试{max_retries}次，启用演示模式")
                    self.demo_mode = True
                    return self.demo_response(prompt)
    
    def demo_response(self, prompt):
        """演示模式响应：智能模拟语义萃取"""
        # 基于关键词匹配的智能响应
        topic_keywords = {
            "知识图谱": ["知识图谱", "节点", "边", "实体", "关系", "关联", "推理"],
            "人工智能": ["人工智能", "机器学习", "深度学习", "神经网络", "算法"],
            "学习": ["学习", "知识", "记忆", "理解", "应用", "练习"],
            "系统": ["系统", "架构", "模块", "组件", "功能", "设计"],
            "数据": ["数据", "信息", "存储", "处理", "分析", "挖掘"],
            "技术": ["技术", "工具", "方法", "流程", "优化", "改进"]
        }
        
        # 查找匹配的主题
        matched_topic = None
        matched_entities = []
        for topic, keywords in topic_keywords.items():
            for kw in keywords:
                if kw in prompt:
                    matched_topic = topic
                    matched_entities = keywords
                    break
            if matched_topic:
                break
        
        # 如果没有匹配，使用默认主题
        if not matched_topic:
            matched_topic = "通用"
            matched_entities = ["任务", "目标", "执行", "结果", "反馈"]
        
        # 生成实体（取前5个）
        entities = matched_entities[:5]
        
        # 生成关系
        relations = []
        for i in range(len(entities) - 1):
            relations.append({
                "source": entities[i],
                "target": entities[i + 1],
                "type": "关联"
            })
        
        # 添加一些额外的关系使知识更丰富
        if len(entities) >= 3:
            relations.append({
                "source": entities[0],
                "target": entities[-1],
                "type": "包含"
            })
        
        return json.dumps({
            "entities": entities,
            "relations": relations
        }, ensure_ascii=False)
    
    def extract_knowledge(self, text):
        """从文本中提取知识"""
        prompt = f"从以下文本中提取实体和关系：\n{text}"
        response = self.call_llm(prompt)
        
        if not response:
            return [], []
        
        try:
            # 尝试解析JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                entities = data.get('entities', [])
                relations = data.get('relations', [])
                return entities, relations
        except:
            pass
        
        return [], []
    
    def generate_task_description(self, task_name):
        """为任务生成语义描述"""
        prompt = f"为这个任务生成简短的执行描述：{task_name}"
        response = self.call_llm(prompt)
        return response if response else f"执行任务：{task_name}"


class FirstPrincipleKG:
    """记忆层：剥离所有冗余，只保留智能本质结构"""
    
    def __init__(self):
        # 优先使用Config类，保持向后兼容
        self.kg_path = getattr(Config, 'KG_PATH', KG_PATH)
        self.weight_decay_rate = getattr(Config, 'WEIGHT_DECAY_RATE', WEIGHT_DECAY_RATE)
        self.weight_boost_rate = getattr(Config, 'WEIGHT_BOOST_RATE', WEIGHT_BOOST_RATE)
        # 【阶段28】数据验证器
        self.validator = DataValidator()
        # 【阶段31】缓存系统
        self.cache = Cache(max_size=200, default_ttl=300)

        self.graph = {
            "nodes": {},
            "edges": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_saved": datetime.now().isoformat(),
                "total_tasks": 0,
                "total_insights": 0,
                "total_saves": 0,
                "agent_version": "2.2.0"
            }
        }
        self.pending_save = False
        # 优化：缓存计算结果
        self._cached_insights = None
        self._insights_updated = time.time()
        self._cache_ttl = 1.0  # 缓存1秒
        self.load()
        # 初始化合理的图谱结构
        if not self.graph["nodes"] or not self.graph["edges"]:
            self._initialize_smart_graph()
    
    def load(self):
        """记忆加载：重启不丢失经验"""
        try:
            with open(self.kg_path, "r", encoding="utf-8") as f:
                self.graph = json.load(f)
                if "metadata" not in self.graph:
                    self.graph["metadata"] = {
                        "created": datetime.now().isoformat(),
                        "last_saved": datetime.now().isoformat(),
                        "total_tasks": 0,
                        "total_insights": 0,
                        "total_saves": 0,
                        "agent_version": "2.2.0",
                        "total_nodes": 0,
                        "total_edges": 0
                    }
                else:
                    # 【修复7】 确保元数据包含所有新字段
                    md = self.graph["metadata"]
                    if "last_saved" not in md:
                        md["last_saved"] = datetime.now().isoformat()
                    if "total_saves" not in md:
                        md["total_saves"] = 0
                    if "agent_version" not in md:
                        md["agent_version"] = "2.2.0"
                    # 补充缺失的统计字段
                    if "total_nodes" not in md:
                        md["total_nodes"] = len(self.graph.get("nodes", {}))
                    if "total_edges" not in md:
                        md["total_edges"] = len(self.graph.get("edges", []))
        except FileNotFoundError:
            self.save()
    
    def save(self, force=False):
        """记忆固化：所有行为落地为知识"""
        if not force and not self.pending_save:
            return
        # 更新保存统计信息
        self.graph["metadata"]["last_saved"] = datetime.now().isoformat()
        self.graph["metadata"]["total_saves"] += 1
        self.graph["metadata"]["agent_version"] = "2.2.0"
        self.graph["metadata"]["total_nodes"] = len(self.graph["nodes"])
        self.graph["metadata"]["total_edges"] = len(self.graph["edges"])
        with open(self.kg_path, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, ensure_ascii=False, indent=2)
        self.pending_save = False
    
    def mark_dirty(self):
        """标记图谱需要保存"""
        self.pending_save = True
    
    def add_node(self, name, attr=None):
        """新增实体（记忆公理核心操作）"""
        if name not in self.graph["nodes"]:
            self.graph["nodes"][name] = attr or {
                "create_time": time.time(),
                "valid": True,
                "access_count": 0,
                "last_access": time.time()
            }
        else:
            # 确保旧节点有必要的属性
            node = self.graph["nodes"][name]
            if "access_count" not in node:
                node["access_count"] = 0
            if "last_access" not in node:
                node["last_access"] = time.time()
            node["access_count"] += 1
            node["last_access"] = time.time()
        self.mark_dirty()
        self._invalidate_insights_cache()
    
    def add_edge(self, source, target, relation, weight=1.0):
        """新增关系（智能迭代核心）"""
        self.add_node(source)
        self.add_node(target)
        
        existing = self.find_edge(source, target, relation)
        if existing:
            existing["weight"] = min(1.0, existing["weight"] + self.weight_boost_rate)
            self.mark_dirty()
            self._invalidate_insights_cache()
            return
        
        self.graph["edges"].append({
            "source": source,
            "target": target,
            "relation": relation,
            "weight": weight,
            "create_time": time.time()
        })
        self.mark_dirty()
        self._invalidate_insights_cache()
    
    def find_edge(self, source, target, relation=None):
        """查找已存在的关系"""
        for edge in self.graph["edges"]:
            if edge["source"] == source and edge["target"] == target:
                if relation is None or edge.get("relation") == relation:
                    return edge
        return None
    
    def graph_traverse(self, start_node, depth=3):
        """图谱遍历：发现关联知识网络"""
        visited = set()
        queue = [(start_node, 0)]
        results = []
        
        while queue:
            node, current_depth = queue.pop(0)
            if node in visited or current_depth > depth:
                continue
            visited.add(node)
            results.append((node, current_depth))
            
            for edge in self.graph["edges"]:
                if edge["source"] == node and edge["weight"] > 0.3:
                    queue.append((edge["target"], current_depth + 1))
                if edge["target"] == node and edge["weight"] > 0.3:
                    queue.append((edge["source"], current_depth + 1))
        
        return results
    
    def get_relation_tasks(self, node, max_tasks=5):
        """自驱核心：通过关联知识自动推导新任务"""
        new_tasks = []
        related = self.graph_traverse(node, depth=2)
        
        for related_node, depth in related:
            for edge in self.graph["edges"]:
                if edge["source"] == related_node and edge["weight"] > 0.2:
                    task = f"推演:{edge['target']}"
                    if task not in new_tasks:
                        new_tasks.append(task)
                        if len(new_tasks) >= max_tasks:
                            return new_tasks
        
        return new_tasks
    
    def generate_autonomous_tasks(self):
        """自驱公理：空闲时自主生成新任务"""
        if not self.graph["edges"]:
            return [
                "🎯 探索:第一性原理",
                "🔨 构建:核心知识图谱",
                "✅ 验证:记忆公理"
            ]
        
        high_weight_edges = [e for e in self.graph["edges"] if e["weight"] > 0.5]
        if not high_weight_edges:
            return [
                "📖 复习:知识图谱",
                "💪 增强:记忆系统",
                "🔄 优化:推理逻辑"
            ]
        
        sorted_edges = sorted(high_weight_edges, key=lambda x: x["weight"], reverse=True)
        selected = sorted_edges[:min(4, len(sorted_edges))]
        
        # 生成更有意义的任务名，增加多样性和emoji
        tasks = []
        task_templates = [
            "🎯 深化:", 
            "🚀 扩展:", 
            "✅ 验证:", 
            "📖 复习:", 
            "💪 增强:", 
            "🔍 分析:", 
            "🔗 关联:"
        ]
        for i, edge in enumerate(selected):
            template = task_templates[i % len(task_templates)]
            tasks.append(f"{template}{edge['target']}")
        
        return tasks
    
    def weight_decay(self):
        """权重衰减：弱化低频知识"""
        for edge in self.graph["edges"]:
            if edge["weight"] > 0.1:
                edge["weight"] = max(0.05, edge["weight"] - self.weight_decay_rate)
        self.mark_dirty()
        self._invalidate_insights_cache()
    
    def trim_useless_knowledge(self):
        """进化：自动清理低价值知识"""
        new_edges = [e for e in self.graph["edges"] if e["weight"] > 0.15]
        removed_count = len(self.graph["edges"]) - len(new_edges)
        self.graph["edges"] = new_edges
        
        invalid_nodes = [
            name for name, attr in self.graph["nodes"].items()
            if attr.get("access_count", 0) < 2 and time.time() - attr.get("create_time", 0) > 86400
        ]
        for node in invalid_nodes:
            del self.graph["nodes"][node]
        
        self.mark_dirty()
        self._invalidate_insights_cache()
        return removed_count
    
    def _initialize_smart_graph(self):
        """初始化合理的知识图谱结构"""
        # 核心概念
        core_concepts = [
            ("第一性原理", "concept"),
            ("知识图谱", "concept"),
            ("记忆", "axiom"),
            ("自驱", "axiom"),
            ("存续", "axiom"),
            ("智能", "concept"),
            ("Agent", "system")
        ]
        
        # 添加核心概念节点
        for name, node_type in core_concepts:
            self.add_node(name, {"type": node_type})
        
        # 添加核心关系
        core_relations = [
            ("第一性原理", "知识图谱", "指导构建", 1.0),
            ("知识图谱", "记忆", "存储", 0.9),
            ("自驱", "知识图谱", "自动扩展", 0.9),
            ("存续", "知识图谱", "持久化", 0.9),
            ("智能", "知识图谱", "结构化", 0.8),
            ("Agent", "知识图谱", "使用", 1.0),
            ("Agent", "第一性原理", "遵循", 1.0),
            ("Agent", "记忆", "应用", 0.9),
            ("Agent", "自驱", "体现", 0.9),
            ("Agent", "存续", "实现", 0.9)
        ]
        
        for source, target, relation, weight in core_relations:
            self.add_edge(source, target, relation, weight)
        
        self.mark_dirty()
        # 【修复5】初始化后让缓存失效，确保下一次get_insights是新数据
        self._invalidate_insights_cache()
    
    def get_insights(self):
        """提取图谱洞察（带缓存优化）"""
        current_time = time.time()
        # 【阶段31】使用Cache类进行缓存
        cached = self.cache.get("insights")
        if cached is not None:
            return cached
        
        # 检查内部缓存是否有效
        if (self._cached_insights is not None and 
            current_time - self._insights_updated < self._cache_ttl):
            self.cache.set("insights", self._cached_insights, ttl=self._cache_ttl)
            return self._cached_insights
        
        # 缓存失效，重新计算
        # 按类型统计节点
        node_types = {}
        for name, attr in self.graph["nodes"].items():
            node_type = attr.get("type", "unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # 最近访问的节点
        sorted_recent = sorted(
            self.graph["nodes"].items(),
            key=lambda x: x[1].get("last_access", 0),
            reverse=True
        )[:10]
        
        # 访问热度最高的节点
        sorted_hot = sorted(
            self.graph["nodes"].items(),
            key=lambda x: x[1].get("access_count", 0),
            reverse=True
        )[:5]
        
        insights = {
            "total_nodes": len(self.graph["nodes"]),
            "total_edges": len(self.graph["edges"]),
            "avg_weight": sum(e["weight"] for e in self.graph["edges"]) / max(1, len(self.graph["edges"])),
            "top_relations": sorted(
                [(e["source"], e["relation"], e["target"], e["weight"]) for e in self.graph["edges"]],
                key=lambda x: x[3], reverse=True
            )[:5],
            "node_types": node_types,
            "recent_nodes": [name for name, _ in sorted_recent],
            "hot_nodes": [(name, attr.get("access_count", 0)) for name, attr in sorted_hot],
            "active_nodes": [
                name for name, attr in self.graph["nodes"].items()
                if attr.get("access_count", 0) > 0
            ]
        }
        
        # 保存到缓存
        self._cached_insights = insights
        self._insights_updated = current_time
        # 【阶段31】保存到Cache类
        self.cache.set("insights", insights, ttl=self._cache_ttl)
        return insights
    
    def _invalidate_insights_cache(self):
        """使洞察缓存失效（在图谱变化时调用）"""
        self._cached_insights = None
    
    def create_backup(self, backup_dir="backups"):
        """【阶段23】创建知识图谱备份"""
        try:
            # 确保备份目录存在
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # 生成备份文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"kg_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 保存备份
            backup_data = {
                "backup_time": datetime.now().isoformat(),
                "agent_version": "2.3.0",
                "graph": self.graph
            }
            
            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            print(f"[备份成功] 知识图谱已备份到 {backup_path}")
            return backup_path
        except Exception as e:
            print(f"[备份失败] {e}")
            return None
    
    def restore_from_backup(self, backup_path):
        """【阶段23】从备份恢复知识图谱"""
        try:
            if not os.path.exists(backup_path):
                print(f"[恢复失败] 备份文件不存在: {backup_path}")
                return False
            
            with open(backup_path, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
            
            if "graph" in backup_data:
                self.graph = backup_data["graph"]
                self.pending_save = True
                self._invalidate_insights_cache()
                print(f"[恢复成功] 知识图谱已从 {backup_path} 恢复")
                print(f"[恢复信息] 备份时间: {backup_data.get('backup_time', '未知')}")
                return True
            else:
                print("[恢复失败] 备份文件格式不正确")
                return False
        except Exception as e:
            print(f"[恢复失败] {e}")
            return False
    
    def list_backups(self, backup_dir="backups"):
        """【阶段23】列出所有备份文件"""
        try:
            if not os.path.exists(backup_dir):
                return []
            
            backups = []
            for filename in os.listdir(backup_dir):
                if filename.startswith("kg_backup_") and filename.endswith(".json"):
                    filepath = os.path.join(backup_dir, filename)
                    stat = os.stat(filepath)
                    backups.append({
                        "filename": filename,
                        "path": filepath,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime
                    })
            
            # 按修改时间排序
            backups.sort(key=lambda x: x["mtime"], reverse=True)
            return backups
        except Exception as e:
            print(f"[列出备份失败] {e}")
            return []
    
    def export_to_graphviz(self, output_path="kg_visualization.dot"):
        """【阶段20】导出为Graphviz DOT格式，用于可视化"""
        try:
            dot_content = ["digraph KnowledgeGraph {"]
            dot_content.append("  rankdir=LR;")
            dot_content.append('  node [shape=box, style=rounded];')
            
            # 添加节点
            for node_name, attr in self.graph["nodes"].items():
                if node_name is None:
                    continue
                node_type = attr.get("type", "unknown") if attr else "unknown"
                color = {
                    "concept": "lightblue",
                    "task": "lightgreen",
                    "semantic": "lightyellow",
                    "axiom": "lightcoral"
                }.get(node_type, "white")
                
                safe_name = str(node_name).replace('"', '\\"')
                dot_content.append(f'  "{safe_name}" [fillcolor={color}, style=filled];')
            
            # 添加边
            for edge in self.graph["edges"]:
                src = edge.get("source", "")
                tgt = edge.get("target", "")
                if src is None or tgt is None:
                    continue
                src = str(src).replace('"', '\\"')
                tgt = str(tgt).replace('"', '\\"')
                rel = edge.get("relation", "关联")
                weight = edge.get("weight", 1.0)
                
                dot_content.append(f'  "{src}" -> "{tgt}" [label="{rel}", weight="{weight:.2f}"];')
            
            dot_content.append("}")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(dot_content))
            
            print(f"[可视化导出] 知识图谱已导出到 {output_path}")
            print(f"[可视化导出] 使用命令: dot -Tpng {output_path} -o kg_visualization.png")
            return True
        except Exception as e:
            print(f"[可视化导出失败] {e}")
            return False
    
    def export_to_json(self, output_path="kg_export.json"):
        """【阶段20】导出为JSON格式"""
        try:
            export_data = {
                "export_time": datetime.now().isoformat(),
                "nodes": self.graph["nodes"],
                "edges": self.graph["edges"],
                "metadata": self.graph["metadata"]
            }
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"[JSON导出] 知识图谱已导出到 {output_path}")
            return True
        except Exception as e:
            print(f"[JSON导出失败] {e}")
            return False


class PerformanceMonitor:
    """性能监控器：收集和分析系统性能指标"""
    
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.metrics = {
            "execution_times": deque(maxlen=window_size),
            "memory_usage": deque(maxlen=window_size),
            "task_counts": deque(maxlen=window_size),
            "error_counts": deque(maxlen=window_size),
            "timestamp": deque(maxlen=window_size)
        }
        self.start_time = time.time()
        self.total_tasks = 0
        self.total_errors = 0
    
    def record_execution(self, exec_time, success=True):
        """记录一次执行"""
        self.metrics["execution_times"].append(exec_time)
        self.metrics["timestamp"].append(time.time())
        self.total_tasks += 1
        
        if not success:
            self.total_errors += 1
    
    def get_stats(self):
        """获取性能统计"""
        times = list(self.metrics["execution_times"])
        if not times:
            return {
                "avg_exec_time": 0,
                "min_exec_time": 0,
                "max_exec_time": 0,
                "total_tasks": 0,
                "total_errors": 0,
                "error_rate": 0,
                "uptime": time.time() - self.start_time
            }
        
        return {
            "avg_exec_time": sum(times) / len(times),
            "min_exec_time": min(times),
            "max_exec_time": max(times),
            "total_tasks": self.total_tasks,
            "total_errors": self.total_errors,
            "error_rate": (self.total_errors / max(1, self.total_tasks)) * 100,
            "uptime": time.time() - self.start_time,
            "recent_tasks": len(times)
        }
    
    def get_performance_report(self):
        """生成性能报告"""
        stats = self.get_stats()
        uptime_str = format_duration(stats["uptime"])
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║  📊 性能监控报告                                              ║
╠══════════════════════════════════════════════════════════════╣
║  运行时间: {uptime_str:<46} ║
║  总任务数: {stats['total_tasks']:<46} ║
║  错误次数: {stats['total_errors']:<46} ║
║  错误率: {stats['error_rate']:.2f}%{'':<44} ║
╠══════════════════════════════════════════════════════════════╣
║  执行时间统计 (最近{stats['recent_tasks']}次)                              ║
║    平均: {stats['avg_exec_time']:.2f}ms{'':<42} ║
║    最小: {stats['min_exec_time']:.2f}ms{'':<42} ║
║    最大: {stats['max_exec_time']:.2f}ms{'':<42} ║
╚══════════════════════════════════════════════════════════════╝
"""
        return report


class PluginManager:
    """【阶段21】插件系统管理器：支持动态加载和管理插件"""
    
    def __init__(self):
        self.plugins = {}
        self.hooks = {
            "before_task": [],
            "after_task": [],
            "before_save": [],
            "after_load": [],
            "on_error": []
        }
    
    def register_plugin(self, name, plugin_instance):
        """注册插件"""
        if name in self.plugins:
            print(f"[插件管理] 插件 '{name}' 已存在，将被覆盖")
        
        self.plugins[name] = plugin_instance
        
        # 自动注册插件的钩子
        if hasattr(plugin_instance, 'hooks'):
            for hook_name, hook_func in plugin_instance.hooks.items():
                if hook_name in self.hooks:
                    self.hooks[hook_name].append(hook_func)
        
        print(f"[插件管理] 插件 '{name}' 注册成功")
        return True
    
    def unregister_plugin(self, name):
        """注销插件"""
        if name in self.plugins:
            del self.plugins[name]
            print(f"[插件管理] 插件 '{name}' 已注销")
            return True
        return False
    
    def execute_hook(self, hook_name, *args, **kwargs):
        """执行指定钩子的所有回调"""
        results = []
        if hook_name in self.hooks:
            for hook_func in self.hooks[hook_name]:
                try:
                    result = hook_func(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"[插件钩子错误] {hook_name}: {e}")
        return results
    
    def list_plugins(self):
        """列出所有已注册的插件"""
        return list(self.plugins.keys())


class I18n:
    """【阶段22】多语言支持框架：简单的国际化支持"""
    
    def __init__(self, default_lang="zh"):
        self.current_lang = default_lang
        self.translations = {
            "zh": {
                "welcome": "第一性原理 · 永动知识图谱Agent 启动",
                "shutdown": "系统正常退出",
                "task_complete": "任务完成",
                "error": "错误",
                "success": "成功",
                "evolution": "进化",
                "health_check": "健康检查",
                "idle_evolve": "空闲进化"
            },
            "en": {
                "welcome": "First Principles · Eternal Knowledge Graph Agent Started",
                "shutdown": "System Shutdown",
                "task_complete": "Task Complete",
                "error": "Error",
                "success": "Success",
                "evolution": "Evolution",
                "health_check": "Health Check",
                "idle_evolve": "Idle Evolution"
            }
        }
    
    def set_language(self, lang):
        """设置当前语言"""
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False
    
    def get(self, key, default=None):
        """获取翻译文本"""
        lang_dict = self.translations.get(self.current_lang, {})
        return lang_dict.get(key, default or key)
    
    def add_translation(self, lang, key, text):
        """添加翻译"""
        if lang not in self.translations:
            self.translations[lang] = {}
        self.translations[lang][key] = text
    
    def list_languages(self):
        """列出所有可用语言"""
        return list(self.translations.keys())


class TaskScheduler:
    """【阶段27】任务调度器：支持定时任务、周期性任务和优先级排序"""

    def __init__(self):
        self.scheduled_tasks = {}
        self.periodic_tasks = {}
        self.task_counter = 0
        self._lock = False

    def _next_id(self):
        self.task_counter += 1
        return f"task_{self.task_counter}"

    def schedule_once(self, task_func, run_at, priority=5, args=None, kwargs=None):
        """调度一次性任务
        
        Args:
            task_func: 任务函数
            run_at: 执行时间戳
            priority: 优先级，数字越小优先级越高（1-10）
            args: 位置参数元组
            kwargs: 关键字参数字典
        """
        task_id = self._next_id()
        self.scheduled_tasks[task_id] = {
            "id": task_id,
            "func": task_func,
            "run_at": run_at,
            "priority": max(1, min(10, priority)),
            "args": args or (),
            "kwargs": kwargs or {},
            "status": "pending",
            "created_at": time.time()
        }
        return task_id

    def schedule_periodic(self, task_func, interval, priority=5, args=None, kwargs=None):
        """调度周期性任务
        
        Args:
            task_func: 任务函数
            interval: 执行间隔（秒）
            priority: 优先级
            args: 位置参数元组
            kwargs: 关键字参数字典
        """
        task_id = self._next_id()
        self.periodic_tasks[task_id] = {
            "id": task_id,
            "func": task_func,
            "interval": interval,
            "priority": max(1, min(10, priority)),
            "args": args or (),
            "kwargs": kwargs or {},
            "last_run": 0,
            "status": "active",
            "created_at": time.time()
        }
        return task_id

    def cancel_task(self, task_id):
        """取消任务"""
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id]["status"] = "cancelled"
            return True
        if task_id in self.periodic_tasks:
            self.periodic_tasks[task_id]["status"] = "cancelled"
            return True
        return False

    def remove_task(self, task_id):
        """移除任务"""
        if task_id in self.scheduled_tasks:
            del self.scheduled_tasks[task_id]
            return True
        if task_id in self.periodic_tasks:
            del self.periodic_tasks[task_id]
            return True
        return False

    def get_pending_tasks(self):
        """获取所有待执行的定时任务，按优先级排序"""
        now = time.time()
        pending = [
            t for t in self.scheduled_tasks.values()
            if t["status"] == "pending" and t["run_at"] <= now
        ]
        return sorted(pending, key=lambda x: (x["priority"], x["run_at"]))

    def get_due_periodic_tasks(self):
        """获取到期的周期性任务，按优先级排序"""
        now = time.time()
        due = []
        for t in self.periodic_tasks.values():
            if t["status"] == "active" and (now - t["last_run"]) >= t["interval"]:
                due.append(t)
        return sorted(due, key=lambda x: x["priority"])

    def execute_task(self, task_id):
        """执行指定任务"""
        task = None
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
        elif task_id in self.periodic_tasks:
            task = self.periodic_tasks[task_id]

        if not task or task["status"] in ("cancelled", "completed"):
            return None

        try:
            result = task["func"](*task.get("args", ()), **task.get("kwargs", {}))
            if task_id in self.scheduled_tasks:
                self.scheduled_tasks[task_id]["status"] = "completed"
            elif task_id in self.periodic_tasks:
                self.periodic_tasks[task_id]["last_run"] = time.time()
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_due_tasks(self):
        """执行所有到期的任务"""
        results = []
        for task in self.get_pending_tasks():
            results.append({"id": task["id"], **self.execute_task(task["id"])})
        for task in self.get_due_periodic_tasks():
            results.append({"id": task["id"], **self.execute_task(task["id"])})
        return results

    def list_tasks(self):
        """列出所有任务"""
        return {
            "scheduled": list(self.scheduled_tasks.values()),
            "periodic": list(self.periodic_tasks.values())
        }

    def get_task_count(self):
        """获取任务数量"""
        return len(self.scheduled_tasks) + len(self.periodic_tasks)


class DataValidator:
    """【阶段28】数据验证器：验证节点、边、任务的数据格式"""

    def __init__(self):
        self.custom_rules = {}

    def validate_node(self, name, attr=None):
        """验证节点数据格式"""
        errors = []
        if not name:
            errors.append("节点名称不能为空")
        if not isinstance(name, str):
            errors.append("节点名称必须是字符串")
        if isinstance(name, str) and len(name) > 200:
            errors.append("节点名称长度不能超过200")

        if attr is not None and not isinstance(attr, dict):
            errors.append("节点属性必须是字典")

        return {"valid": len(errors) == 0, "errors": errors}

    def validate_edge(self, source, target, relation, weight=1.0):
        """验证边数据格式"""
        errors = []
        if not source or not isinstance(source, str):
            errors.append("边的源节点必须是有效的字符串")
        if not target or not isinstance(target, str):
            errors.append("边的目标节点必须是有效的字符串")
        if not relation or not isinstance(relation, str):
            errors.append("边的关系必须是有效的字符串")
        if not isinstance(weight, (int, float)):
            errors.append("边的权重必须是数字")
        elif weight < 0 or weight > 1.0:
            errors.append("边的权重必须在0.0到1.0之间")

        return {"valid": len(errors) == 0, "errors": errors}

    def validate_task(self, task):
        """验证任务数据格式"""
        errors = []
        if not task:
            errors.append("任务不能为空")
        if not isinstance(task, str):
            errors.append("任务必须是字符串")
        if isinstance(task, str) and len(task) > 500:
            errors.append("任务长度不能超过500")

        return {"valid": len(errors) == 0, "errors": errors}

    def add_custom_rule(self, name, rule_func):
        """添加自定义验证规则"""
        self.custom_rules[name] = rule_func
        return True

    def validate_with_custom(self, data, rule_name):
        """使用自定义规则验证数据"""
        if rule_name not in self.custom_rules:
            return {"valid": False, "errors": [f"自定义规则 '{rule_name}' 不存在"]}

        try:
            result = self.custom_rules[rule_name](data)
            if isinstance(result, bool):
                return {"valid": result, "errors": [] if result else [f"自定义规则 '{rule_name}' 验证失败"]}
            elif isinstance(result, dict):
                return result
            else:
                return {"valid": bool(result), "errors": []}
        except Exception as e:
            return {"valid": False, "errors": [f"自定义规则执行异常: {str(e)}"]}

    def validate_all(self, name=None, attr=None, source=None, target=None, relation=None, weight=None, task=None):
        """统一验证入口"""
        results = {}
        if name is not None:
            results["node"] = self.validate_node(name, attr)
        if source is not None and target is not None:
            results["edge"] = self.validate_edge(source, target, relation or "关联", weight if weight is not None else 1.0)
        if task is not None:
            results["task"] = self.validate_task(task)
        return results


class EventSystem:
    """【阶段29】事件系统：支持事件发布/订阅和监听器管理"""

    def __init__(self):
        self.listeners = {}
        self.once_listeners = {}

    def on(self, event_name, listener):
        """注册事件监听器"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)
        return True

    def once(self, event_name, listener):
        """注册一次性事件监听器"""
        if event_name not in self.once_listeners:
            self.once_listeners[event_name] = []
        self.once_listeners[event_name].append(listener)
        return True

    def off(self, event_name, listener=None):
        """注销事件监听器
        
        Args:
            event_name: 事件名称
            listener: 指定监听器，为None则移除该事件所有监听器
        """
        removed = False
        if event_name in self.listeners:
            if listener is None:
                del self.listeners[event_name]
                removed = True
            else:
                if listener in self.listeners[event_name]:
                    self.listeners[event_name].remove(listener)
                    removed = True
                if not self.listeners[event_name]:
                    del self.listeners[event_name]

        if event_name in self.once_listeners:
            if listener is None:
                del self.once_listeners[event_name]
                removed = True
            else:
                if listener in self.once_listeners[event_name]:
                    self.once_listeners[event_name].remove(listener)
                    removed = True
                if not self.once_listeners[event_name]:
                    del self.once_listeners[event_name]

        return removed

    def emit(self, event_name, *args, **kwargs):
        """发布事件"""
        results = []

        # 触发普通监听器
        if event_name in self.listeners:
            for listener in list(self.listeners[event_name]):
                try:
                    result = listener(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})

        # 触发一次性监听器
        if event_name in self.once_listeners:
            for listener in list(self.once_listeners[event_name]):
                try:
                    result = listener(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})
            del self.once_listeners[event_name]

        return results

    def listener_count(self, event_name):
        """获取指定事件的监听器数量"""
        count = 0
        if event_name in self.listeners:
            count += len(self.listeners[event_name])
        if event_name in self.once_listeners:
            count += len(self.once_listeners[event_name])
        return count

    def event_names(self):
        """获取所有已注册的事件名称"""
        names = set(self.listeners.keys()) | set(self.once_listeners.keys())
        return list(names)

    def clear(self):
        """清除所有监听器"""
        self.listeners.clear()
        self.once_listeners.clear()
        return True


class HealthCheck:
    """【阶段30】健康检查端点：检查系统各组件状态"""

    def __init__(self, agent=None):
        self.agent = agent
        self.checks = {}

    def register_check(self, name, check_func):
        """注册健康检查项"""
        self.checks[name] = check_func
        return True

    def check_component(self, name):
        """检查单个组件"""
        if name in self.checks:
            try:
                result = self.checks[name]()
                if isinstance(result, dict):
                    return {"name": name, "healthy": result.get("healthy", False), **result}
                return {"name": name, "healthy": bool(result)}
            except Exception as e:
                return {"name": name, "healthy": False, "error": str(e)}
        return {"name": name, "healthy": False, "error": "检查项未注册"}

    def run_all_checks(self):
        """运行所有健康检查"""
        results = []
        for name in self.checks:
            results.append(self.check_component(name))
        return results

    def get_health_report(self):
        """生成健康报告"""
        checks = self.run_all_checks()
        healthy_count = sum(1 for c in checks if c.get("healthy"))
        total_count = len(checks)

        report = {
            "status": "healthy" if healthy_count == total_count and total_count > 0 else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total_count,
                "healthy": healthy_count,
                "unhealthy": total_count - healthy_count
            },
            "checks": checks
        }
        return report

    def check_agent(self):
        """检查Agent状态"""
        if not self.agent:
            return {"healthy": False, "error": "Agent未初始化"}
        return {
            "healthy": self.agent.alive,
            "run_count": self.agent.run_count,
            "uptime": time.time() - self.agent.start_time
        }

    def check_kg(self):
        """检查知识图谱状态"""
        if not self.agent or not self.agent.kg:
            return {"healthy": False, "error": "知识图谱未初始化"}
        insights = self.agent.kg.get_insights()
        return {
            "healthy": insights.get("total_nodes", 0) > 0,
            "nodes": insights.get("total_nodes", 0),
            "edges": insights.get("total_edges", 0)
        }

    def check_api(self):
        """检查API状态"""
        if not self.agent or not hasattr(self.agent, 'api'):
            return {"healthy": False, "error": "API未初始化"}
        return {
            "healthy": True,
            "routes": {
                "GET": len(self.agent.api.routes.get("GET", {})),
                "POST": len(self.agent.api.routes.get("POST", {}))
            }
        }

    def _register_default_checks(self):
        """注册默认健康检查"""
        self.register_check("agent", self.check_agent)
        self.register_check("kg", self.check_kg)
        self.register_check("api", self.check_api)


class APIWrapper:
    """【阶段26】API接口封装：提供RESTful风格的API接口"""
    
    def __init__(self, agent=None):
        self.agent = agent
        self.routes = {
            "GET": {},
            "POST": {},
            "PUT": {},
            "DELETE": {}
        }
        # 【阶段30】健康检查端点
        self.health_check = HealthCheck(agent)
        self.health_check._register_default_checks()
        # 【阶段32】限流器
        self.rate_limiter = RateLimiter(rate=20, capacity=20, strategy="token_bucket")
        self._register_default_routes()
    
    def _register_default_routes(self):
        """注册默认路由"""
        self.register_route("GET", "/status", self.get_status)
        self.register_route("GET", "/insights", self.get_insights)
        self.register_route("GET", "/tasks", self.get_tasks)
        self.register_route("POST", "/tasks", self.add_task)
        self.register_route("GET", "/nodes", self.get_nodes)
        self.register_route("GET", "/edges", self.get_edges)
        self.register_route("POST", "/backup", self.create_backup)
        self.register_route("GET", "/backups", self.list_backups)
        self.register_route("GET", "/config", self.get_config)
        self.register_route("PUT", "/config", self.update_config)
        # 【阶段30】健康检查路由
        self.register_route("GET", "/health", self.get_health)

    def get_health(self):
        """获取健康检查报告"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        report = self.health_check.get_health_report()
        report["status"] = 200 if report.get("status") == "healthy" else 503
        return report
    
    def register_route(self, method, path, handler):
        """注册路由"""
        if method in self.routes:
            self.routes[method][path] = handler
    
    def handle_request(self, method, path, data=None):
        """处理请求"""
        # 【阶段32】限流检查
        if not self.rate_limiter.allow():
            return {"error": "Rate limit exceeded", "status": 429}
        if method in self.routes and path in self.routes[method]:
            try:
                handler = self.routes[method][path]
                if data:
                    return handler(data)
                return handler()
            except Exception as e:
                return {"error": str(e), "status": 500}
        return {"error": "Not Found", "status": 404}
    
    def get_status(self):
        """获取系统状态"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        return {
            "status": 200,
            "run_count": self.agent.run_count,
            "alive": self.agent.alive,
            "uptime": time.time() - self.agent.start_time,
            "task_total": self.agent.task_total,
            "task_success": self.agent.task_success,
            "task_failed": self.agent.task_failed
        }
    
    def get_insights(self):
        """获取图谱洞察"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        insights = self.agent.kg.get_insights()
        insights["status"] = 200
        return insights
    
    def get_tasks(self):
        """获取任务列表"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        return {
            "status": 200,
            "tasks": list(TASK_POOL),
            "task_count": len(TASK_POOL)
        }
    
    def add_task(self, data):
        """添加任务"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        task = data.get("task", "")
        if task:
            TASK_POOL.append(task)
            return {"status": 200, "message": "Task added", "task": task}
        return {"error": "Task is required", "status": 400}
    
    def get_nodes(self):
        """获取节点列表"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        return {
            "status": 200,
            "nodes": list(self.agent.kg.graph["nodes"].keys()),
            "count": len(self.agent.kg.graph["nodes"])
        }
    
    def get_edges(self):
        """获取边列表"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        return {
            "status": 200,
            "edges": self.agent.kg.graph["edges"],
            "count": len(self.agent.kg.graph["edges"])
        }
    
    def create_backup(self):
        """创建备份"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        backup_path = self.agent.kg.create_backup()
        if backup_path:
            return {"status": 200, "backup_path": backup_path}
        return {"error": "Backup failed", "status": 500}
    
    def list_backups(self):
        """列出备份"""
        if not self.agent:
            return {"error": "Agent not initialized", "status": 500}
        
        backups = self.agent.kg.list_backups()
        return {
            "status": 200,
            "backups": backups,
            "count": len(backups)
        }
    
    def get_config(self):
        """获取配置"""
        return {
            "status": 200,
            "config": {
                "LOOP_SLEEP": Config.LOOP_SLEEP,
                "EVOLVE_CYCLE": Config.EVOLVE_CYCLE,
                "KG_PATH": Config.KG_PATH,
                "TASK_MAX_LEN": Config.TASK_MAX_LEN,
                "LLM_ENABLED": Config.LLM_ENABLED,
                "LLM_DEMO_MODE": Config.LLM_DEMO_MODE
            }
        }
    
    def update_config(self, data):
        """更新配置"""
        for key, value in data.items():
            if hasattr(Config, key):
                setattr(Config, key, value)
        
        return {"status": 200, "message": "Config updated"}


class FirstPrincipleEternalAgent:
    """永动主体：严格遵循三大公理"""
    
    def __init__(self, quick_test_rounds=None):
        self.kg = FirstPrincipleKG()
        self.llm = LLMSemanticExtractor()
        self.run_count = 0
        self.alive = True
        # 快速测试模式
        self.quick_test_rounds = quick_test_rounds
        # 【阶段22】多语言支持
        self.i18n = I18n()
        # 优先使用Config类，保持向后兼容
        self.context_max_len = getattr(Config, 'CONTEXT_MAX_LEN', CONTEXT_MAX_LEN)
        self.execution_context = deque(maxlen=self.context_max_len)
        self.failed_tasks = deque(maxlen=20)
        self.success_tasks = deque(maxlen=50)
        self.start_time = time.time()
        # 统计信息
        self.task_total = 0
        self.task_success = 0
        self.task_failed = 0
        # 性能统计
        self.execution_times = deque(maxlen=50)  # 记录最近50次执行时间
        self.nodes_added = 0
        self.edges_added = 0
        # 【阶段21】插件系统
        self.plugin_manager = PluginManager()
        # 进度指示符号
        self.progress_symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        # 性能监控
        self.last_qps_check = self.start_time
        self.tasks_since_last_check = 0
        # 【阶段18】添加性能监控器
        self.perf_monitor = PerformanceMonitor()
        # 【阶段26】API接口封装
        self.api = APIWrapper(self)
        # 【阶段27】任务调度器
        self.task_scheduler = TaskScheduler()
        # 【阶段29】事件系统
        self.event_system = EventSystem()
        # 【修复4】删除冗余变量，这些完全没有使用！
    
    def get_current_qps(self):
        """计算当前QPS（每秒任务数）"""
        current_time = time.time()
        time_diff = current_time - self.last_qps_check
        
        if time_diff >= 1.0:  # 每秒更新一次
            qps = self.tasks_since_last_check / time_diff
            # 重置计数器
            self.last_qps_check = current_time
            self.tasks_since_last_check = 0
            return qps
        
        return None  # 未到更新时间
    
    def health_check(self):
        """存续公理：健康自检"""
        self.run_count += 1
        self.tasks_since_last_check += 1
        
        # 优先使用Config类，保持向后兼容
        save_every_n = getattr(Config, 'SAVE_EVERY_N', SAVE_EVERY_N)
        evolve_cycle = getattr(Config, 'EVOLVE_CYCLE', EVOLVE_CYCLE)
        task_max_len = getattr(Config, 'TASK_MAX_LEN', TASK_MAX_LEN)
        
        # 定期保存图谱
        if self.run_count % save_every_n == 0:
            self.kg.save()
        
        if self.run_count % evolve_cycle == 0:
            removed = self.kg.trim_useless_knowledge()
            self.kg.weight_decay()
            
            insights = self.kg.get_insights()
            uptime = time.time() - self.start_time
            uptime_str = format_duration(uptime)
            print("\n" + "╔" + "═" * 58 + "╗", flush=True)
            print(f"║  🔄 [进化 #{self.run_count}] 存活 {uptime_str} | 精简 {removed} 条知识", flush=True)
            print("╠" + "═" * 58 + "╣", flush=True)
            print(f"║  📊 图谱: {insights['total_nodes']}节点, {insights['total_edges']}边, 平均权重{insights['avg_weight']:.2f}", flush=True)
            if insights.get('hot_nodes'):
                hot_preview = [f"{name}({count}次)" for name, count in insights['hot_nodes'][:3]]
                print(f"║  🔥 热门节点: {', '.join(hot_preview)}", flush=True)
            print("╚" + "═" * 58 + "╝", flush=True)
        
        if self.run_count % 20 == 0 and self.run_count % evolve_cycle != 0:
            insights = self.kg.get_insights()
            pool_preview = list(TASK_POOL)[:3]  # 显示前3个任务
            preview_str = f"[{', '.join(repr(t)[:20] for t in pool_preview)}...]" if len(TASK_POOL) > 3 else str(list(TASK_POOL))
            
            # 计算任务池饱和度
            pool_size = len(TASK_POOL)
            pool_capacity = task_max_len
            saturation_pct = (pool_size / pool_capacity) * 100 if pool_capacity > 0 else 0
            
            # 任务池健康状态
            if saturation_pct < 30:
                health_status = "健康 💚"
            elif saturation_pct < 70:
                health_status = "良好 💛"
            else:
                health_status = "忙碌 ❤️"
            
            # 性能统计
            avg_time = sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0
            current_qps = self.get_current_qps()
            # 【修复3】 安全处理 None 值
            qps_str = f"QPS:{current_qps:.2f}" if current_qps is not None else "QPS:计算中..."
            perf_str = f"性能:{avg_time:.0f}ms/轮, {qps_str}, +{self.nodes_added}节点+{self.edges_added}边"
            
            print(f"📋 [状态] 图谱:{insights['total_nodes']}节点, {insights['total_edges']}边, 任务池:{pool_size}/{pool_capacity}个 ({saturation_pct:.0f}%, {health_status}) | {perf_str} | 待执行: {preview_str}", flush=True)
    
    def self_repair(self):
        """存续公理：故障自愈"""
        # 优先使用Config类，保持向后兼容
        loop_sleep = getattr(Config, 'LOOP_SLEEP', LOOP_SLEEP)
        time.sleep(loop_sleep * 2)
        
        if len(TASK_POOL) == 0:
            auto_tasks = self.kg.generate_autonomous_tasks()
            for task in auto_tasks:
                TASK_POOL.append(task)
            print(f"✅ [自修复完成] 已恢复 {len(auto_tasks)} 个任务到任务池")
    
    def get_task(self):
        """获取运行任务（支持优先级）"""
        if not TASK_POOL:
            return None
        
        # 【阶段19】简单的优先级系统
        # 优先级：高优先级任务 > 普通任务 > 迭代任务
        high_priority = []
        normal = []
        low_priority = []
        
        for task in TASK_POOL:
            if any(prefix in task for prefix in ["🎯", "🔨", "✅"]):
                high_priority.append(task)
            elif task.startswith("迭代_"):
                low_priority.append(task)
            else:
                normal.append(task)
        
        # 按优先级选择任务
        if high_priority:
            selected = high_priority[0]
        elif normal:
            selected = normal[0]
        else:
            selected = low_priority[0] if low_priority else TASK_POOL[0]
        
        TASK_POOL.remove(selected)
        return selected
    
    def idle_evolve(self):
        """自驱公理：无任务时自主进化"""
        # 优先使用Config类，保持向后兼容
        loop_sleep = getattr(Config, 'LOOP_SLEEP', LOOP_SLEEP)
        
        auto_tasks = self.kg.generate_autonomous_tasks()
        for task in auto_tasks:
            TASK_POOL.append(task)
        
        # 获取进度指示符号
        progress_symbol = self.progress_symbols[self.run_count % len(self.progress_symbols)]
        
        insights = self.kg.get_insights()
        print(f"  {progress_symbol} [空闲进化] 图谱含{insights['total_nodes']}实体 {insights['total_edges']}关联 | 生成{len(auto_tasks)}个自主任务")
        
        time.sleep(loop_sleep)
    
    def execute(self, task):
        """核心闭环：任务→沉淀知识→生成新任务（记忆+自驱公理）"""
        # 优先使用Config类，保持向后兼容
        max_execution_depth = getattr(Config, 'MAX_EXECUTION_DEPTH', MAX_EXECUTION_DEPTH)
        
        start_time = time.time()
        
        # 获取进度指示符号
        progress_symbol = self.progress_symbols[self.run_count % len(self.progress_symbols)]
        
        # 记录执行前的图谱状态
        before_nodes = len(self.kg.graph["nodes"])
        before_edges = len(self.kg.graph["edges"])
        
        # 显示友好的执行日志
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {progress_symbol} 执行 #{self.run_count}: {task}", flush=True)
        
        # 显示执行阶段进度条
        print(f"  {'─' * 55}", flush=True)
        print(f"  ⚙️  阶段 1/4: 语义萃取  {'░' * 30}  ⏳", flush=True)
        
        self.execution_context.append({
            "task": task,
            "time": start_time,
            "depth": self.run_count % max_execution_depth
        })
        
        # 第1步：调用LLM进行语义萃取（可选，非阻塞）
        semantic_entities = []
        semantic_relations = []
        if self.llm.enabled:
            try:
                task_text = f"任务主题：{task}。这是一个关于知识图谱构建和智能演进的任务。"
                entities, relations = self.llm.extract_knowledge(task_text)
                if entities:
                    semantic_entities = entities
                    semantic_relations = relations
                    print(f"  ✅ 阶段 1/4: 语义萃取  {'█' * 30}  完成", flush=True)
            except Exception as e:
                print(f"  ⚠️  阶段 1/4: 语义萃取  {'░' * 30}  跳过", flush=True)
        else:
            print(f"  ⏭️  阶段 1/4: 语义萃取  {'─' * 30}  禁用", flush=True)
        
        # 第2步：沉淀知识到图谱
        self.kg.add_node(task, {"type": "task"})
        
        # 沉淀LLM提取的语义知识
        for entity in semantic_entities:
            self.kg.add_node(entity, {"type": "semantic"})
            self.kg.add_edge(task, entity, "包含实体", weight=0.7)
        
        for rel in semantic_relations:
            try:
                src = rel.get("source")
                tgt = rel.get("target")
                # 给关系中的节点也标注类型
                self.kg.add_node(src, {"type": "concept"})
                self.kg.add_node(tgt, {"type": "concept"})
                self.kg.add_edge(
                    src,
                    tgt,
                    rel.get("type", "关联"),
                    weight=0.9
                )
            except Exception as e:
                # 【修复8】 记录异常而不是直接忽略
                print(f"  ⚠️ [语义关系处理] 跳过: {str(e)}", flush=True)
        
        print(f"  ✅ 阶段 2/4: 知识沉淀  {'█' * 30}  完成", flush=True)
        
        # 第3步：图谱关联推演
        derive_tasks = self.kg.get_relation_tasks(task)
        print(f"  ✅ 阶段 3/4: 关联推演  {'█' * 30}  完成", flush=True)
        
        # 第4步：生成衍生任务
        # 智能任务名称生成：避免过长的递归名称
        if task.startswith("迭代_"):
            # 如果已经是迭代任务，只保留层数信息
            follow_task = f"迭代_{self.run_count}"
        else:
            # 正常生成迭代任务
            clean_task = task.replace("推演:", "").replace("迭代_", "")
            follow_task = f"迭代_{self.run_count}_{clean_task[:15]}"
        
        self.kg.add_edge(task, follow_task, "自主衍生", weight=0.8)
        
        # 避免重复任务：检查是否已存在于池中
        current_pool = set(TASK_POOL)
        
        if derive_tasks:
            for related in derive_tasks[:3]:
                self.kg.add_edge(task, related, "知识推演", weight=0.6)
                if related not in current_pool:
                    TASK_POOL.append(related)
        
        if follow_task not in current_pool:
            TASK_POOL.append(follow_task)
        
        print(f"  ✅ 阶段 4/4: 任务生成  {'█' * 30}  完成", flush=True)
        print(f"  {'─' * 55}", flush=True)
        
        # 更新统计
        self.kg.graph["metadata"]["total_tasks"] += 1
        self.success_tasks.append(task)
        self.task_total += 1
        self.task_success += 1
        
        # 计算耗时
        exec_time = (time.time() - start_time) * 1000
        
        # 显示执行后的变化
        after_nodes = len(self.kg.graph["nodes"])
        after_edges = len(self.kg.graph["edges"])
        nodes_diff = after_nodes - before_nodes
        edges_diff = after_edges - before_edges
        
        # 更新性能统计
        self.execution_times.append(exec_time)
        self.nodes_added += nodes_diff
        self.edges_added += edges_diff
        
        # 【阶段18】记录性能监控数据
        self.perf_monitor.record_execution(exec_time, success=True)
        
        # 显示总体进度和统计
        print(f"  ✅ 任务完成! +{nodes_diff}节点, +{edges_diff}边, 任务池:{len(TASK_POOL)}, 耗时:{exec_time:.0f}ms", flush=True)
    
    def _show_welcome_animation(self):
        """显示启动欢迎动画"""
        animation_symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        welcome_lines = [
            "正在唤醒Agent...",
            "加载知识图谱...",
            "初始化认知引擎...",
            "启动完成！"
        ]
        for i, line in enumerate(welcome_lines):
            if i < len(welcome_lines) - 1:
                for symbol in animation_symbols[:4]:
                    print(f"\r  {symbol} {line}", end="", flush=True)
                    time.sleep(0.1)
                print(f"\r  ✅ {line}", flush=True)
            else:
                print(f"\r  🚀 {line}", flush=True)
            time.sleep(0.2)
        print()
    
    def eternal_loop(self):
        """绝对永动主循环（存续公理终极实现）"""
        # 优先使用Config类，保持向后兼容
        loop_sleep = getattr(Config, 'LOOP_SLEEP', LOOP_SLEEP)
        
        # 启动信息展示
        self._show_welcome_animation()
        insights = self.kg.get_insights()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 【阶段25】使用i18n显示欢迎信息
        welcome_msg = self.i18n.get("welcome", "第一性原理 · 永动知识图谱Agent 启动")
        
        print("\n" + "╔" + "═" * 58 + "╗", flush=True)
        print(f"║  🚀 {welcome_msg:<47} ║", flush=True)
        print("╠" + "═" * 58 + "╣", flush=True)
        print("║  版本: 2.4.0  |  启动时间: " + current_time, flush=True)
        print("╠" + "─" * 58 + "╣", flush=True)
        print("║  三大公理：存续 | 记忆 | 自驱", flush=True)
        
        # 显示快速测试模式信息
        if self.quick_test_rounds is not None:
            print("╠" + "─" * 58 + "╣", flush=True)
            print(f"║  🧪 快速测试模式: 将运行 {self.quick_test_rounds} 轮后自动退出", flush=True)
        
        print("╠" + "─" * 58 + "╣", flush=True)
        print(f"║  📊 初始状态: {insights['total_nodes']} 节点, {insights['total_edges']} 边", flush=True)
        print(f"║  📋 节点类型: {insights.get('node_types', {})}", flush=True)
        print(f"║  📝 总任务数: {self.kg.graph['metadata']['total_tasks']}", flush=True)
        print("╠" + "─" * 58 + "╣", flush=True)
        print("║  💡 提示: 按 Ctrl+C 优雅退出", flush=True)
        print("╚" + "═" * 58 + "╝", flush=True)
        
        while self.alive:
            try:
                # 快速测试模式检查
                if self.quick_test_rounds is not None and self.run_count >= self.quick_test_rounds:
                    print(f"\n🧪 快速测试完成: 已运行 {self.run_count} 轮", flush=True)
                    self.shutdown()
                    break
                
                self.health_check()
                task = self.get_task()
                
                if not task:
                    self.idle_evolve()
                    continue
                
                self.execute(task)
                time.sleep(loop_sleep)
                
            except KeyboardInterrupt:
                print("\n[存续] 收到终止信号，执行优雅退出")
                self.shutdown()
                break
            except Exception as e:
                print("\n" + "╔" + "═" * 58 + "╗", flush=True)
                print(f"║  ⚠️ [异常捕获] {type(e).__name__}", flush=True)
                print("╠" + "─" * 58 + "╣", flush=True)
                print(f"║  错误信息: {str(e)}", flush=True)
                print("╠" + "─" * 58 + "╣", flush=True)
                print("║  正在执行故障自修复...", flush=True)
                print("╚" + "═" * 58 + "╝", flush=True)
                
                self.failed_tasks.append({"task": "unknown", "error": str(e), "time": time.time()})
                self.task_total += 1
                self.task_failed += 1
                # 【阶段18】记录错误到性能监控
                self.perf_monitor.record_execution(0, success=False)
                # 仅在调试时打印完整堆栈
                # traceback.print_exc()
                self.self_repair()
    
    def shutdown(self):
        """优雅关闭"""
        self.kg.save(force=True)
        insights = self.kg.get_insights()
        uptime = time.time() - self.start_time
        uptime_str = format_duration(uptime)
        
        # 计算性能统计
        avg_exec_time_ms = sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0
        
        # 【阶段25】使用i18n显示关闭信息
        shutdown_msg = self.i18n.get("shutdown", "系统正常退出")
        
        print("\n" + "╔" + "═" * 58 + "╗", flush=True)
        print(f"║  👋 {shutdown_msg}  |  总运行 {self.run_count} 轮  |  存活 {uptime_str}  ║", flush=True)
        print("╠" + "═" * 58 + "╣", flush=True)
        
        # 执行统计
        success_rate = (self.task_success / self.task_total * 100) if self.task_total > 0 else 0
        print("║  📊 执行统计", flush=True)
        print(f"║    ├─ 总任务: {self.task_total}", flush=True)
        print(f"║    ├─ 成功: {self.task_success}  ✅", flush=True)
        print(f"║    ├─ 失败: {self.task_failed}  ❌", flush=True)
        print(f"║    └─ 成功率: {success_rate:.1f}%", flush=True)
        print("╠" + "─" * 58 + "╣", flush=True)
        
        # 【阶段18】显示性能监控报告
        print(self.perf_monitor.get_performance_report())
        
        # 性能摘要
        print("║  ⚡ 性能摘要", flush=True)
        print(f"║    ├─ 平均执行时间: {avg_exec_time_ms:.1f}ms", flush=True)
        print(f"║    ├─ 新增节点: +{self.nodes_added}", flush=True)
        print(f"║    └─ 新增边: +{self.edges_added}", flush=True)
        print("╠" + "─" * 58 + "╣", flush=True)
        
        # 图谱状态
        print("║  📈 图谱状态", flush=True)
        print(f"║    ├─ 节点: {insights['total_nodes']} 个, 类型分布: {insights.get('node_types', {})}", flush=True)
        print(f"║    ├─ 边: {insights['total_edges']} 条, 平均权重: {insights['avg_weight']:.2f}", flush=True)
        print(f"║    └─ 总任务数: {self.kg.graph['metadata']['total_tasks']}", flush=True)
        print("╠" + "─" * 58 + "╣", flush=True)
        
        # 最高权重关系
        if insights.get('top_relations'):
            print("║  ⭐ 最高权重关系", flush=True)
            for i, (src, rel, tgt, weight) in enumerate(insights['top_relations'][:3]):
                bar_len = int(weight * 20)
                bar = "█" * bar_len + "░" * (20 - bar_len)
                print(f"║    {i+1}. {bar} {src} --[{rel}]--> {tgt} ({weight:.2f})", flush=True)
            print("╠" + "─" * 58 + "╣", flush=True)
        
        # 热节点展示
        if insights.get('hot_nodes'):
            print("║  🔥 热门节点（访问次数）", flush=True)
            for i, (name, count) in enumerate(insights['hot_nodes'][:5]):
                print(f"║    {i+1}. {name}: {count} 次", flush=True)
            print("╠" + "─" * 58 + "╣", flush=True)
        
        # 运行配置 - 优先使用Config类，保持向后兼容
        llm_enabled = getattr(Config, 'LLM_ENABLED', LLM_ENABLED)
        llm_demo_mode = getattr(Config, 'LLM_DEMO_MODE', LLM_DEMO_MODE)
        loop_sleep = getattr(Config, 'LOOP_SLEEP', LOOP_SLEEP)
        evolve_cycle = getattr(Config, 'EVOLVE_CYCLE', EVOLVE_CYCLE)
        kg_path = getattr(Config, 'KG_PATH', KG_PATH)
        
        print("║  ⚙️ 运行配置", flush=True)
        print(f"║    ├─ LLM 启用: {'是' if llm_enabled else '否'}", flush=True)
        print(f"║    ├─ LLM 演示: {'是' if llm_demo_mode else '否'}", flush=True)
        print(f"║    ├─ 循环间隔: {loop_sleep}s", flush=True)
        print(f"║    └─ 进化周期: {evolve_cycle}轮", flush=True)
        print("╠" + "─" * 58 + "╣", flush=True)
        
        print("║  💾 知识图谱已保存至 " + kg_path, flush=True)
        print("╚" + "═" * 58 + "╝", flush=True)


# ====================== 阶段31-50：基础设施类 ======================

class Cache:
    """【阶段31】缓存系统：支持TTL过期和LRU淘汰"""

    def __init__(self, max_size=100, default_ttl=None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._data = OrderedDict()
        self._expires = {}
        self._access_count = 0
        self._hit_count = 0
        self._miss_count = 0

    def _is_expired(self, key):
        if key not in self._expires:
            return False
        exp = self._expires[key]
        if exp is None:
            return False
        return time.time() > exp

    def _cleanup_expired(self):
        now = time.time()
        expired_keys = [k for k, v in self._expires.items() if v is not None and now > v]
        for k in expired_keys:
            self._remove(k)

    def _remove(self, key):
        if key in self._data:
            del self._data[key]
        if key in self._expires:
            del self._expires[key]

    def _evict_lru(self):
        if self._data:
            oldest = next(iter(self._data))
            self._remove(oldest)

    def get(self, key, default=None):
        self._access_count += 1
        if key in self._data and not self._is_expired(key):
            self._hit_count += 1
            self._data.move_to_end(key)
            return self._data[key]
        if key in self._data and self._is_expired(key):
            self._remove(key)
        self._miss_count += 1
        return default

    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.default_ttl
        if key in self._data:
            self._data.move_to_end(key)
        else:
            if len(self._data) >= self.max_size:
                self._evict_lru()
        self._data[key] = value
        self._expires[key] = time.time() + ttl if ttl else None

    def delete(self, key):
        if key in self._data:
            self._remove(key)
            return True
        return False

    def clear(self):
        self._data.clear()
        self._expires.clear()

    def keys(self):
        self._cleanup_expired()
        return list(self._data.keys())

    def values(self):
        self._cleanup_expired()
        return list(self._data.values())

    def items(self):
        self._cleanup_expired()
        return list(self._data.items())

    def size(self):
        self._cleanup_expired()
        return len(self._data)

    def stats(self):
        total = self._hit_count + self._miss_count
        hit_rate = (self._hit_count / total * 100) if total > 0 else 0
        return {
            "size": self.size(),
            "max_size": self.max_size,
            "access_count": self._access_count,
            "hit_count": self._hit_count,
            "miss_count": self._miss_count,
            "hit_rate": round(hit_rate, 2)
        }


class RateLimiter:
    """【阶段32】限流器：基于令牌桶算法"""

    def __init__(self, rate=10, capacity=10, strategy="token_bucket"):
        self.rate = rate
        self.capacity = capacity
        self.strategy = strategy
        self.tokens = capacity
        self.last_update = time.time()
        self._lock = threading.Lock()
        self._request_count = 0
        self._reject_count = 0

    def _add_tokens(self):
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

    def allow(self, tokens=1):
        with self._lock:
            self._request_count += 1
            if self.strategy == "token_bucket":
                self._add_tokens()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True
                self._reject_count += 1
                return False
            elif self.strategy == "fixed_window":
                now = time.time()
                window = int(now)
                if not hasattr(self, '_window_start') or self._window_start != window:
                    self._window_start = window
                    self._window_count = 0
                if self._window_count < self.capacity:
                    self._window_count += tokens
                    return True
                self._reject_count += 1
                return False
            elif self.strategy == "sliding_window":
                now = time.time()
                if not hasattr(self, '_window_requests'):
                    self._window_requests = []
                window = 1.0
                self._window_requests = [t for t in self._window_requests if now - t < window]
                if len(self._window_requests) < self.capacity:
                    self._window_requests.extend([now] * tokens)
                    return True
                self._reject_count += 1
                return False
            else:
                return True

    def get_stats(self):
        return {
            "rate": self.rate,
            "capacity": self.capacity,
            "strategy": self.strategy,
            "tokens": self.tokens,
            "requests": self._request_count,
            "rejected": self._reject_count
        }


class Serializer:
    """【阶段33】序列化器：支持JSON和自定义序列化"""

    def __init__(self, format_type="json"):
        self.format_type = format_type
        self.custom_rules = {}

    def serialize(self, obj):
        if self.format_type == "json":
            return json.dumps(obj, ensure_ascii=False, default=self._default_encoder)
        elif self.format_type == "bytes":
            return str(obj).encode("utf-8")
        else:
            return str(obj)

    def deserialize(self, data):
        if self.format_type == "json":
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            return json.loads(data)
        elif self.format_type == "bytes":
            if isinstance(data, bytes):
                return data.decode("utf-8")
            return data
        else:
            return data

    def _default_encoder(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, deque):
            return list(obj)
        raise TypeError(f"不可序列化类型: {type(obj)}")

    def add_custom_rule(self, type_name, encoder, decoder):
        self.custom_rules[type_name] = {"encoder": encoder, "decoder": decoder}

    def save_to_file(self, obj, filepath):
        data = self.serialize(obj)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(data)
        return True

    def load_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()
        return self.deserialize(data)


class Compressor:
    """【阶段34】压缩器：支持gzip和bzip2"""

    def __init__(self, method="gzip", threshold=1024):
        self.method = method
        self.threshold = threshold

    def compress(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        if len(data) < self.threshold:
            return data
        if self.method == "gzip":
            return gzip.compress(data)
        elif self.method == "bzip2":
            return bz2.compress(data)
        return data

    def decompress(self, data):
        if self.method == "gzip":
            try:
                return gzip.decompress(data)
            except Exception:
                return data
        elif self.method == "bzip2":
            try:
                return bz2.decompress(data)
            except Exception:
                return data
        return data

    def compress_file(self, src_path, dst_path=None):
        if dst_path is None:
            dst_path = src_path + ".gz" if self.method == "gzip" else src_path + ".bz2"
        with open(src_path, "rb") as f:
            data = f.read()
        compressed = self.compress(data)
        with open(dst_path, "wb") as f:
            f.write(compressed)
        return dst_path

    def decompress_file(self, src_path, dst_path=None):
        if dst_path is None:
            dst_path = src_path.replace(".gz", "").replace(".bz2", "")
        with open(src_path, "rb") as f:
            data = f.read()
        decompressed = self.decompress(data)
        with open(dst_path, "wb") as f:
            f.write(decompressed)
        return dst_path


class Encryptor:
    """【阶段35】加密器：支持简单XOR加密（纯Python，无外部依赖）"""

    def __init__(self, key=None):
        self.key = key or self._generate_key()

    def _generate_key(self, length=32):
        chars = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.SystemRandom().choice(chars) for _ in range(length))

    def _derive_key(self, text_key, length=32):
        h = hashlib.sha256(text_key.encode("utf-8")).digest()
        return h[:length]

    def encrypt(self, data, key=None):
        if key is None:
            key = self.key
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(key, str):
            key = self._derive_key(key)
        encrypted = bytearray()
        for i, b in enumerate(data):
            encrypted.append(b ^ key[i % len(key)])
        return bytes(encrypted)

    def decrypt(self, data, key=None):
        return self.encrypt(data, key)

    def encrypt_file(self, src_path, dst_path=None, key=None):
        if dst_path is None:
            dst_path = src_path + ".enc"
        with open(src_path, "rb") as f:
            data = f.read()
        encrypted = self.encrypt(data, key)
        with open(dst_path, "wb") as f:
            f.write(encrypted)
        return dst_path

    def decrypt_file(self, src_path, dst_path=None, key=None):
        if dst_path is None:
            dst_path = src_path.replace(".enc", ".dec")
        with open(src_path, "rb") as f:
            data = f.read()
        decrypted = self.decrypt(data, key)
        with open(dst_path, "wb") as f:
            f.write(decrypted)
        return dst_path


class Hasher:
    """【阶段36】哈希器：支持多种哈希算法和数据完整性校验"""

    ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]

    def __init__(self, algorithm="sha256"):
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"不支持的算法: {algorithm}")
        self.algorithm = algorithm

    def hash(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        hasher = hashlib.new(self.algorithm)
        hasher.update(data)
        return hasher.hexdigest()

    def hash_file(self, filepath):
        hasher = hashlib.new(self.algorithm)
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()

    def verify(self, data, expected_hash):
        return self.hash(data) == expected_hash

    def verify_file(self, filepath, expected_hash):
        return self.hash_file(filepath) == expected_hash

    def checksum(self, data, algorithm=None):
        old = self.algorithm
        if algorithm:
            self.algorithm = algorithm
        result = self.hash(data)
        self.algorithm = old
        return result


class SecureRandom:
    """【阶段37】安全随机数生成器：密码学安全的随机数"""

    def __init__(self):
        self._rng = random.SystemRandom()

    def random(self):
        return self._rng.random()

    def randint(self, a, b):
        return self._rng.randint(a, b)

    def choice(self, seq):
        return self._rng.choice(seq)

    def choices(self, seq, k=1):
        return self._rng.choices(seq, k=k)

    def shuffle(self, seq):
        self._rng.shuffle(seq)
        return seq

    def uniform(self, a, b):
        return self._rng.uniform(a, b)

    def gauss(self, mu=0, sigma=1):
        return self._rng.gauss(mu, sigma)

    def bytes(self, n):
        return os.urandom(n)

    def hex(self, n):
        return os.urandom(n).hex()

    def token(self, length=32):
        alphabet = string.ascii_letters + string.digits
        return "".join(self._rng.choice(alphabet) for _ in range(length))


class UUIDGenerator:
    """【阶段38】UUID生成器：支持多种UUID版本"""

    @staticmethod
    def v1():
        return str(uuid.uuid1())

    @staticmethod
    def v4():
        return str(uuid.uuid4())

    @staticmethod
    def v5(namespace, name):
        if isinstance(namespace, str):
            namespace = uuid.UUID(namespace)
        return str(uuid.uuid5(namespace, name))

    @staticmethod
    def custom_namespace(name):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

    @staticmethod
    def is_valid(uuid_str):
        try:
            uuid.UUID(uuid_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse(uuid_str):
        try:
            return str(uuid.UUID(uuid_str))
        except ValueError:
            return None


class TimeUtils:
    """【阶段39】时间工具：格式化、时区、定时器"""

    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def now_utc():
        return datetime.now(timezone.utc)

    @staticmethod
    def format(dt, fmt="%Y-%m-%d %H:%M:%S"):
        return dt.strftime(fmt)

    @staticmethod
    def parse(time_str, fmt="%Y-%m-%d %H:%M:%S"):
        return datetime.strptime(time_str, fmt)

    @staticmethod
    def timestamp():
        return time.time()

    @staticmethod
    def timestamp_ms():
        return int(time.time() * 1000)

    @staticmethod
    def to_utc(dt):
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @staticmethod
    def add_seconds(dt, seconds):
        return dt + timedelta(seconds=seconds)

    @staticmethod
    def add_days(dt, days):
        return dt + timedelta(days=days)

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)

    @staticmethod
    def timer(name="timer"):
        return {"name": name, "start": time.time()}

    @staticmethod
    def timer_elapsed(t):
        return time.time() - t["start"]

    @staticmethod
    def isoformat(dt=None):
        if dt is None:
            dt = datetime.now()
        return dt.isoformat()


class StringUtils:
    """【阶段40】字符串工具：处理、正则、文本分析"""

    @staticmethod
    def is_empty(s):
        return s is None or len(s.strip()) == 0

    @staticmethod
    def is_not_empty(s):
        return not StringUtils.is_empty(s)

    @staticmethod
    def trim(s):
        return s.strip() if s else s

    @staticmethod
    def truncate(s, max_len, suffix="..."):
        if s and len(s) > max_len:
            return s[:max_len - len(suffix)] + suffix
        return s

    @staticmethod
    def contains(s, sub):
        return sub in s if s else False

    @staticmethod
    def starts_with(s, prefix):
        return s.startswith(prefix) if s else False

    @staticmethod
    def ends_with(s, suffix):
        return s.endswith(suffix) if s else False

    @staticmethod
    def split(s, delimiter=","):
        return [x.strip() for x in s.split(delimiter)] if s else []

    @staticmethod
    def join(seq, delimiter=","):
        return delimiter.join(str(x) for x in seq)

    @staticmethod
    def to_camel_case(s):
        parts = re.split(r"[_\-]", s)
        return parts[0] + "".join(x.title() for x in parts[1:])

    @staticmethod
    def to_snake_case(s):
        s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()

    @staticmethod
    def match(pattern, s):
        return re.match(pattern, s)

    @staticmethod
    def find_all(pattern, s):
        return re.findall(pattern, s)

    @staticmethod
    def replace_all(pattern, repl, s):
        return re.sub(pattern, repl, s)

    @staticmethod
    def word_count(s):
        return len(s.split()) if s else 0

    @staticmethod
    def char_count(s, char):
        return s.count(char) if s else 0


class MathUtils:
    """【阶段41】数学工具：统计、概率、数值优化"""

    @staticmethod
    def mean(data):
        return statistics.mean(data) if data else 0

    @staticmethod
    def median(data):
        return statistics.median(data) if data else 0

    @staticmethod
    def stdev(data):
        return statistics.stdev(data) if len(data) > 1 else 0

    @staticmethod
    def variance(data):
        return statistics.variance(data) if len(data) > 1 else 0

    @staticmethod
    def max(data):
        return max(data) if data else 0

    @staticmethod
    def min(data):
        return min(data) if data else 0

    @staticmethod
    def sum(data):
        return sum(data) if data else 0

    @staticmethod
    def normalize(data):
        if not data:
            return []
        min_val = min(data)
        max_val = max(data)
        rng = max_val - min_val
        if rng == 0:
            return [0.0] * len(data)
        return [(x - min_val) / rng for x in data]

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(max_val, value))

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * MathUtils.clamp(t, 0, 1)

    @staticmethod
    def sigmoid(x):
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    @staticmethod
    def softmax(values):
        if not values:
            return []
        max_val = max(values)
        exp_vals = [math.exp(v - max_val) for v in values]
        sum_exp = sum(exp_vals)
        return [v / sum_exp for v in exp_vals]

    @staticmethod
    def entropy(probs):
        if not probs:
            return 0
        return -sum(p * math.log2(p) for p in probs if p > 0)


class CollectionUtils:
    """【阶段42】集合工具：集合操作、排序、搜索"""

    @staticmethod
    def unique(seq):
        seen = set()
        result = []
        for item in seq:
            key = item
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    @staticmethod
    def flatten(seq):
        result = []
        for item in seq:
            if isinstance(item, (list, tuple)):
                result.extend(CollectionUtils.flatten(item))
            else:
                result.append(item)
        return result

    @staticmethod
    def chunk(seq, size):
        return [seq[i:i + size] for i in range(0, len(seq), size)]

    @staticmethod
    def group_by(seq, key_func):
        groups = {}
        for item in seq:
            key = key_func(item)
            groups.setdefault(key, []).append(item)
        return groups

    @staticmethod
    def sort_by(seq, key_func, reverse=False):
        return sorted(seq, key=key_func, reverse=reverse)

    @staticmethod
    def top_n(seq, n, key_func=None):
        if key_func:
            return sorted(seq, key=key_func, reverse=True)[:n]
        return sorted(seq, reverse=True)[:n]

    @staticmethod
    def binary_search(seq, target, key_func=None):
        arr = sorted(seq, key=key_func) if key_func else sorted(seq)
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_val = key_func(arr[mid]) if key_func else arr[mid]
            if mid_val == target:
                return mid
            elif mid_val < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    @staticmethod
    def filter_by(seq, predicate):
        return [x for x in seq if predicate(x)]

    @staticmethod
    def map_to(seq, mapper):
        return [mapper(x) for x in seq]


class FileUtils:
    """【阶段43】文件工具：文件操作、目录遍历、监控"""

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)

    @staticmethod
    def size(path):
        return os.path.getsize(path) if os.path.exists(path) else 0

    @staticmethod
    def read(path, mode="r", encoding="utf-8"):
        if "b" in mode:
            with open(path, mode) as f:
                return f.read()
        with open(path, mode, encoding=encoding) as f:
            return f.read()

    @staticmethod
    def write(path, data, mode="w", encoding="utf-8"):
        if "b" in mode:
            with open(path, mode) as f:
                f.write(data)
        else:
            with open(path, mode, encoding=encoding) as f:
                f.write(data)
        return True

    @staticmethod
    def ensure_dir(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            return True
        return False

    @staticmethod
    def list_files(path, pattern="*"):
        if not os.path.isdir(path):
            return []
        return [os.path.join(path, f) for f in os.listdir(path) if fnmatch.fnmatch(f, pattern)]

    @staticmethod
    def walk(path):
        result = []
        for root, dirs, files in os.walk(path):
            for f in files:
                result.append(os.path.join(root, f))
        return result

    @staticmethod
    def copy(src, dst):
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        elif os.path.isdir(src):
            shutil.copytree(src, dst)
        return True

    @staticmethod
    def move(src, dst):
        shutil.move(src, dst)
        return True

    @staticmethod
    def remove(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        return True

    @staticmethod
    def get_mtime(path):
        return os.path.getmtime(path) if os.path.exists(path) else 0


class NetworkUtils:
    """【阶段44】网络工具：HTTP请求、URL解析、网络检测"""

    @staticmethod
    def http_get(url, timeout=10, headers=None):
        req = urllib.request.Request(url, method="GET")
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "body": resp.read().decode("utf-8", errors="replace")}

    @staticmethod
    def http_post(url, data, timeout=10, headers=None):
        if isinstance(data, dict):
            data = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            data = data.encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "body": resp.read().decode("utf-8", errors="replace")}

    @staticmethod
    def parse_url(url):
        parsed = urlparse(url)
        return {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": parse_qs(parsed.query),
            "fragment": parsed.fragment
        }

    @staticmethod
    def build_url(base, params):
        query = urlencode(params, doseq=True)
        return f"{base}?{query}" if query else base

    @staticmethod
    def is_port_open(host, port, timeout=2):
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except Exception:
            return False

    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"


class ProcessUtils:
    """【阶段45】进程工具：进程管理、资源监控、信号处理"""

    @staticmethod
    def run(cmd, shell=False, timeout=30):
        try:
            result = subprocess.run(
                cmd if shell else cmd.split(),
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"returncode": -1, "stdout": "", "stderr": "timeout"}
        except Exception as e:
            return {"returncode": -1, "stdout": "", "stderr": str(e)}

    @staticmethod
    def run_async(cmd, shell=False):
        return subprocess.Popen(
            cmd if shell else cmd.split(),
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    @staticmethod
    def get_pid():
        return os.getpid()

    @staticmethod
    def get_ppid():
        return os.getppid()

    @staticmethod
    def kill(pid, sig=9):
        try:
            os.kill(pid, sig)
            return True
        except Exception:
            return False

    @staticmethod
    def cpu_count():
        return os.cpu_count() or 1

    @staticmethod
    def get_env(key, default=None):
        return os.environ.get(key, default)

    @staticmethod
    def set_env(key, value):
        os.environ[key] = value
        return True


class ThreadUtils:
    """【阶段46】线程工具：线程池、并发控制、异步执行"""

    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self._threads = []
        self._results = {}
        self._counter = 0
        self._lock = threading.Lock()

    def submit(self, func, *args, **kwargs):
        def wrapper():
            tid = threading.current_thread().name
            try:
                result = func(*args, **kwargs)
                with self._lock:
                    self._results[tid] = {"success": True, "result": result}
            except Exception as e:
                with self._lock:
                    self._results[tid] = {"success": False, "error": str(e)}

        with self._lock:
            self._counter += 1
        t = threading.Thread(target=wrapper, name=f"worker_{self._counter}")
        t.start()
        self._threads.append(t)
        return t.name

    def map(self, func, iterable):
        threads = []
        for item in iterable:
            t = threading.Thread(target=lambda x: func(x), args=(item,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return True

    def wait_all(self, timeout=None):
        for t in self._threads:
            t.join(timeout=timeout)
        self._threads.clear()
        return True

    def active_count(self):
        return sum(1 for t in self._threads if t.is_alive())

    def get_results(self):
        with self._lock:
            return dict(self._results)

    def clear_results(self):
        with self._lock:
            self._results.clear()

    @staticmethod
    def current_thread_name():
        return threading.current_thread().name

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)

    @staticmethod
    def lock():
        return threading.Lock()


class DatabaseInterface:
    """【阶段47】数据库接口：SQLite支持、连接池、CRUD操作"""

    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self._local = threading.local()
        self._pool = []
        self._pool_size = 5
        self._pool_lock = threading.Lock()
        self._init_pool()

    def _init_pool(self):
        for _ in range(self._pool_size):
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._pool.append(conn)

    def _get_conn(self):
        if hasattr(self._local, "conn") and self._local.conn:
            return self._local.conn
        with self._pool_lock:
            if self._pool:
                conn = self._pool.pop()
                self._local.conn = conn
                return conn
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _release_conn(self, conn):
        with self._pool_lock:
            if len(self._pool) < self._pool_size:
                self._pool.append(conn)

    def execute(self, sql, params=()):
        conn = self._get_conn()
        try:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self._release_conn(conn)

    def fetchall(self, sql, params=()):
        cursor = self.execute(sql, params)
        return cursor.fetchall()

    def fetchone(self, sql, params=()):
        cursor = self.execute(sql, params)
        return cursor.fetchone()

    def create_table(self, table_name, columns):
        cols = ", ".join(f"{name} {dtype}" for name, dtype in columns.items())
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"
        self.execute(sql)
        return True

    def insert(self, table_name, data):
        keys = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"
        self.execute(sql, tuple(data.values()))
        return True

    def select(self, table_name, where=None, params=()):
        sql = f"SELECT * FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        return self.fetchall(sql, params)

    def update(self, table_name, data, where, params=()):
        sets = ", ".join(f"{k}=?" for k in data)
        sql = f"UPDATE {table_name} SET {sets} WHERE {where}"
        self.execute(sql, tuple(data.values()) + params)
        return True

    def delete(self, table_name, where, params=()):
        sql = f"DELETE FROM {table_name} WHERE {where}"
        self.execute(sql, params)
        return True

    def close(self):
        with self._pool_lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()


class MessageQueue:
    """【阶段48】消息队列：内存队列、持久化队列、发布订阅"""

    def __init__(self, max_size=1000, persistent_path=None):
        self.max_size = max_size
        self.persistent_path = persistent_path
        self._queues = {}
        self._subscribers = {}
        self._lock = threading.Lock()
        if persistent_path:
            self._load_persistent()

    def _load_persistent(self):
        if os.path.exists(self.persistent_path):
            try:
                with open(self.persistent_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._queues = {k: deque(v, maxlen=self.max_size) for k, v in data.items()}
            except Exception:
                self._queues = {}

    def _save_persistent(self):
        if self.persistent_path:
            try:
                data = {k: list(v) for k, v in self._queues.items()}
                with open(self.persistent_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
            except Exception:
                pass

    def publish(self, queue_name, message):
        with self._lock:
            if queue_name not in self._queues:
                self._queues[queue_name] = deque(maxlen=self.max_size)
            self._queues[queue_name].append(message)
            subs = list(self._subscribers.get(queue_name, []))
        for sub in subs:
            try:
                sub(message)
            except Exception:
                pass
        self._save_persistent()
        return True

    def subscribe(self, queue_name, callback):
        with self._lock:
            if queue_name not in self._subscribers:
                self._subscribers[queue_name] = []
            self._subscribers[queue_name].append(callback)
        return True

    def consume(self, queue_name, block=False, timeout=None):
        with self._lock:
            q = self._queues.get(queue_name, deque())
            if q:
                return q.popleft()
        return None

    def queue_size(self, queue_name):
        with self._lock:
            return len(self._queues.get(queue_name, deque()))

    def list_queues(self):
        with self._lock:
            return list(self._queues.keys())

    def clear_queue(self, queue_name):
        with self._lock:
            if queue_name in self._queues:
                self._queues[queue_name].clear()
        self._save_persistent()
        return True


class CacheStrategy:
    """【阶段49】缓存策略：多种淘汰策略、预热、统计"""

    STRATEGIES = ["lru", "lfu", "fifo", "random"]

    def __init__(self, max_size=100, strategy="lru"):
        if strategy not in self.STRATEGIES:
            raise ValueError(f"不支持的策略: {strategy}")
        self.max_size = max_size
        self.strategy = strategy
        self._data = {}
        self._meta = {}
        self._access_stats = {}
        self._insert_order = []
        self._lock = threading.Lock()

    def _evict(self):
        if not self._data:
            return
        if self.strategy == "lru":
            key = min(self._meta, key=lambda k: self._meta[k]["last_access"])
        elif self.strategy == "lfu":
            key = min(self._meta, key=lambda k: self._meta[k]["access_count"])
        elif self.strategy == "fifo":
            key = self._insert_order[0]
        elif self.strategy == "random":
            key = random.choice(list(self._data.keys()))
        else:
            return
        self._remove(key)

    def _remove(self, key):
        if key in self._data:
            del self._data[key]
        if key in self._meta:
            del self._meta[key]
        if key in self._access_stats:
            del self._access_stats[key]
        if key in self._insert_order:
            self._insert_order.remove(key)

    def get(self, key):
        with self._lock:
            if key in self._data:
                self._meta[key]["last_access"] = time.time()
                self._meta[key]["access_count"] += 1
                self._access_stats[key] = self._access_stats.get(key, 0) + 1
                return self._data[key]
            return None

    def set(self, key, value):
        with self._lock:
            if key in self._data:
                self._data[key] = value
                self._meta[key]["last_access"] = time.time()
                return True
            if len(self._data) >= self.max_size:
                self._evict()
            self._data[key] = value
            self._meta[key] = {"last_access": time.time(), "access_count": 1}
            self._insert_order.append(key)
            return True

    def delete(self, key):
        with self._lock:
            if key in self._data:
                self._remove(key)
                return True
            return False

    def clear(self):
        with self._lock:
            self._data.clear()
            self._meta.clear()
            self._access_stats.clear()
            self._insert_order.clear()

    def warm_up(self, data_dict):
        for k, v in data_dict.items():
            self.set(k, v)

    def stats(self):
        with self._lock:
            return {
                "size": len(self._data),
                "max_size": self.max_size,
                "strategy": self.strategy,
                "keys": list(self._data.keys()),
                "access_stats": dict(self._access_stats)
            }


class ConnectionPool:
    """【阶段50】连接池：资源管理、超时处理、健康检查"""

    def __init__(self, factory, max_size=10, timeout=30, health_check_interval=60):
        self.factory = factory
        self.max_size = max_size
        self.timeout = timeout
        self.health_check_interval = health_check_interval
        self._pool = deque()
        self._in_use = {}
        self._lock = threading.Lock()
        self._created = 0
        self._health_checks = 0

    def _create_connection(self):
        if self._created < self.max_size:
            conn = self.factory()
            self._created += 1
            return conn
        return None

    def _is_healthy(self, conn):
        self._health_checks += 1
        if hasattr(conn, "healthy"):
            return conn.healthy()
        return True

    def acquire(self):
        start = time.time()
        while time.time() - start < self.timeout:
            with self._lock:
                while self._pool:
                    conn = self._pool.popleft()
                    if self._is_healthy(conn):
                        self._in_use[id(conn)] = conn
                        return conn
                    self._created -= 1
                if self._created < self.max_size:
                    conn = self._create_connection()
                    if conn:
                        self._in_use[id(conn)] = conn
                        return conn
            time.sleep(0.01)
        raise TimeoutError("获取连接超时")

    def release(self, conn):
        with self._lock:
            cid = id(conn)
            if cid in self._in_use:
                del self._in_use[cid]
                self._pool.append(conn)
                return True
            return False

    def close(self, conn):
        with self._lock:
            cid = id(conn)
            if cid in self._in_use:
                del self._in_use[cid]
            self._created -= 1
        if hasattr(conn, "close"):
            conn.close()
        return True

    def close_all(self):
        with self._lock:
            all_conns = list(self._pool) + list(self._in_use.values())
            self._pool.clear()
            self._in_use.clear()
            self._created = 0
        for conn in all_conns:
            if hasattr(conn, "close"):
                conn.close()
        return True

    def stats(self):
        with self._lock:
            return {
                "max_size": self.max_size,
                "available": len(self._pool),
                "in_use": len(self._in_use),
                "created": self._created,
                "health_checks": self._health_checks
            }


# ====================== 阶段51-75：AI与算法引擎 ======================

class TemplateEngine:
    """【阶段51】模板引擎：简单变量替换、条件渲染、循环渲染"""

    def __init__(self):
        self.globals = {}

    def render(self, template, context=None):
        context = context or {}
        ctx = {**self.globals, **context}
        result = template
        result = self._render_loops(result, ctx)
        result = self._render_conditionals(result, ctx)
        result = self._render_variables(result, ctx)
        return result

    def _render_variables(self, template, ctx):
        def replace_var(m):
            key = m.group(1).strip()
            return str(ctx.get(key, m.group(0)))
        return re.sub(r'\{\{\s*(\w+)\s*\}\}', replace_var, template)

    def _render_conditionals(self, template, ctx):
        pattern = r'\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}'
        def replace_cond(m):
            key = m.group(1).strip()
            body = m.group(2)
            if ctx.get(key):
                return body
            return ''
        return re.sub(pattern, replace_cond, template, flags=re.DOTALL)

    def _render_loops(self, template, ctx):
        pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'
        def replace_loop(m):
            item_name = m.group(1).strip()
            list_name = m.group(2).strip()
            body = m.group(3)
            items = ctx.get(list_name, [])
            out = []
            for item in items:
                sub_ctx = {**ctx, item_name: item}
                rendered = self._render_variables(body, sub_ctx)
                out.append(rendered)
            return ''.join(out)
        return re.sub(pattern, replace_loop, template, flags=re.DOTALL)

    def set_global(self, key, value):
        self.globals[key] = value


class WorkflowEngine:
    """【阶段52】工作流引擎：步骤定义、条件分支、并行执行"""

    def __init__(self):
        self.steps = OrderedDict()
        self.results = {}

    def add_step(self, name, func, condition=None, parallel=False):
        self.steps[name] = {"func": func, "condition": condition, "parallel": parallel}

    def run(self, context=None):
        context = context or {}
        self.results = {}
        for name, step in self.steps.items():
            if step["condition"] and not step["condition"](context):
                continue
            if step["parallel"]:
                self.results[name] = step["func"](context)
            else:
                self.results[name] = step["func"](context)
        return self.results

    def run_parallel(self, context=None):
        context = context or {}
        self.results = {}
        threads = []
        for name, step in self.steps.items():
            if step["condition"] and not step["condition"](context):
                continue
            t = threading.Thread(target=lambda n, s: self.results.update({n: s["func"](context)}), args=(name, step))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return self.results


class RuleEngine:
    """【阶段53】规则引擎：规则定义、规则匹配、规则执行"""

    def __init__(self):
        self.rules = []

    def add_rule(self, name, condition, action, priority=0):
        self.rules.append({"name": name, "condition": condition, "action": action, "priority": priority})
        self.rules.sort(key=lambda r: r["priority"], reverse=True)

    def evaluate(self, facts):
        triggered = []
        for rule in self.rules:
            if rule["condition"](facts):
                triggered.append(rule)
        return triggered

    def execute(self, facts):
        results = []
        for rule in self.evaluate(facts):
            try:
                result = rule["action"](facts)
                results.append({"rule": rule["name"], "result": result})
            except Exception as e:
                results.append({"rule": rule["name"], "error": str(e)})
        return results

    def get_rules(self):
        return [r["name"] for r in self.rules]


class StateMachine:
    """【阶段54】状态机：状态定义、转换规则、事件触发"""

    def __init__(self, initial_state=None):
        self.states = set()
        self.transitions = {}
        self.current_state = initial_state
        self.history = []

    def add_state(self, state):
        self.states.add(state)

    def add_transition(self, from_state, event, to_state, action=None):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = {"to": to_state, "action": action}

    def trigger(self, event, data=None):
        if self.current_state not in self.transitions:
            return False
        if event not in self.transitions[self.current_state]:
            return False
        trans = self.transitions[self.current_state][event]
        self.history.append((self.current_state, event, trans["to"]))
        self.current_state = trans["to"]
        if trans["action"]:
            trans["action"](data)
        return True

    def can_trigger(self, event):
        return self.current_state in self.transitions and event in self.transitions[self.current_state]

    def get_available_events(self):
        return list(self.transitions.get(self.current_state, {}).keys())


class DecisionTree:
    """【阶段55】决策树：节点定义、路径选择、结果输出"""

    class Node:
        def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
            self.feature = feature
            self.threshold = threshold
            self.left = left
            self.right = right
            self.value = value

    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.root = None

    def fit(self, X, y):
        self.root = self._build_tree(X, y, depth=0)

    def _build_tree(self, X, y, depth):
        if not X or depth >= self.max_depth or len(set(y)) == 1:
            return self.Node(value=self._most_common(y))
        best_feature, best_threshold = self._best_split(X, y)
        if best_feature is None:
            return self.Node(value=self._most_common(y))
        left_X, left_y, right_X, right_y = self._split_data(X, y, best_feature, best_threshold)
        if not left_X or not right_X:
            return self.Node(value=self._most_common(y))
        left = self._build_tree(left_X, left_y, depth + 1)
        right = self._build_tree(right_X, right_y, depth + 1)
        return self.Node(feature=best_feature, threshold=best_threshold, left=left, right=right)

    def _best_split(self, X, y):
        best_gain = -1
        best_feature = None
        best_threshold = None
        n_features = len(X[0]) if X else 0
        for feature in range(n_features):
            values = sorted(set(row[feature] for row in X))
            for threshold in values:
                gain = self._information_gain(X, y, feature, threshold)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        return best_feature, best_threshold

    def _information_gain(self, X, y, feature, threshold):
        parent_entropy = self._entropy(y)
        left_y = [y[i] for i in range(len(X)) if X[i][feature] <= threshold]
        right_y = [y[i] for i in range(len(X)) if X[i][feature] > threshold]
        if not left_y or not right_y:
            return 0
        n = len(y)
        child_entropy = (len(left_y) / n) * self._entropy(left_y) + (len(right_y) / n) * self._entropy(right_y)
        return parent_entropy - child_entropy

    def _entropy(self, y):
        from collections import Counter
        counts = Counter(y)
        total = len(y)
        return -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)

    def _split_data(self, X, y, feature, threshold):
        left_X, left_y, right_X, right_y = [], [], [], []
        for i in range(len(X)):
            if X[i][feature] <= threshold:
                left_X.append(X[i]); left_y.append(y[i])
            else:
                right_X.append(X[i]); right_y.append(y[i])
        return left_X, left_y, right_X, right_y

    def _most_common(self, y):
        from collections import Counter
        return Counter(y).most_common(1)[0][0] if y else None

    def predict(self, x):
        node = self.root
        while node and node.value is None:
            if x[node.feature] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value if node else None

    def predict_batch(self, X):
        return [self.predict(x) for x in X]


class BayesianNetwork:
    """【阶段56】贝叶斯网络：概率计算、推理引擎、学习更新"""

    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.cpts = {}

    def add_node(self, name, states):
        self.nodes[name] = states

    def add_edge(self, parent, child):
        self.edges.append((parent, child))

    def set_cpt(self, node, cpt):
        self.cpts[node] = cpt

    def get_probability(self, node, state, evidence=None):
        evidence = evidence or {}
        cpt = self.cpts.get(node, {})
        if not cpt:
            return 1.0 / len(self.nodes.get(node, [state]))
        key = tuple(evidence.get(p, None) for p in self._parents(node))
        probs = cpt.get(key, cpt.get((), {}))
        return probs.get(state, 0.0)

    def _parents(self, node):
        return [p for p, c in self.edges if c == node]

    def infer(self, query, evidence=None):
        evidence = evidence or {}
        states = self.nodes.get(query, [])
        if not states:
            return {}
        total = sum(self.get_probability(query, s, evidence) for s in states)
        if total == 0:
            return {s: 1.0 / len(states) for s in states}
        return {s: self.get_probability(query, s, evidence) / total for s in states}

    def update_cpt(self, node, data):
        from collections import Counter
        counts = Counter(tuple(d.get(p) for p in self._parents(node)) for d in data)
        state_counts = {}
        for d in data:
            key = tuple(d.get(p) for p in self._parents(node))
            if key not in state_counts:
                state_counts[key] = Counter()
            state_counts[key][d.get(node)] += 1
        cpt = {}
        for key, counter in state_counts.items():
            total = sum(counter.values())
            cpt[key] = {s: c / total for s, c in counter.items()}
        self.cpts[node] = cpt


class NeuralNetwork:
    """【阶段57】神经网络：前馈网络、反向传播、预测功能"""

    def __init__(self, layers, learning_rate=0.1):
        self.layers = layers
        self.lr = learning_rate
        self.weights = []
        self.biases = []
        for i in range(len(layers) - 1):
            self.weights.append([[random.uniform(-1, 1) for _ in range(layers[i])] for _ in range(layers[i + 1])])
            self.biases.append([random.uniform(-1, 1) for _ in range(layers[i + 1])])

    def _sigmoid(self, x):
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def _sigmoid_derivative(self, x):
        s = self._sigmoid(x)
        return s * (1 - s)

    def forward(self, x):
        activations = [x]
        zs = []
        for w, b in zip(self.weights, self.biases):
            z = [sum(activations[-1][j] * w[i][j] for j in range(len(activations[-1]))) + b[i] for i in range(len(w))]
            zs.append(z)
            a = [self._sigmoid(v) for v in z]
            activations.append(a)
        return activations, zs

    def predict(self, x):
        return self.forward(x)[0][-1]

    def train(self, X, y, epochs=100):
        for _ in range(epochs):
            for xi, yi in zip(X, y):
                activations, zs = self.forward(xi)
                deltas = [None] * len(self.weights)
                error = [activations[-1][i] - yi[i] for i in range(len(yi))]
                deltas[-1] = [error[i] * self._sigmoid_derivative(zs[-1][i]) for i in range(len(error))]
                for l in range(len(self.weights) - 2, -1, -1):
                    deltas[l] = [sum(deltas[l + 1][k] * self.weights[l + 1][k][j] for k in range(len(deltas[l + 1]))) * self._sigmoid_derivative(zs[l][j]) for j in range(len(zs[l]))]
                for l in range(len(self.weights)):
                    for i in range(len(self.weights[l])):
                        for j in range(len(self.weights[l][i])):
                            self.weights[l][i][j] -= self.lr * deltas[l][i] * activations[l][j]
                        self.biases[l][i] -= self.lr * deltas[l][i]


class GeneticAlgorithm:
    """【阶段58】遗传算法：种群初始化、选择交叉变异、适应度评估"""

    def __init__(self, population_size=50, mutation_rate=0.01, crossover_rate=0.8, gene_length=10):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.gene_length = gene_length
        self.population = []

    def initialize(self):
        self.population = [[random.randint(0, 1) for _ in range(self.gene_length)] for _ in range(self.population_size)]

    def fitness(self, individual):
        return sum(individual)

    def select(self):
        fitnesses = [self.fitness(ind) for ind in self.population]
        total = sum(fitnesses)
        if total == 0:
            return random.choice(self.population)
        r = random.uniform(0, total)
        cumulative = 0
        for ind, fit in zip(self.population, fitnesses):
            cumulative += fit
            if cumulative >= r:
                return ind
        return self.population[-1]

    def crossover(self, p1, p2):
        if random.random() > self.crossover_rate:
            return p1, p2
        point = random.randint(1, self.gene_length - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        return c1, c2

    def mutate(self, individual):
        return [1 - gene if random.random() < self.mutation_rate else gene for gene in individual]

    def evolve(self, generations=100):
        self.initialize()
        best = None
        best_fitness = -1
        for _ in range(generations):
            new_population = []
            while len(new_population) < self.population_size:
                p1 = self.select()
                p2 = self.select()
                c1, c2 = self.crossover(p1, p2)
                new_population.append(self.mutate(c1))
                if len(new_population) < self.population_size:
                    new_population.append(self.mutate(c2))
            self.population = new_population[:self.population_size]
            for ind in self.population:
                fit = self.fitness(ind)
                if fit > best_fitness:
                    best_fitness = fit
                    best = ind[:]
        return best, best_fitness


class AntColony:
    """【阶段59】蚁群算法：路径搜索、信息素更新、最优解发现"""

    def __init__(self, n_nodes, alpha=1.0, beta=2.0, evaporation=0.5, q=100):
        self.n_nodes = n_nodes
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.q = q
        self.pheromone = [[1.0 for _ in range(n_nodes)] for _ in range(n_nodes)]
        self.distances = [[1.0 for _ in range(n_nodes)] for _ in range(n_nodes)]

    def set_distances(self, distances):
        self.distances = distances

    def _select_next(self, current, unvisited):
        probs = []
        for j in unvisited:
            tau = self.pheromone[current][j] ** self.alpha
            eta = (1.0 / max(self.distances[current][j], 0.001)) ** self.beta
            probs.append(tau * eta)
        total = sum(probs)
        if total == 0:
            return random.choice(unvisited)
        r = random.uniform(0, total)
        cumulative = 0
        for j, p in zip(unvisited, probs):
            cumulative += p
            if cumulative >= r:
                return j
        return unvisited[-1]

    def _construct_path(self):
        start = random.randint(0, self.n_nodes - 1)
        path = [start]
        unvisited = list(set(range(self.n_nodes)) - {start})
        while unvisited:
            next_node = self._select_next(path[-1], unvisited)
            path.append(next_node)
            unvisited.remove(next_node)
        return path

    def _path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += self.distances[path[i]][path[i + 1]]
        length += self.distances[path[-1]][path[0]]
        return length

    def _update_pheromone(self, paths):
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                self.pheromone[i][j] *= (1 - self.evaporation)
        for path, length in paths:
            delta = self.q / max(length, 0.001)
            for i in range(len(path) - 1):
                self.pheromone[path[i]][path[i + 1]] += delta
            self.pheromone[path[-1]][path[0]] += delta

    def solve(self, iterations=100, n_ants=10):
        best_path = None
        best_length = float('inf')
        for _ in range(iterations):
            paths = []
            for _ in range(n_ants):
                path = self._construct_path()
                length = self._path_length(path)
                paths.append((path, length))
                if length < best_length:
                    best_length = length
                    best_path = path[:]
            self._update_pheromone(paths)
        return best_path, best_length


class ParticleSwarm:
    """【阶段60】粒子群优化：粒子初始化、速度更新、全局最优"""

    def __init__(self, n_particles, dim, bounds=None, w=0.7, c1=1.5, c2=1.5):
        self.n_particles = n_particles
        self.dim = dim
        self.bounds = bounds or [(-5, 5)] * dim
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.particles = []
        self.velocities = []
        self.pbest = []
        self.pbest_fitness = []
        self.gbest = None
        self.gbest_fitness = float('inf')

    def initialize(self):
        self.particles = [[random.uniform(self.bounds[d][0], self.bounds[d][1]) for d in range(self.dim)] for _ in range(self.n_particles)]
        self.velocities = [[random.uniform(-1, 1) for _ in range(self.dim)] for _ in range(self.n_particles)]
        self.pbest = [p[:] for p in self.particles]
        self.pbest_fitness = [float('inf')] * self.n_particles
        self.gbest = None
        self.gbest_fitness = float('inf')

    def fitness(self, position):
        return sum(x ** 2 for x in position)

    def optimize(self, iterations=100):
        self.initialize()
        for _ in range(iterations):
            for i in range(self.n_particles):
                fit = self.fitness(self.particles[i])
                if fit < self.pbest_fitness[i]:
                    self.pbest_fitness[i] = fit
                    self.pbest[i] = self.particles[i][:]
                if fit < self.gbest_fitness:
                    self.gbest_fitness = fit
                    self.gbest = self.particles[i][:]
            for i in range(self.n_particles):
                for d in range(self.dim):
                    r1, r2 = random.random(), random.random()
                    v = self.w * self.velocities[i][d] + self.c1 * r1 * (self.pbest[i][d] - self.particles[i][d]) + self.c2 * r2 * (self.gbest[d] - self.particles[i][d])
                    self.velocities[i][d] = v
                    self.particles[i][d] += v
                    lo, hi = self.bounds[d]
                    self.particles[i][d] = max(lo, min(hi, self.particles[i][d]))
        return self.gbest, self.gbest_fitness


class SimulatedAnnealing:
    """【阶段61】模拟退火：温度控制、接受准则、冷却策略"""

    def __init__(self, initial_temp=100, cooling_rate=0.95, min_temp=0.01):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp

    def acceptance_probability(self, old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        return math.exp((old_cost - new_cost) / max(temperature, 0.0001))

    def optimize(self, initial_solution, neighbor_func, cost_func, max_iterations=1000):
        current = initial_solution[:]
        best = current[:]
        current_cost = cost_func(current)
        best_cost = current_cost
        temperature = self.initial_temp
        for _ in range(max_iterations):
            if temperature < self.min_temp:
                break
            neighbor = neighbor_func(current)
            neighbor_cost = cost_func(neighbor)
            if random.random() < self.acceptance_probability(current_cost, neighbor_cost, temperature):
                current = neighbor[:]
                current_cost = neighbor_cost
                if current_cost < best_cost:
                    best = current[:]
                    best_cost = current_cost
            temperature *= self.cooling_rate
        return best, best_cost


class MonteCarlo:
    """【阶段62】蒙特卡洛方法：随机采样、概率估计、数值积分"""

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def sample(self, distribution, n_samples):
        if distribution == "uniform":
            return [random.uniform(0, 1) for _ in range(n_samples)]
        elif distribution == "normal":
            return [random.gauss(0, 1) for _ in range(n_samples)]
        elif distribution == "bernoulli":
            return [random.choice([0, 1]) for _ in range(n_samples)]
        return []

    def estimate_probability(self, predicate, n_samples=10000):
        count = sum(1 for _ in range(n_samples) if predicate())
        return count / n_samples

    def integrate(self, func, a, b, n_samples=10000):
        total = sum(func(random.uniform(a, b)) for _ in range(n_samples))
        return (b - a) * total / n_samples

    def estimate_pi(self, n_samples=100000):
        inside = sum(1 for _ in range(n_samples) if random.random() ** 2 + random.random() ** 2 <= 1)
        return 4 * inside / n_samples


class MarkovChain:
    """【阶段63】马尔可夫链：状态转移、稳态分布、序列生成"""

    def __init__(self, states):
        self.states = states
        self.transitions = {s: {s2: 0.0 for s2 in states} for s in states}

    def set_transition(self, from_state, to_state, probability):
        self.transitions[from_state][to_state] = probability

    def normalize(self):
        for s in self.states:
            total = sum(self.transitions[s].values())
            if total > 0:
                for s2 in self.states:
                    self.transitions[s][s2] /= total

    def next_state(self, current_state):
        probs = [self.transitions[current_state][s] for s in self.states]
        r = random.random()
        cumulative = 0
        for s, p in zip(self.states, probs):
            cumulative += p
            if r <= cumulative:
                return s
        return self.states[-1]

    def generate_sequence(self, length, initial_state=None):
        state = initial_state or random.choice(self.states)
        sequence = [state]
        for _ in range(length - 1):
            state = self.next_state(state)
            sequence.append(state)
        return sequence

    def steady_state(self, iterations=1000):
        dist = {s: 1.0 / len(self.states) for s in self.states}
        for _ in range(iterations):
            new_dist = {s: 0.0 for s in self.states}
            for s in self.states:
                for s2 in self.states:
                    new_dist[s2] += dist[s] * self.transitions[s][s2]
            dist = new_dist
        return dist


class HMM:
    """【阶段64】隐马尔可夫模型：前向算法、维特比算法、参数学习"""

    def __init__(self, states, observations):
        self.states = states
        self.observations = observations
        self.initial = {s: 1.0 / len(states) for s in states}
        self.transition = {s: {s2: 1.0 / len(states) for s2 in states} for s in states}
        self.emission = {s: {o: 1.0 / len(observations) for o in observations} for s in states}

    def set_initial(self, probs):
        self.initial = probs

    def set_transition(self, trans):
        self.transition = trans

    def set_emission(self, emit):
        self.emission = emit

    def forward(self, obs_sequence):
        alpha = [{s: self.initial[s] * self.emission[s][obs_sequence[0]] for s in self.states}]
        for t in range(1, len(obs_sequence)):
            alpha.append({})
            for s in self.states:
                alpha[t][s] = sum(alpha[t - 1][s2] * self.transition[s2][s] for s2 in self.states) * self.emission[s][obs_sequence[t]]
        return alpha

    def viterbi(self, obs_sequence):
        delta = [{s: math.log(max(self.initial[s] * self.emission[s][obs_sequence[0]], 1e-10)) for s in self.states}]
        psi = [{s: None for s in self.states}]
        for t in range(1, len(obs_sequence)):
            delta.append({})
            psi.append({})
            for s in self.states:
                best_val = float('-inf')
                best_state = None
                for s2 in self.states:
                    val = delta[t - 1][s2] + math.log(max(self.transition[s2][s], 1e-10))
                    if val > best_val:
                        best_val = val
                        best_state = s2
                delta[t][s] = best_val + math.log(max(self.emission[s][obs_sequence[t]], 1e-10))
                psi[t][s] = best_state
        best_final = max(self.states, key=lambda s: delta[-1][s])
        path = [best_final]
        for t in range(len(obs_sequence) - 1, 0, -1):
            path.insert(0, psi[t][path[0]])
        return path

    def baum_welch(self, observations_list, iterations=10):
        for _ in range(iterations):
            gamma_sum = {s: 0.0 for s in self.states}
            xi_sum = {s: {s2: 0.0 for s2 in self.states} for s in self.states}
            emit_sum = {s: {o: 0.0 for o in self.observations} for s in self.states}
            for obs_seq in observations_list:
                alpha = self.forward(obs_seq)
                beta = self._backward(obs_seq)
                for t in range(len(obs_seq)):
                    denom = sum(alpha[t][s] * beta[t][s] for s in self.states)
                    for s in self.states:
                        gamma = alpha[t][s] * beta[t][s] / max(denom, 1e-10)
                        gamma_sum[s] += gamma
                        emit_sum[s][obs_seq[t]] += gamma
                for t in range(len(obs_seq) - 1):
                    denom = sum(alpha[t][s1] * self.transition[s1][s2] * self.emission[s2][obs_seq[t + 1]] * beta[t + 1][s2] for s1 in self.states for s2 in self.states)
                    for s1 in self.states:
                        for s2 in self.states:
                            xi = alpha[t][s1] * self.transition[s1][s2] * self.emission[s2][obs_seq[t + 1]] * beta[t + 1][s2] / max(denom, 1e-10)
                            xi_sum[s1][s2] += xi
            for s in self.states:
                total = sum(xi_sum[s].values())
                for s2 in self.states:
                    self.transition[s][s2] = xi_sum[s][s2] / max(total, 1e-10)
                total_emit = sum(emit_sum[s].values())
                for o in self.observations:
                    self.emission[s][o] = emit_sum[s][o] / max(total_emit, 1e-10)

    def _backward(self, obs_sequence):
        beta = [{s: 1.0 for s in self.states}]
        for t in range(len(obs_sequence) - 2, -1, -1):
            beta.insert(0, {})
            for s in self.states:
                beta[0][s] = sum(self.transition[s][s2] * self.emission[s2][obs_sequence[t + 1]] * beta[1][s2] for s2 in self.states)
        return beta


class SVM:
    """【阶段65】支持向量机：分类功能、核函数、超平面"""

    def __init__(self, learning_rate=0.001, lambda_param=0.01, epochs=1000, kernel="linear"):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.epochs = epochs
        self.kernel = kernel
        self.w = None
        self.b = 0

    def _kernel_func(self, x1, x2):
        if self.kernel == "linear":
            return sum(a * b for a, b in zip(x1, x2))
        elif self.kernel == "rbf":
            gamma = 0.1
            return math.exp(-gamma * sum((a - b) ** 2 for a, b in zip(x1, x2)))
        return sum(a * b for a, b in zip(x1, x2))

    def fit(self, X, y):
        n_samples = len(X)
        n_features = len(X[0]) if X else 0
        self.w = [0.0] * n_features
        self.b = 0
        for _ in range(self.epochs):
            for i in range(n_samples):
                condition = y[i] * (sum(self.w[j] * X[i][j] for j in range(n_features)) - self.b) >= 1
                if condition:
                    for j in range(n_features):
                        self.w[j] -= self.lr * (2 * self.lambda_param * self.w[j])
                else:
                    for j in range(n_features):
                        self.w[j] -= self.lr * (2 * self.lambda_param * self.w[j] - y[i] * X[i][j])
                    self.b -= self.lr * y[i]

    def predict(self, X):
        if self.w is None:
            return 0
        return 1 if sum(self.w[j] * X[j] for j in range(len(self.w))) - self.b >= 0 else -1

    def predict_batch(self, X):
        return [self.predict(x) for x in X]

    def decision_function(self, X):
        return sum(self.w[j] * X[j] for j in range(len(self.w))) - self.b


class KMeans:
    """【阶段66】K均值聚类：聚类算法、中心点更新、收敛判断"""

    def __init__(self, k=3, max_iters=100, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None
        self.labels = None

    def fit(self, X):
        n_samples = len(X)
        n_features = len(X[0]) if X else 0
        self.centroids = [X[i][:] for i in random.sample(range(n_samples), min(self.k, n_samples))]
        if len(self.centroids) < self.k:
            while len(self.centroids) < self.k:
                self.centroids.append([random.uniform(min(x[i] for x in X), max(x[i] for x in X)) for i in range(n_features)])
        for _ in range(self.max_iters):
            self.labels = [self._closest_centroid(x) for x in X]
            new_centroids = []
            for i in range(self.k):
                cluster_points = [X[j] for j in range(n_samples) if self.labels[j] == i]
                if cluster_points:
                    new_centroids.append([sum(p[d] for p in cluster_points) / len(cluster_points) for d in range(n_features)])
                else:
                    new_centroids.append(self.centroids[i][:])
            converged = all(sum((new_centroids[i][d] - self.centroids[i][d]) ** 2 for d in range(n_features)) < self.tol for i in range(self.k))
            self.centroids = new_centroids
            if converged:
                break

    def _closest_centroid(self, x):
        distances = [sum((x[d] - self.centroids[i][d]) ** 2 for d in range(len(x))) for i in range(self.k)]
        return distances.index(min(distances))

    def predict(self, X):
        return [self._closest_centroid(x) for x in X]


class PCA:
    """【阶段67】主成分分析：降维处理、特征提取、方差保留"""

    def __init__(self, n_components=2):
        self.n_components = n_components
        self.components = None
        self.mean = None

    def fit(self, X):
        n_samples = len(X)
        n_features = len(X[0]) if X else 0
        self.mean = [sum(X[i][j] for i in range(n_samples)) / n_samples for j in range(n_features)]
        centered = [[X[i][j] - self.mean[j] for j in range(n_features)] for i in range(n_samples)]
        cov = [[sum(centered[i][j] * centered[i][k] for i in range(n_samples)) / (n_samples - 1) for k in range(n_features)] for j in range(n_features)]
        eigenvalues, eigenvectors = self._eigen_decomposition(cov)
        sorted_indices = sorted(range(len(eigenvalues)), key=lambda i: eigenvalues[i], reverse=True)
        self.components = [eigenvectors[i] for i in sorted_indices[:self.n_components]]

    def _eigen_decomposition(self, matrix, max_iter=100):
        n = len(matrix)
        vectors = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        for _ in range(max_iter):
            for i in range(n):
                for j in range(i + 1, n):
                    if abs(matrix[i][j]) < 1e-10:
                        continue
                    tau = (matrix[j][j] - matrix[i][i]) / (2 * matrix[i][j])
                    t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1 + tau * tau))
                    c = 1 / math.sqrt(1 + t * t)
                    s = t * c
                    a_ii = matrix[i][i]
                    a_jj = matrix[j][j]
                    matrix[i][i] = c * c * a_ii - 2 * c * s * matrix[i][j] + s * s * a_jj
                    matrix[j][j] = s * s * a_ii + 2 * c * s * matrix[i][j] + c * c * a_jj
                    matrix[i][j] = matrix[j][i] = 0
                    for k in range(n):
                        if k != i and k != j:
                            a_ki = matrix[k][i]
                            a_kj = matrix[k][j]
                            matrix[k][i] = matrix[i][k] = c * a_ki - s * a_kj
                            matrix[k][j] = matrix[j][k] = s * a_ki + c * a_kj
                    for k in range(n):
                        v_ki = vectors[k][i]
                        v_kj = vectors[k][j]
                        vectors[k][i] = c * v_ki - s * v_kj
                        vectors[k][j] = s * v_ki + c * v_kj
        eigenvalues = [matrix[i][i] for i in range(n)]
        return eigenvalues, vectors

    def transform(self, X):
        centered = [[x[j] - self.mean[j] for j in range(len(x))] for x in X]
        return [[sum(centered[i][j] * self.components[k][j] for j in range(len(centered[i]))) for k in range(self.n_components)] for i in range(len(centered))]

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def explained_variance_ratio(self, X):
        n_samples = len(X)
        centered = [[X[i][j] - self.mean[j] for j in range(len(X[0]))] for i in range(n_samples)]
        total_var = sum(sum(centered[i][j] ** 2 for j in range(len(centered[i]))) for i in range(n_samples)) / (n_samples - 1)
        explained = []
        for comp in self.components:
            proj_var = sum(sum(centered[i][j] * comp[j] for j in range(len(comp))) ** 2 for i in range(n_samples)) / (n_samples - 1)
            explained.append(proj_var / max(total_var, 1e-10))
        return explained


class LinearRegression:
    """【阶段68】线性回归：拟合计算、预测功能、误差评估"""

    def __init__(self):
        self.coef = None
        self.intercept = 0

    def fit(self, X, y):
        n = len(X)
        x_mean = sum(X) / n
        y_mean = sum(y) / n
        numerator = sum((X[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((X[i] - x_mean) ** 2 for i in range(n))
        if denominator == 0:
            self.coef = 0
        else:
            self.coef = numerator / denominator
        self.intercept = y_mean - self.coef * x_mean

    def predict(self, X):
        if self.coef is None:
            return [self.intercept] * len(X)
        return [self.coef * x + self.intercept for x in X]

    def score(self, X, y):
        preds = self.predict(X)
        ss_res = sum((y[i] - preds[i]) ** 2 for i in range(len(y)))
        y_mean = sum(y) / len(y)
        ss_tot = sum((yi - y_mean) ** 2 for yi in y)
        return 1 - ss_res / max(ss_tot, 1e-10)

    def mse(self, X, y):
        preds = self.predict(X)
        return sum((y[i] - preds[i]) ** 2 for i in range(len(y))) / len(y)


class LogisticRegression:
    """【阶段69】逻辑回归：分类预测、概率输出、梯度下降"""

    def __init__(self, learning_rate=0.01, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0

    def _sigmoid(self, z):
        try:
            return 1 / (1 + math.exp(-z))
        except OverflowError:
            return 0.0 if z < 0 else 1.0

    def fit(self, X, y):
        n_samples = len(X)
        n_features = len(X[0]) if X else 0
        self.weights = [0.0] * n_features
        for _ in range(self.epochs):
            for i in range(n_samples):
                z = sum(self.weights[j] * X[i][j] for j in range(n_features)) + self.bias
                pred = self._sigmoid(z)
                error = pred - y[i]
                for j in range(n_features):
                    self.weights[j] -= self.lr * error * X[i][j]
                self.bias -= self.lr * error

    def predict_proba(self, X):
        if self.weights is None:
            return 0.5
        z = sum(self.weights[j] * X[j] for j in range(len(self.weights))) + self.bias
        return self._sigmoid(z)

    def predict(self, X):
        return 1 if self.predict_proba(X) >= 0.5 else 0

    def predict_batch(self, X):
        return [self.predict(x) for x in X]


class RandomForest:
    """【阶段70】决策森林：多树集成、投票机制、特征重要性"""

    def __init__(self, n_trees=10, max_depth=5, sample_ratio=0.8):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.sample_ratio = sample_ratio
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        n_samples = len(X)
        n_sample = max(1, int(n_samples * self.sample_ratio))
        for _ in range(self.n_trees):
            indices = [random.randint(0, n_samples - 1) for _ in range(n_sample)]
            X_sample = [X[i] for i in indices]
            y_sample = [y[i] for i in indices]
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, x):
        votes = [tree.predict(x) for tree in self.trees]
        from collections import Counter
        return Counter(votes).most_common(1)[0][0]

    def predict_batch(self, X):
        return [self.predict(x) for x in X]

    def feature_importance(self, X, y):
        n_features = len(X[0]) if X else 0
        importances = [0.0] * n_features
        base_acc = self._accuracy(X, y)
        for j in range(n_features):
            X_shuffled = [x[:] for x in X]
            values = [x[j] for x in X_shuffled]
            random.shuffle(values)
            for i in range(len(X_shuffled)):
                X_shuffled[i][j] = values[i]
            shuffled_acc = self._accuracy(X_shuffled, y)
            importances[j] = max(0, base_acc - shuffled_acc)
        total = sum(importances)
        if total > 0:
            importances = [i / total for i in importances]
        return importances

    def _accuracy(self, X, y):
        preds = self.predict_batch(X)
        correct = sum(1 for i in range(len(y)) if preds[i] == y[i])
        return correct / len(y)


class GradientBoosting:
    """【阶段71】梯度提升：迭代优化、残差学习、模型集成"""

    def __init__(self, n_estimators=10, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.initial_prediction = 0

    def fit(self, X, y):
        self.initial_prediction = sum(y) / len(y)
        current_pred = [self.initial_prediction] * len(y)
        for _ in range(self.n_estimators):
            residuals = [y[i] - current_pred[i] for i in range(len(y))]
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X, residuals)
            self.trees.append(tree)
            for i in range(len(y)):
                current_pred[i] += self.learning_rate * tree.predict(X[i])

    def predict(self, x):
        pred = self.initial_prediction
        for tree in self.trees:
            pred += self.learning_rate * tree.predict(x)
        return pred

    def predict_batch(self, X):
        return [self.predict(x) for x in X]


class WordVector:
    """【阶段72】词向量：词嵌入、相似度计算、语义分析"""

    def __init__(self, vector_size=10):
        self.vector_size = vector_size
        self.vectors = {}

    def fit(self, sentences):
        vocab = set()
        for sentence in sentences:
            words = sentence.lower().split()
            vocab.update(words)
        for word in vocab:
            self.vectors[word] = [random.uniform(-0.5, 0.5) for _ in range(self.vector_size)]
        for _ in range(10):
            for sentence in sentences:
                words = sentence.lower().split()
                for i, word in enumerate(words):
                    context = [w for j, w in enumerate(words) if abs(j - i) <= 2 and j != i]
                    if context:
                        grad = [0.0] * self.vector_size
                        for cw in context:
                            for d in range(self.vector_size):
                                grad[d] += self.vectors[cw][d] - self.vectors[word][d]
                        for d in range(self.vector_size):
                            self.vectors[word][d] += 0.01 * grad[d] / len(context)

    def get_vector(self, word):
        return self.vectors.get(word.lower(), [0.0] * self.vector_size)

    def similarity(self, word1, word2):
        v1 = self.get_vector(word1)
        v2 = self.get_vector(word2)
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(a * a for a in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def most_similar(self, word, top_n=5):
        similarities = [(w, self.similarity(word, w)) for w in self.vectors if w != word.lower()]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]


class TFIDF:
    """【阶段73】TF-IDF：词频计算、逆文档频率、权重计算"""

    def __init__(self):
        self.idf = {}
        self.vocab = []

    def fit(self, documents):
        n_docs = len(documents)
        vocab_set = set()
        for doc in documents:
            vocab_set.update(doc.lower().split())
        self.vocab = sorted(vocab_set)
        for term in self.vocab:
            doc_count = sum(1 for doc in documents if term in doc.lower().split())
            self.idf[term] = math.log(n_docs / max(doc_count, 1)) + 1

    def transform(self, documents):
        vectors = []
        for doc in documents:
            words = doc.lower().split()
            word_count = {}
            for w in words:
                word_count[w] = word_count.get(w, 0) + 1
            max_count = max(word_count.values()) if word_count else 1
            vector = []
            for term in self.vocab:
                tf = 0.5 + 0.5 * (word_count.get(term, 0) / max_count)
                vector.append(tf * self.idf.get(term, 0))
            vectors.append(vector)
        return vectors

    def fit_transform(self, documents):
        self.fit(documents)
        return self.transform(documents)

    def get_feature_names(self):
        return self.vocab


class TextClassifier:
    """【阶段74】文本分类：特征提取、分类训练、预测标签"""

    def __init__(self):
        self.tfidf = TFIDF()
        self.classifier = LogisticRegression(learning_rate=0.1, epochs=500)
        self.classes = []

    def fit(self, documents, labels):
        X = self.tfidf.fit_transform(documents)
        self.classes = sorted(set(labels))
        y = [self.classes.index(l) for l in labels]
        self.classifier.fit(X, y)

    def predict(self, document):
        X = self.tfidf.transform([document])
        pred = self.classifier.predict(X[0])
        return self.classes[pred]

    def predict_batch(self, documents):
        return [self.predict(doc) for doc in documents]

    def score(self, documents, labels):
        preds = self.predict_batch(documents)
        correct = sum(1 for i in range(len(labels)) if preds[i] == labels[i])
        return correct / len(labels)


class SentimentAnalyzer:
    """【阶段75】情感分析：情感词典、极性判断、强度评分"""

    def __init__(self):
        self.positive_words = set([
            "good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "happy",
            "joy", "beautiful", "awesome", "perfect", "best", "nice", "positive", "glad",
            "excited", "pleased", "satisfied", "delightful", "brilliant", "superb", "lovely"
        ])
        self.negative_words = set([
            "bad", "terrible", "awful", "horrible", "hate", "sad", "angry", "worst",
            "poor", "disappointing", "negative", "unhappy", "disgusting", "annoying",
            "boring", "useless", "stupid", "ugly", "painful", "depressed", "frustrated"
        ])
        self.intensifiers = set(["very", "extremely", "really", "quite", "too", "so", "highly"])
        self.negations = set(["not", "no", "never", "neither", "nor", "hardly", "barely"])

    def analyze(self, text):
        words = text.lower().split()
        score = 0
        intensifier = 1.0
        negation = 1.0
        for word in words:
            if word in self.intensifiers:
                intensifier = 1.5
                continue
            if word in self.negations:
                negation = -1.0
                continue
            if word in self.positive_words:
                score += 1 * intensifier * negation
                intensifier = 1.0
                negation = 1.0
            elif word in self.negative_words:
                score -= 1 * intensifier * negation
                intensifier = 1.0
                negation = 1.0
        polarity = "positive" if score > 0 else ("negative" if score < 0 else "neutral")
        intensity = min(abs(score) / 3, 1.0)
        return {"score": score, "polarity": polarity, "intensity": round(intensity, 2)}

    def analyze_batch(self, texts):
        return [self.analyze(t) for t in texts]


class CommandPattern:
    """【阶段76】命令模式：命令封装、撤销重做、命令队列"""

    def __init__(self):
        self._history = []
        self._redo_stack = []
        self._queue = deque()

    def execute(self, command):
        result = command.execute()
        self._history.append(command)
        self._redo_stack.clear()
        return result

    def undo(self):
        if not self._history:
            return None
        cmd = self._history.pop()
        self._redo_stack.append(cmd)
        return cmd.undo()

    def redo(self):
        if not self._redo_stack:
            return None
        cmd = self._redo_stack.pop()
        self._history.append(cmd)
        return cmd.execute()

    def enqueue(self, command):
        self._queue.append(command)

    def process_queue(self):
        results = []
        while self._queue:
            cmd = self._queue.popleft()
            results.append(self.execute(cmd))
        return results

    def get_history(self):
        return self._history[:]

    def clear_history(self):
        self._history.clear()
        self._redo_stack.clear()


class Command:
    """命令基类"""

    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


class AddCommand(Command):
    """加法命令"""

    def __init__(self, receiver, value):
        self.receiver = receiver
        self.value = value

    def execute(self):
        self.receiver.value += self.value
        return self.receiver.value

    def undo(self):
        self.receiver.value -= self.value
        return self.receiver.value


class ObserverPattern:
    """【阶段77】观察者模式：主题订阅、通知机制、自动更新"""

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                cb for cb in self._subscribers[event_type] if cb != callback
            ]

    def notify(self, event_type, data=None):
        if event_type not in self._subscribers:
            return []
        results = []
        for callback in self._subscribers[event_type]:
            results.append(callback(data))
        return results

    def get_subscribers(self, event_type):
        return self._subscribers.get(event_type, [])


class StrategyPattern:
    """【阶段78】策略模式：策略定义、动态切换、上下文管理"""

    def __init__(self, default_strategy=None):
        self._strategy = default_strategy
        self._strategies = {}

    def register(self, name, strategy):
        self._strategies[name] = strategy

    def set_strategy(self, name):
        if name in self._strategies:
            self._strategy = self._strategies[name]
            return True
        return False

    def execute(self, *args, **kwargs):
        if self._strategy is None:
            raise ValueError("No strategy set")
        return self._strategy(*args, **kwargs)

    def get_available(self):
        return list(self._strategies.keys())


class FactoryPattern:
    """【阶段79】工厂模式：对象创建、类型注册、延迟初始化"""

    def __init__(self):
        self._registry = {}
        self._instances = {}

    def register(self, name, creator):
        self._registry[name] = creator

    def create(self, name, *args, **kwargs):
        if name not in self._registry:
            raise ValueError(f"Unknown type: {name}")
        return self._registry[name](*args, **kwargs)

    def get_registered(self):
        return list(self._registry.keys())

    def get_or_create(self, name, creator=None, *args, **kwargs):
        if name not in self._instances:
            if creator is not None and name not in self._registry:
                self._registry[name] = creator
            self._instances[name] = self.create(name, *args, **kwargs)
        return self._instances[name]


class SingletonPattern:
    """【阶段80】单例模式：唯一实例、线程安全、延迟加载"""

    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def get_instance(cls):
        return cls.__new__(cls)

    @classmethod
    def reset(cls):
        if cls in cls._instances:
            del cls._instances[cls]


class ProxyPattern:
    """【阶段81】代理模式：访问控制、延迟加载、缓存代理"""

    def __init__(self, target=None):
        self._target = target
        self._cache = {}
        self._access_log = []
        self._enabled = True

    def set_target(self, target):
        self._target = target

    def __getattr__(self, name):
        if not self._enabled:
            raise PermissionError("Proxy access disabled")
        self._access_log.append(name)
        if name in self._cache:
            return self._cache[name]
        attr = getattr(self._target, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                key = (name, args, tuple(sorted(kwargs.items())))
                if key in self._cache:
                    return self._cache[key]
                result = attr(*args, **kwargs)
                self._cache[key] = result
                return result
            return wrapper
        return attr

    def cache_result(self, key, value):
        self._cache[key] = value

    def get_access_log(self):
        return self._access_log[:]

    def set_enabled(self, enabled):
        self._enabled = enabled


class DecoratorPattern:
    """【阶段82】装饰器模式：动态增强、功能叠加、透明包装"""

    def __init__(self, component):
        self._component = component

    def __getattr__(self, name):
        return getattr(self._component, name)

    def operation(self):
        return self._component.operation()


class ConcreteDecoratorA(DecoratorPattern):
    """装饰器A：添加前缀"""

    def operation(self):
        return f"DecoratorA({self._component.operation()})"


class ConcreteDecoratorB(DecoratorPattern):
    """装饰器B：添加后缀"""

    def operation(self):
        return f"{self._component.operation()}[DecoratorB]"


class AdapterPattern:
    """【阶段83】适配器模式：接口转换、兼容封装、多适配器"""

    def __init__(self, adaptee, method_map=None):
        self._adaptee = adaptee
        self._method_map = method_map or {}

    def __getattr__(self, name):
        if name in self._method_map:
            target_name = self._method_map[name]
            return getattr(self._adaptee, target_name)
        return getattr(self._adaptee, name)

    def add_mapping(self, source, target):
        self._method_map[source] = target


class BridgePattern:
    """【阶段84】桥接模式：抽象分离、实现独立、组合扩展"""

    def __init__(self, implementation):
        self._implementation = implementation

    def operation(self):
        return self._implementation.operation_impl()

    def set_implementation(self, implementation):
        self._implementation = implementation


class BridgeImplementationA:
    def operation_impl(self):
        return "ImplementationA"


class BridgeImplementationB:
    def operation_impl(self):
        return "ImplementationB"


class CompositePattern:
    """【阶段85】组合模式：树形结构、统一接口、递归操作"""

    def __init__(self, name):
        self.name = name
        self._children = []

    def add(self, component):
        self._children.append(component)
        return self

    def remove(self, component):
        self._children.remove(component)
        return self

    def operation(self):
        results = [self.name]
        for child in self._children:
            results.extend(child.operation())
        return results

    def get_children(self):
        return self._children[:]


class FlyweightPattern:
    """【阶段86】享元模式：对象共享、内存优化、状态分离"""

    _pool = {}
    _lock = threading.Lock()

    def __new__(cls, key, *args, **kwargs):
        if key not in cls._pool:
            with cls._lock:
                if key not in cls._pool:
                    instance = super().__new__(cls)
                    instance._key = key
                    instance._intrinsic_state = kwargs
                    cls._pool[key] = instance
        return cls._pool[key]

    def get_key(self):
        return self._key

    def get_state(self):
        return self._intrinsic_state

    @classmethod
    def get_pool_size(cls):
        return len(cls._pool)

    @classmethod
    def clear_pool(cls):
        cls._pool.clear()


class ChainOfResponsibility:
    """【阶段87】责任链模式：请求传递、动态链、处理分离"""

    def __init__(self):
        self._handlers = []

    def add_handler(self, handler):
        self._handlers.append(handler)
        return self

    def handle(self, request):
        for handler in self._handlers:
            result = handler(request)
            if result is not None:
                return result
        return None

    def set_handlers(self, handlers):
        self._handlers = handlers[:]


class MediatorPattern:
    """【阶段88】中介者模式：对象解耦、集中控制、消息路由"""

    def __init__(self):
        self._colleagues = {}
        self._messages = []

    def register(self, name, colleague):
        self._colleagues[name] = colleague
        colleague.set_mediator(self)

    def send(self, message, sender, receiver=None):
        if receiver and receiver in self._colleagues:
            self._messages.append({"message": message, "sender": sender, "receiver": receiver})
            self._colleagues[receiver].receive(message, sender)
        elif receiver is None:
            recipients = [n for n in self._colleagues if n != sender]
            for name in recipients:
                self._messages.append({"message": message, "sender": sender, "receiver": name})
                self._colleagues[name].receive(message, sender)

    def get_messages(self):
        return self._messages[:]


class Colleague:
    """同事基类"""

    def __init__(self, name):
        self.name = name
        self._mediator = None
        self._received = []

    def set_mediator(self, mediator):
        self._mediator = mediator

    def send(self, message, receiver=None):
        if self._mediator:
            self._mediator.send(message, self.name, receiver)

    def receive(self, message, sender):
        self._received.append({"message": message, "sender": sender})

    def get_received(self):
        return self._received[:]


class MementoPattern:
    """【阶段89】备忘录模式：状态保存、恢复机制、历史管理"""

    def __init__(self):
        self._states = []
        self._current = -1

    def save(self, state):
        self._current += 1
        self._states = self._states[:self._current]
        self._states.append(state)
        return self._current

    def restore(self, index=None):
        if index is None:
            index = self._current
        if 0 <= index < len(self._states):
            self._current = index
            return self._states[index]
        return None

    def undo(self):
        if self._current > 0:
            self._current -= 1
            return self._states[self._current]
        return None

    def redo(self):
        if self._current < len(self._states) - 1:
            self._current += 1
            return self._states[self._current]
        return None

    def get_history(self):
        return self._states[:]


class VisitorPattern:
    """【阶段90】访问者模式：操作分离、双重分发、扩展方便"""

    def __init__(self):
        self._visitors = {}

    def register(self, element_type, visitor_fn):
        self._visitors[element_type] = visitor_fn

    def visit(self, element):
        element_type = type(element)
        if element_type in self._visitors:
            return self._visitors[element_type](element)
        for cls in element_type.__mro__[1:]:
            if cls in self._visitors:
                return self._visitors[cls](element)
        return None


class IteratorPattern:
    """【阶段91】迭代器模式：遍历抽象、多种迭代、惰性求值"""

    def __init__(self, collection):
        self._collection = collection
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._collection):
            raise StopIteration
        value = self._collection[self._index]
        self._index += 1
        return value

    def reset(self):
        self._index = 0

    def has_next(self):
        return self._index < len(self._collection)


class ReverseIteratorPattern(IteratorPattern):
    """反向迭代器"""

    def __init__(self, collection):
        super().__init__(collection)
        self._index = len(collection) - 1

    def __next__(self):
        if self._index < 0:
            raise StopIteration
        value = self._collection[self._index]
        self._index -= 1
        return value

    def has_next(self):
        return self._index >= 0


class InterpreterPattern:
    """【阶段92】解释器模式：语法解析、表达式求值、规则执行"""

    def __init__(self):
        self._variables = {}

    def set_variable(self, name, value):
        self._variables[name] = value

    def evaluate(self, expression):
        tokens = expression.split()
        return self._parse(tokens)

    def _parse(self, tokens):
        if not tokens:
            return 0
        token = tokens.pop(0)
        if token in self._variables:
            return self._variables[token]
        if token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
            return int(token)
        if token == "+":
            return self._parse(tokens) + self._parse(tokens)
        if token == "-":
            return self._parse(tokens) - self._parse(tokens)
        if token == "*":
            return self._parse(tokens) * self._parse(tokens)
        if token == "/":
            return self._parse(tokens) // self._parse(tokens)
        return 0


class BuilderPattern:
    """【阶段93】构建器模式：分步构建、参数配置、产品创建"""

    def __init__(self):
        self._product = {}

    def reset(self):
        self._product = {}
        return self

    def set(self, key, value):
        self._product[key] = value
        return self

    def build(self):
        return self._product.copy()


class PrototypePattern:
    """【阶段94】原型模式：对象克隆、深拷贝浅拷贝、原型注册"""

    def __init__(self):
        self._prototypes = {}

    def register(self, name, prototype):
        self._prototypes[name] = prototype

    def clone(self, name, deep=True, overrides=None):
        if name not in self._prototypes:
            raise ValueError(f"Unknown prototype: {name}")
        original = self._prototypes[name]
        if deep:
            import copy
            new_obj = copy.deepcopy(original)
        else:
            new_obj = original.copy() if hasattr(original, "copy") else original
        overrides = overrides or {}
        for key, value in overrides.items():
            setattr(new_obj, key, value) if hasattr(new_obj, key) else None
            if isinstance(new_obj, dict):
                new_obj[key] = value
        return new_obj

    def get_registered(self):
        return list(self._prototypes.keys())


class FacadePattern:
    """【阶段95】外观模式：统一接口、子系统封装、简化使用"""

    def __init__(self):
        self._subsystems = {}

    def register(self, name, subsystem):
        self._subsystems[name] = subsystem

    def call(self, subsystem_name, method_name, *args, **kwargs):
        if subsystem_name not in self._subsystems:
            raise ValueError(f"Unknown subsystem: {subsystem_name}")
        subsystem = self._subsystems[subsystem_name]
        method = getattr(subsystem, method_name)
        return method(*args, **kwargs)

    def get_subsystems(self):
        return list(self._subsystems.keys())


class AbstractFactory:
    """【阶段96】抽象工厂：产品族创建、工厂注册、一致性保证"""

    def __init__(self):
        self._factories = {}

    def register(self, family, factory):
        self._factories[family] = factory

    def create(self, family, product_type, *args, **kwargs):
        if family not in self._factories:
            raise ValueError(f"Unknown family: {family}")
        return self._factories[family].create(product_type, *args, **kwargs)

    def get_families(self):
        return list(self._factories.keys())


class DependencyInjection:
    """【阶段97】依赖注入：容器管理、自动装配、生命周期"""

    def __init__(self):
        self._registrations = {}
        self._singletons = {}

    def register(self, interface, implementation, singleton=False):
        self._registrations[interface] = {"impl": implementation, "singleton": singleton}

    def resolve(self, interface):
        if interface not in self._registrations:
            raise ValueError(f"No registration for: {interface}")
        reg = self._registrations[interface]
        if reg["singleton"]:
            if interface not in self._singletons:
                self._singletons[interface] = reg["impl"]()
            return self._singletons[interface]
        return reg["impl"]()

    def get_registrations(self):
        return list(self._registrations.keys())


class AOPAspect:
    """【阶段98】AOP切面：切面定义、拦截器、动态代理"""

    def __init__(self):
        self._aspects = []

    def add_aspect(self, before=None, after=None, around=None):
        self._aspects.append({"before": before, "after": after, "around": around})

    def apply(self, target, method_name):
        original = getattr(target, method_name)

        def wrapper(*args, **kwargs):
            for aspect in self._aspects:
                if aspect["before"]:
                    aspect["before"](target, method_name, args, kwargs)
            if any(a["around"] for a in self._aspects):
                result = None
                for aspect in self._aspects:
                    if aspect["around"]:
                        result = aspect["around"](target, method_name, args, kwargs, original)
                        break
            else:
                result = original(*args, **kwargs)
            for aspect in self._aspects:
                if aspect["after"]:
                    aspect["after"](target, method_name, args, kwargs, result)
            return result

        setattr(target, method_name, wrapper)
        return wrapper


class ORMMapper:
    """【阶段99】ORM映射：对象关系映射、CRUD封装、查询构建"""

    def __init__(self, db_path=":memory:"):
        self._conn = sqlite3.connect(db_path)
        self._tables = {}

    def register(self, table_name, columns):
        self._tables[table_name] = columns
        cols = ", ".join([f"{k} {v}" for k, v in columns.items()])
        self._conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})")
        self._conn.commit()

    def insert(self, table_name, data):
        if table_name not in self._tables:
            raise ValueError(f"Unknown table: {table_name}")
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        cursor = self._conn.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})", tuple(data.values()))
        self._conn.commit()
        return cursor.lastrowid

    def select(self, table_name, where=None):
        sql = f"SELECT * FROM {table_name}"
        params = ()
        if where:
            conditions = " AND ".join([f"{k} = ?" for k in where])
            sql += f" WHERE {conditions}"
            params = tuple(where.values())
        cursor = self._conn.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def update(self, table_name, data, where):
        sets = ", ".join([f"{k} = ?" for k in data])
        conditions = " AND ".join([f"{k} = ?" for k in where])
        values = tuple(data.values()) + tuple(where.values())
        self._conn.execute(f"UPDATE {table_name} SET {sets} WHERE {conditions}", values)
        self._conn.commit()

    def delete(self, table_name, where):
        conditions = " AND ".join([f"{k} = ?" for k in where])
        self._conn.execute(f"DELETE FROM {table_name} WHERE {conditions}", tuple(where.values()))
        self._conn.commit()

    def close(self):
        self._conn.close()


class ServiceBus:
    """【阶段100】服务总线：消息路由、服务注册、事件驱动"""

    def __init__(self):
        self._services = {}
        self._handlers = {}
        self._history = []

    def register_service(self, name, service):
        self._services[name] = service

    def subscribe(self, event_type, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event_type, message):
        self._history.append({"event": event_type, "message": message})
        if event_type not in self._handlers:
            return []
        results = []
        for handler in self._handlers[event_type]:
            results.append(handler(message))
        return results

    def send(self, service_name, message):
        if service_name not in self._services:
            raise ValueError(f"Unknown service: {service_name}")
        return self._services[service_name](message)

    def get_history(self):
        return self._history[:]

    def get_services(self):
        return list(self._services.keys())


# ====================== 系统启动（唯一入口）======================
if __name__ == "__main__":
    # 【修复1】 先解析命令行参数，再初始化 Agent
    # 简单的命令行参数解析
    parser = argparse.ArgumentParser(
        description="第一性原理永动知识图谱Agent"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="启用LLM演示模式（不需要API）"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="完全禁用LLM功能"
    )
    parser.add_argument(
        "--loop-sleep",
        type=float,
        default=LOOP_SLEEP,
        help="循环间隔（秒），默认0.5"
    )
    parser.add_argument(
        "--kg-path",
        type=str,
        default=KG_PATH,
        help="知识图谱保存路径"
    )
    parser.add_argument(
        "--evolve-cycle",
        type=int,
        default=EVOLVE_CYCLE,
        help="进化周期（轮数），默认50"
    )
    parser.add_argument(
        "--save-every-n",
        type=int,
        default=SAVE_EVERY_N,
        help="保存间隔（轮数），默认5"
    )
    parser.add_argument(
        "--task-max-len",
        type=int,
        default=TASK_MAX_LEN,
        help="任务池最大长度，默认200"
    )
    parser.add_argument(
        "--context-max-len",
        type=int,
        default=CONTEXT_MAX_LEN,
        help="上下文最大长度，默认100"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="第一性原理永动知识图谱Agent 2.4.0",
        help="显示版本信息"
    )
    parser.add_argument(
        "--quick-test",
        type=int,
        nargs="?",
        const=10,
        default=None,
        help="快速测试模式，运行指定轮数后自动退出（默认10轮）"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="指定JSON配置文件路径"
    )
    
    args = parser.parse_args()
    
    # 【阶段16】 先加载配置文件（如果指定）
    if args.config:
        Config.load_from_file(args.config)
    else:
        # 尝试加载默认配置文件
        Config.load_from_file()
    
    # 【修复1】 先应用所有参数，再初始化 Agent！
    if args.no_llm:
        LLM_ENABLED = False
    elif args.demo:
        LLM_DEMO_MODE = True
        LLM_ENABLED = True
    
    LOOP_SLEEP = args.loop_sleep
    KG_PATH = args.kg_path
    EVOLVE_CYCLE = args.evolve_cycle
    SAVE_EVERY_N = args.save_every_n
    TASK_MAX_LEN = args.task_max_len
    CONTEXT_MAX_LEN = args.context_max_len
    
    # 同步到集中式Config对象！
    Config.sync_from_global()
    
    # 现在才初始化，此时全局变量已经是最新值！
    agent = FirstPrincipleEternalAgent(quick_test_rounds=args.quick_test)
    
    # 【阶段25】创建初始备份（如果图谱已存在）
    if os.path.exists(Config.KG_PATH):
        agent.kg.create_backup()
    
    # 初始化根任务（系统启动原点）
    initial_tasks = [
        "🎯 探索:第一性原理知识图谱",
        "🚀 启动:核心自驱循环",
        "⚡ 初始化:三大公理体系"
    ]
    for task in initial_tasks:
        TASK_POOL.append(task)
    agent.eternal_loop()
