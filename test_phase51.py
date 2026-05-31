"""阶段51：模板引擎测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import TemplateEngine

def test_template_engine():
    engine = TemplateEngine()

    # 测试变量替换
    template = "Hello, {{ name }}!"
    result = engine.render(template, {"name": "World"})
    assert result == "Hello, World!", f"变量替换失败: {result}"

    # 测试条件渲染
    template = "{% if show %}visible{% endif %}"
    assert engine.render(template, {"show": True}) == "visible"
    assert engine.render(template, {"show": False}) == ""

    # 测试循环渲染
    template = "{% for item in items %}{{ item }},{% endfor %}"
    result = engine.render(template, {"items": ["a", "b", "c"]})
    assert result == "a,b,c,", f"循环渲染失败: {result}"

    # 测试全局变量
    engine.set_global("app", "MyApp")
    result = engine.render("{{ app }}", {})
    assert result == "MyApp"

    print("✅ 阶段51 模板引擎测试通过")

if __name__ == "__main__":
    test_template_engine()
