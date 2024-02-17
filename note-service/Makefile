FRONTEND_APP_DIR := frontend
SERVER_APP_DIR := server

build:
	cd $(FRONTEND_APP_DIR) && npm run build
	rm -rf $(SERVER_APP_DIR)/public
	cp -R $(FRONTEND_APP_DIR)/public $(SERVER_APP_DIR)/

.PHONY: build