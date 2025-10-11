# ============================================================
# 🧱 DevOps Project Automation
# Terraform + Ansible + Yandex.Cloud
# ============================================================

# Переменные
ANSIBLE_DIR=ansible
TERRAFORM_DIR=terraform
INVENTORY=$(ANSIBLE_DIR)/inventory.ini
PLAYBOOK=$(ANSIBLE_DIR)/playbook.yml

# ============================================================
# 🔹 Terraform commands
# ============================================================

init:
	@echo "🔧 Инициализация Terraform..."
	cd $(TERRAFORM_DIR) && terraform init

plan:
	@echo "🧩 Планирование инфраструктуры..."
	cd $(TERRAFORM_DIR) && terraform plan

apply:
	@echo "🚀 Создание инфраструктуры..."
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

destroy:
	@echo "💣 Удаление инфраструктуры..."
	cd $(TERRAFORM_DIR) && terraform destroy -auto-approve

run-terraform:
	@echo "🚀 Запускаем init!"
	$(MAKE) init
	@echo "🚀 Запускаем plan!"
	$(MAKE) plan
	@echo "🚀 Запускаем apply!"
	$(MAKE) apply
	@echo "✅ Terraform успешно выполнил полный цикл!"

# ============================================================
# 🔹 Ansible commands
# ============================================================

ping:
	@echo "🔍 Проверка соединения с ВМ..."
	cd $(ANSIBLE_DIR) && ansible all -i $(INVENTORY) -m ping

deploy:
	@echo "⚙️  Развёртывание приложения через Ansible..."
	cd $(ANSIBLE_DIR) && ansible-playbook -i $(INVENTORY) $(PLAYBOOK)

