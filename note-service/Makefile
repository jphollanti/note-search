APP = note-service
VERSION = 1.0.0
FRONTEND_APP_DIR := frontend
SERVER_APP_DIR := server

build:
	cd $(FRONTEND_APP_DIR) && npm run build
	rm -rf $(SERVER_APP_DIR)/public
	cp -R $(FRONTEND_APP_DIR)/public $(SERVER_APP_DIR)/
	docker build -t ${APP}:${VERSION} server

run: rm
	docker run --name ${APP} \
		-d \
		--restart unless-stopped \
		-p 3000:3000 \
		-v $(HOME)/.note-search.cfg:/app/.note-search.cfg \
  		-v $(HOME)/notebooks:/notebooks \
		${APP}:${VERSION}

rm: 
	docker rm -f ${APP}

.PHONY: build