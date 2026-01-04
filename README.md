# Rental API Backend（FastAPI + MySQL）

包含：
- 登录（JWT）
- 简单权限（admin/user）
- 房间（房间号、固定月租、三表底表）
- 抄表（按月水/电/气读数）
- 单价配置（按生效时间：水/电/气/物业单价）
- 账单生成（含物业费 = 当月实际用电量 × 物业单价，默认 0.5）
- 收款状态（未收/已收、时间、方式、备注）
- 批量收款/反收款
- 导出 Excel / PDF（按月份 period 必填）

## 目录
```
app/
  main.py
  db.py
  models.py
  schemas.py
  security.py
  deps.py
  billing.py
```

## 本地运行（示例）
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 修改 .env 中 DATABASE_URL / APP_SECRET / INIT_ADMIN_PASSWORD

# 运行
uvicorn app.main:app --reload --port 8000
```

## 宝塔部署建议
- 后端仅监听 127.0.0.1:8000
- Nginx 反代 /api/ 到 http://127.0.0.1:8000/api/
- 使用 start.sh 启动（会 source .env）

## 重要提醒
- 这是 create_all 自动建表方案；如需长期迁移建议后续引入 Alembic。
