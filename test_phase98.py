"""阶段98：AOP切面测试"""
import sys
sys.path.insert(0, '/workspace')
from first_principles_agent import AOPAspect

class TargetService:
    def __init__(self):
        self.value = 0

    def do_something(self, x):
        self.value += x
        return self.value

def test_aop_aspect():
    target = TargetService()
    aspect = AOPAspect()

    logs = []

    def before_aspect(target, method, args, kwargs):
        logs.append(f"before:{method}:{args}")

    def after_aspect(target, method, args, kwargs, result):
        logs.append(f"after:{method}:{result}")

    aspect.add_aspect(before=before_aspect, after=after_aspect)
    aspect.apply(target, "do_something")

    # 测试拦截器执行
    result = target.do_something(5)
    assert result == 5
    assert "before:do_something:(5,)" in logs
    assert "after:do_something:5" in logs

    # 测试around拦截
    target2 = TargetService()
    aspect2 = AOPAspect()

    def around_aspect(target, method, args, kwargs, original):
        return original(*args, **kwargs) * 2

    aspect2.add_aspect(around=around_aspect)
    aspect2.apply(target2, "do_something")
    assert target2.do_something(3) == 6

    print("✅ 阶段98 AOP切面测试通过")

if __name__ == "__main__":
    test_aop_aspect()
