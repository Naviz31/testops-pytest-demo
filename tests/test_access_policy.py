import allure
import pytest

from mock_autotests.shop import AccessPolicy


pytestmark = [
    pytest.mark.allure_label("naviz31", label_type="owner"),
    pytest.mark.allure_label("unit", label_type="layer"),
    pytest.mark.allure_label("access-policy", label_type="component"),
    pytest.mark.allure_label("Моковый интернет-магазин", label_type="parentSuite"),
    pytest.mark.allure_label("Права доступа", label_type="suite"),
]


@allure.epic("Моковый интернет-магазин")
@allure.feature("Права доступа")
@allure.story("Проверка роли")
@allure.title("Роль {role} и право {permission}: доступ={expected}")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("regression", "unit", "offline")
@pytest.mark.regression
@pytest.mark.unit
@pytest.mark.parametrize(
    ("role", "permission", "expected"),
    [
        pytest.param("admin", "users:manage", True, id="администратор-управляет"),
        pytest.param("manager", "orders:edit", True, id="менеджер-редактирует"),
        pytest.param("viewer", "orders:read", True, id="наблюдатель-читает"),
        pytest.param("viewer", "orders:edit", False, id="наблюдатель-не-редактирует"),
        pytest.param("unknown", "orders:read", False, id="неизвестная-роль"),
    ],
)
def test_access_policy(
    role: str,
    permission: str,
    expected: bool,
) -> None:
    policy = AccessPolicy()

    with allure.step(f"Проверить право {permission} для роли {role}"):
        actual = policy.is_allowed(role, permission)

    assert actual is expected
